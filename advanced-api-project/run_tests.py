#!/usr/bin/env python3
"""
Test Runner for Django REST Framework API Tests

This script runs the comprehensive test suite for the advanced-api-project
and provides a summary of test results.

Usage:
    python run_tests.py
    python run_tests.py --verbose
    python run_tests.py --specific BookCRUDTestCase
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def run_command(command, description):
    """Run a command and return the result."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    start_time = time.time()
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    end_time = time.time()
    
    print(f"Duration: {end_time - start_time:.2f} seconds")
    print(f"Exit Code: {result.returncode}")
    
    if result.stdout:
        print(f"\nOutput:\n{result.stdout}")
    
    if result.stderr:
        print(f"\nErrors:\n{result.stderr}")
    
    return result.returncode == 0, result

def main():
    """Main test runner function."""
    print("Django REST Framework API Test Suite")
    print("=" * 80)
    print(f"Start Time: {datetime.now()}")
    print(f"Python Version: {sys.version}")
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Please run this script from the project root directory.")
        return False
    
    # Parse command line arguments
    verbose = '--verbose' in sys.argv
    specific_test = None
    
    for arg in sys.argv[1:]:
        if arg.startswith('--specific='):
            specific_test = arg.split('=')[1]
        elif arg not in ['--verbose']:
            specific_test = arg
    
    # Test categories to run
    if specific_test:
        test_categories = [f"api.test_views.{specific_test}"]
    else:
        test_categories = [
            "api.test_views.BookCRUDTestCase",
            "api.test_views.BookFilteringTestCase", 
            "api.test_views.AuthorAPITestCase",
            "api.test_views.CustomEndpointsTestCase",
            "api.test_views.PermissionAndAuthenticationTestCase",
            "api.test_views.DataValidationTestCase",
            "api.test_views.ErrorHandlingTestCase"
        ]
    
    # Run tests
    all_passed = True
    results = {}
    
    for category in test_categories:
        verbosity = "--verbosity=2" if verbose else "--verbosity=1"
        command = f"python manage.py test {category} {verbosity}"
        
        success, result = run_command(command, f"Testing {category}")
        results[category] = {
            'success': success,
            'output': result.stdout,
            'errors': result.stderr
        }
        
        if not success:
            all_passed = False
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed_count = 0
    failed_count = 0
    
    for category, result in results.items():
        status = "✅ PASSED" if result['success'] else "❌ FAILED"
        print(f"{status}: {category}")
        
        if result['success']:
            passed_count += 1
        else:
            failed_count += 1
            
        # Extract test count from output
        if "Ran" in result['output']:
            try:
                test_line = [line for line in result['output'].split('\n') if line.startswith('Ran')][0]
                print(f"    {test_line}")
            except:
                pass
    
    print(f"\nOverall Results:")
    print(f"✅ Passed: {passed_count} test categories")
    print(f"❌ Failed: {failed_count} test categories")
    print(f"🎯 Success Rate: {(passed_count/(passed_count+failed_count)*100):.1f}%")
    
    # Individual test recommendations
    if failed_count > 0:
        print(f"\n📋 To debug specific failures, run:")
        for category, result in results.items():
            if not result['success']:
                print(f"    python manage.py test {category} --verbosity=2")
    
    print(f"\nEnd Time: {datetime.now()}")
    
    if all_passed:
        print("\n🎉 All tests passed! Your API is working correctly.")
        return True
    else:
        print(f"\n⚠️  Some tests failed. Please review the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
