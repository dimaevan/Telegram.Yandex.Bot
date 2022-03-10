req:
	@pip freeze> requirements.txt
	@echo "requirements.txt is update!"
lint:
	@flake8
dead:
	@vulture .
install:
	@poetry install
run:
	@poetry run python3 main.py
check:
	@make lint
	@make dead
