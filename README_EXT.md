Quick run examples

Run without activating a venv (call the venv python directly):

```powershell
.\.venv-msstore\Scripts\python.exe sat_math_tutor.py --include-algebra
```

Run interactively (recommended):

```powershell
. .\.venv-msstore\Scripts\Activate.ps1
python sat_math_tutor.py --include-algebra
```

Run tests:

```powershell
. .\.venv-msstore\Scripts\Activate.ps1
python -m pytest -q
```

Supported Python versions

Tested with Python 3.13 (Microsoft Store and python.org installers). The project aims to be compatible with Python 3.8 and above.

Dependency notes

- `requirements.txt` includes runtime dependencies (pandas). It currently also includes `pytest` for convenience. Use `dev-requirements.txt` for development-only deps if you prefer.

How to answer examples

- Quadratic: enter both roots separated by a comma, e.g. `1,2` or `2,1`.
- Fractional linear: enter decimal answers (up to 4 decimals), e.g. `0.8333`.

CI / Automation

A sample GitHub Actions workflow can be added to run tests on push and pull requests. It should install dependencies and run `pytest`.
