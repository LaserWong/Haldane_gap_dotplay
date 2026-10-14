"""Run with python -m gapflow."""
import argparse
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Budgeted model-input gap workflow")
    parser.add_argument("input", nargs="?", help="Input JSON file")
    parser.add_argument("--output", default="results/latest", help="Result directory")
    parser.add_argument("--resume", action="store_true", help="Verify and reuse a matching completed run")
    parser.add_argument("--internal-worker", nargs=2, metavar=("REQUEST", "RESPONSE"), help=argparse.SUPPRESS)
    args = parser.parse_args()
    from .workflow import run, worker
    if args.internal_worker:
        worker(Path(args.internal_worker[0]), Path(args.internal_worker[1]))
        return 0
    if not args.input:
        parser.error("input is required")
    try:
        result = run(Path(args.input), Path(args.output), resume=args.resume)
    except (ValueError, OSError) as exc:
        print(json.dumps({'status': 'invalid_input_or_resume', 'reason': str(exc)}))
        return 2
    print(json.dumps({"status": result["status"], "output": str(Path(args.output).resolve()),
                      "claim": result.get("claim"), "reason": result.get("reason")}, indent=2))
    return 0 if result["status"] in {"certified_finite_size", "certified_uniform_family", "certified_gapless_family"} else 2


if __name__ == "__main__":
    sys.exit(main())
