# L6_L7_10 — Bus Transit Fare

Lab 7: Fuzz Testing with Hypothesis

## About

A set of property-based fuzz tests targeting transit corridor codes, passenger concession categories, and route passenger density ratios to find unexpected crashes.

## Files

| File | Description |
|------|-------------|
| `processor.py` | The module under test (buggy starter code) |
| `test_processor.py` | Starter test file to complete using Hypothesis |

Keep all your Lab 7 work in this `LAB7` folder.

Refer to the lab handout for instructions.

## Lab 7 work

| File | Description |
|------|-------------|
| `processor_original.py` | Untouched copy of the buggy starter code (for reference) |
| `processor.py` | Fixed module: invalid input returns `None` instead of crashing |
| `test_processor.py` | Hypothesis fuzz tests for all three functions (8 tests) |
| `screenshots/` | Terminal output of each step (`.txt` logs and `.png` images) |
| `Lab7_FuzzTesting_Report.pdf` | Consolidated report: screenshots + both source files |

Run: `python processor.py` and `python -m pytest test_processor.py -v`
