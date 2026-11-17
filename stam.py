import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_timestamp(ts_raw: Any) -> datetime | None:
    """Преобразует ISO-строку или Unix timestamp в локальный datetime."""
    if not ts_raw:
        return None
    try:
        if isinstance(ts_raw, (int, float)):
            # Если timestamp в миллисекундах
            if ts_raw > 1e12:
                ts_raw /= 1000.0
            return datetime.fromtimestamp(ts_raw, tz=timezone.utc).astimezone()
        if isinstance(ts_raw, str):
            clean_ts = ts_raw.replace("Z", "+00:00")
            return datetime.fromisoformat(clean_ts).astimezone()
    except ValueError:
        return None
    return None


def extract_usage(record: dict[str, Any]) -> tuple[int, int, int] | None:
    """
    Извлекает (input_tokens, output_tokens, cached_tokens) из различных форматов
    событий логов OpenAI Codex CLI.
    """
    payload = record.get("payload", record)
    if not isinstance(payload, dict):
        return None

    # Вариант 1: Событие token_count в Codex CLI (info.last_token_usage / info.total_token_usage)
    if payload.get("type") == "token_count" or "info" in payload:
        info = payload.get("info") or {}
        usage = info.get("last_token_usage") or info.get("usage")
        if isinstance(usage, dict):
            inp = usage.get("input_tokens", 0) or usage.get("prompt_tokens", 0)
            out = usage.get("output_tokens", 0) or usage.get("completion_tokens", 0)
            cached = usage.get("cached_input_tokens", 0) or (
                usage.get("input_tokens_details", {}).get("cached_tokens", 0)
            )
            return int(inp), int(out), int(cached)

    # Вариант 2: События Responses API (response.completed / response.done)
    response_obj = payload.get("response", payload)
    if isinstance(response_obj, dict) and isinstance(response_obj.get("usage"), dict):
        usage = response_obj["usage"]
        inp = usage.get("input_tokens", 0) or usage.get("prompt_tokens", 0)
        out = usage.get("output_tokens", 0) or usage.get("completion_tokens", 0)
        cached = usage.get("input_tokens_details", {}).get("cached_tokens", 0)
        return int(inp), int(out), int(cached)

    return None


def extract_prompt_text(record: dict[str, Any]) -> str | None:
    """Извлекает текст пользовательского промпта из записи сессии."""
    payload = record.get("payload", record)
    if not isinstance(payload, dict):
        return None

    # Прямое сообщение пользователя
    role = payload.get("role") or payload.get("item", {}).get("role")
    if role == "user":
        content = payload.get("content") or payload.get("item", {}).get("content")
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            parts = [
                block.get("text", "")
                for block in content
                if isinstance(block, dict) and block.get("type") in ("input_text", "text")
            ]
            joined = " ".join(p.strip() for p in parts if p.strip())
            if joined:
                return joined

    # Событие user_message
    if payload.get("type") == "user_message" and isinstance(payload.get("message"), str):
        return payload["message"].strip()

    return None


def extract_cwd(record: dict[str, Any]) -> str | None:
    """Извлекает рабочую директорию проекта (cwd) из метаданных сессии."""
    payload = record.get("payload", record)
    if isinstance(payload, dict):
        cwd = payload.get("cwd") or record.get("cwd")
        if isinstance(cwd, str) and cwd.strip():
            return cwd.strip()
    return None


