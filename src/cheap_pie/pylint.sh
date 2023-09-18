#!/usr/bin/env bash
pylint $(git ls-files '*.py') > pylint.log