# Mini NPU Simulator — 평가문항 체크 & 답변 (sol.md)

> 코드 기준: `main.py` (447줄), `data.json`, `README.md`

---

## ✅ 항목 1: 기능 동작 검증 — 체크리스트

| # | 평가 항목 | 충족 여부 | 근거 (코드 위치) |
|---|-----------|:---------:|-----------------|
| 1 | 모드 1에서 3×3 필터 2개·패턴 입력 후 MAC 점수/판정(A/B/판정 불가)/시간(ms) 출력 | ✅ | `mode1_user_input()` L202–248 |
| 2 | 모드 1에서 허용오차 내 동점 → "판정 불가" 출력 | ✅ | `judge()` L92–103, `mode1_user_input()` L241–243 |
| 3 | 모드 1 입력 오류(행/열 불일치, 숫자 파싱 실패) 시 안내 후 재입력 유도 | ✅ | `input_matrix()` L109–141 |
| 4 | 모드 2에서 data.json의 filters/patterns 로드, 키에서 N 추출해 올바른 필터 선택 | ✅ | `mode2_json_analysis()` L308–317, `load_filters()` L253–271 |
| 5 | expected('+','x')와 filter 키('cross','x')가 표준 라벨(Cross/X)로 정규화되어 비교 | ✅ | `normalize_label()` L57–69 |
| 6 | 모드 2에서 동점 → "UNDECIDED" 출력 + FAIL 집계 | ✅ | `judge()` L98, `mode2_json_analysis()` L372–374 |
| 7 | 성능 분석 표에 크기·평균 시간(ms)·연산 횟수(N²) 출력 (크기별 10회 평균) | ✅ | `performance_analysis()` L181–196, `REPEAT_COUNT=10` L15 |
| 8 | 콘솔에서 총 테스트/통과/실패 및 실패 케이스 요약 출력 | ✅ | `mode2_json_analysis()` L398–412 |
| 9 | README에 "결과 리포트 (실패 원인 + 복잡도)" 섹션 존재 (최소 10줄) | ✅ | README.md L142–194 (약 52줄) |

---

## ✅ 항목 2: 코드 구조 및 설계 — 질문 & 답변

### Q1. MAC 연산 로직의 전체 흐름(입력 → 위치별 곱셈 → 누적 합산 → 점수 반환)을 코드 구조 기준으로 설명하라.

**A.**

```
[입력]
  mode1_user_input() / mode2_json_analysis()
       ↓
  input_matrix() 또는 Pattern.from_2d_list()
  → Pattern 객체 (N×N 2차원 배열) 생성
       ↓
[MAC 연산 — mac_compute(pattern, filter_p)]
  score = 0.0
  for i in range(N):           ← 행 순회
      for j in range(N):       ← 열 순회
          score += pattern[i][j] * filter[i][j]   ← 위치별 곱셈 & 누적 합산
  return score                 ← 유사도 점수 반환
       ↓
[판정 — judge(score_cross, score_x)]
  |score_cross - score_x| < 1e-9 → "UNDECIDED"
  score_cross > score_x          → "Cross"
  else                           → "X"
       ↓
[출력]
  점수, 판정, 시간(ms) 콘솔 출력
```

핵심 구조는 **Pattern** 클래스가 데이터 보관을 담당하고, **mac_compute** 함수가 순수하게 연산만 수행하며, **judge** 함수가 결과만 해석하는 **단일 책임 분리** 방식이다.

---

### Q2. patterns 키에서 크기 N을 추출하고 filters의 size_N과 매칭하는 로직을 어떻게 설계했는지 설명하라.

**A.**

```python
# pat_key 예: "size_5_1", "size_13_2"
parts = pat_key.split("_")   # → ['size', '5', '1']
size_key = f"size_{parts[1]}"  # → 'size_5'

# filters 딕셔너리에서 해당 키 조회
if size_key not in filters:
    # FAIL 처리
cross_filter = filters[size_key]["Cross"]
x_filter     = filters[size_key]["X"]
```

