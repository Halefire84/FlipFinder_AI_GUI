# FlipFinder_AI_GUI

Ebay / Goodwill / Auction deal finder with a Streamlit GUI for tracking
and evaluating resale opportunities across multiple marketplaces.

Quickstart
----------

1. Create a Python virtual environment and activate it:

	python3 -m venv .venv
	source .venv/bin/activate

2. Install dependencies:

	pip install -r requirements.txt

3. Run the Streamlit app:

	python main.py run

Or run directly with Streamlit:

	streamlit run app.py

Notes
-----

- The main Streamlit UI is in `app.py`.
- Several modules (`flipfinder_core.py`, `marketplace_scraper.py`,
  `ai_value_estimator.py`, `risk_model.py`, `utils.py`) are currently
  empty stubs — implement scraping and estimation logic there as needed.

