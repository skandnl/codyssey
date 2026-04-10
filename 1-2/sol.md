# 퀴즈 게임 과제 자가 검토 답변서 (sol.md)

---

## ✅ 1. 기능 동작 검증

### 1-1. 프로그램 실행 시 메뉴가 정상적으로 표시되고, 퀴즈 풀기/추가/목록/점수 확인 기능이 모두 동작하는가?

**✔ 충족**

- **메뉴 출력**: `game.py` → `QuizGame.show_menu()` (line 60–69)
- **기능 분기**:  `QuizGame.run()` (line 184–213)의 `if/elif` 블록으로 1~5번 선택에 따라 각 메서드 호출
  - `1` → `play_quiz()`
  - `2` → `add_quiz()`
  - `3` → `list_quizzes()`
  - `4` → `show_score()`
  - `5` → 저장 후 종료
- **잘못된 입력 처리**: 범위 외 입력 시 경고 메시지 출력 (`game.py` line 207)

---

### 1-2. 퀴즈 풀기 시 정답/오답 판정이 정확하고, 최소 입력 오류 케이스에 대한 처리가 되어 있는가?

**✔ 충족**

- **정답 판정**: `quiz.py` → `Quiz.check_answer(user_answer)` (line 24–28): `user_answer == self.answer` 비교
- **오답 표시**: `game.py` line 102: 정답 번호를 알려줌 (`정답은 {quiz.answer}번이에요.`)
- **입력 오류 처리** (`game.py` line 89–95):
  - `"1"~"4"` 범위 밖 입력 → 경고 후 재입력 (`while True` 루프 사용)
  - `.strip()` 사용으로 앞뒤 공백 제거 (line 90)
  - 숫자 변환 실패: `user_input in ["1","2","3","4"]` 문자열 비교로 사전 차단 (숫자 외 문자, 빈 입력 모두 걸러짐)
  - 빈 입력, 문자 입력 → 동일 경고 메시지 후 재입력

---

### 1-3. 프로그램 종료 후 재실행해도 추가한 퀴즈와 최고 점수가 유지되는가?

**✔ 충족**

- **저장**: `QuizGame.save_state()` (`game.py` line 49–55)
  - `state.json`에 `quizzes` 목록과 `best_score`(정수)를 UTF-8로 JSON 직렬화하여 저장
  - 퀴즈 추가 후(line 156), 게임 종료 후(line 119, 199, 212) 자동 호출
- **불러오기**: `QuizGame.load_state()` (`game.py` line 27–47)
  - 실행 시 `state.json`에서 퀴즈와 최고 점수를 불러옴
  - `Quiz.from_dict()` (`quiz.py` line 38–45)로 딕셔너리 → `Quiz` 객체 복원

---

### 1-4. 기본 퀴즈가 5개 이상 포함되어 있는가?

**✔ 충족**

- `quiz.py` → `DEFAULT_QUIZZES` (line 50–76): **5개**의 Python 상식 퀴즈 정의
  1. Python 창시자
  2. 리스트 마지막 요소 인덱스
  3. 딕셔너리 키 조회 방법
  4. 파일 안전 열기 키워드
  5. 클래스 생성자 이름
- `game.py` line 30: 파일이 없을 때 `list(DEFAULT_QUIZZES)`를 초기값으로 사용

---

### 1-5. GitHub 저장소에 코드가 업로드되어 있고, 10개 이상의 의미 있는 커밋이 존재하는가?

**✔ 충족**

`git log --oneline --graph` 결과 (1-2 관련 커밋):

```
* 81e4ad4 Chore: .DS_Store 파일 트래킹 해제
* 2693679 Refactor: 초보자가 읽기 쉽도록 퀴즈 게임 코드 전면 단순화
* 166b734 Docs: README에 캡처 이미지 포함
* 24f18c5 Docs: 실행 화면 스크린샷 4장 추가
* 00d0afb Docs: README 스크린샷 요구사항 추가
* e0d780c Docs: Clone 및 Pull 실습 내용 추가
*   c018be3 Merge: feature/update-readme 브랜치 병합
|\
| * 4b477b3 Docs: README 협업 규칙 내용 추가
| * 8c49d75 Docs: 스크린샷 저장용 폴더 생성
|/
* 6ba14e1 Refactor: 1-2 퀴즈 게임 전체 구현 반영
* 8719afb Feat: main.py 진입점 추가
* 377410c Feat: Quiz 클래스 구현
* 9ae1777 Init: 1-2 프로젝트 초기 설정
```

총 **13개** 커밋 (1-2 관련), 기능/문서/리팩터 단위로 분리

---

### 1-6. 브랜치 생성 및 병합 기록이 git log --oneline --graph에서 확인되는가?

**✔ 충족**

