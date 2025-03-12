#!/usr/bin/env python3
"""
Code Quality Audit Tool for Chad Battles Cabal Feature
This script performs static analysis on the codebase to identify
potential issues, code smells, and best practices violations.
"""

import os
import re
import sys
import glob
from datetime import datetime
from collections import defaultdict, Counter

# Configuration
CODEBASE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REPORT_FILENAME = 'cabal_audit_report.md'

# Files and patterns to analyze
ANALYSIS_PATTERNS = [
    os.path.join(CODEBASE_ROOT, 'app/models/cabal.py'),
    os.path.join(CODEBASE_ROOT, 'app/controllers/cabal.py'),
    os.path.join(CODEBASE_ROOT, 'app/templates/cabal/*.html'),
    os.path.join(CODEBASE_ROOT, 'app/utils/bot_commands.py'),
    os.path.join(CODEBASE_ROOT, 'tests/test_cabal_*.py')
]

# Security patterns to check for
SECURITY_PATTERNS = [
    (r'eval\(', 'Use of eval() function'),
    (r'exec\(', 'Use of exec() function'),
    (r'os\.system\(', 'Use of os.system()'),
    (r'subprocess\..*shell\s*=\s*True', 'Shell injection risk'),
    (r'__import__\(', 'Dynamic imports'),
    (r'request\.form\.get\(.*\)', 'Form data without validation'),
    (r'json\.loads\(.*request', 'Parsing JSON from request without validation'),
]

# Code smell patterns
CODE_SMELL_PATTERNS = [
    (r'# TODO', 'TODO comment'),
    (r'# FIXME', 'FIXME comment'),
    (r'print\(', 'Debug print statement'),
    (r'\.commit\(\)', 'Explicit commit - check transaction management'),
    (r'except:(?!\s*#)', 'Bare except clause'),
    (r'except Exception', 'Catching Exception - too broad'),
    (r'return None', 'Explicit return None'),
    (r'if\s+[^:]+\s*==\s*(True|False)', 'Comparison to True/False'),
    (r'\.first\(\)\.', 'Accessing attributes after .first() without checking None'),
    (r'datetime\.utcnow\(\)[^)]', 'Datetime usage - check for timezone awareness'),
]

# Best practices
BEST_PRACTICE_PATTERNS = [
    (r'def\s+\w+\([^)]*\):\s*(?!\s*""")', 'Function without docstring'),
    (r'class\s+\w+(\([\w, ]+\))?:\s*(?!\s*""")', 'Class without docstring'),
    (r'if\s+len\(.*\)\s*[=><!]=?\s*[0-9]', 'Using len() in comparison - use implicit truthiness'),
    (r'(?<!\w)self\..*\s=\s.*\bself\.', 'Self assignment in method/constructor'),
    (r'\s{4,}', 'Indentation over 4 spaces'),
    (r'\t', 'Tab character used for indentation'),
    (r'# noqa', 'Linter suppression'),
]

def find_files():
    """Find all files matching the given patterns."""
    files = []
    
    for pattern in ANALYSIS_PATTERNS:
        # Use glob to find files matching the pattern
        matched_files = glob.glob(pattern, recursive=True)
        if matched_files:
            for file_path in matched_files:
                # Convert to relative path for reporting
                rel_path = os.path.relpath(file_path, CODEBASE_ROOT)
                files.append(rel_path)
        else:
            print(f"No files found matching pattern: {pattern}")
    
    return sorted(set(files))

def count_lines(file_path):
    """Count the number of code lines in a file."""
    full_path = os.path.join(CODEBASE_ROOT, file_path)
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        # Try another encoding if UTF-8 fails
        try:
            with open(full_path, 'r', encoding='latin-1') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return {'total': 0, 'code': 0, 'blank': 0, 'comment': 0}
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return {'total': 0, 'code': 0, 'blank': 0, 'comment': 0}
    
    code_lines = 0
    blank_lines = 0
    comment_lines = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            blank_lines += 1
        elif line.startswith('#') or line.startswith('//') or line.startswith('<!--'):
            comment_lines += 1
        else:
            code_lines += 1
    
    return {
        'total': len(lines),
        'code': code_lines,
        'blank': blank_lines,
        'comment': comment_lines
    }

def analyze_file(file_path):
    """Analyze a single file for issues."""
    results = {
        'security': [],
        'code_smells': [],
        'best_practices': []
    }
    
    # Don't try to analyze binary files
    if not file_path.endswith(('.py', '.html', '.js', '.css', '.md')):
        return results
    
    full_path = os.path.join(CODEBASE_ROOT, file_path)
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
    except UnicodeDecodeError:
        # Try another encoding if UTF-8 fails
        try:
            with open(full_path, 'r', encoding='latin-1') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return results
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return results
    
    # Check for security issues
    for pattern, description in SECURITY_PATTERNS:
        for i, line in enumerate(lines):
            if re.search(pattern, line):
                results['security'].append({
                    'line': i + 1,
                    'description': description,
                    'snippet': line.strip()
                })
    
    # Check for code smells
    for pattern, description in CODE_SMELL_PATTERNS:
        for i, line in enumerate(lines):
            if re.search(pattern, line):
                results['code_smells'].append({
                    'line': i + 1,
                    'description': description,
                    'snippet': line.strip()
                })
    
    # Check for best practice violations
    for pattern, description in BEST_PRACTICE_PATTERNS:
        for i, line in enumerate(lines):
            if re.search(pattern, line):
                results['best_practices'].append({
                    'line': i + 1,
                    'description': description,
                    'snippet': line.strip()
                })
    
    return results

