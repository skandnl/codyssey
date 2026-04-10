"""
Mini NPU Simulator
MAC(Multiply-Accumulate) 연산 기반 패턴 판별기
외부 라이브러리 사용 금지 - 표준 라이브러리(json, time)만 사용
"""

import json
import time
import os

# ============================================================
# 상수 정의
# ============================================================
EPSILON = 1e-9          # 동점 판정 허용오차
REPEAT_COUNT = 10       # 성능 측정 반복 횟수
DATA_FILE = "data.json" # 데이터 파일 경로


# ============================================================
# Pattern 클래스: N×N 2차원 배열 저장/읽기
# ============================================================
class Pattern:
    """N×N 크기의 2차원 패턴 또는 필터를 저장하는 클래스"""

    def __init__(self, n: int):
        self.n = n
        self.data = [[0.0] * n for _ in range(n)]

    def set_value(self, row: int, col: int, value: float):
        """특정 위치에 값 저장"""
        self.data[row][col] = value

    def get_value(self, row: int, col: int) -> float:
        """특정 위치의 값 읽기"""
        return self.data[row][col]

    @classmethod
    def from_2d_list(cls, array_2d: list) -> "Pattern":
        """2차원 리스트로부터 Pattern 객체 생성"""
        n = len(array_2d)
        p = cls(n)
        for i in range(n):
            for j in range(len(array_2d[i])):
                p.set_value(i, j, float(array_2d[i][j]))
        return p

    def __repr__(self):
        lines = []
        for row in self.data:
            lines.append("  " + " ".join(f"{v:.0f}" for v in row))
        return "\n".join(lines)


# ============================================================
# 라벨 정규화 (표준화)
# ============================================================
def normalize_label(label: str) -> str:
    """
    다양한 형태의 라벨을 표준 라벨로 정규화
      '+' or 'cross' → 'Cross'
      'x' or 'X'    → 'X'
    """
    normalized = label.strip().lower()
    if normalized in ("+", "cross"):
        return "Cross"
    elif normalized in ("x",):
        return "X"
    else:
        return label  # 알 수 없는 라벨은 그대로 반환


# ============================================================
# MAC 연산 (외부 라이브러리 금지, 반복문으로 직접 구현)
# ============================================================
def mac_compute(pattern: Pattern, filter_p: Pattern) -> float:
    """
    MAC(Multiply-Accumulate) 연산
    입력 패턴과 필터를 위치별로 곱하고 모두 더해 점수를 반환
    시간 복잡도: O(N²)
    """
    n = pattern.n
    score = 0.0
    for i in range(n):
        for j in range(n):
            score += pattern.get_value(i, j) * filter_p.get_value(i, j)
    return score


# ============================================================
# 점수 비교 → 판정
# ============================================================
def judge(score_a: float, score_b: float,
          label_a: str = "Cross", label_b: str = "X") -> str:
    """
    두 점수를 비교해 판정 결과를 반환
    |score_a - score_b| < EPSILON 이면 UNDECIDED
    """
    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"
    elif score_a > score_b:
        return label_a
    else:
        return label_b


# ============================================================
# 입력 유틸리티
# ============================================================
def input_matrix(size: int, name: str) -> Pattern:
    """
    콘솔에서 size×size 행렬을 입력받아 Pattern 객체로 반환
    입력 오류 시 재입력 유도
    """
    print(f"\n{name} ({size}줄 입력, 공백 구분)")
    rows = []
    while len(rows) < size:
        remaining = size - len(rows)
        try:
            line = input()
            values = line.strip().split()
            if len(values) != size:
                print(f"  입력 형식 오류: 각 줄에 {size}개의 숫자를 공백으로 구분해 입력하세요.")
                print(f"  (현재 {len(values)}개 입력됨 — 이 줄을 다시 입력합니다)")
                continue
            # 숫자 파싱 검증
            parsed = []
            parse_ok = True
            for v in values:
                try:
                    parsed.append(float(v))
                except ValueError:
                    print(f"  입력 형식 오류: '{v}'은(는) 숫자가 아닙니다. 이 줄을 다시 입력하세요.")
                    parse_ok = False
                    break
            if not parse_ok:
                continue
            rows.append(parsed)
        except EOFError:
            print("  입력 종료 감지. 프로그램을 종료합니다.")
            raise SystemExit(1)
    return Pattern.from_2d_list(rows)


# ============================================================
# 성능 분석: MAC 연산 반복 측정
# ============================================================
def measure_mac_time(pattern: Pattern, filter_p: Pattern,
                     repeat: int = REPEAT_COUNT) -> float:
    """
    MAC 연산을 repeat회 반복 측정하여 평균 시간(ms)을 반환
    I/O 시간 제외, 연산 함수 호출 구간만 측정
    """
    total = 0.0
    for _ in range(repeat):
        start = time.perf_counter()
        mac_compute(pattern, filter_p)
        end = time.perf_counter()
        total += (end - start) * 1000  # 초 → ms
    return total / repeat