- `feature/update-readme` 브랜치 생성 후 2개 커밋(문서 추가), `main`에 병합
- `git log` 그래프에서 `|\` → `|/` 형태로 시각적으로 확인 가능

---

### 1-7. clone과 pull 실습 수행 흔적을 README 또는 스크린샷으로 확인할 수 있는가?

**✔ 충족**
gr
- `README.md` line 114: **"Clone & Pull 테스트 완료 (과제 1-2 요구사항 충족)"** 명시
- 커밋 `e0d780c`: "Clone 및 Pull 실습 내용 추가"로 실습 수행 기록

---

## ✅ 2. 코드 구조 및 설계

### 2-1. Quiz와 QuizGame 클래스의 책임을 어떻게 나눴는가?

| 클래스 | 파일 | 책임 |
|--------|------|------|
| `Quiz` | `quiz.py` | **단일 퀴즈 데이터**를 표현. 문제 출력(`display`), 정답 확인(`check_answer`), JSON 직렬화/역직렬화(`to_dict`, `from_dict`) |
| `QuizGame` | `game.py` | **게임 전체 흐름** 관리. 메뉴 출력, 퀴즈 진행, 퀴즈 추가, 목록 표시, 점수 확인, 파일 저장/불러오기 |
| 진입점 | `main.py` | `QuizGame` 인스턴스 생성 후 `game.run()` 호출만 담당 |

→ **단일 책임 원칙(SRP)**: 데이터(Quiz)와 로직(QuizGame)을 분리

---

### 2-2. 입력 처리/게임 진행/데이터 저장 로직을 어떤 기준으로 분리했는가?

| 역할 | 위치 |
|------|------|
| **입력 검증** | 각 메서드 내부의 `while True` + `if/else` 블록 (예: `game.py` line 89–95, 129–143) |
| **게임 진행** | `play_quiz()` (`game.py` line 71–123), `add_quiz()` (line 125–157) |
| **파일 저장/불러오기** | `load_state()` (line 27–47), `save_state()` (line 49–55) |

- 입력 검증은 **사용자 접점 메서드 내**에 포함 (검증과 흐름을 직결)
- 파일 I/O는 **명시적으로 분리된 두 메서드**(`load_state` / `save_state`)에서만 수행

---

### 2-3. state.json 읽기/쓰기 흐름이 어디서, 어떤 순서로 발생하는가?

**읽기 흐름**:
```
main.py: QuizGame()
  → game.py: __init__() (line 16)
    → load_state() (line 27)
      → os.path.exists() 확인 → json.load() → Quiz.from_dict() → self.quizzes / self.best_score 복원
```

**쓰기 흐름** (총 3개 경로):
```
퀴즈 추가 후  → add_quiz()    (game.py line 152) → save_state()
게임 완료 후  → play_quiz()   (game.py line 119) → save_state()
정상 종료 시  → run() 5번     (game.py line 199) → save_state()
비정상 종료   → KeyboardInterrupt (game.py line 212) → save_state()
```

---

### 2-4. Ctrl+C 또는 EOF 상황에서 안전 종료를 위해 어떤 처리를 했는가?

**✔ 구현 완료**

`game.py` line 210–213:
```python
except (KeyboardInterrupt, EOFError):
    print("\n\n⚠️  비정상적인 종료 신호입니다. 데이터를 저장하고 나갑니다.")
    self.save_state()
    break
