"""
quiz.py - 퀴즈 한 개를 나타내는 클래스
"""


class Quiz:
    # __init__: 퀴즈 객체를 처음 만들 때 실행되는 함수입니다.
    def __init__(self, question, choices, answer, last_correct=None):
        self.question = question        # 문제 내용
        self.choices = choices          # 선택지 리스트 (4개)
        self.answer = answer            # 정답 번호 (1~4)
        self.last_correct = last_correct  # 마지막 시행 정답 여부 (True/False/None)

    # 화면에 문제와 선택지를 보여주는 함수입니다.
    def display(self, index):
        print("\n----------------------------------------")
        print(f"[문제 {index}]")
        print(f"{self.question}\n")

        # 선택지를 1번부터 4번까지 순서대로 출력합니다.
        for i in range(len(self.choices)):
            print(f"  {i + 1}. {self.choices[i]}")

    # 사용자가 입력한 번호가 정답인지 확인하는 함수입니다.
    def check_answer(self, user_answer):
        if user_answer == self.answer:
            return True
        else:
            return False

    # 퀴즈 데이터를 딕셔너리(dict) 형태로 변환합니다. (파일 저장용)
    def to_dict(self):
        quiz_dict = {}
        quiz_dict["question"] = self.question
        quiz_dict["choices"] = self.choices
        quiz_dict["answer"] = self.answer
        quiz_dict["last_correct"] = self.last_correct
        return quiz_dict




# ======================================================================
# 파일(state.json)이 없을 때 사용하는 기본 퀴즈 5개입니다.
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
    ),
]
