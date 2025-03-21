.PHONY: run install organize clean zip deploy lint

run:
	python3 src/main.py

install:
	pip install -r requirements.txt

organize:
	mkdir -p src
	mkdir -p assets/sounds

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +

zip:
	zip -r asteroids-neon.zip src assets Makefile requirements.txt README.md .gitignore

deploy:
	git add .
	git commit -m "Auto commit from Makefile"
	git push
	@echo "✔ Repo changes pushed!"

lint:
	flake8 src/*.py
