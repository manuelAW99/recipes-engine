.PHONY: run
run:
	pip install -r requeriments.txt
	python3 start.py
	streamlit run app.py