#!/usr/bin/env python3
"""
Oracle SQL Formatter for DBeaver
Simple and reliable formatter for Oracle SQL style
"""

import sys
import argparse
from pathlib import Path
import sqlparse
import yaml
import re


def load_config():
    """Load configuration from default locations"""
    config_paths = [
        Path.home() / '.oracle_formatter.yaml',
        Path('.oracle_formatter.yaml'),
    ]

    default_config = {
        'indent_width': 9,
        'keyword_case': 'upper',
        'comma_before': True,
        'line_between_queries': 2,
    }

    for config_path in config_paths:
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = yaml.safe_load(f) or {}
                    default_config.update(user_config)
                    break
            except Exception:
                pass

    return default_config


def merge_case_statements(text):
    """
    Merge multi-line CASE statements into single lines.
    Handles nested CASE statements correctly.
    """
    lines = text.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Check if this line contains CASE keyword
        if re.search(r'\bCASE\b', stripped, re.IGNORECASE):
            # Get base indentation
            indent_match = re.match(r'^(\s*)', line)
            base_indent = indent_match.group(1) if indent_match else ''

            # Collect all parts of the CASE statement
            case_parts = [stripped]
            i += 1

            # Track CASE depth for nested statements
            case_depth = stripped.upper().count('CASE') - stripped.upper().count('END')

            # Collect lines until all CASE statements are closed
            while i < len(lines) and case_depth > 0:
                current_line = lines[i].strip()

                if current_line:  # Skip empty lines
                    case_parts.append(current_line)

                    # Update depth
                    case_depth += current_line.upper().count('CASE')
                    case_depth -= current_line.upper().count('END')

                i += 1

            # Merge into single line
            merged = base_indent + ' '.join(case_parts)
            result.append(merged)
        else:
            result.append(line)
            i += 1

    return '\n'.join(result)


def format_sql(sql_text, config):
    """Format SQL text with Oracle style"""

    # Use sqlparse for basic formatting
    formatted = sqlparse.format(
        sql_text,
        keyword_case='upper',
        identifier_case=None,
        strip_comments=False,
        reindent=True,
        indent_tabs=False,
        indent_width=config.get('indent_width', 9),
        use_space_around_operators=True,
        comma_first=config.get('comma_before', True),
        reindent_aligned=True,
    )

    # Post-process: merge standalone commas with next line
    lines = formatted.split('\n')
    merged_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # If this is a standalone comma, merge with next line
        if stripped == ',' and i + 1 < len(lines):
            next_line = lines[i + 1]
            indent = len(line) - len(stripped)
            merged = ' ' * indent + ', ' + next_line.strip()
            merged_lines.append(merged)
            i += 2
        else:
            merged_lines.append(line)
            i += 1

    formatted = '\n'.join(merged_lines)

    # Post-process: merge CASE statements into single lines
    formatted = merge_case_statements(formatted)

    return formatted


def main():
    parser = argparse.ArgumentParser(
        description='Oracle SQL Formatter for DBeaver',
        epilog='Example: echo "select * from emp" | python oracle_formatter.py'
    )

    parser.add_argument(
        '--indent-width',
        type=int,
        help='Number of spaces for indentation (default: 9)'
    )

    parser.add_argument(
        '--keyword-case',
        choices=['upper', 'lower', 'capitalize'],
        help='Keyword case transformation (default: upper)'
    )

    parser.add_argument(
        '--comma-before',
        action='store_true',
        default=True,
        help='Place comma before items in lists (default: True)'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='Oracle SQL Formatter 2.0.0'
    )

    args = parser.parse_args()

    # Load configuration
    config = load_config()

    # Override with command-line arguments
    if args.indent_width is not None:
        config['indent_width'] = args.indent_width
    if args.keyword_case is not None:
        config['keyword_case'] = args.keyword_case
    if args.comma_before is not None:
        config['comma_before'] = args.comma_before

    # Read SQL from stdin
    try:
        sql_input = sys.stdin.read()

        if not sql_input.strip():
            print("Error: No SQL input provided", file=sys.stderr)
            sys.exit(1)

        # Format the SQL
        formatted_sql = format_sql(sql_input, config)

        # Output to stdout with proper error handling
        try:
            sys.stdout.write(formatted_sql)
            sys.stdout.write('\n')
            sys.stdout.flush()
        except BrokenPipeError:
            sys.stderr.close()
            sys.exit(0)

    except KeyboardInterrupt:
        sys.exit(0)
    except BrokenPipeError:
        import os
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
