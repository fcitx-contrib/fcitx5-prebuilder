#!/bin/sh
set -e

ruff check scripts
ruff format --check scripts
pyright scripts/*.py
