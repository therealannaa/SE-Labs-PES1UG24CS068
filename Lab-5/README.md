# Lab 5: Static Code Analysis — Campus Parking Permit Manager

Assigned repo: [SETAPESU26/L5_10_parking_permits](https://github.com/SETAPESU26/L5_10_parking_permits)

## Deliverables

| File | Contents |
|------|----------|
| `parking_system.py` | Cleaned version of the program |
| `issues.md` | Issue table (what each tool found and how it was fixed) |
| `reflection.md` | Answers to the reflection questions |
| `reports/before/` | Pylint, Bandit and Flake8 reports on the original code |
| `reports/after/` | The same reports on the fixed code |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.32/10 | 10.00/10 |
| Bandit | 2 issues | 0 issues |
| Flake8 | 16 issues | 0 issues |

## Commits

1. Add starter code and before reports
2. Fix Bandit issues
3. Fix Flake8 issues
4. Fix Pylint issues
5. Fix logic bugs not caught by the tools
6. Add after reports, issue table and reflection

## Run

```bash
python parking_system.py
pylint parking_system.py
bandit -r parking_system.py
flake8 parking_system.py
```
