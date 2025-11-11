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


def load_rules():
    """Load formatting rules from format_rules.yaml"""
    rules_file = Path(__file__).parent / 'format_rules.yaml'

    # Default rules
    default_rules = {
        'indentation': {
            'column_indent': 5,
            'from_indent': 2,
            'where_indent': 1,
            'join_indent': 2,
            'on_indent': 4,
            'left_join_on_indent': 9,
            'and_or_indent': 3,
            'subquery_indent': 11,
        },
        'select': {
            'no_newline_after': True,
            'comma_before': True,
        },
        'case': {
            'first_when_inline': True,
            'when_newline': True,
            'else_newline': True,
            'end_newline': True,
            'when_indent': 12,
            'else_indent': 7,
            'end_indent': 7,
        },
        'keywords': {
            'case': 'upper',
        },
        'misc': {
            'preserve_comments': True,
        }
    }

    if rules_file.exists():
        try:
            with open(rules_file, 'r', encoding='utf-8') as f:
                rules = yaml.safe_load(f)
                # Merge with defaults
                for key in default_rules:
                    if key not in rules:
                        rules[key] = default_rules[key]
                    elif isinstance(default_rules[key], dict):
                        for subkey in default_rules[key]:
                            if subkey not in rules[key]:
                                rules[key][subkey] = default_rules[key][subkey]
                return rules
        except Exception as e:
            print(f"Warning: Could not load rules: {e}", file=sys.stderr)
            return default_rules
    return default_rules


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


def format_sql(sql_text, rules):
    """Format SQL with Oracle style"""

    # Step 1: Basic cleanup and keyword uppercase
    formatted = sqlparse.format(
        sql_text,
        keyword_case=rules['keywords']['case'],
        strip_comments=not rules['misc'].get('preserve_comments', True)
    )

    # Step 2: Remove all line breaks - work with single line
    formatted = ' '.join(formatted.split())

    # Step 3: Add line breaks at key points based on rules
    indent = rules['indentation']

    # Add newline before FROM
    from_spaces = ' ' * indent['from_indent']
    formatted = re.sub(r'\s+FROM\s+', f'\n{from_spaces}FROM ', formatted, flags=re.IGNORECASE)

    # Add newline before WHERE
    where_spaces = ' ' * indent['where_indent']
    formatted = re.sub(r'\s+WHERE\s+', f'\n{where_spaces}WHERE ', formatted, flags=re.IGNORECASE)

    # Add newline before JOIN
    join_spaces = ' ' * indent['join_indent']
    formatted = re.sub(
        r'\s+(LEFT\s+JOIN|RIGHT\s+JOIN|INNER\s+JOIN|FULL\s+JOIN|CROSS\s+JOIN|JOIN)\s+',
        rf'\n{join_spaces}\1 ',
        formatted,
        flags=re.IGNORECASE
    )

    # Add newline before ON with different indentation based on JOIN type
    # First, add newline before all ON keywords
    formatted = re.sub(r'\s+ON\s+', r'\nON_PLACEHOLDER ', formatted, flags=re.IGNORECASE)

    # Now process line by line to add correct indentation
    lines = formatted.split('\n')
    result_lines = []
    for i, line in enumerate(lines):
        if line.strip().startswith('ON_PLACEHOLDER'):
            # Check if previous line has a multi-word JOIN
            if i > 0 and re.search(r'(LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN', lines[i-1], re.IGNORECASE):
                left_on_spaces = ' ' * indent.get('left_join_on_indent', 9)
                line = line.replace('ON_PLACEHOLDER', f'{left_on_spaces}ON')
            else:
                on_spaces = ' ' * indent['on_indent']
                line = line.replace('ON_PLACEHOLDER', f'{on_spaces}ON')
        result_lines.append(line)
    formatted = '\n'.join(result_lines)

    # Add newline before ORDER BY
    formatted = re.sub(r'\s+ORDER\s+BY\s+', f'\n{where_spaces}ORDER BY ', formatted, flags=re.IGNORECASE)

    # Add newline before GROUP BY
    formatted = re.sub(r'\s+GROUP\s+BY\s+', f'\n{where_spaces}GROUP BY ', formatted, flags=re.IGNORECASE)

    # Add newline before AND/OR in WHERE and ON clauses
    and_or_spaces = ' ' * indent['and_or_indent']
    lines = formatted.split('\n')
    result_lines = []
    for line in lines:
        # Check if this is a WHERE or ON line
        if re.match(r'\s*(WHERE|ON)\s+', line, re.IGNORECASE):
            # Add line breaks before AND/OR
            line = re.sub(r'\s+(AND|OR)\s+', rf'\n{and_or_spaces}\1 ', line, flags=re.IGNORECASE)
        result_lines.append(line)
    formatted = '\n'.join(result_lines)

    # Step 4: Handle commas in SELECT list
    lines = formatted.split('\n')
    result = []
    column_spaces = ' ' * indent['column_indent']

    for line in lines:
        if line.strip().startswith('SELECT'):
            # Split on commas smartly
            select_part, rest = line.split('SELECT', 1)
            items = smart_split_on_comma(rest)

            # First item goes on SELECT line
            result.append('SELECT ' + items[0].strip())

            # Rest go on new lines with comma prefix
            for item in items[1:]:
                result.append(f'{column_spaces}, ' + item.strip())
        else:
            result.append(line)

    formatted = '\n'.join(result)

    # Step 5: Format CASE statements based on rules
    if rules['case']['when_newline'] or rules['case']['else_newline']:
        formatted = format_case_statements(formatted, rules)

    # Step 6: Format subqueries (basic support)
    formatted = format_subqueries(formatted, rules)

    return formatted.strip()


