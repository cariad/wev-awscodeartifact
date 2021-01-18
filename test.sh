#!/bin/bash -e

if [[ "${CI:=}" == "true" ]]; then
  echo "Linting in CI mode. Warnings will result in failure."
  ci=1
else
  echo "Linting in LOCAL mode. Warnings will be fixed when possible."
  ci=0
fi

echo "Linting YAML..."
yamllint . --strict

echo "Sorting Python import definitions..."
if [[ "${ci:?}" == "1" ]]; then
  isort . --check-only --diff
else
  isort .
fi

echo "Applying opinionated Python code style..."
if [[ "${ci:?}" == "1" ]]; then
  black . --check --diff
else
  black .
fi

echo "Checking PEP8 compliance..."
flake8 .

echo "Checking Python types..."
mypy wev_awscodeartifact

echo "Testing..."
pytest
