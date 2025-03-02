#!/bin/bash
# this script runs the linters
black --check .
flake8 .
isort --check .
# mypy .