def generate_cross_pattern(n: int) -> Pattern:
    """N×N 십자가(Cross) 패턴을 자동 생성 (보너스: 패턴 생성기)"""
    p = Pattern(n)
    mid = n // 2
    for i in range(n):
        p.set_value(mid, i, 1.0)
        p.set_value(i, mid, 1.0)
    return p


def generate_x_pattern(n: int) -> Pattern:
    """N×N X 패턴을 자동 생성 (보너스: 패턴 생성기)"""
    p = Pattern(n)
    for i in range(n):
        p.set_value(i, i, 1.0)
        p.set_value(i, n - 1 - i, 1.0)
    return p


def performance_analysis(sizes: list):
    """
    크기별 MAC 연산 시간 측정 및 표 출력
    Cross 패턴과 Cross 필터로 측정 (생성기 활용)
    """
    print("\n" + "#" * 43)
    print(f"# [성능 분석] 평균 시간 (반복: {REPEAT_COUNT}회)")
    print("#" * 43)
    print(f"{'크기':<10} {'평균 시간(ms)':>14} {'연산 횟수(N²)':>14}")
    print("-" * 43)
    for n in sizes:
        pattern = generate_cross_pattern(n)
        filt = generate_cross_pattern(n)
        avg_ms = measure_mac_time(pattern, filt, REPEAT_COUNT)
        ops = n * n
        print(f"{str(n) + '×' + str(n):<10} {avg_ms:>14.4f} {ops:>14}")


# ============================================================
# 모드 1: 사용자 입력 (3×3)
# ============================================================
def mode1_user_input():
    """
    3×3 필터 A, B와 패턴을 콘솔로 입력받아
    MAC 연산 결과와 판정을 출력하는 모드
    """
    SIZE = 3

    print("\n" + "#" * 43)
    print("# [1] 필터 입력")
    print("#" * 43)

    filter_a = input_matrix(SIZE, "필터 A")
    filter_b = input_matrix(SIZE, "필터 B")

    print(f"\n  ✓ 필터 A 저장 완료:")
    print(filter_a)
    print(f"  ✓ 필터 B 저장 완료:")
    print(filter_b)

    print("\n" + "#" * 43)
    print("# [2] 패턴 입력")
    print("#" * 43)

    pattern = input_matrix(SIZE, "패턴")

    print("\n" + "#" * 43)
    print("# [3] MAC 결과")
    print("#" * 43)

    # MAC 연산 + 시간 측정
    score_a = mac_compute(pattern, filter_a)
    score_b = mac_compute(pattern, filter_b)
    avg_ms = measure_mac_time(pattern, filter_a, REPEAT_COUNT)

    print(f"A 점수: {score_a:.16f}")
    print(f"B 점수: {score_b:.16f}")
    print(f"연산 시간(평균/{REPEAT_COUNT}회): {avg_ms:.4f} ms")

    result = judge(score_a, score_b, "A", "B")
    if result == "UNDECIDED":
        print(f"판정: 판정 불가 (|A-B| < {EPSILON})")
    else:
        print(f"판정: {result}")

    # 성능 분석 (3×3)
    performance_analysis([3])


# ============================================================
# 모드 2: data.json 분석
# ============================================================
def load_filters(data: dict) -> dict:
    """
    data.json의 filters 섹션을 로드하고 라벨 정규화 적용
    반환: { 'size_5': {'Cross': Pattern, 'X': Pattern}, ... }
    """
    print("\n" + "#" * 43)
    print("# [1] 필터 로드")
    print("#" * 43)

    filters = {}
    for size_key, filter_dict in data.get("filters", {}).items():
        normalized = {}
        for label, arr in filter_dict.items():
            std_label = normalize_label(label)
            normalized[std_label] = Pattern.from_2d_list(arr)
        filters[size_key] = normalized
        loaded_labels = ", ".join(normalized.keys())
        print(f"  ✓ {size_key:<8} 필터 로드 완료 ({loaded_labels})")
    return filters