설계 포인트:
1. 키 구조를 `size_{N}_{idx}` 형식으로 약속하고, `split("_")[1]`로 N을 추출한다.
2. 추출한 N으로 `size_N` 문자열을 조합해 `filters` 딕셔너리를 직접 조회한다.
3. `filters`는 `load_filters()` 단계에서 이미 라벨 정규화(`Cross`/`X`)까지 완료된 상태이므로, 매칭 시 추가 변환이 불필요하다.
4. 키 파싱 실패 또는 필터 누락 시 명확한 오류 메시지와 함께 해당 케이스만 FAIL 처리하고 프로그램은 계속 실행한다.

---

### Q3. 라벨 정규화(normalize_label)를 별도 함수/모듈로 분리한 이유와 장점을 설명하라.

**A.**

```python
def normalize_label(label: str) -> str:
    normalized = label.strip().lower()
    if normalized in ("+", "cross"):  return "Cross"
    elif normalized in ("x",):        return "X"
    return label
```

**분리한 이유:**
- `data.json`의 `expected` 필드(`'+'`, `'x'`)와 `filters` 키(`'cross'`, `'x'`)가 서로 다른 표기를 사용한다.
- 이 변환 로직이 두 곳 이상에서 필요하므로(필터 로드 시 + expected 비교 시), 중복을 제거하기 위해 함수로 분리했다.

**장점:**
1. **단일 진실 원천(SSOT)**: 라벨 매핑 규칙이 한 곳에만 존재하므로, 새 라벨 추가 시 이 함수만 수정하면 된다.
2. **테스트 용이성**: 순수 함수(입력→출력만 존재, 부작용 없음)로 검증이 쉽다.
3. **가독성**: 호출부에서 `normalize_label(raw)` 한 줄로 의도를 명확히 표현한다.
4. **확장성**: 새 라벨(`'o'`, `'circle'`)이 추가되어도 이 함수에 한 조건만 추가하면 된다.

---

### Q4. 시간 측정 시 I/O를 배제하고 "연산 구간"을 측정하기 위해 어떤 경계를 잡았는지 설명하라.

**A.**

```python
def measure_mac_time(pattern, filter_p, repeat=REPEAT_COUNT) -> float:
    total = 0.0
    for _ in range(repeat):
        start = time.perf_counter()    # ← 연산 직전
        mac_compute(pattern, filter_p) # ← 순수 MAC 연산만
        end = time.perf_counter()      # ← 연산 직후
        total += (end - start) * 1000
    return total / repeat
```

**경계 설정 전략:**
- `time.perf_counter()`를 `mac_compute()` 호출 **코드 바로 앞뒤**에만 배치하여, 입력 파싱·출력 포매팅·파일 I/O가 측정 범위에 포함되지 않도록 한다.
- `time.perf_counter()`는 Python에서 사용 가능한 가장 높은 해상도의 단조 증가 타이머로, 운영체제 시간 조정의 영향을 받지 않는다.
- 10회 반복 후 평균을 내어 OS 스케줄러 등에 의한 **일회성 노이즈**를 완화한다.
- 성능 분석(`performance_analysis`) 시에는 `generate_cross_pattern(n)`으로 패턴을 미리 생성해두고 측정에 집입하므로, 패턴 생성 시간도 측정에서 배제된다.

---

## ✅ 항목 3: 핵심 기술 원리 적용 — 질문 & 답변

### Q5. MAC 점수가 높을수록 "더 유사하다"고 판단할 수 있는 이유를 설명하라.

**A.**

MAC(Multiply-Accumulate) 연산의 수식은 다음과 같다:

```
score = Σ (pattern[i][j] × filter[i][j])   (i, j = 0 ~ N-1)
```

필터 값은 패턴의 **"어느 위치에 1이 있어야 하는가"**를 표현한다. 예를 들어 Cross 필터는 십자가 위치에 1, 나머지는 0이다.

- 패턴도 같은 위치에 1이 있으면: `1 × 1 = 1` → 점수 누적
- 패턴이 다른 위치에만 1이 있으면: `0 × 1 = 0` → 점수 없음
- 노이즈(불필요한 1)가 필터의 0 위치와 곱해지면: `1 × 0 = 0` → 점수 없음

