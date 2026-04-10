"""
game.py - 퀴즈 게임의 전체 흐름을 담당하는 코드

[역할 분리]
- Quiz 클래스 (quiz.py) : 퀴즈 한 개의 데이터와 정답 채점을 담당
- QuizGame 클래스 (game.py) : 게임 진행, 메뉴 표시, 파일 저장/불러오기를 담당
- main.py : 프로그램 시작점 (QuizGame을 실행하기만 함)
"""

import datetime
import json
import os

from quiz import Quiz, DEFAULT_QUIZZES

# state.json 파일이 저장될 경로입니다. (game.py와 같은 폴더)
STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")


class QuizGame:
    # ==============================================================
    # 프로그램 시작 시 변수 초기화
    # ==============================================================
    def __init__(self):
        self.quizzes = []       # 퀴즈 목록을 담는 리스트
        self.best_score = 0     # 역대 최고 점수 (맞힌 문제 수)
        self.game_history = []  # 시행별 게임 기록 리스트

        # 프로그램 시작 시 저장된 데이터를 파일에서 불러옵니다.
        self.load_state()

    # ==============================================================
    # 1. 파일 불러오기 (state.json → 프로그램 변수)
    # ==============================================================
    def load_state(self):
        # 저장 파일이 없으면 기본 퀴즈 5개로 시작합니다.
        if not os.path.exists(STATE_FILE):
            for quiz in DEFAULT_QUIZZES:
                self.quizzes.append(quiz)
            return

        # 파일이 있으면 읽어서 데이터를 복원합니다.
        # try/except: 파일이 손상되거나 형식이 잘못되었을 때 오류 없이 처리합니다.
        try:
            f = open(STATE_FILE, "r", encoding="utf-8")
            data = json.load(f)
            f.close()

            # 저장된 퀴즈 목록을 Quiz 객체로 하나씩 복원합니다.
            self.quizzes = []
            for q_data in data["quizzes"]:
                question = q_data["question"]
                choices = q_data["choices"]
                answer = q_data["answer"]

                # last_correct 키가 파일에 없을 수도 있으므로 확인합니다.
                if "last_correct" in q_data:
                    last_correct = q_data["last_correct"]
                else:
                    last_correct = None

                quiz = Quiz(question, choices, answer, last_correct)
                self.quizzes.append(quiz)

            # 최고 점수를 불러옵니다.
            self.best_score = data["best_score"]

            # 게임 기록을 불러옵니다. (없을 수도 있으므로 확인 후 불러옵니다)
            if "game_history" in data:
                self.game_history = data["game_history"]
            else:
                self.game_history = []

            # 불러온 정보를 화면에 출력합니다.
            total = len(self.quizzes)
            if total > 0:
                score_percent = int(self.best_score / total * 100)
            else:
                score_percent = 0
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {total}개, 최고점수 {score_percent}점)")

        except Exception:
            # 파일을 읽는 도중 어떤 오류가 나도 기본 퀴즈로 초기화합니다.
            print("⚠️  저장 파일이 손상되어 기본 문제로 다시 시작합니다.")
            self.quizzes = []
            for quiz in DEFAULT_QUIZZES:
                self.quizzes.append(quiz)
            self.best_score = 0
            self.game_history = []

    # ==============================================================
    # 2. 파일 저장하기 (프로그램 변수 → state.json)
    # ==============================================================
    def save_state(self):
        # 퀴즈 리스트를 딕셔너리 리스트로 변환합니다.
        quiz_list = []
        for quiz in self.quizzes:
            quiz_list.append(quiz.to_dict())

        # 저장할 데이터를 딕셔너리로 묶습니다.
        data = {}
        data["quizzes"] = quiz_list
        data["best_score"] = self.best_score
        data["game_history"] = self.game_history

        # 파일에 JSON 형식으로 씁니다.
        f = open(STATE_FILE, "w", encoding="utf-8")
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.close()

    # ==============================================================
    # 3. 메뉴 출력
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

    # ==============================================================
    # 4. 퀴즈 풀기
    # ==============================================================
    def play_quiz(self):
        # 퀴즈가 없으면 안내 후 종료합니다.
        if len(self.quizzes) == 0:
            print("\n📭 등록된 퀴즈가 없습니다. 메뉴에서 '2번'을 눌러 먼저 퀴즈를 추가해 주세요.")
            return

        correct_count = 0
        total_count = len(self.quizzes)

        print(f"\n📝 퀴즈를 시작합니다! (총 {total_count}문제)")

        # for 반복문으로 퀴즈를 하나씩 출력하고 답을 받습니다.
        index = 1
        for quiz in self.quizzes:
            quiz.display(index)

            # 올바른 숫자(1~4)를 입력할 때까지 반복합니다.
            while True:
                user_input = input("\n정답 입력 (1-4): ").strip()

                # 빈 입력 처리
                if user_input == "":
                    print("⚠️  입력값이 없습니다. 1~4 사이의 숫자를 입력해 주세요.")

                # 숫자가 아닌 문자 처리
                elif user_input != "1" and user_input != "2" and user_input != "3" and user_input != "4":
                    print("⚠️  1~4 사이의 숫자만 입력해 주세요.")

                # 올바른 입력이면 반복 탈출
                else:
                    answer_number = int(user_input)
                    break

            # 정답 여부를 확인하고 결과를 출력합니다.
            if quiz.check_answer(answer_number):
                print("✅ 정답입니다!")
                correct_count = correct_count + 1
                quiz.last_correct = True   # 이 퀴즈의 마지막 정답 여부 기록
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번이에요.")
                quiz.last_correct = False  # 이 퀴즈의 마지막 정답 여부 기록

            index = index + 1

        # 최종 결과를 계산합니다.
        score_percent = int(correct_count / total_count * 100)
        print("\n========================================")
        print(f"🏆 결과: {total_count}문제 중 {correct_count}문제 정답! ({score_percent}점)")

        # 최고 점수를 경신했는지 확인합니다.
        if correct_count > self.best_score:
            self.best_score = correct_count
            print("🎉 새로운 최고 기록을 달성했습니다!")
        print("========================================")

        # 이번 시행 기록을 game_history 리스트에 추가합니다.
        record = {}
        record["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record["correct"] = correct_count
        record["total"] = total_count
        record["score_percent"] = score_percent
        self.game_history.append(record)

        # 결과를 파일에 저장합니다.
        self.save_state()

    # ==============================================================
    # 5. 퀴즈 추가
    # ==============================================================
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
        i = 1
        while i <= 4:
            choice = input(f"선택지 {i}번: ").strip()
            if choice != "":
                choices.append(choice)
                i = i + 1
            else:
                print("⚠️  내용을 입력해 주세요.")

        # 3. 정답 번호 입력 (1~4)
        while True:
            ans_input = input("정답 번호 (1-4): ").strip()

            if ans_input == "":
                print("⚠️  입력값이 없습니다. 1~4 사이의 숫자를 입력해 주세요.")
            elif ans_input != "1" and ans_input != "2" and ans_input != "3" and ans_input != "4":
                print("⚠️  1~4 사이의 숫자만 입력해 주세요.")
            else:
                answer = int(ans_input)
                break

        # 4. 새로운 퀴즈 객체를 만들고 리스트에 추가합니다.
        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        self.save_state()
        print("\n✅ 퀴즈가 성공적으로 추가되었습니다!")

    # ==============================================================
    # 6. 퀴즈 목록 보기
    # ==============================================================
    def list_quizzes(self):
        if len(self.quizzes) == 0:
            print("\n📭 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("----------------------------------------")
        index = 1
        for quiz in self.quizzes:
            print(f"  [{index}] {quiz.question}")
            index = index + 1
        print("----------------------------------------")

    # ==============================================================
    # 7. 점수 확인
    # ==============================================================
    def show_score(self):
        total = len(self.quizzes)

        if total == 0:
            print("\n🏆 등록된 퀴즈가 없습니다.")
        elif self.best_score == 0:
            print("\n🏆 아직 퀴즈에서 점수를 낸 기록이 없습니다. (또는 0점)")
        else:
            score_percent = int(self.best_score / total * 100)
            print(f"\n🏆 역대 최고 점수: {score_percent}점 (총 {total}문제 중 {self.best_score}문제 정답)")

        # 게임 기록이 있으면 시행 이력도 함께 보여줍니다.
        if len(self.game_history) > 0:
            print("\n📊 시행 기록:")
            i = 1
            for record in self.game_history:
                print(f"  {i}회차 ({record['date']}): {record['correct']}/{record['total']}문제 ({record['score_percent']}점)")
                i = i + 1

    # ==============================================================
    # 8. 메인 게임 루프 (프로그램이 종료될 때까지 반복)
    # ==============================================================
    def run(self):
        while True:
            try:
                # 메뉴를 보여주고 입력을 받습니다.
                self.show_menu()
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
                    break
                else:
                    print("⚠️  잘못된 입력입니다. 1번부터 5번 사이의 숫자만 적어주세요.")

            # Ctrl+C 또는 EOF(파이프 종료) 신호가 오면 안전하게 저장 후 종료합니다.
            except (KeyboardInterrupt, EOFError):
                print("\n\n⚠️  종료 신호가 감지되었습니다. 데이터를 저장하고 나갑니다.")
                self.save_state()
                break