def mode2_json_analysis():
    """
    data.json을 로드하여 각 패턴을 판별하고
    PASS/FAIL을 출력하는 모드
    """
    # 파일 경로 결정 (main.py와 같은 디렉토리 우선)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, DATA_FILE)

    if not os.path.exists(data_path):
        print(f"  오류: '{data_path}' 파일을 찾을 수 없습니다.")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 필터 로드
    filters = load_filters(data)

    print("\n" + "#" * 43)
    print("# [2] 패턴 분석 (라벨 정규화 적용)")
    print("#" * 43)

    patterns_data = data.get("patterns", {})
    total = 0
    passed = 0
    failed = 0
    fail_cases = []

    for pat_key in sorted(patterns_data.keys()):
        pat_info = patterns_data[pat_key]
        print(f"\n  --- {pat_key} ---")
        total += 1

        # 키에서 크기(N) 추출: size_{N}_{idx}
        parts = pat_key.split("_")  # ['size', '5', '1']
        if len(parts) < 3:
            reason = f"키 형식 오류 ('{pat_key}'에서 크기 추출 실패)"
            print(f"  FAIL: {reason}")
            failed += 1
            fail_cases.append((pat_key, reason))
            continue

        size_key = f"size_{parts[1]}"  # 'size_5'

        # 해당 크기 필터 존재 여부 확인
        if size_key not in filters:
            reason = f"필터 '{size_key}' 없음"
            print(f"  FAIL: {reason}")
            failed += 1
            fail_cases.append((pat_key, reason))
            continue

        cross_filter = filters[size_key].get("Cross")
        x_filter = filters[size_key].get("X")

        if cross_filter is None or x_filter is None:
            reason = f"'{size_key}' Cross 또는 X 필터 누락"
            print(f"  FAIL: {reason}")
            failed += 1
            fail_cases.append((pat_key, reason))
            continue

        # 패턴 로드
        try:
            input_arr = pat_info["input"]
            pattern = Pattern.from_2d_list(input_arr)
        except (KeyError, TypeError, ValueError) as e:
            reason = f"패턴 데이터 오류: {e}"
            print(f"  FAIL: {reason}")
            failed += 1
            fail_cases.append((pat_key, reason))
            continue

        # 크기 일치 검증
        if pattern.n != cross_filter.n:
            reason = (f"크기 불일치: 패턴 {pattern.n}×{pattern.n} vs "
                      f"필터 {cross_filter.n}×{cross_filter.n}")
            print(f"  FAIL: {reason}")
            failed += 1
            fail_cases.append((pat_key, reason))
            continue

        # MAC 연산
        score_cross = mac_compute(pattern, cross_filter)
        score_x = mac_compute(pattern, x_filter)

        print(f"  Cross 점수: {score_cross:.16f}")
        print(f"  X 점수:     {score_x:.16f}")

        # 판정
        verdict = judge(score_cross, score_x, "Cross", "X")

        # expected 라벨 정규화
        raw_expected = pat_info.get("expected", "")
        expected = normalize_label(raw_expected)

        # PASS/FAIL 판정
        if verdict == "UNDECIDED":
            is_pass = False
            result_str = f"FAIL (동점/UNDECIDED)"
        elif verdict == expected:
            is_pass = True
            result_str = "PASS"
        else:
            is_pass = False
            result_str = "FAIL"

        print(f"  판정: {verdict} | expected: {expected} | {result_str}")

        if is_pass:
            passed += 1
        else:
            failed += 1
            if verdict == "UNDECIDED":
                reason = f"동점(UNDECIDED) 처리 규칙에 따라 FAIL"
            else:
                reason = f"판정={verdict}, expected={expected}"
            fail_cases.append((pat_key, reason))

    # 성능 분석 (모드 2: 3×3 포함 전체 크기)
    performance_analysis([3, 5, 13, 25])

    # 결과 요약
    print("\n" + "#" * 43)
    print("# [4] 결과 요약")
    print("#" * 43)
    print(f"  총 테스트: {total}개")
    print(f"  통과:     {passed}개")
    print(f"  실패:     {failed}개")

    if fail_cases:
        print("\n  실패 케이스:")
        for case_id, reason in fail_cases:
            print(f"    - {case_id}: {reason}")
    else:
        print("\n  ✓ 모든 테스트 통과!")
        print("  (라벨 정규화 및 epsilon 정책 적용으로 FAIL 0건 달성)")

    print("\n  (상세 원인 분석 및 복잡도 설명은 README.md의 \"결과 리포트\" 섹션 참조)")


# ============================================================
# 메인 진입점
# ============================================================
def main():
    print("=" * 43)
    print("  Mini NPU Simulator")
    print("  MAC 연산 기반 패턴 판별기")
    print("=" * 43)

    print("\n[모드 선택]")
    print("  1. 사용자 입력 (3×3)")
    print("  2. data.json 분석")

    while True:
        choice = input("선택: ").strip()
        if choice == "1":
            mode1_user_input()
            break
        elif choice == "2":
            mode2_json_analysis()
            break
        else:
            print("  1 또는 2를 입력하세요.")

    print("\n" + "=" * 43)
    print("  시뮬레이션 종료")
    print("=" * 43)


if __name__ == "__main__":
    main()