따라서 **패턴과 필터가 겹치는 위치가 많을수록** 곱의 합이 커진다.
이는 내적(Dot Product)과 동일한 원리로, 두 벡터가 같은 방향일수록 내적 값이 커지는 것과 같다.
결론적으로 **MAC 점수가 높다 = 필터와 일치하는 위치가 많다 = 더 유사하다**.

---

### Q6. 패턴 크기가 N일 때 연산 횟수가 N²으로 증가하며, 측정 결과가 O(N²) 경향을 보이는 이유를 설명하라.

**A.**

`mac_compute()` 함수는 두 개의 중첩 `for` 루프로 구성된다:

```python
for i in range(N):       # N번
    for j in range(N):   # N번
        score += ...     # 1회 곱셈 + 1회 덧셈
```

총 연산 횟수 = N × N = **N²**

| 크기 | N² (연산 횟수) | 이론적 배율 (기준: 3×3) |
|------|--------------|----------------------|
| 3×3  | 9            | 1×                   |
| 5×5  | 25           | 2.8×                 |
| 13×13| 169          | 18.8×                |
| 25×25| 625          | 69.4×                |

실측 시간도 이 비율에 근사하게 증가하여 O(N²) 경향을 보인다.
(실측 배율이 이론보다 약간 낮은 이유: CPU L1/L2 캐시 히트율, 반복문 고정 오버헤드, OS 스케줄러 영향 등)

N이 커질수록 반복문 오버헤드의 비중이 줄고 순수 연산 비중이 늘기 때문에, 실측 값이 이론적 N² 곡선에 점점 더 가깝게 수렴한다.

---

### Q7. 부동소수점 오차가 왜 발생하며, 비교 정책(epsilon)이 왜 필요한지 설명하라.

**A.**

**부동소수점 오차 발생 원인:**

컴퓨터는 실수를 IEEE 754 배정도(64비트) 이진수로 표현한다.
대부분의 십진수 소수(0.1, 0.3 등)는 이진수로 정확히 표현되지 않아 반올림 오차가 생긴다.

```python
>>> 0.1 + 0.2
0.30000000000000004   # 수학적으로는 0.3이지만 이진 표현 한계로 오차 발생
```

MAC 연산처럼 수백 번의 덧셈을 누적하면 이 오차가 쌓인다.
예를 들어 수학적으로 동일한 두 점수가 `1.0000000000000002`와 `0.9999999999999998`처럼 표현될 수 있다.

**epsilon 정책이 필요한 이유:**

```python
EPSILON = 1e-9
if abs(score_a - score_b) < EPSILON:
    return "UNDECIDED"
```

수학적으로 동점인 케이스를 `score_a == score_b`로 비교하면 부동소수점 오차로 인해 동점이 검출되지 않을 수 있다.
`|score_a - score_b| < 1e-9` 조건은 "물리적으로 의미 없는 작은 차이는 동점으로 보겠다"는 안전 장치다.

현재 데이터는 정수 배열이므로 MAC 결과도 정수값이어서 오차가 거의 없지만, 실수 가중치를 사용하는 실제 AI 모델에서는 이 정책이 필수적이다.

---

### Q8. 동점 처리 규칙을 "mode 1 vs mode 2"로 다르게 둔 이유를 요구사항 관점에서 설명하라.

**A.**

| 모드 | 동점 출력 | PASS/FAIL 처리 |
|------|----------|---------------|
| 모드 1 (사용자 입력) | `"판정 불가"` (한국어) | 없음 (출력만) |
| 모드 2 (data.json) | `"UNDECIDED"` (영어) | FAIL로 집계 |

**이유:**

- **모드 1**은 사람이 직접 필터와 패턴을 입력하는 **인터랙티브 탐색** 모드다.
  동점이 발생했을 때 단순히 "판별이 불가능하다"는 정보를 사용자에게 알려주는 것이 목적이므로, PASS/FAIL 개념이 없다.
  한국어 출력("판정 불가")은 사용자 친화적 UX를 위한 선택이다.

- **모드 2**는 `data.json`에 정의된 **expected 정답이 존재하는 자동 검증** 모드다.
  정답이 있는 상황에서 UNDECIDED가 발생하면 올바른 판정을 내리지 못한 것이므로, 요구사항대로 **FAIL**로 집계해야 한다.
  영어 출력("UNDECIDED")은 로그/리포트 목적에 맞는 표준적인 표기다.

