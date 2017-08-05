#!/usr/bin/sh

echo "Test script{% if project_codename %} for {{ project_codename }}{% endif %}"

# Alternative: test a specific file
# python -m unittest test.test_{% if project_codename %}{{ project_codename }}{% else %}something{% endif %}

python3 -m unittest discover -s test
