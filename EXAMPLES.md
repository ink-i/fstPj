# Usage Examples

## Basic Usage

### Format a simple query

```bash
echo "select * from emp" | python sql_formatter.py
```

**Output:**
```sql
SELECT *
  FROM emp
```

### Format from file

```bash
cat query.sql | python sql_formatter.py
```

### Save formatted output

```bash
cat query.sql | python sql_formatter.py > formatted.sql
```

## Command-Line Options

### Change indentation width

```bash
echo "select empno,ename from emp" | python sql_formatter.py --indent-width 4
```

**Output:**
```sql
SELECT empno,
       ename
    FROM emp
```

### Lowercase keywords

```bash
echo "SELECT * FROM EMP" | python sql_formatter.py --keyword-case lower
```

**Output:**
```sql
select *
  from EMP
```

### Uppercase identifiers

```bash
echo "select empno,ename from emp" | python sql_formatter.py --identifier-case upper
```

**Output:**
```sql
SELECT EMPNO,
       ENAME
  FROM EMP
```

### Comma-first style

```bash
echo "select empno,ename,sal from emp" | python sql_formatter.py --comma-before
```

**Output:**
```sql
SELECT empno
     , ename
     , sal
  FROM emp
```

## Complex Queries

### JOIN with WHERE clause

**Input:**
```sql
select e.empno,e.ename,d.dname from emp e join dept d on e.deptno=d.deptno where e.sal>2000
```

**Command:**
```bash
cat input.sql | python sql_formatter.py
```

**Output:**
```sql
SELECT e.empno,
       e.ename,
       d.dname
  FROM emp e
  JOIN dept d
    ON e.deptno = d.deptno
 WHERE e.sal > 2000
```

### Subquery

**Input:**
```sql
select * from emp where sal>(select avg(sal) from emp)
```

**Output:**
```sql
SELECT *
  FROM emp
 WHERE sal >
        (SELECT avg(sal)
          FROM emp
       )
```

### CASE expression

**Input:**
```sql
select empno,ename,case when sal<1500 then 'LOW' when sal<3000 then 'MED' else 'HIGH' end as grade from emp
```

**Output:**
```sql
SELECT empno,
       ename,
       CASE
         WHEN sal < 1500 THEN 'LOW'
         WHEN sal < 3000 THEN 'MED'
         ELSE 'HIGH'
       END AS grade
  FROM emp
```

### Window functions

**Input:**
```sql
select empno,ename,sal,rank() over (partition by deptno order by sal desc) as rank from emp
```

**Output:**
```sql
SELECT empno,
       ename,
       sal,
       rank() over (partition BY deptno
                    ORDER BY sal DESC) AS rank
  FROM emp
```

### INSERT statement

**Input:**
```sql
insert into dept(deptno,dname,loc)values(50,'IT','BOSTON')
```

**Output:**
```sql
INSERT INTO dept(deptno,
                 dname,
                 loc)
VALUES(50,
       'IT',
       'BOSTON')
```

### UPDATE statement

**Input:**
```sql
update emp set sal=sal*1.1,comm=500 where deptno=20
```

**Output:**
```sql
UPDATE emp
   SET sal = sal * 1.1,
       comm = 500
 WHERE deptno = 20
```

## DBeaver Integration

### Format SQL in editor

1. Write or paste your SQL in DBeaver
2. Press `Ctrl+Shift+F` (or `Cmd+Shift+F` on Mac)
3. SQL is automatically formatted!

### Before formatting:
```sql
select e.empno,e.ename,e.sal,d.dname from emp e inner join dept d on e.deptno=d.deptno where e.sal>2000 order by e.empno;
```

### After formatting (in DBeaver):
```sql
SELECT e.empno,
       e.ename,
       e.sal,
       d.dname
  FROM emp e
 INNER JOIN dept d
    ON e.deptno = d.deptno
 WHERE e.sal > 2000
 ORDER BY e.empno;
```

## Configuration File

Create `~/.sql_formatter.yaml`:

```yaml
indent_width: 4
keyword_case: upper
identifier_case: preserve
comma_before: false
line_between_queries: 2
reindent_aligned: true
wrap_after: 100
```

Now all formatting will use these settings by default!

## Tips

1. **Test before using in DBeaver**: Always test the formatter on sample queries first
2. **Backup your SQL**: DBeaver replaces your SQL in-place when formatting
3. **Use version control**: Keep your SQL files in Git
4. **Customize settings**: Adjust `.sql_formatter.yaml` to match your team's style
5. **Format on save**: Configure DBeaver to auto-format when saving (optional)
