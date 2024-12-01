default:
	@echo "Usage: make run DAY=01 or make new DAY=02"

run:
	@poetry run python -m aoc.$(DAY).main

new:
	@cp -r ./template ./aoc/$(DAY)

format:
	@poetry run ruff format aoc template