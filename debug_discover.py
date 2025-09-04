#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, '.')

from pylint.lint.pylinter import PyLinter
from pylint.lint.run import Run
import re

# Create a test instance
linter = PyLinter()
linter.load_default_plugins()

# Setup config manually  
linter.config.ignore = []
linter.config.ignore_patterns = []
linter.config.ignore_paths = [re.compile(r'^\.a$')]

print("Testing _discover_files with debug output:")
print(f"ignore_paths patterns: {[p.pattern for p in linter.config.ignore_paths]}")
print()

os.chdir('test_recursive')
discovered = list(linter._discover_files(['.']))
print("Discovered files:")
for f in discovered:
    print(f"  {f}")
