# Oracle SQL Formatter - 예시 기반 설정 가이드

## 📁 파일 구조

```
fstPj/
├── oracle_formatter.py              # 메인 포맷터
├── format_rules.yaml                # 포맷팅 룰 설정 파일 ⭐
├── examples/                        # 예시 파일 디렉토리 ⭐
│   └── formatting_examples.yaml    # 모든 포맷팅 예시 (통합 파일)
└── README_EXAMPLES.md               # 이 파일
```

## 🎯 포맷팅 룰 수정 방법

### 1. format_rules.yaml 파일 수정

가장 간단한 방법입니다. `format_rules.yaml` 파일을 열어서 원하는 룰을 수정하세요.

**예시: 컬럼 들여쓰기 변경**
```yaml
indentation:
  column_indent: 5  # 5에서 7로 변경하면 쉼표 앞 공백이 7칸이 됩니다
```

**예시: CASE 문 들여쓰기 변경**
```yaml
case:
  when_indent: 10   # WHEN 키워드 앞 들여쓰기
  else_indent: 10   # ELSE 키워드 앞 들여쓰기
  end_indent: 7     # END 키워드 앞 들여쓰기
```

### 2. 예시 파일 추가/수정

`examples/formatting_examples.yaml` 파일을 열어서 예시를 추가하거나 수정하세요.

**새 예시 추가하기:**

```yaml
# examples/formatting_examples.yaml
examples:
  # ... 기존 예시들 ...

  # 새로운 예시 추가
  - name: "내가 원하는 포맷"
    description: "설명을 여기에 작성"
    input: |
      SELECT A.COL1, A.COL2 FROM TABLE_A A WHERE A.ID = 1

    expected_output: |
      SELECT A.COL1
           , A.COL2
        FROM TABLE_A A
       WHERE A.ID = 1

    rules:
      column_indent: 5
      from_indent: 2
```

## 🔧 주요 설정 항목

### indentation (들여쓰기)
- `column_indent`: SELECT 컬럼 쉼표 앞 공백 (기본: 5)
- `from_indent`: FROM 키워드 앞 공백 (기본: 2)
- `where_indent`: WHERE 키워드 앞 공백 (기본: 1)
- `join_indent`: JOIN 키워드 앞 공백 (기본: 2)
- `on_indent`: ON 키워드 앞 공백 (기본: 4)
- `and_or_indent`: AND/OR 키워드 앞 공백 (기본: 3)

### select (SELECT 절)
- `no_newline_after`: SELECT 후 줄바꿈 없이 컬럼 시작 (기본: true)
- `comma_before`: 쉼표를 컬럼 앞에 위치 (기본: true)

### case (CASE 문)
- `when_newline`: WHEN 앞에 줄바꿈 (기본: true)
- `else_newline`: ELSE 앞에 줄바꿈 (기본: true)
- `end_newline`: END 앞에 줄바꿈 (기본: true)
- `when_indent`: WHEN 들여쓰기 (기본: 10)
- `else_indent`: ELSE 들여쓰기 (기본: 10)
- `end_indent`: END 들여쓰기 (기본: 7)

### keywords (키워드)
- `case`: 키워드 대소문자 (upper/lower/preserve, 기본: upper)

## 🧪 테스트 방법

### 1. 현재 룰 확인
```bash
python oracle_formatter.py --show-rules
```

### 2. 예시 파일 확인
```bash
# 예시 파일 열어보기
cat examples/formatting_examples.yaml
```

### 3. 커스텀 SQL 테스트
```bash
echo "SELECT A, B FROM T WHERE X = 1" | python oracle_formatter.py
```

## 📝 예시 파일 작성 가이드

새로운 포맷팅 패턴을 추가하려면:

1. `examples/formatting_examples.yaml` 파일 열기
2. `examples:` 리스트에 새 항목 추가:

```yaml
examples:
  # 기존 예시들...

  - name: "포맷팅 패턴 이름"
    description: "이 패턴에 대한 설명"
    input: |
      포맷 전 SQL

    expected_output: |
      포맷 후 SQL

    rules:
      적용할_룰1: 값
      적용할_룰2: 값
```

3. 필요한 경우 `format_rules.yaml`에 새 룰 추가

## 💡 팁

1. **들여쓰기 변경**: `format_rules.yaml`의 `indentation` 섹션만 수정
2. **새 패턴 추가**: `examples/` 디렉토리에 예시 추가
3. **빠른 테스트**: `--show-rules`로 현재 설정 확인
4. **롤백**: Git으로 이전 버전 복원

## 🚀 DBeaver 설정

### 설정 방법

**1. DBeaver Preferences 열기**
- Windows/Linux: `Window` > `Preferences`
- Mac: `DBeaver` > `Preferences`

**2. SQL Editor > Formatting 찾기**
- 왼쪽 트리에서: `Editors` > `SQL Editor` > `Formatting`

**3. External Formatter 선택**
- `Formatter:` 드롭다운에서 `External`를 선택

**4. Command 설정 (다음 중 하나 선택)**

#### 방법 1: 절대 경로 사용 (권장)
```
/usr/local/bin/python /home/user/fstPj/oracle_formatter.py
```

#### 방법 2: 상대 경로 사용
```
python /home/user/fstPj/oracle_formatter.py
```

#### 방법 3: Command와 Arguments 분리
- Command: `/usr/local/bin/python`
- Arguments: `/home/user/fstPj/oracle_formatter.py`

**5. Apply 클릭 후 OK**

### 사용 방법

1. SQL 에디터에서 SQL 작성
2. SQL 선택 (전체 선택: Ctrl+A / Cmd+A)
3. 포맷 실행:
   - Windows/Linux: `Ctrl + Shift + F`
   - Mac: `Cmd + Shift + F`

### ⚠️ 문제 해결

#### "Python" 또는 빈 결과만 나오는 경우

**원인**: DBeaver가 formatter를 제대로 실행하지 못함

**해결 방법**:

1. **Python 경로 확인**
   ```bash
   which python
   which python3
   ```
   결과를 Command에 정확히 입력

2. **Formatter 파일 권한 확인**
   ```bash
   chmod +x /home/user/fstPj/oracle_formatter.py
   ```

3. **터미널에서 먼저 테스트**
   ```bash
   echo "SELECT A, B FROM T" | python /home/user/fstPj/oracle_formatter.py
   ```
   이게 작동하면 DBeaver 설정 문제입니다.

4. **DBeaver 로그 확인**
   - `Help` > `Error Log` 열어서 에러 메시지 확인

5. **절대 경로 사용**
   상대 경로 대신 전체 경로 사용:
   ```
   /usr/local/bin/python /home/user/fstPj/oracle_formatter.py
   ```

#### 포맷은 되지만 스타일이 이상한 경우

`format_rules.yaml` 파일을 수정하세요. 변경 후 DBeaver에서 다시 포맷하면 바로 적용됩니다!

### ✅ 정상 작동 확인

포맷 전:
```sql
SELECT A.SITE_CD, A.SITE_NM FROM PMA_CON_INFO A WHERE A.YM = '202510'
```

포맷 후:
```sql
SELECT A.SITE_CD
     , A.SITE_NM
  FROM PMA_CON_INFO A
 WHERE A.YM = '202510'
```
