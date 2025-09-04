#!/usr/bin/env python3
"""Test script to validate the recursive ignore fix"""

import os
import tempfile
import shutil
import subprocess
import sys

def test_recursive_ignore_fix():
    """Test that ignore patterns work in recursive mode"""
    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        os.makedirs(os.path.join(tmpdir, '.hidden'))
        
        with open(os.path.join(tmpdir, 'main.py'), 'w') as f:
            f.write('# main file\n')
            
        with open(os.path.join(tmpdir, '.hidden', 'secret.py'), 'w') as f:
            f.write('# hidden file\n')
        
        # Test 1: Without ignore patterns - should find both files
        print("Test 1: Without ignore patterns")
        result = subprocess.run([
            sys.executable, '-m', 'pylint', 
            '--recursive=y', '--disable=all', '--enable=missing-module-docstring',
            tmpdir
        ], capture_output=True, text=True, cwd=tmpdir)
        
        if 'main.py' in result.stdout and 'secret.py' in result.stdout:
            print("✅ Both files found (expected)")
        else:
            print("❌ Not all files found")
            print("STDOUT:", result.stdout)
            return False
        
        # Test 2: With ignore patterns - should ignore hidden directory  
        print("\nTest 2: With ignore patterns")
        result = subprocess.run([
            sys.executable, '-m', 'pylint',
            '--recursive=y', '--disable=all', '--enable=missing-module-docstring',
            '--ignore-patterns=^\\.hidden$',
            tmpdir
        ], capture_output=True, text=True, cwd=tmpdir)
        
        if 'main.py' in result.stdout and 'secret.py' not in result.stdout:
            print("✅ Hidden file ignored (expected)")
        else:
            print("❌ Hidden file not ignored")  
            print("STDOUT:", result.stdout)
            return False
            
        # Test 3: With ignore option - should ignore hidden directory
        print("\nTest 3: With ignore option")
        result = subprocess.run([
            sys.executable, '-m', 'pylint',
            '--recursive=y', '--disable=all', '--enable=missing-module-docstring', 
            '--ignore=.hidden',
            tmpdir
        ], capture_output=True, text=True, cwd=tmpdir)
        
        if 'main.py' in result.stdout and 'secret.py' not in result.stdout:
            print("✅ Hidden file ignored with --ignore (expected)")
        else:
            print("❌ Hidden file not ignored with --ignore")
            print("STDOUT:", result.stdout)
            return False
    
    print("\n🎉 All tests passed! The recursive ignore fix is working.")
    return True

if __name__ == '__main__':
    success = test_recursive_ignore_fix()
    sys.exit(0 if success else 1)