요약: **탐색 목적(모드 1)** vs **정확도 검증 목적(모드 2)**라는 요구사항의 차이가 동점 처리 규칙의 차이를 만든다.

---

## ✅ 항목 4: 심층 인터뷰 — 질문 & 답변

### Q9. data.json에 새로운 라벨(예: 'o')이 추가된다면, 정규화/판정/출력/테스트를 어떤 순서로 확장할지 설명하라.

**A.**

확장 순서:

#### 1단계: 정규화 (normalize_label) 확장
```python
def normalize_label(label: str) -> str:
    normalized = label.strip().lower()
    if normalized in ("+", "cross"):  return "Cross"
    elif normalized in ("x",):        return "X"
    elif normalized in ("o", "circle"): return "Circle"   # ← 추가
    return label
```
모든 入출력 라벨 변환의 진입점이므로 가장 먼저 수정한다.

#### 2단계: data.json 확장
```json
"filters": {
  "size_5": {
    "cross": [...],
    "x": [...],
    "o": [...]         ← 원형(Circle) 필터 추가
  }
},
"patterns": {
  "size_5_4": { "input": [...], "expected": "o" }   ← 추가
}
```

#### 3단계: 판정 로직 (judge) 확장
현재 `judge()` 함수는 두 점수(Cross vs X)만 비교한다.
라벨이 3개 이상이면 **모든 필터에 대해 MAC 점수를 계산 후 최고 점수 라벨**을 반환하는 멀티 클래스 판정으로 교체해야 한다:
```python
def judge_multi(pattern, filters_dict):
    scores = {label: mac_compute(pattern, f) for label, f in filters_dict.items()}
    max_score = max(scores.values())
    candidates = [l for l, s in scores.items() if abs(s - max_score) < EPSILON]
    return "UNDECIDED" if len(candidates) > 1 else candidates[0]
```

#### 4단계: 출력 확장
점수 출력 루프를 동적으로 변경:
```python
for label, score in scores.items():
    print(f"  {label} 점수: {score:.16f}")
```

#### 5단계: 테스트 데이터 추가
`data.json`에 Circle 패턴 케이스를 추가하고 expected를 `"o"` 또는 `"Circle"`로 설정한다.

**확장 원칙:** 정규화 → 데이터 → 판정 로직 → 출력 → 테스트 순서는 "변환 → 표현 → 처리 → 검증"의 계층 순서를 따른다.

---

### Q10. 1000×1000 패턴을 처리한다면 시간/메모리 측면에서 어떤 문제가 발생하며, 어떤 최적화를 우선 적용할지 설명하라.

**A.**

#### 문제 분석

**시간 측면:**
- 연산 횟수 = 1000² = **1,000,000회** (순수 Python 루프)
- 현재 코드에서 25×25(625회)의 평균 시간 ≈ 0.06 ms라면,
  1000×1000은 단순 비례로 약 **96 ms** (1회 MAC만)
- 다수의 필터 혹은 패턴을 처리하면 초 단위로 증가

**메모리 측면:**
- 1000×1000 float 배열: 1,000,000 × 8 bytes = **8 MB** (패턴 1개)
- 필터 수가 많으면 필터만 수백 MB
- Python 리스트는 원시 배열보다 객체 오버헤드가 크므로 실제로는 수배 더 소모

#### 우선 적용할 최적화 (중요도 순)

| 우선순위 | 최적화 방법 | 효과 |
|--------|-----------|------|
| 1위 | **NumPy 벡터화** (`np.dot(a.flatten(), b.flatten())`) | 반복문 제거, 100~1000× 속도 향상 |
| 2위 | **배열 구조 변경** (Python 중첩 리스트 → 연속 메모리 배열) | 캐시 히트율 향상 |
| 3위 | **병렬 처리** (multiprocessing, 패턴별 병렬 MAC) | 코어 수 배 속도 향상 |
| 4위 | **부분 업데이트** (슬라이딩 윈도우 MAC 재사용) | 합성곱 구조에서 중복 연산 제거 |
| 5위 | **FFT 기반 합성곱** | 큰 필터에서 O(N² log N) 달성 |

