# Lab 5: Issue Table

Line numbers refer to the original `parking_system.py` (see `reports/before/`).

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Wrong expiry date format (not flagged by any tool) | Bug | 51-52, 60, 27-30 | `setExpiry` stores `"01/01/2020"`, but `is_expired` parses `%Y-%m-%d`. The parse fails, the bare `except` returns `False`, so an expired permit is reported as valid and `KA01AB1234` is never flagged in zone A. | `set_expiry` now validates the date with `strptime` and raises `ValueError` on a bad format; `main` uses `"2020-01-01"`; `is_expired` treats an unreadable date as expired instead of valid. |
| No input validation (not flagged by any tool) | Bug | 9-17, 57-59 | Permits are issued for a non-existent zone `"Z"`, an empty plate `""` and `None` (saved to JSON as the key `"null"`). | `register_permit` returns `None` unless the plate is a non-empty string and the zone is in `ZONES`; plates are stripped and upper-cased (input too). |
| Mutable default argument (Pylint W0102) | Bug | 9 | `zone_records=[]` is created once and shared across every call, so records leak between calls. | Default changed to `None` and a new list is created inside the function. |
| Insecure random generator (Bandit B311) | Security | 11 | `random.randint` is predictable, so permit numbers can be guessed. Numbers could also collide. | Use `secrets.randbelow`, and regenerate if the number is already issued. |
| Try / except / pass (Bandit B110) | Security | 20-23 | Every error in `revoke_permit` is silently swallowed. | Replaced with an explicit `if vehicle_plate in permits:` check. |
| Bare `except` (Pylint W0702, Flake8 E722) | Bug | 16, 22, 29, 43 | Catches everything, including `KeyboardInterrupt` and programming errors, and hides real bugs (see the first row). | Catch only the expected exceptions (`KeyError`, `ValueError`, `OSError`, `json.JSONDecodeError`) or remove the try block. |
| File not closed safely / no encoding (Pylint R1732, W1514) | Bug | 42, 47-49 | `json.load(open(file))` never closes the file, and `save` leaks it if `json.dump` fails. No encoding is given. | Use `with open(file, ..., encoding="utf-8") as f:`. |
| Global statement (Pylint W0603) | Code smell | 40 | `global permits` rebinds the module dictionary. | Mutate the existing dict with `permits.clear()` and `permits.update(...)`. |
| Non snake_case name (Pylint C0103) | Style | 51 | `setExpiry` breaks PEP 8 naming. | Renamed to `set_expiry`. |
| Missing docstrings (Pylint C0114, C0116) | Style | 1, 9, 19, 25, 32, 39, 46, 51, 54 | No module or function docstrings. | Added a module docstring and a docstring for every function. |
| Missing blank lines (Flake8 E302, E305) | Style | 9-68 | Top-level functions separated by 1 blank line instead of 2. | Added 2 blank lines between top-level definitions. |
| Line too long (Flake8 E501, Pylint C0301) | Style | 13, 27, 62 | Lines longer than 79 characters. | Wrapped the dict, the `strptime` call and the `print`. |
| Code runs on import | Code smell | 68 | `main()` runs (and waits for input) whenever the module is imported. | Wrapped it in `if __name__ == "__main__":`. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.32/10 | 10.00/10 |
| Bandit | 2 issues (Low) | 0 issues |
| Flake8 | 16 issues | 0 issues |
