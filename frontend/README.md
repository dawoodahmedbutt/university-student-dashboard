# UniSystem Dashboard — Frontend v2

This is an organized, modular Streamlit frontend scaffold based on your existing dashboard.

Structure:

- `src/app.py` — main entrypoint
- `src/pages/` — page modules (`director`, `wellbeing`, `explorer`, `data_management`)
- `src/components/` — shared UI helpers
- `src/data/dashboard_api.py` — lightweight fake backend/data layer
- `src/utils.py` — helpers

Run:

```powershell
cd e:\WarWick\PAI\GrouAssignment\fron-end\frontend_v2\src
streamlit run app.py
```

Notes:

- The fake backend lives in `src/data/dashboard_api.py` and returns randomized demo data.
- Pages are small and easy to extend; split widgets into `components` as needed.

Next steps I can do for you:

- Port more of the original dashboard UI/logic into each page.
- Add tests or type hints across modules.
- Wire this repo to a git branch and commit the scaffold.
