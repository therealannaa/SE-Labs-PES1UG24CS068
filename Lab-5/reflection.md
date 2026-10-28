# Lab 5: Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The easiest were the Flake8 style issues (blank lines, long lines) and the Pylint naming and docstring warnings. They are mechanical and do not change behaviour. The mutable default argument and the `with open(...)` fixes were also quick once I knew the standard pattern.

The hardest were the bugs no tool reported. Removing the bare `except` in `is_expired` showed that the program had been hiding a real bug: `setExpiry` wrote `01/01/2020`, `is_expired` could not parse it, and the swallowed error made an expired permit look valid. I had to read the program's output to notice it. Replacing `global permits` without breaking `load_permit_database` also needed thought.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

Bandit's B311 warning on `random.randint` could be seen as a false positive in a small lab script, because the permit number is not a password or a token. In a real permit system, though, a guessable permit number could be forged, so I switched to `secrets`. Pylint's missing-docstring warnings are not bugs either, but they are useful for readability. The bigger problem was the opposite of a false positive: the tools missed the date-format and input-validation bugs completely.

**3. How would you integrate static analysis tools into your actual software development workflow?**

- Run Flake8 and Pylint in the editor so problems show up while typing.
- Add a pre-commit hook that runs Flake8, Pylint and Bandit before each commit.
- Run all three in CI (for example a GitHub Actions workflow) on every push and pull request, and fail the build if Bandit finds Medium or High issues, Flake8 finds anything, or the Pylint score drops below a set threshold such as 9.5.
- Keep a shared config (`.pylintrc`, `setup.cfg`) so the whole team uses the same rules.

Because the tools missed the logic bugs, I would combine them with unit tests and code review.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**

- The Pylint score went from 6.32 to 10.00, and Bandit and Flake8 now report 0 issues.
- The program now gives correct output: the expired permit `KA01AB1234` is flagged, and invalid zones, empty plates and `None` are rejected instead of being saved.
- Errors are no longer swallowed, so future bugs will show up instead of being hidden.
- Files are always closed, permit numbers are unpredictable and unique, and the module can be imported without running `main()`.
- Docstrings, consistent naming and PEP 8 formatting make the code easier to read and maintain.
