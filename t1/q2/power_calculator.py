#!/usr/bin/env python3
"""
power_calculator.py
간단한 거듭제곱 계산기:
- 숫자(실수)와 지수(정수)를 입력받아 숫자를 지수만큼 거듭제곱
- **, pow() 미사용
- 음수 지수 지원 (역수 계산)
"""

def power(base: float, exponent: int) -> float:
    """반복문으로 거듭제곱을 계산한다."""
    result = 1.0
    # 절댓값만큼 곱셈 수행
    for _ in range(abs(exponent)):
        result *= base

    # 음수 지수일 경우 역수 반환
    if exponent < 0:
        # 0의 음수 거듭제곱은 정의되지 않음
        if base == 0:
            raise ZeroDivisionError("0 cannot be raised to a negative exponent.")
        result = 1.0 / result
    return result


def main() -> None:
    # 숫자 입력
    try:
        number_input = input("Enter number: ").strip()
        number = float(number_input)
    except ValueError:
        print("Invalid number input.")
        return

    # 지수 입력
    try:
        exponent_input = input("Enter exponent: ").strip()
        exponent = int(exponent_input)
    except ValueError:
        print("Invalid exponent input.")
        return

    try:
        result = power(number, exponent)
    except ZeroDivisionError as e:
        print(e)
        return

    # 정수처럼 떨어지면 소수점 생략
    if result.is_integer():
        print(f"Result: {int(result)}")
    else:
        print(f"Result: {result}")


if __name__ == "__main__":
    main()
