all:
	@echo "Do 'make venv' once, 'make install' at least once and then 'make run'."

venv:
	python -m venv .

install:
	. bin/activate && pip install -U -r requirements.txt

run:
	. bin/activate && python bot.py

git:
	git pull
