VENV_NAME?=.venv
PATH_TO_ACTIVATE = $(VENV_NAME)/bin/activate

create_venv:
	python3 -m venv $(VENV_NAME)

install: create_venv requirements.txt
	(. $(PATH_TO_ACTIVATE) && pip install -e .)

data: nfl_analysis/etl/scraper.py
	(cd nfl_analysis/etl && python3 scraper.py)

dashboard: data nfl_analysis/dashboard/app.py
	(. $(PATH_TO_ACTIVATE) && cd nfl_analysis/dashboard && streamlit run app.py)

testrun: tests
	(. $(PATH_TO_ACTIVATE) && pytest tests)

beautiful:
	(. $(PATH_TO_ACTIVATE) && black nfl_analysis)