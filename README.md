# Student Performance and Study-Time Predictor Using Exponential Growth Model

A small Streamlit project for a Computational Mathematics Laboratory assignment. It applies an exponential model to show how a student's score could approach a chosen target over a study period. The application calculates a score for every day, displays a summary and table, and plots the results.

This is a simplified mathematical simulation, not a scientifically validated predictor of actual exam results. Daily study hours are used to calculate total planned study time; the given score formula depends on elapsed days and the improvement constant `k`, not directly on daily hours.

## Requirements

- Python 3.10 or newer
- The packages listed in `requirements.txt`

## Install and run on Windows

Open PowerShell in this project folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If PowerShell blocks virtual-environment activation, open Command Prompt and use:

```bat
py -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit prints a local URL in the terminal, usually `http://localhost:8501`. Open that address in a browser. Stop the application with `Ctrl+C` in the terminal.

## Formula

The app uses

\[
\mathrm{Score}(t) = S_{\max} - (S_{\max} - S_0)e^{-kt}
\]

where `S0` is the current score percentage, `Smax` is the target percentage, `k` is a positive improvement constant, and `t` is study time in days. The expression models exponential decay of the remaining gap to the target. At day zero the result is the initial score; as time increases it approaches the target. When the target equals the initial score, the gap is zero and the model remains constant.

## Example

Enter these values in the sidebar:

| Input | Example |
| --- | ---: |
| Student name | Alex Morgan |
| Current score | 58% |
| Target score | 90% |
| Daily study hours | 2.5 |
| Study period | 30 days |
| Improvement constant `k` | 0.08 |

The planned study time is `75.0 hours`. The modelled score is `58.00%` on day 0 and approximately `87.10%` on day 30, a modelled increase of `29.10 percentage points`. The target is approached but not reached within this finite period.

## Files

- `app.py` — Streamlit interface, input validation, NumPy calculation, table, and Matplotlib graph.
- `requirements.txt` — application dependencies.
- `documentation.md` — formal project report.