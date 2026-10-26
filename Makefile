run:
	python3 a_maze_ing.py config.txt

install:
	pip install -r requirements.txt

build:
	pip install build
	python -m build
	mv ./dist/*.whl . && rm -rf dist && rm -rf src/mazegen.egg-info

debug:
	.venv/bin/python3 -m pdb a_maze_ing.py config.txt

lint:
	python3 -m flake8 --exclude=.venv . && python3 -m mypy --strict --exclude '^.venv/' .

clean:
	rm -rf __pycache__
	rm -rf mypy_cache
	rm -rf venv
	rm -rf .mypy_cache