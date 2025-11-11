#!/usr/bin/env python3
"""
Oracle SQL Formatter for DBeaver
"""

import sys
import argparse
from pathlib import Path
import sqlparse
import yaml
import re


def load_config():
    """Load configuration"""
    return {'column_indent': 5}


def smart_split_on_comma(text):
    """
    Split text on commas, but not commas inside parentheses or CASE...END
    """
    items = []
    current = []
    paren_depth = 0
    case_depth = 0
    i = 0

    while i < len(text):
        char = text[i]

        # Track parentheses
        if char == '(':
            paren_depth += 1
        elif char == ')':
            paren_depth -= 1

        # Track CASE...END
        # Look ahead for keywords
        if text[i:i+4].upper() == 'CASE':
            case_depth += 1
        elif text[i:i+3].upper() == 'END':
            # Make sure it's END keyword, not part of another word
            if i + 3 >= len(text) or not text[i+3].isalnum():
                case_depth -= 1

        # Split on comma only if not inside parentheses or CASE
        if char == ',' and paren_depth == 0 and case_depth == 0:
            items.append(''.join(current))
            current = []
        else:
            current.append(char)

        i += 1

    # Add the last item
    if current:
        items.append(''.join(current))

    return items


def format_sql(sql_text, config):
    """Format SQL with Oracle style"""

    # Step 1: Basic cleanup and keyword uppercase
    formatted = sqlparse.format(sql_text, keyword_case='upper', strip_comments=False)

    # Step 2: Remove all line breaks - work with single line
    formatted = ' '.join(formatted.split())

    # Step 3: Add line breaks at key points
    # Add newline before FROM
    formatted = re.sub(r'\s+FROM\s+', '\n  FROM ', formatted, flags=re.IGNORECASE)

    # Add newline before WHERE
    formatted = re.sub(r'\s+WHERE\s+', '\n WHERE ', formatted, flags=re.IGNORECASE)

    # Add newline before JOIN
    formatted = re.sub(r'\s+(LEFT\s+JOIN|RIGHT\s+JOIN|INNER\s+JOIN|FULL\s+JOIN|CROSS\s+JOIN|JOIN)\s+',
                      r'\n  \1 ', formatted, flags=re.IGNORECASE)

    # Add newline before ON
    formatted = re.sub(r'\s+ON\s+', '\n    ON ', formatted, flags=re.IGNORECASE)

    # Add newline before ORDER BY
    formatted = re.sub(r'\s+ORDER\s+BY\s+', '\n ORDER BY ', formatted, flags=re.IGNORECASE)

    # Add newline before GROUP BY
    formatted = re.sub(r'\s+GROUP\s+BY\s+', '\n GROUP BY ', formatted, flags=re.IGNORECASE)

    # Step 4: Handle commas in SELECT list
    lines = formatted.split('\n')
    result = []

    for line in lines:
        if line.strip().startswith('SELECT'):
            # This is the SELECT line - split on commas smartly
            select_part, rest = line.split('SELECT', 1)
            items = smart_split_on_comma(rest)

            # First item goes on SELECT line
            result.append('SELECT ' + items[0].strip())

            # Rest go on new lines with comma prefix
            for item in items[1:]:
                result.append('     , ' + item.strip())
        else:
            result.append(line)

    formatted = '\n'.join(result)

    # Step 5: Format CASE statements
    formatted = format_case_statements(formatted)

    return formatted.strip()


def format_case_statements(text):
    """Format CASE statements with WHEN/ELSE on new lines"""

    # Track CASE depth
    def process_case(match):
        case_content = match.group(0)

        # Add line breaks before WHEN
        case_content = re.sub(r'\s+WHEN\s+', '\n          WHEN ', case_content, flags=re.IGNORECASE)

        # Add line breaks before ELSE (but not for NULLIF, etc)
        case_content = re.sub(r'(?<![A-Z])ELSE\s+', '\n          ELSE ', case_content, flags=re.IGNORECASE)

        # Add line break before final END
        # This is tricky - we need to find the matching END
        # For now, let's do a simple approach
        parts = re.split(r'(\bEND\b)', case_content, flags=re.IGNORECASE)

        if len(parts) >= 2:
            # Rejoin with newline before last END
            result_parts = []
            for i, part in enumerate(parts):
                if part.upper() == 'END' and i == len(parts) - 2:
                    result_parts.append('\n       ' + part)
                else:
                    result_parts.append(part)
            case_content = ''.join(result_parts)

        return case_content

    # Find outermost CASE statements and process them
    # This regex finds CASE...END but needs to handle nesting
    text = re.sub(r'CASE\s+.*?\s+END', process_case, text, flags=re.IGNORECASE | re.DOTALL)

    return text


def main():
    parser = argparse.ArgumentParser(description='Oracle SQL Formatter')

    parser.add_argument('--version', action='version', version='2.0.0')

    args = parser.parse_args()
    config = load_config()

    try:
        sql_input = sys.stdin.read()

        if not sql_input.strip():
            print("Error: No SQL input", file=sys.stderr)
            sys.exit(1)

        formatted_sql = format_sql(sql_input, config)

        sys.stdout.write(formatted_sql)
        sys.stdout.write('\n')
        sys.stdout.flush()

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
