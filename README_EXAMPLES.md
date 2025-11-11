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

DBeaver에서 사용할 때도 동일한 `format_rules.yaml`을 참조합니다:

```
Command: python /home/user/fstPj/oracle_formatter.py
```

룰을 변경하고 DBeaver에서 다시 포맷하면 바로 적용됩니다!
