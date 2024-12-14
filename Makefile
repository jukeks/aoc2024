default:
	@echo "Usage: make run day=01 or make new day=02"

run:
	@uv run python -m aoc.$(day).main

new:
	@cp -r ./template ./aoc/$(day)

format:
	@uv run ruff format aoc template