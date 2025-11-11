# Installation Guide

## Method 1: Direct Usage (Recommended for Testing)

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Make Script Executable

```bash
chmod +x sql_formatter.py
```

### Step 3: Test the Formatter

```bash
echo "select empno,ename,sal from emp where deptno=10 order by sal desc" | python sql_formatter.py
```

### Step 4: Configure DBeaver

1. Open DBeaver
2. Go to `Window` → `Preferences` (or `DBeaver` → `Preferences` on Mac)
3. Navigate to `Editors` → `SQL Editor` → `Formatting`
4. Select `External SQL formatter`
5. In the `Command line` field, enter:
   ```
   python /full/path/to/fstPj/sql_formatter.py
   ```
   Replace `/full/path/to/fstPj/` with the actual path to your project directory

6. Click `Test` to verify it works
7. Click `Apply` and `OK`

## Method 2: System-wide Installation

### Step 1: Install as Python Package

```bash
pip install -e .
```

This installs the `sql-formatter` command globally.

### Step 2: Configure DBeaver

1. Open DBeaver
2. Go to `Window` → `Preferences` → `Editors` → `SQL Editor` → `Formatting`
3. Select `External SQL formatter`
4. In the `Command line` field, enter:
   ```
   sql-formatter
   ```
5. Click `Test` to verify it works
6. Click `Apply` and `OK`

## Method 3: Standalone Executable (Advanced)

If you want to create a standalone executable without requiring Python:

### Using PyInstaller

```bash
pip install pyinstaller
pyinstaller --onefile sql_formatter.py
```

The executable will be in the `dist/` directory.

Configure DBeaver to use:
```
/path/to/dist/sql_formatter
```

## Usage in DBeaver

Once configured:

1. Open any SQL file in DBeaver
2. Press `Ctrl+Shift+F` (Windows/Linux) or `Cmd+Shift+F` (Mac)
3. Your SQL will be formatted!

## Customization

Edit `~/.sql_formatter.yaml` to customize formatting options:

```yaml
indent_width: 2
keyword_case: upper
identifier_case: lower
comma_before: false
line_between_queries: 2
reindent_aligned: true
wrap_after: 80
```

## Troubleshooting

### "Command not found" error

Make sure Python is in your PATH and the script path is correct.

### "Permission denied" error

Run `chmod +x sql_formatter.py` to make the script executable.

### Formatting doesn't look right

Try adjusting the options in `~/.sql_formatter.yaml` or use command-line flags:

```bash
python sql_formatter.py --indent-width 4 --keyword-case upper
```

### DBeaver shows an error

1. Test the formatter manually first:
   ```bash
   echo "select * from dual" | python sql_formatter.py
   ```
2. Check that the path in DBeaver is absolute (not relative)
3. Make sure Python and all dependencies are installed
