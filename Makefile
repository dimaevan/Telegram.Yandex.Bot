req:
	@pip freeze> requirements.txt
	@echo "requirements.txt is update!"
lint:
	@flake8
dead:
	@vulture .