def format_case_statements(text, rules):
    """Format CASE statements with WHEN/ELSE on new lines based on rules"""

    case_rules = rules['case']
    when_indent = ' ' * case_rules['when_indent']
    else_indent = ' ' * case_rules['else_indent']
    end_indent = ' ' * case_rules['end_indent']
    first_when_inline = case_rules.get('first_when_inline', True)

    def process_case(match):
        case_content = match.group(0)

        if first_when_inline:
            # Keep CASE and first WHEN on same line, but break subsequent WHENs
            # Split into tokens to identify first vs subsequent WHENs
            tokens = re.split(r'\b(WHEN|ELSE|END)\b', case_content, flags=re.IGNORECASE)
            result = []
            when_count = 0

            for i, token in enumerate(tokens):
                if token.upper() == 'WHEN':
                    when_count += 1
                    if when_count == 1:
                        # First WHEN - keep on same line with CASE
                        result.append(' ' + token)
                    else:
                        # Subsequent WHENs - new line with indent
                        result.append(f'\n{when_indent}' + token)
                elif token.upper() == 'ELSE':
                    if case_rules['else_newline']:
                        result.append(f'\n{else_indent}' + token)
                    else:
                        result.append(' ' + token)
                elif token.upper() == 'END':
                    if case_rules['end_newline']:
                        result.append(f'\n{end_indent}' + token)
                    else:
                        result.append(' ' + token)
                else:
                    result.append(token)

            case_content = ''.join(result)
        else:
            # Old behavior - line break before every WHEN
            if case_rules['when_newline']:
                case_content = re.sub(
                    r'\s+WHEN\s+',
                    f'\n{when_indent}WHEN ',
                    case_content,
                    flags=re.IGNORECASE
                )

            if case_rules['else_newline']:
                case_content = re.sub(
                    r'\s+ELSE\s+',
                    f'\n{else_indent}ELSE ',
                    case_content,
                    flags=re.IGNORECASE
                )

            if case_rules['end_newline']:
                parts = re.split(r'(\bEND\b)', case_content, flags=re.IGNORECASE)
                if len(parts) >= 2:
                    result_parts = []
                    for i, part in enumerate(parts):
                        if part.upper() == 'END' and i == len(parts) - 2:
                            result_parts.append(f'\n{end_indent}' + part)
                        else:
                            result_parts.append(part)
                    case_content = ''.join(result_parts)

        return case_content

    # Process CASE statements
    text = re.sub(r'CASE\b.*?\bEND', process_case, text, flags=re.IGNORECASE | re.DOTALL)

    return text