def analyze_sessions(sessions_dir: Path, target_date: str, top_n: int = 10) -> None:
    if not sessions_dir.exists():
        print(f"Директория сессий не найдена: {sessions_dir}")
        return

    project_stats: dict[str, dict[str, int]] = defaultdict(
        lambda: {"input": 0, "output": 0, "cached": 0, "turns": 0}
    )
    expensive_turns: list[dict[str, Any]] = []

    jsonl_files = sorted(sessions_dir.rglob("*.jsonl"))
    if not jsonl_files:
        print(f"В директории {sessions_dir} не найдено .jsonl файлов.")
        return

    for file_path in jsonl_files:
        current_cwd = "Неизвестный проект"
        last_user_prompt = "(системный вызов / без текста промпта)"
        file_default_dt: datetime | None = None

        # Пробуем вытащить дату из имени файла (формат rollout-YYYY-MM-DDTHH-MM-SS-...)
        for part in file_path.stem.split("-"):
            if len(part) == 4 and part.isdigit() and part.startswith("20"):
                idx = file_path.stem.index(part)
                date_candidate = file_path.stem[idx : idx + 10]
                try:
                    file_default_dt = datetime.strptime(date_candidate, "%Y-%m-%d").astimezone()
                except ValueError:
                    pass
                break

        try:
            with file_path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    # 1. Обновляем рабочую директорию проекта
                    cwd = extract_cwd(record)
                    if cwd:
                        current_cwd = cwd

                    # 2. Запоминаем последний промпт пользователя в этой сессии
                    prompt = extract_prompt_text(record)
                    if prompt:
                        last_user_prompt = prompt

                    # 3. Проверяем расход токенов
                    usage = extract_usage(record)
                    if not usage:
                        continue

                    dt = parse_timestamp(record.get("timestamp")) or file_default_dt
                    if not dt:
                        continue

                    if dt.strftime("%Y-%m-%d") != target_date:
                        continue

                    inp, out, cached = usage
                    total = inp + out
                    if total == 0:
                        continue

                    proj = project_stats[current_cwd]
                    proj["input"] += inp
                    proj["output"] += out
                    proj["cached"] += cached
                    proj["turns"] += 1

                    expensive_turns.append(
                        {
                            "time": dt.strftime("%H:%M:%S"),
                            "project": Path(current_cwd).name if current_cwd != "Неизвестный проект" else current_cwd,
                            "full_project": current_cwd,
                            "input": inp,
                            "output": out,
                            "cached": cached,
                            "total": total,
                            "prompt": last_user_prompt,
                            "session_file": file_path.name,
                        }
                    )
        except OSError as e:
            print(f"Ошибка чтения {file_path}: {e}")

    if not expensive_turns:
        print(f"За дату {target_date} активность токенов в {sessions_dir} не найдена.")
        return

    # Вывод сводки по проектам
    print(f"\n{'=' * 80}")
    print(f"ОТЧЕТ ПО ТОКЕНАМ CODEX CLI ЗА {target_date}")
    print(f"{'=' * 80}\n")

    print("1. РАСХОД ПО ПРОЕКТАМ (ДИРЕКТОРИЯМ):")
    print("-" * 80)
    sorted_projects = sorted(
        project_stats.items(),
        key=lambda item: item[1]["input"] + item[1]["output"],
        reverse=True,
    )

    grand_input = sum(p["input"] for _, p in sorted_projects)
    grand_output = sum(p["output"] for _, p in sorted_projects)
    grand_cached = sum(p["cached"] for _, p in sorted_projects)

    for cwd, stats in sorted_projects:
        total_proj = stats["input"] + stats["output"]
        print(f"Проект: {cwd}")
        print(
            f"  Всего: {total_proj:,} ток. | Вход (Input): {stats['input']:,} "
            f"(из кэша: {stats['cached']:,}) | Выход (Output): {stats['output']:,} | Шагов: {stats['turns']}"
        )

    print("-" * 80)
    print(
        f"ИТОГО ЗА ДЕНЬ: {grand_input + grand_output:,} ток. "
        f"(Input: {grand_input:,}, Cached: {grand_cached:,}, Output: {grand_output:,})\n"
    )

    # Вывод топ-N самых дорогих запросов
    print(f"2. ТОП-{top_n} САМЫХ ЗАТРАТНЫХ ЗАПРОСОВ / ШАГОВ:")
    print("-" * 80)
    expensive_turns.sort(key=lambda x: x["total"], reverse=True)

    for idx, turn in enumerate(expensive_turns[:top_n], start=1):
        clean_prompt = " ".join(turn["prompt"].split())
        if len(clean_prompt) > 120:
            clean_prompt = clean_prompt[:117] + "..."

        print(
            f"#{idx:<2} [{turn['time']}] Всего: {turn['total']:>8,} ток. "
            f"(In: {turn['input']:,} / Out: {turn['output']:,}) | Проект: {turn['project']}"
        )
        print(f"    Запрос: {clean_prompt}")
        print(f"    Файл:   {turn['session_file']}\n")


def main() -> None:
    default_dir = Path.home() / ".codex" / "sessions"
    today_str = datetime.now().strftime("%Y-%m-%d")

    parser = argparse.ArgumentParser(
        description="Анализ расхода токенов в локальных сессиях OpenAI Codex CLI за выбранную дату."
    )
    parser.add_argument(
        "-d",
        "--date",
        default=today_str,
        help=f"Дата в формате YYYY-MM-DD (по умолчанию сегодня: {today_str})",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=Path,
        default=default_dir,
        help=f"Путь к папке sessions (по умолчанию: {default_dir})",
    )
    parser.add_argument(
        "-n",
        "--top",
        type=int,
        default=10,
        help="Сколько самых дорогих запросов показать (по умолчанию: 10)",
    )

    args = parser.parse_args()
    analyze_sessions(args.path, args.date, args.top)


if __name__ == "__main__":
    main()
