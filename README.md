# Oracle SQL Formatter for DBeaver

A command-line SQL formatter specifically designed for Oracle SQL, integrated with DBeaver.

## Features

- Oracle SQL syntax support
- Customizable formatting options
- Stdin/stdout interface for DBeaver integration
- Keyword capitalization
- Proper indentation
- Comment preservation

## Installation

### Prerequisites

- Python 3.7 or higher
- pip

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Make the script executable

```bash
chmod +x sql_formatter.py
```

## Usage

### Command Line

```bash
# Format SQL from stdin
echo "select * from emp where deptno=10" | python sql_formatter.py

# Format SQL from file
cat query.sql | python sql_formatter.py

# With custom options
echo "select * from emp" | python sql_formatter.py --indent-width 4 --keyword-case upper
```

### DBeaver Integration

1. Open DBeaver
2. Go to `Window` → `Preferences` → `Editors` → `SQL Editor` → `Formatting`
3. Click `External Formatter`
4. Configure:
   - **Command**: `/path/to/python /path/to/sql_formatter.py`
   - Or if installed globally: `sql-formatter`
5. Click `Apply` and `OK`

Now you can format SQL in DBeaver by pressing `Ctrl+Shift+F` (or `Cmd+Shift+F` on Mac)

## Configuration

You can customize formatting by:

1. Command-line arguments (see `--help`)
2. Configuration file `~/.sql_formatter.yaml`

### Configuration Options

```yaml
indent_width: 2
keyword_case: upper  # upper, lower, capitalize
identifier_case: lower  # upper, lower, preserve
comma_before: false
line_between_queries: 2
```

## Examples

### Before

```sql
select emp.empno,emp.ename,dept.dname from emp inner join dept on emp.deptno=dept.deptno where emp.sal>2000 order by emp.empno;
```

### After

```sql
SELECT
  emp.empno,
  emp.ename,
  dept.dname
FROM
  emp
  INNER JOIN dept ON emp.deptno = dept.deptno
WHERE
  emp.sal > 2000
ORDER BY
  emp.empno;
```

## License

MIT
