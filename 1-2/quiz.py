"""
quiz.py - 퀴즈 한 개를 나타내는 클래스 (초보자용 단순화 버전)
"""

class Quiz:
    # 파이썬 클래스의 기초: __init__ 메서드로 변수를 설정합니다.
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    # 화면에 문제를 보여주는 기능입니다.
    def display(self, index):
        print("\n----------------------------------------")
        print(f"[문제 {index}]")
        print(f"{self.question}\n")
        
        # 선택지를 1번부터 4번까지 보여줍니다.
        # enumerate(_, 1)은 1부터 번호를 매기는 기능입니다.
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")

    # 입력한 정답이 진짜 정답인지 확인하는 기능입니다.
    def check_answer(self, user_answer):
        if user_answer == self.answer:
            return True
        else:
            return False

    # 데이터를 파일(state.json)에 저장할 수 있도록 딕셔너리로 바꿉니다.
    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    # 파일에 저장된 딕셔너리 데이터를 다시 Quiz 클래스로 되돌리는 기능입니다.
    @classmethod
    def from_dict(cls, data):
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"]
        )

# ======================================================================
# 만약 파일(state.json)이 없을 때 사용하기 위한 게임의 기본 문제들입니다.
# ======================================================================
DEFAULT_QUIZZES = [
    Quiz(
        question="Python을 처음 만든 사람은 누구인가요?",
        choices=["James Gosling", "Guido van Rossum", "Linus Torvalds", "Bjarne Stroustrup"],
        answer=2
    ),
    Quiz(
        question="Python에서 리스트(list)의 마지막 요소에 접근하는 올바른 인덱스는?",
        choices=["list[0]", "list[-0]", "list[-1]", "list[last]"],
        answer=3
    ),
    Quiz(
        question="Python에서 딕셔너리(dict)의 모든 키를 가져오는 방법은?",
        choices=[".values()", ".items()", ".keys()", ".all()"],
        answer=3
    ),
    Quiz(
        question="Python 파일을 안전하게 열고 닫기 위해 쓰는 키워드는?",
        choices=["try", "with", "open", "import"],
        answer=2
    ),
    Quiz(
        question="Python에서 클래스의 생성자(처음 만들 때 실행되는) 함수 이름은?",
        choices=["__start__", "__new__", "__create__", "__init__"],
        answer=4
    )
]
