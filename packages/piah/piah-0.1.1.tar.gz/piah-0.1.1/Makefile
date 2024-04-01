.PHONY: clean test run-pre-commit install-pre-commit

test:
	pytest

run-pre-commit:
	pre-commit run --all-files

install-pre-commit:
	pre-commit install
	@echo "Now pre-commit will run on every commit :)"

clean:
	rm -rf .venv
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/

.ONESHELL:
