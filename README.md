# 🧮 SAT Math Tutor

## Badges

These badges will be added when CI runs on the repository (placeholders until the workflow completes):

- CI: ![CI](https://img.shields.io/badge/ci-pending-lightgrey)
- Tests: ![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
- License: ![License](https://img.shields.io/badge/license-MIT-blue)

## 🧩 Overview
SAT Math Tutor is a Python program that generates random SAT-style math problems, quizzes the user, and saves results to a CSV file.

## ⚙️ Features
## Overview
This project presents arithmetic/algebra problems, gives immediate feedback, tracks the score, and can save answers and timestamps to `sat_math_results.csv`.

## Prerequisites
- Python 3.8+ (recommended: the python.org installer, not the Microsoft Store build)
- pip

## Recommended setup (PowerShell)
1. Create and activate a virtual environment (recommended):

```powershell
# Use a specific Python executable if you have multiple installs:
# "C:\Path\To\Python.exe" -m venv .venv
python -m venv .venv

# Activate the venv in PowerShell
. .\.venv\Scripts\Activate.ps1

# Upgrade pip and install requirements
python -m pip install --upgrade pip
python -m pip install -r .\requirements.txt
```

If you prefer to use the Program Files installation directly (what I used in this workspace), replace `python` with the full path to that `python.exe`.

### Using the Microsoft Store Python

If your `python` comes from the Microsoft Store (WindowsApps) you can still create a venv. The Store Python is usually accessible via the `python` command, but creating a venv requires the `python` launcher to be the one from the Store. To create a venv specifically named `.venv-msstore` and install dependencies, run the included helper script in PowerShell:

```powershell
# Run this from the project root
.\setup_msstore_venv.ps1
```

The script tries to locate the Microsoft Store Python and create `.venv-msstore` for the project, then install `requirements.txt` into it. After that activate with:

```powershell
. .\.venv-msstore\Scripts\Activate.ps1
```

If the script cannot find the Store Python automatically, open PowerShell and run `where.exe python` to see which `python.exe` is being used, then run the full path with `-m venv .venv-msstore`.


## Editor setup (VS Code / Pylance)
If you use VS Code, point the editor to the project virtual environment so language servers (Pylance) and linters can resolve imports like `pandas`:

1. Open Command Palette (Ctrl+Shift+P) -> `Python: Select Interpreter`.
2. Choose the interpreter that points to `.venv-msstore\Scripts\python.exe` (or `.venv-pf` / `.venv` if you prefer).
3. Reload the window (Developer: Reload Window) if diagnostics don't update immediately.

After that the "Import could not be resolved" warning for `pandas` should disappear.
## Run the tutor

With the venv activated run:

```powershell
python sat_math_tutor.py
```

The script is interactive and will ask how many questions you want to try. When finished it will optionally save results to `sat_math_results.csv` in the project root.

### Command-line options

You can run the tutor non-interactively or include algebra problems using these flags:

```powershell
# Ask for 10 questions interactively (default interactive flow)
python sat_math_tutor.py

# Ask for 20 questions non-interactively
python sat_math_tutor.py --count 20

# Include algebra-style problems (solve for x)
python sat_math_tutor.py --count 15 --include-algebra

# Auto-answer (useful for testing) and save results without prompting
python sat_math_tutor.py --count 5 --include-algebra --auto
```

## Notes
- If you have multiple Python installations, creating a virtual environment ensures the project uses a consistent interpreter and isolated packages.
- Add your venv directory to `.gitignore` (example below) to avoid committing dependencies:

```powershell
echo ".venv/" >> .gitignore
# or for a venv named .venv-pf
echo ".venv-pf/" >> .gitignore
```

## Troubleshooting
- If `python` refers to the Microsoft Store build and you want to use the python.org install, call the full path to the desired `python.exe` when creating the venv or running commands.
- If `pip install -r requirements.txt` fails, check that `requirements.txt` contains valid package names (one per line). You can open it to inspect its contents.

## Interactive algebra flow
When `--include-algebra` is used (or when algebra problems appear in interactive mode), algebra questions are interactive and guide the student step-by-step:

- For `x + b = c` problems the program asks for the intermediate RHS after subtracting `b`, then asks for `x`.
- For `ax = b` problems the program asks for the result after dividing by `a`.
- For `ax + b = c` problems the program asks to subtract `b` (intermediate RHS) and then asks to divide by `a`.

Additional algebra topics
- Fractional linear equations: the program may present problems with non-integer solutions (e.g., "Solve for x: 3x + 1 = 7.5"). Intermediate answers may be fractional; enter decimals (the program accepts up to 4 decimal places).
- Basic quadratics: the program now generates simple factorable quadratics (e.g., "Solve for x: x^2 - 3x + 2 = 0"). For quadratic questions enter both roots separated by a comma (either order is accepted), for example: `1,2` or `2,1`.

Intermediate answers accept fractional/decimal input when needed (you can enter numbers with decimals). If parsing fails the program falls back to the simple single-answer prompt.

## Timing and results
Each question records a timestamp and duration (seconds) in `sat_math_results.csv`. The CSV now contains these columns:

- Problem, Your Answer, Correct Answer, Result, Timestamp, Duration


## Contributing
Improvements are welcome. If you want the tutor to support non-interactive runs (for CI or automated testing), I can add a `--count` flag and a `--no-prompt` mode—ask and I will implement it.

## 🧰 Technologies
- Python 3  
- random (built-in module)  
- pandas (optional, for tracking results)

## 🧪 Run Instructions
1. Install dependencies:  
```bash
pip install -r requirements.txt
