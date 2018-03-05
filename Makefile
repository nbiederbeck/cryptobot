all:
	@echo "Do 'make install' and then 'make run'."

install:
	python -m venv .
	. bin/activate && pip install -U -r requirements.txt

run:
	. bin/activate && python bot.py
