UV_RUN	= uv run
MYPY	= $(UV_RUN) -m mypy
FLAKE8	= $(UV_RUN) -m flake8
CONFIG	:= config.jsonc

ARGS	?=

run: install
	@PYGAME_HIDE_SUPPORT_PROMPT=1 $(UV_RUN) -m src $(ARGS) $(CONFIG)

install:
	uv sync

debug: install
	@$(UV_RUN) -m pdb -m src $(ARGS)

test:
	uv run pytest $(ARGS)

test-verbose:
	uv run pytest -v $(ARGS)

lint: install
	$(FLAKE8) src
	$(MYPY) src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: install
	$(FLAKE8) src
	$(MYPY) src --strict

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf build dist
	uv clean

fclean: clean
	rm -rf .venv
	rm -rf .pak-man

build: clean
	uv run --locked pyinstaller --noconfirm --clean "pak-man.spec"
	cd dist && zip -qr "pac-man.zip" pak-man
	rm -rf build

.PHONY: run clean fclean install lint lint-strict debug test build
