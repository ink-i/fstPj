#!/usr/bin/env python3
"""
Oracle SQL Formatter for DBeaver
Formats SQL from stdin and outputs to stdout
"""

import sys
import argparse
import os
from pathlib import Path
import sqlparse
from sqlparse.tokens import Keyword, Name
import yaml


def load_config():
    """Load configuration from default locations"""
    config_paths = [
        Path.home() / '.sql_formatter.yaml',
        Path('.sql_formatter.yaml'),
    ]

    default_config = {
        'indent_width': 2,
        'keyword_case': 'upper',
        'identifier_case': 'preserve',
        'comma_before': False,
        'line_between_queries': 2,
        'reindent_aligned': True,
        'wrap_after': 80,
    }

    for config_path in config_paths:
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = yaml.safe_load(f) or {}
                    default_config.update(user_config)
                    break
            except Exception as e:
                print(f"Warning: Could not load config from {config_path}: {e}",
                      file=sys.stderr)

    return default_config


def format_sql(sql_text, config):
    """Format SQL text using sqlparse with Oracle-specific settings"""

    # Parse keyword case
    keyword_case = config.get('keyword_case', 'upper')
    if keyword_case not in ['upper', 'lower', 'capitalize']:
        keyword_case = 'upper'

    # Parse identifier case
    identifier_case = config.get('identifier_case', 'preserve')
    if identifier_case not in ['upper', 'lower', 'preserve']:
        identifier_case = 'preserve'

    # Format options for sqlparse
    format_options = {
        'keyword_case': keyword_case,
        'identifier_case': identifier_case if identifier_case != 'preserve' else None,
        'strip_comments': False,
        'reindent': True,
        'indent_tabs': False,
        'indent_width': config.get('indent_width', 2),
        'wrap_after': config.get('wrap_after', 80) if config.get('wrap_after', 80) > 0 else None,
        'use_space_around_operators': True,
        'comma_first': config.get('comma_before', False),
        'reindent_aligned': config.get('reindent_aligned', True),
    }

    # Remove None values
    format_options = {k: v for k, v in format_options.items() if v is not None}

    # Split multiple statements and format each
    statements = sqlparse.split(sql_text)
    formatted_statements = []

    for statement in statements:
        if statement.strip():
            formatted = sqlparse.format(statement, **format_options)
            formatted_statements.append(formatted.strip())

    # Join with appropriate line spacing
    line_between = '\n' * config.get('line_between_queries', 2)
    result = line_between.join(formatted_statements)

    # Ensure single newline at end
    if result and not result.endswith('\n'):
        result += '\n'

    return result


def main():
    parser = argparse.ArgumentParser(
        description='Oracle SQL Formatter for DBeaver',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  echo "select * from emp" | python sql_formatter.py
  cat query.sql | python sql_formatter.py --indent-width 4
  python sql_formatter.py --keyword-case upper < input.sql > output.sql
        """
    )

    parser.add_argument(
        '--indent-width',
        type=int,
        help='Number of spaces for indentation (default: 2)'
    )

    parser.add_argument(
        '--keyword-case',
        choices=['upper', 'lower', 'capitalize'],
        help='Keyword case transformation (default: upper)'
    )

    parser.add_argument(
        '--identifier-case',
        choices=['upper', 'lower', 'preserve'],
        help='Identifier case transformation (default: preserve)'
    )

    parser.add_argument(
        '--comma-before',
        action='store_true',
        help='Place comma before items in lists'
    )

    parser.add_argument(
        '--line-between-queries',
        type=int,
        help='Number of blank lines between queries (default: 2)'
    )

    parser.add_argument(
        '--wrap-after',
        type=int,
        help='Wrap lines after N characters (0 = no wrap, default: 80)'
    )

    parser.add_argument(
        '--config',
        type=Path,
        help='Path to config file (default: ~/.sql_formatter.yaml)'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='Oracle SQL Formatter 1.0.0'
    )

    args = parser.parse_args()

    # Load base configuration
    config = load_config()

    # Override with command-line arguments
    if args.indent_width is not None:
        config['indent_width'] = args.indent_width
    if args.keyword_case is not None:
        config['keyword_case'] = args.keyword_case
    if args.identifier_case is not None:
        config['identifier_case'] = args.identifier_case
    if args.comma_before:
        config['comma_before'] = True
    if args.line_between_queries is not None:
        config['line_between_queries'] = args.line_between_queries
    if args.wrap_after is not None:
        config['wrap_after'] = args.wrap_after

    # Read SQL from stdin
    try:
        sql_input = sys.stdin.read()

        if not sql_input.strip():
            print("Error: No SQL input provided", file=sys.stderr)
            sys.exit(1)

        # Format the SQL
        formatted_sql = format_sql(sql_input, config)

        # Output to stdout
        print(formatted_sql, end='')

    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
