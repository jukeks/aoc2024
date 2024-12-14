default:
	@echo "Usage: make run DAY=01 or make new DAY=02"

run:
	@uv run python -m aoc.$(DAY).main

new:
	@cp -r ./template ./aoc/$(DAY)

format:
	@uv run ruff format aoc template