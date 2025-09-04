#!/usr/bin/env python3
"""
Comprehensive test to validate the recursive ignore pattern fix.

This test reproduces the exact issue described in the GitHub issue and validates
that all the reported commands now work correctly.
"""

import os
import tempfile
import subprocess
import sys

def create_test_structure(base_dir):
    """Create the exact file structure from the issue"""
    # Create .a/foo.py
    os.makedirs(os.path.join(base_dir, '.a'))
    with open(os.path.join(base_dir, '.a', 'foo.py'), 'w') as f:
        f.write('# import re\n')
    
    # Create bar.py  
    with open(os.path.join(base_dir, 'bar.py'), 'w') as f:
        f.write('# import re\n')

def run_pylint(args, cwd):
    """Run pylint with given args and return stdout"""
    cmd = [sys.executable, '-m', 'pylint'] + args
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    return result.stdout, result.returncode

def test_issue_commands():
    """Test all commands from the original GitHub issue"""
    print("🧪 Testing Pylint Recursive Mode Ignore Pattern Fix")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        create_test_structure(tmpdir)
        print(f"📁 Created test structure in {tmpdir}")
        print("   ├── .a/")
        print("   │   └── foo.py")
        print("   └── bar.py")
        print()
        
        # Test cases from the original issue
        test_cases = [
            {
                'name': 'Default recursive mode (no ignore)',
                'args': ['--recursive=y', '.'],
                'expect_both': True,
                'description': 'Should find both files'
            },
            {
                'name': 'Recursive with --ignore=.a',
                'args': ['--recursive=y', '--ignore=.a', '.'], 
                'expect_both': False,
                'description': 'Should ignore .a directory (now fixed)'
            },
            {
                'name': 'Recursive with --ignore-patterns="^\.a"',
                'args': ['--recursive=y', '--ignore-patterns=^\.a', '.'],
                'expect_both': False, 
                'description': 'Should ignore directories starting with .a (now fixed)'
            }
        ]
        
        all_passed = True
        
        for i, test in enumerate(test_cases, 1):
            print(f"Test {i}: {test['name']}")
            print(f"Command: pylint {' '.join(test['args'])}")
            print(f"Expected: {test['description']}")
            
            stdout, returncode = run_pylint(test['args'], tmpdir)
            
            has_foo = '.a/foo.py' in stdout or 'foo' in stdout
            has_bar = 'bar.py' in stdout or 'bar' in stdout
            
            if test['expect_both']:
                # Should find both files
                if has_foo and has_bar:
                    print("✅ PASS: Both files found as expected")
                else:
                    print(f"❌ FAIL: Expected both files, got foo={has_foo}, bar={has_bar}")
                    all_passed = False
            else:
                # Should ignore .a/foo.py, only find bar.py
                if not has_foo and has_bar:
                    print("✅ PASS: Only bar.py found, .a/foo.py correctly ignored")
                else:
                    print(f"❌ FAIL: Expected only bar.py, got foo={has_foo}, bar={has_bar}")
                    all_passed = False
            
            print(f"Output preview: {stdout[:100].strip()}{'...' if len(stdout) > 100 else ''}")
            print()
        
        print("=" * 60)
        if all_passed:
            print("🎉 SUCCESS: All tests passed! The recursive ignore fix is working correctly.")
            print("\n📋 Summary:")
            print("   ✅ --ignore option now works in recursive mode")
            print("   ✅ --ignore-patterns option now works in recursive mode") 
            print("   ✅ Default recursive behavior unchanged")
            print("\n🐛 The original issue has been resolved!")
        else:
            print("❌ FAILURE: Some tests failed. The fix needs more work.")
        
        return all_passed

if __name__ == '__main__':
    success = test_issue_commands()
    sys.exit(0 if success else 1)