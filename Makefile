PACKAGES = \


install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install $(PACKAGES)

run:
	.venv/bin/python3 a_maze_ing.py config.txt

debug:
	.venv/bin/python3 -m pdb a_maze_ing.py config.txt

lint:
	python3 -m flake8 . && mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean:
	rm -rf __pycache__
	rm -rf mypy_cache
	rm -rf .venv