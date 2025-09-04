#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, '.')

# Monkey patch to debug the flow
original_expand_modules = None
original_discover_files = None

def debug_expand_modules(modules, ignore_list, ignore_list_re, ignore_list_paths_re):
    print(f"expand_modules called with modules: {modules}")
    result, errors = original_expand_modules(modules, ignore_list, ignore_list_re, ignore_list_paths_re)
    print(f"expand_modules returning {len(result)} results:")
    for r in result:
        print(f"  {r['path']} -> {r['name']}")
    return result, errors

def debug_discover_files(self, files_or_modules):
    print(f"_discover_files called with: {files_or_modules}")
    result = list(original_discover_files(self, files_or_modules))
    print(f"_discover_files returning: {result}")
    return result

# Patch the functions
from pylint.lint import expand_modules as expand_mod
from pylint.lint.pylinter import PyLinter

original_expand_modules = expand_mod.expand_modules
original_discover_files = PyLinter._discover_files

expand_mod.expand_modules = debug_expand_modules
PyLinter._discover_files = debug_discover_files

# Now run the actual test
os.chdir('test_recursive')
import subprocess
result = subprocess.run([
    sys.executable, '-m', 'pylint', 
    '--recursive=y', '--ignore-paths=^\.a$', '.'
], capture_output=True, text=True)

print("Final output:", result.stdout)