```
- `KeyboardInterrupt`: Ctrl+C 입력 시 발생
- `EOFError`: 입력 스트림이 닫혔을 때 발생 (파이프, 리다이렉션 등)
- 두 경우 모두 안내 메시지 출력 → `save_state()` 호출 → 루프 탈출로 안전 종료

---

### 2-5. 커밋을 어떤 단위로 나누었고, 커밋 메시지 규칙은?

- **커밋 단위**: 기능 단위 (Quiz 클래스, 진입점, 전체 게임 구현, README, 스크린샷 등)
- **메시지 규칙**: `타입: 설명` 형식
  - `Init:` 초기 설정
  - `Feat:` 기능 추가
  - `Docs:` 문서/README 변경
  - `Refactor:` 구조 정리
  - `Chore:` 관리성 변경 (.gitignore 등)
  - `Merge:` 브랜치 병합

---

## ✅ 3. 핵심 기술 원리 적용

### 3-1. 클래스를 사용한 이유는? 함수만으로 구현할 때와의 차이는?

- **이유**: 퀴즈(데이터+행동)와 게임(상태+흐름)을 **캡슐화**하여 관련 데이터와 기능을 한 곳에 묶음
- **함수만 쓸 경우**: `question`, `choices`, `answer`를 별도 리스트나 딕셔너리로 관리해야 하고, `display()`, `check_answer()`도 독립 함수로 분산됨 → 퀴즈가 많아질수록 관리 어려움
- **클래스 사용 시**: `Quiz` 인스턴스 하나가 문제·선택지·정답·출력·검사를 모두 담당 → 코드가 자기 완결적이고 확장 용이

---

### 3-2. JSON 파일로 데이터를 저장하는 이유와 JSON 형식의 특징은?

- **이유**: 프로그램 종료 후에도 데이터를 유지(영속성)하기 위해 파일 저장이 필요
- **JSON을 선택한 이유**:
  - 사람이 읽고 편집 가능한 텍스트 형식
  - Python 표준 라이브러리 `json` 모듈로 별도 설치 없이 사용 가능
  - 딕셔너리·리스트 구조를 그대로 직렬화/역직렬화 가능
- **특징**: `key: value` 쌍, 중첩 가능, UTF-8 인코딩 권장 (`ensure_ascii=False` 사용, `game.py` line 55)

---

### 3-3. 파일 입출력에서 try/except가 필요한 이유는?

`game.py` line 33–47 참조

발생 가능한 실패 케이스:
| 상황 | 예외 |
|------|------|
| 파일 권한 없음 | `PermissionError` |
| JSON 형식이 깨짐 | `json.JSONDecodeError` |
| 파일 읽기 도중 중단 | `IOError` |
| 예상 키 없음 (`.get()` 미사용 시) | `KeyError` |

→ `except Exception`으로 모든 예외를 잡아 기본 데이터로 복구 (`game.py` line 44–47)

---

### 3-4. 브랜치를 분리해 작업한 이유와 병합(merge)의 의미는?

- **이유**: `main` 브랜치를 항상 안정적인 상태로 유지하고, 새 기능(README 업데이트)을 독립적으로 작업하기 위해 `feature/update-readme` 브랜치 생성
- **병합(merge)의 의미**: 브랜치에서 완성된 작업을 `main`에 합쳐 하나의 히스토리로 통합. 병합 커밋(`c018be3`)이 두 브랜치의 합류 지점을 기록

---

### 3-5. state.json의 데이터 구조를 현재 형태로 설계한 이유는?

현재 구조:
```json
{
  "quizzes": [ { "question": "...", "choices": [...], "answer": 1 } ],
  "best_score": 5
}
```

- **`quizzes`를 배열로**: 여러 개의 퀴즈를 순서대로 관리하기 쉽고, `for` 반복문으로 순회 가능
- **각 퀴즈를 객체로**: `question/choices/answer` 3개 필드가 논리적으로 한 묶음 → `Quiz.to_dict()` / `from_dict()`와 1:1 대응
- **`best_score`를 정수로**: 맞춘 문제 수만 저장하면 충분 (퍼센트 계산은 `len(self.quizzes)`를 사용)하며, 과제 스키마 예시와 일치 (`"best_score": 3`)

---

## 🔍 심층 인터뷰

### Q1. 퀴즈 데이터가 1000개 이상으로 늘어난다면?

**현재 방식의 한계**:
- 전체 `state.json`을 매번 통째로 읽고(`json.load`) 통째로 씀(`json.dump`) → 파일이 커질수록 속도 저하
- 1000개의 퀴즈가 메모리에 모두 올라옴 → 메모리 사용 증가
- JSON은 부분 읽기(스트리밍)나 인덱스 검색이 불가

**가능한 대안**:
- SQLite 등 데이터베이스 사용 (`import sqlite3`, 표준 라이브러리 포함)
- JSONL(한 줄씩 JSON) 형식으로 점진적 읽기

---

### Q2. state.json이 손상되어 JSON 파싱에 실패한다면?

**현재 대응** (`game.py` line 44–47):
```python
except Exception:
    print("⚠️  저장 파일이 손상되어 기본 문제로 다시 시작합니다.")
    self.quizzes = list(DEFAULT_QUIZZES)
    self.best_score = 0
```
→ 손상된 파일을 그대로 두고 기본값으로 초기화 (기존 데이터 유실 가능)

**개선 가능한 방법**:
- 저장 전 `state.json.bak` 백업 파일 생성
- 손상 시 백업 파일에서 복구 시도
- 손상된 파일을 `state_corrupted_YYYYMMDD.json`으로 이름 변경 후 보존

---

### Q3. 점수 계산 방식이나 퀴즈 구조가 바뀐다면, 어떤 파일/클래스/메서드를 수정해야 하는가?

| 변경 상황 | 수정 위치 |
|-----------|-----------|
| 정답 채점 방식 변경 (예: 부분 점수) | `quiz.py` → `Quiz.check_answer()` |
| 최고 점수 계산 방식 변경 | `game.py` → `QuizGame.play_quiz()` (best_score 갱신 로직), `show_score()` |
| 선택지 개수 변경 (4개 → 5개) | `quiz.py` → `DEFAULT_QUIZZES` + `Quiz.__init__()` / `game.py` → `add_quiz()` 입력 루프 + `play_quiz()` 입력 검증 범위 |
| JSON 필드명 변경 | `quiz.py` → `to_dict()`, `from_dict()` / `game.py` → `load_state()`, `save_state()` |

→ 구조가 역할별로 분리되어 있어 **수정 범위가 최소화**됨
