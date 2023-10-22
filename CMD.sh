#!/bin/bash

function install {
    pip install pre-commit
    pre-commit install
}

function test {
    python -m pytest test_main.py
}

function commit {
    git add .
    git commit
}

function fmt {
    python -m black .
}

"$@"
