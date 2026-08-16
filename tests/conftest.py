"""Gamified test output: a rocket on green, a sad cat on red."""

import pytest

ROCKET = r"""
        /\
       /  \
      | /\ |
      |/  \|
     /|    |\
    / |    | \
   |  | /\ |  |
   |  |/  \|  |
   |__|____|__|
      |    |
     /|    |\
    / |    | \
   /__|____|__\

  All tests pass. Commit a done: entry and pick the next task.
"""

SAD_CAT = r"""
   /\_/\
  ( o.o )
   > ^ <
  /     \

  Some tests are still red. The task doc holds the spec you need.
"""


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """Print a rocket or a sad cat when the test session ends."""
    print()
    if exitstatus == 0:
        print(ROCKET)
    else:
        print(SAD_CAT)
        print(f"  {session.testsfailed} test(s) failed. Keep going.")
    print()
