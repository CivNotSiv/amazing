run:
	python3 a_maze_ing.py config.txt

install:
	pip install -r requirements.txt

build:
	rm -rf *.whl
	pip install build
	python -m build
	mv ./dist/*.whl . 

debug:
	python3 -m pdb a_maze_ing.py config.txt

lint:
	python3 -m flake8 --exclude=.venv . 
	python3 -m mypy --strict --exclude '^.venv/' .

clean:
	pyclean . --debris
	rm -rf .mypy_cache

.PHONY: run install build debug lint clean
