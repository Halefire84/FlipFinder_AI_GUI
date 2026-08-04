# Deployment & Windows build

This project is a Streamlit app. Below are quick instructions to run locally, deploy on Streamlit Cloud, and build a Windows `.exe` using GitHub Actions or locally.

Local (run):
```
python -m venv .venv
.venv/bin/activate    # on Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Deploy to Streamlit Community Cloud (free for public repos):
- Push this repository to GitHub.
- Sign in to https://share.streamlit.io and connect your repo.
- Add `requirements.txt` if not present (this repo already has one).

Build Windows EXE (CI):
- I added a GitHub Actions workflow at [.github/workflows/build-windows.yml](.github/workflows/build-windows.yml).
- Trigger it via `Actions` → `Build Windows EXE` → `Run workflow` or push to `main`/`master`.
- The built `CooperRiverDealFinder.exe` will be uploaded as an artifact from the workflow.

Installer (optional)
- The workflow now also builds an NSIS installer. The NSIS script is at `installer/CooperRiverInstaller.nsi`.
- The workflow uploads both the single-file EXE and the `CooperRiverDealFinder-setup.exe` installer as artifacts.

Build Windows EXE (local Windows machine):
- Run the helper script: `scripts\build_windows.ps1` in PowerShell.

Notes:
- Free hosting services may sleep or reset app state; use the CSV export to persist data.
- Building on Linux cannot produce a Windows single-file `.exe` natively — use the CI workflow or a Windows machine.
