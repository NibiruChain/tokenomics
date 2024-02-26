# Displays available recipes by running `just -l`.
setup:
  #!/usr/bin/env bash
  just -l

run:
  poetry run python main.py

alias r := run

i:
  poetry install

# Cleans and resets the environment for Poetry
clean:
  # Cleans and resets the enviroment for the Poetry package manager, which is
  # used to manage Python dependencies.
  echo "clearing .cache/pypoetry" 
  rm -rf ~/.cache/pypoetry

  echo "clearing .venv" 
  rm -rf .venv

  echo "clearing poetry.lock" 
  rm -f poetry.lock

  echo "poetry cache clear pypi --all"
  poetry cache clear pypi --all

  poetry env use $(pyenv versions | grep '*' | cut -d' ' -f2)

# Build everything.
build:
  poetry install
  poetry build

alias b := build

fmt: 
  poetry run black .

lint:
  poetry run mypy pkg main.py