def format_subqueries(text, rules):
    """Format subqueries with proper indentation"""

    subquery_indent = rules['indentation'].get('subquery_indent', 11)
    sub_spaces = ' ' * subquery_indent
    from_indent_adj = subquery_indent + rules['indentation']['from_indent']
    where_indent_adj = subquery_indent + rules['indentation']['where_indent']

    # Look for FROM ( pattern and format the subquery
    # Split FROM (SELECT into FROM ( and then SELECT on new line
    lines = text.split('\n')
    result_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this line has FROM (SELECT
        match = re.search(r'FROM\s*\(SELECT', line, re.IGNORECASE)
        if match:
            # Split into FROM ( and SELECT parts
            before_paren = line[:match.end()-6]  # Up to and including (
            select_part = line[match.end()-6:]  # SELECT onwards

            result_lines.append(before_paren)
            i += 1

            # Track parentheses
            paren_count = 1  # We already have opening (

            # Process the SELECT part
            if select_part.strip():
                result_lines.append(sub_spaces + select_part.strip())

            # Process subsequent lines until closing )
            while i < len(lines) and paren_count > 0:
                subline = lines[i]

                # Check if this line has the closing )
                if ')' in subline:
                    # Split on )
                    parts = subline.split(')')
                    before_close = parts[0]
                    after_close = ')'.join(parts[1:])

                    # Process the part before )
                    if before_close.strip():
                        stripped = before_close.lstrip()
                        if stripped.upper().startswith('FROM'):
                            result_lines.append(' ' * from_indent_adj + stripped)
                        elif stripped.upper().startswith('WHERE'):
                            result_lines.append(' ' * where_indent_adj + stripped)
                        else:
                            result_lines.append(sub_spaces + stripped)

                    # Add closing paren line
                    paren_count -= 1
                    if after_close.strip():
                        result_lines.append(' ' * 7 + ')' + after_close)
                    else:
                        result_lines.append(' ' * 7 + ')')
                else:
                    # Regular subquery line
                    stripped = subline.lstrip()
                    if stripped.upper().startswith('SELECT'):
                        result_lines.append(sub_spaces + stripped)
                    elif stripped.upper().startswith('FROM'):
                        result_lines.append(' ' * from_indent_adj + stripped)
                    elif stripped.upper().startswith('WHERE'):
                        result_lines.append(' ' * where_indent_adj + stripped)
                    else:
                        result_lines.append(sub_spaces + stripped)

                i += 1
        else:
            result_lines.append(line)
            i += 1

    return '\n'.join(result_lines)


def main():
    parser = argparse.ArgumentParser(
        description='Oracle SQL Formatter - Rules-based formatting',
        epilog='Edit format_rules.yaml to customize formatting rules'
    )

    parser.add_argument(
        '--show-rules',
        action='store_true',
        help='Show current formatting rules and exit'
    )

    parser.add_argument('--version', action='version', version='2.1.0')

    args = parser.parse_args()

    # Load rules
    rules = load_rules()

    # Show rules if requested
    if args.show_rules:
        print("Current Formatting Rules:")
        print("=" * 50)
        print(yaml.dump(rules, default_flow_style=False, allow_unicode=True))
        sys.exit(0)

    try:
        sql_input = sys.stdin.read()

        if not sql_input.strip():
            print("Error: No SQL input", file=sys.stderr)
            sys.exit(1)

        formatted_sql = format_sql(sql_input, rules)

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
