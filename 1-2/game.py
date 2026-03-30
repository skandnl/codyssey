"""
game.py - 게임 진행 흐름을 한눈에 쉽게 볼 수 있도록 작성한 퀴즈 게임 코드
"""

import json
import os
import random

from quiz import Quiz, DEFAULT_QUIZZES

# 파일 저장 위치를 설정합니다. 현재 폴더에 state.json 이름으로 저장됩니다.
STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")


class QuizGame:
    def __init__(self):
        # 파이썬 리스트와 딕셔너리로 기본 변수를 설정합니다.
        self.quizzes = []
        self.best_score = {"correct": 0, "total": 0}
        
        # 프로그램을 시작할 때 파일에서 저장된 데이터를 불러옵니다.
        self.load_state()

    # ==============================================================
    # 1. 파일 저장 및 불러오기 (초보자에게는 어려울 수 있으니 그대로 사용하세요)
    # ==============================================================
    def load_state(self):
        if not os.path.exists(STATE_FILE):
            # 처음 실행해서 파일이 없으면 기본 문제를 준비합니다.
            self.quizzes = list(DEFAULT_QUIZZES)
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 저장된 딕셔너리를 다시 Quiz 클래스로 만듭니다.
            self.quizzes = []
            for q_data in data.get("quizzes", []):
                self.quizzes.append(Quiz.from_dict(q_data))
                
            self.best_score = data.get("best_score", {"correct": 0, "total": 0})
            print(f"📂 저장된 데이터를 불러왔습니다. (점수: {self.best_score['correct']}/{self.best_score['total']})")
        except Exception:
            print("⚠️  저장 파일이 손상되어 기본 문제로 다시 시작합니다.")
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = {"correct": 0, "total": 0}

    def save_state(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score
        }
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ==============================================================
    # 2. 기능 구현 (파이썬 기초 조건문/반복문 활용)
    # ==============================================================
    def show_menu(self):
        print("\n========================================")
        print("         🎯 나만의 퀴즈 게임 🎯")
        print("========================================")
        print("  1. 퀴즈 풀기")
        print("  2. 퀴즈 추가")
        print("  3. 퀴즈 목록")
        print("  4. 점수 확인")
        print("  5. 종료")
        print("========================================")

    def play_quiz(self):
        if len(self.quizzes) == 0:
            print("\n📭 등록된 퀴즈가 없습니다. 메뉴에서 '2번'을 눌러 먼저 퀴즈를 추가해 주세요.")
            return

        # 모든 문제를 무작위(랜덤)로 섞습니다.
        random.shuffle(self.quizzes)
        correct_count = 0
        total_count = len(self.quizzes)

        print(f"\n📝 퀴즈를 시작합니다! (총 {total_count}문제)")

        # for 반복문: 리스트에 있는 퀴즈를 하나씩 풉니다.
        index = 1
        for quiz in self.quizzes:
            quiz.display(index)
            
            # 제대로 된 숫자를 입력할 때까지 무한 반복(while True) 합니다.
            while True:
                user_input = input("\n정답 입력 (1-4): ").strip()
                if user_input in ["1", "2", "3", "4"]:
                    answer_number = int(user_input)
                    break # 정답을 맞게 입력하면 무한루프 탈출
                else:
                    print("⚠️  1~4 사이의 숫자만 입력해 주세요.")
            
            # 입력한 값이 진짜 정답인지 확인합니다. (if 조건문)
            if quiz.check_answer(answer_number):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번이에요.")
                
            index += 1

        # 결과 출력 및 최고 점수 저장 로직
        score_percent = int(correct_count / total_count * 100)
        print("\n========================================")
        print(f"🏆 결과: {total_count}문제 중 {correct_count}문제 정답! ({score_percent}점)")

        # 기존 점수와 비교해서 최고 기록을 경신했는지 확인합니다.
        prev_correct = self.best_score["correct"]
        prev_total = self.best_score["total"]
        if prev_total == 0 or (correct_count / total_count) > (prev_correct / prev_total):
            self.best_score = {"correct": correct_count, "total": total_count}
            print("🎉 새로운 최고 기록을 달성했습니다!")
        print("========================================")

        self.save_state()  # 점수를 파일에 저장합니다.

    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        
        # 1. 문제 입력 (빈 칸 입력 방지)
        while True:
            question = input("문제를 입력하세요: ").strip()
            if question != "":
                break
            print("⚠️  내용을 입력해 주세요.")

        # 2. 선택지 4개 입력
        choices = []
        for i in range(1, 5):
            while True:
                choice = input(f"선택지 {i}번: ").strip()
                if choice != "":
                    choices.append(choice)
                    break
                print("⚠️  내용을 입력해 주세요.")

        # 3. 정답 번호 입력 (1~4 확인)
        while True:
            ans_input = input("정답 번호 (1-4): ").strip()
            if ans_input in ["1", "2", "3", "4"]:
                answer = int(ans_input)
                break
            print("⚠️  1~4 사이의 숫자만 입력해 주세요.")

        # 4. 새로운 퀴즈 객체를 만들고 리스트에 저장
        new_quiz = Quiz(question=question, choices=choices, answer=answer)
        self.quizzes.append(new_quiz)
        self.save_state()
        print("\n✅ 퀴즈가 성공적으로 추가되었습니다!")

    def list_quizzes(self):
        if len(self.quizzes) == 0:
            print("\n📭 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("----------------------------------------")
        index = 1
        for quiz in self.quizzes:
            print(f"  [{index}] {quiz.question}")
            index += 1
        print("----------------------------------------")

    def show_score(self):
        correct = self.best_score["correct"]
        total = self.best_score["total"]
        if total == 0:
            print("\n🏆 아직 퀴즈를 푼 기록이 없습니다.")
        else:
            score_percent = int(correct / total * 100)
            print(f"\n🏆 역대 최고 점수: {score_percent}점 (총 {total}문제 중 {correct}문제 정답)")

    # ==============================================================
    # 3. 메인 게임 루프 (게임을 반복해서 실행하는 핵심 공간입니다)
    # ==============================================================
    def run(self):
        while True:
            try:
                # 1. 화면에 1번~5번 메뉴를 보여줍니다.
                self.show_menu()
                
                # 2. 사용자에게 번호를 입력받습니다.
                menu_input = input("선택 (1~5): ").strip()
                
                if menu_input == "1":
                    self.play_quiz()
                elif menu_input == "2":
                    self.add_quiz()
                elif menu_input == "3":
                    self.list_quizzes()
                elif menu_input == "4":
                    self.show_score()
                elif menu_input == "5":
                    print("\n👋 게임을 종료합니다. 안녕히 가세요!")
                    self.save_state()
                    break # 무한 루프(while True)를 탈출하여 프로그램 종료!
                else:
                    # 1~5가 아닌 엉뚱한 값을 적었을 경우
                    print("⚠️  잘못된 입력입니다. 1번부터 5번 사이의 숫자만 적어주세요.")
            
            # Ctrl+C 등을 눌러 강제로 비정상 종료 시 안전하게 저장하고 나가는 코드
            except (KeyboardInterrupt, EOFError):
                print("\n\n⚠️  비정상적인 종료 신호입니다. 데이터를 저장하고 나갑니다.")
                self.save_state()
                break