**실무적 결론:** 첫 번째 최적화로 NumPy를 도입하면 대부분의 문제가 해결된다.
더 나아가 GPU/NPU를 활용하면 병렬 MAC 연산으로 추가로 수백 배까지 가속 가능하다.

---

### Q11. CPU의 직렬 처리와 NPU의 병렬 처리 관점에서, 이 문제(대규모 MAC)의 병목이 어디에 생기는지 설명하라.

**A.**

#### CPU 직렬 처리에서의 병목

현재 코드(Python 이중 루프)의 실행 흐름:

```
for i in range(N):
    for j in range(N):
        score += pattern[i][j] * filter[i][j]
```

- **각 곱셈과 덧셈은 순서대로(직렬로) 실행**된다.
- `i=0, j=0` 의 결과가 완료된 후 `i=0, j=1`이 시작되므로, N² 번의 연산이 모두 순차적이다.
- **병목 1 — 연산 직렬성:** 이전 연산 결과(score)가 다음 연산에 필요하므로 파이프라이닝이 어렵다.
- **병목 2 — 메모리 접근:** N이 클수록 배열이 L1/L2 캐시를 벗어나 RAM 접근 빈도가 높아진다. 메모리 접근 지연이 연산 속도보다 훨씬 느려서 CPU가 데이터를 기다리는 시간(Memory Bound)이 발생한다.
- **병목 3 — Python 인터프리터 오버헤드:** 각 루프 반복마다 bytecode 해석, 타입 검사 등 추가 비용이 든다.

#### NPU 병렬 처리에서의 이점

NPU(Neural Processing Unit)는 MAC 연산을 위해 설계된 **대규모 병렬 처리 아키텍처**다:

```
NPU 내부: 수천 개의 MAC 유닛이 동시(병렬)에 곱셈 수행
          → score = Σ(pattern[i,j] × filter[i,j])를 한 싸이클에 처리
```

- 모든 위치의 곱셈을 **한 번에(병렬로)** 실행하므로 이론적으로 O(N²) → **O(1)** (충분한 병렬 유닛이 있을 때)
- **병목 위치:** NPU에서의 병목은 연산이 아니라 **데이터 전송(Memory Bandwidth)**이다.
  연산 유닛이 아무리 많아도, CPU RAM → NPU 내부 SRAM으로 데이터를 옮기는 속도가 연산 속도를 따라가지 못하면 유닛들이 데이터를 기다리게 된다.

#### 결론 요약

| 구분 | 병목 원인 | 위치 |
|------|----------|------|
| CPU (Python 루프) | 직렬 연산 + 인터프리터 오버헤드 + 캐시 미스 | 연산 및 메모리 접근 |
| CPU (NumPy BLAS) | L3 캐시 초과 시 메모리 대역폭 | 메모리 |
| NPU/GPU | 호스트↔디바이스 데이터 전송 (PCIe/버스 대역폭) | 데이터 I/O |

대규모 MAC에서는 **"얼마나 빠르게 연산하느냐"보다 "얼마나 빠르게 데이터를 공급하느냐"**가 실질적 성능을 결정한다. 이것이 NPU/GPU 설계에서 Memory Bandwidth를 최우선 사양으로 보는 이유다.

---

## 📌 전체 평가 결과 요약

| 항목 | 충족 개수 | 총 개수 | 비고 |
|------|:--------:|:------:|------|
| 항목 1: 기능 동작 검증 | **9** | 9 | 모든 항목 충족 |
| 항목 2: 코드 구조 및 설계 | **4** | 4 | 질문별 답변 위에 기술 |
| 항목 3: 핵심 기술 원리 적용 | **4** | 4 | 질문별 답변 위에 기술 |
| 항목 4: 심층 인터뷰 | **3** | 3 | 질문별 답변 위에 기술 |

> **결론:** 현재 `main.py` 구현은 평가문항의 모든 기능 요구사항을 충족하며, 각 설계 결정에 대한 명확한 근거를 설명할 수 있다.
