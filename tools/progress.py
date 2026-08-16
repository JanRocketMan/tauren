"""Compare tauren's implemented code with the Tau reference.

Prints a progress banner showing how many lines of the reference have been
reimplemented so far. Run it from the project root:

    uv run python tools/progress.py [--reference PATH]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUR_MODULES = ROOT / "src" / "agent"
DEFAULT_REFERENCE = Path.home() / "tau" / "src" / "tau_agent"
BAR_WIDTH = 24


def count_lines(path: Path) -> int:
    """Return the number of lines in a text file."""
    return sum(1 for _ in path.open(encoding="utf-8"))


def reference_root() -> Path:
    """Return the reference path from --reference or the default."""
    for index, arg in enumerate(sys.argv):
        if arg == "--reference" and index + 1 < len(sys.argv):
            return Path(sys.argv[index + 1])
    return DEFAULT_REFERENCE


def bar(fraction: float) -> str:
    """Return a filled progress bar for a fraction."""
    filled = round(fraction * BAR_WIDTH)
    return "█" * filled + "░" * (BAR_WIDTH - filled)


def count_test_functions() -> int:
    """Return the number of test functions in the tests directory."""
    tests_dir = ROOT / "tests"
    count = 0
    for test_file in tests_dir.glob("test_*.py"):
        for line in test_file.open(encoding="utf-8"):
            if line.lstrip().startswith("def test_"):
                count += 1
    return count


def main() -> int:
    """Print the progress banner."""
    reference = reference_root()
    if not reference.is_dir():
        print(f"Reference not found: {reference}")
        print("Pass --reference PATH or adjust the default in tools/progress.py")
        return 0

    print()
    print("  tauren course progress: lines reimplemented vs the reference")
    print("  " + "-" * 52)

    rows = []
    our_total = 0
    ref_total = 0
    for our_file in sorted(OUR_MODULES.glob("*.py")):
        if our_file.name == "__init__.py":
            continue
        ref_file = reference / our_file.name
        if not ref_file.exists():
            continue
        ours = count_lines(our_file)
        ref_lines = count_lines(ref_file)
        our_total += ours
        ref_total += ref_lines
        fraction = ours / ref_lines if ref_lines else 0.0
        rows.append((f"agent/{our_file.name}", ours, ref_lines, fraction))

    for name, ours, ref_lines, fraction in rows:
        print(f"  {name:<28} {ours:>4} / {ref_lines:<4} {bar(fraction)} {fraction:>5.0%}")
    print("  " + "-" * 52)
    total_fraction = our_total / ref_total if ref_total else 0.0
    total_row = f"  {'total':<28} {our_total:>4} / {ref_total:<4}"
    print(f"{total_row} {bar(total_fraction)} {total_fraction:>5.0%}")

    tests = count_test_functions()
    print()
    print(f"  {tests} test functions waiting for your implementation")
    print()
    print("  Line parity is not the goal. Understand each piece, then move on.")
    print(f"  Reference: {reference}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
