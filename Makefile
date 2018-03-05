all:
	@echo "Do 'make install' and then 'make run'."

install:
	python -m venv .
	source bin/activate
	pip install -U -r requirements.txt
	deactivate

run:
	source bin/activate
	python bot.py
	deactivate
