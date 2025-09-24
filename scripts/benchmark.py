#!/usr/bin/env python3
"""Measure Markdown↔HTML conversion performance."""

from __future__ import annotations

import argparse
import json
import sys
import textwrap
import time
from datetime import datetime
from pathlib import Path
from typing import Dict

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import chatgpt_md_converter  # noqa: E402

telegram_format = chatgpt_md_converter.telegram_format
html_to_telegram_markdown = chatgpt_md_converter.html_to_telegram_markdown


def _build_samples(multiplier: int) -> Dict[str, str]:
    base = {
        "short_inline": "Hello, **bold** _italic_ __underline__ [link](http://example.com)",
        "medium_block": textwrap.dedent(
            """
            # Heading Example
            > Quote line 1
            > Quote line 2
            >
            > Quote line 4

            - Item 1 with `code`
            - Item 2 with **bold** and _italic_
            - Item 3 with __underline__ and ~~strike~~

            ```python
            for i in range(100):
                print(i)
            ```
            """
        ).strip(),
        "long_mixed": textwrap.dedent(
            """
            # Heading
            > Quote line 1
            > Quote line 2

            - Item 1 with `code`
            - Item 2 with **bold** and _italic_
            - Item 3 with __underline__ and ~~strike~~ and ||spoiler||

            ```python
            for i in range(200):
                print(i)
            ```

            End text with paragraphs and more inline `code`.
            """
        ).strip(),
    }
    samples = base.copy()
    samples["long_mixed"] = samples["long_mixed"] * multiplier
    return samples


def _benchmark(callable_fn, payload: str, iterations: int) -> Dict[str, float]:
    start = time.perf_counter()
    for _ in range(iterations):
        callable_fn(payload)
    total = time.perf_counter() - start
    return {
        "iterations": iterations,
        "total_seconds": total,
        "avg_ms_per_call": (total / iterations) * 1000,
        "ops_per_second": iterations / total,
    }


def run_benchmarks(iterations: int, long_multiplier: int) -> Dict[str, Dict[str, Dict[str, float]]]:
    results: Dict[str, Dict[str, Dict[str, float]]] = {}
    samples = _build_samples(long_multiplier)
    for name, markdown in samples.items():
        html = telegram_format(markdown)
        results[name] = {
            "md_to_html": _benchmark(telegram_format, markdown, iterations),
            "html_to_md": _benchmark(html_to_telegram_markdown, html, iterations),
        }
    return results


def _format_summary(results: Dict[str, Dict[str, Dict[str, float]]]) -> str:
    lines = [
        f"Benchmark run: {datetime.utcnow().isoformat(timespec='seconds')}Z",
        "Sample        Direction        Avg ms/call   Ops/sec",
    ]
    for sample, dirs in results.items():
        for direction, stats in dirs.items():
            lines.append(
                f"{sample:<13}{direction:<16}{stats['avg_ms_per_call']:.3f}         {stats['ops_per_second']:.1f}"
            )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iterations", type=int, default=1000, help="loops per sample (default: 1000)")
    parser.add_argument(
        "--long-multiplier",
        type=int,
        default=5,
        help="repeat the long sample this many times (default: 5)",
    )
    parser.add_argument("--json", type=Path, help="optional path to write JSON results")
    parser.add_argument("--summary", type=Path, help="optional path to write text summary")
    args = parser.parse_args()

    results = run_benchmarks(args.iterations, args.long_multiplier)

    summary = _format_summary(results)
    if args.summary:
        args.summary.write_text(summary + "\n", encoding="utf-8")
    else:
        print(summary)

    if args.json:
        args.json.write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