def calculate_metrics(files):
    """Calculate code metrics from analyzed files."""
    metrics = {
        'total_files': len(files),
        'total_lines': 0,
        'code_lines': 0,
        'comment_lines': 0,
        'blank_lines': 0,
        'lines_per_file': 0,
        'security_issues': 0,
        'code_smells': 0,
        'best_practice_issues': 0,
        'file_types': Counter()
    }
    
    for file_path in files:
        ext = os.path.splitext(file_path)[1]
        metrics['file_types'][ext] += 1
        
        # Count lines
        line_counts = count_lines(file_path)
        metrics['total_lines'] += line_counts['total']
        metrics['code_lines'] += line_counts['code']
        metrics['comment_lines'] += line_counts['comment']
        metrics['blank_lines'] += line_counts['blank']
        
        # Count issues
        issues = analyze_file(file_path)
        metrics['security_issues'] += len(issues['security'])
        metrics['code_smells'] += len(issues['code_smells'])
        metrics['best_practice_issues'] += len(issues['best_practices'])
    
    if metrics['total_files'] > 0:
        metrics['lines_per_file'] = metrics['total_lines'] / metrics['total_files']
    
    return metrics

def generate_report(files, metrics, issues_by_file):
    """Generate a markdown report of findings."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# Code Audit Report: Cabal Feature
Generated on: {now}

## Summary
- Total Files: {metrics['total_files']}
- Total Lines: {metrics['total_lines']}
  - Code: {metrics['code_lines']} ({(metrics['code_lines']/metrics['total_lines']*100 if metrics['total_lines'] > 0 else 0):.1f}%)
  - Comments: {metrics['comment_lines']} ({(metrics['comment_lines']/metrics['total_lines']*100 if metrics['total_lines'] > 0 else 0):.1f}%)
  - Blank: {metrics['blank_lines']} ({(metrics['blank_lines']/metrics['total_lines']*100 if metrics['total_lines'] > 0 else 0):.1f}%)
- Average Lines per File: {metrics['lines_per_file']:.1f}
- Issues Found:
  - Security Issues: {metrics['security_issues']}
  - Code Smells: {metrics['code_smells']}
  - Best Practice Violations: {metrics['best_practice_issues']}

## File Types
"""
    
    for ext, count in metrics['file_types'].most_common():
        report += f"- {ext or 'no extension'}: {count} files\n"
    
    report += "\n## Files Analyzed\n"
    for file_path in files:
        report += f"- {file_path}\n"
    
    report += "\n## Issues by File\n"
    
    for file_path in files:
        file_issues = issues_by_file[file_path]
        total_issues = (len(file_issues['security']) + 
                        len(file_issues['code_smells']) + 
                        len(file_issues['best_practices']))
        
        if total_issues == 0:
            continue
        
        report += f"\n### {file_path} ({total_issues} issues)\n"
        
        if file_issues['security']:
            report += "\n#### Security Issues\n"
            for issue in file_issues['security']:
                report += f"- Line {issue['line']}: {issue['description']}\n  `{issue['snippet']}`\n"
        
        if file_issues['code_smells']:
            report += "\n#### Code Smells\n"
            for issue in file_issues['code_smells']:
                report += f"- Line {issue['line']}: {issue['description']}\n  `{issue['snippet']}`\n"
        
        if file_issues['best_practices']:
            report += "\n#### Best Practice Violations\n"
            for issue in file_issues['best_practices']:
                report += f"- Line {issue['line']}: {issue['description']}\n  `{issue['snippet']}`\n"
    
    report += "\n## Recommendations\n\n"
    
    # Add recommendations based on findings
    if metrics['security_issues'] > 0:
        report += "### Security\n"
        report += "- Review all SQL queries for potential injection risks\n"
        report += "- Ensure all user inputs are validated and sanitized\n"
        report += "- Add CSRF protection to all forms\n"
        report += "- Review authentication checks in sensitive routes\n\n"
    
    if metrics['code_smells'] > 0:
        report += "### Code Quality\n"
        report += "- Remove debug print statements\n"
        report += "- Address TODOs and FIXMEs\n"
        report += "- Improve exception handling - use specific exceptions\n"
        report += "- Review database transaction management\n\n"
    
    if metrics['best_practice_issues'] > 0:
        report += "### Best Practices\n"
        report += "- Add docstrings to all functions and classes\n"
        report += "- Standardize indentation and spacing\n"
        report += "- Use more descriptive variable names where needed\n"
        report += "- Add type hints to function parameters and return values\n\n"
    
    report += "### Testing\n"
    report += "- Increase test coverage for critical functionality\n"
    report += "- Add integration tests for battle mechanics\n"
    report += "- Add performance tests for power calculation\n"
    report += "- Add security tests for leadership actions\n\n"
    
    return report

def main():
    """Main function to run the audit."""
    print(f"Starting code audit for Cabal feature...")
    
    # Find files to analyze
    files = find_files()
    print(f"Found {len(files)} files to analyze.")
    
    if not files:
        print("No files found to analyze. Check the analysis patterns.")
        return
    
    # Analyze each file
    issues_by_file = {}
    for file_path in files:
        print(f"Analyzing {file_path}...")
        issues_by_file[file_path] = analyze_file(file_path)
    
    # Calculate metrics
    metrics = calculate_metrics(files)
    
    # Generate report
    report = generate_report(files, metrics, issues_by_file)
    
    # Write report to file
    report_path = os.path.join(CODEBASE_ROOT, REPORT_FILENAME)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Audit complete. Report written to {report_path}")
    
    # Summary
    print("\nSummary:")
    print(f"Total Files: {metrics['total_files']}")
    print(f"Total Lines: {metrics['total_lines']}")
    print(f"Security Issues: {metrics['security_issues']}")
    print(f"Code Smells: {metrics['code_smells']}")
    print(f"Best Practice Violations: {metrics['best_practice_issues']}")

if __name__ == "__main__":
    main() 