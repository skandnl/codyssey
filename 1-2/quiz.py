"""
quiz.py - Quiz 클래스 정의 및 기본 퀴즈 데이터
"""


class Quiz:
    """개별 퀴즈를 표현하는 클래스."""

    def __init__(self, question: str, choices: list[str], answer: int):
        """
        Args:
            question: 문제 문자열
            choices: 선택지 4개 리스트
            answer: 정답 번호 (1~4)
        """
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, index: int) -> None:
        """퀴즈를 터미널에 출력한다."""
        print(f"\n----------------------------------------")
        print(f"[문제 {index}]")
        print(f"{self.question}\n")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")

    def check_answer(self, user_answer: int) -> bool:
        """사용자 답변이 정답인지 확인한다."""
        return user_answer == self.answer

    def to_dict(self) -> dict:
        """JSON 저장을 위해 딕셔너리로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        """딕셔너리에서 Quiz 인스턴스를 생성한다."""
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
        )


# ────────────────────────────────────────────
# 기본 퀴즈 데이터 (Python 프로그래밍 상식)
# ────────────────────────────────────────────
DEFAULT_QUIZZES: list[Quiz] = [
    Quiz(
        question="Python을 처음 만든 사람은 누구인가요?",
        choices=["James Gosling", "Guido van Rossum", "Linus Torvalds", "Bjarne Stroustrup"],
        answer=2,
    ),
    Quiz(
        question="Python에서 리스트(list)의 마지막 요소에 접근하는 올바른 인덱스는?",
        choices=["list[0]", "list[-0]", "list[-1]", "list[last]"],
        answer=3,
    ),
    Quiz(
        question="Python에서 딕셔너리(dict)의 모든 키를 반환하는 메서드는?",
        choices=[".values()", ".items()", ".keys()", ".all()"],
        answer=3,
    ),
    Quiz(
        question="Python 파일을 안전하게 열고 닫는 데 사용하는 키워드는?",
        choices=["try", "with", "open", "import"],
        answer=2,
    ),
    Quiz(
        question="Python에서 클래스의 생성자 메서드 이름은?",
        choices=["__start__", "__new__", "__create__", "__init__"],
        answer=4,
    ),
    Quiz(
        question="다음 중 Python의 불변(immutable) 자료형은?",
        choices=["list", "dict", "tuple", "set"],
        answer=3,
    ),
    Quiz(
        question="JSON 데이터를 Python 딕셔너리로 변환하는 함수는?",
        choices=["json.load()", "json.dumps()", "json.encode()", "json.parse()"],
        answer=1,
    ),
]
