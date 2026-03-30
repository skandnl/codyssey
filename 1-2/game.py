"""
game.py - QuizGame 클래스: 전체 게임 흐름 관리
"""

import json
import os
import random

from quiz import Quiz, DEFAULT_QUIZZES

STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")


class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스."""

    def __init__(self):
        self.quizzes: list[Quiz] = []
        self.best_score: dict = {"correct": 0, "total": 0}
        self.load_state()

    # ──────────────────────────────────────────
    # 파일 저장 / 불러오기
    # ──────────────────────────────────────────

    def load_state(self) -> None:
        """state.json에서 퀴즈 데이터와 최고 점수를 불러온다."""
        if not os.path.exists(STATE_FILE):
            # 첫 실행: 기본 데이터 사용
            self.quizzes = list(DEFAULT_QUIZZES)
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
            self.best_score = data.get("best_score", {"correct": 0, "total": 0})
            correct = self.best_score.get("correct", 0)
            total = self.best_score.get("total", 0)
            print(f"📂 저장된 데이터를 불러왔습니다. "
                  f"(퀴즈 {len(self.quizzes)}개, 최고점수 {self._score_str(correct, total)})")
        except (json.JSONDecodeError, KeyError, TypeError):
            print("⚠️  저장 파일이 손상되었습니다. 기본 퀴즈 데이터로 초기화합니다.")
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = {"correct": 0, "total": 0}
        except OSError as e:
            print(f"⚠️  파일 읽기 오류: {e}. 기본 데이터를 사용합니다.")
            self.quizzes = list(DEFAULT_QUIZZES)

    def save_state(self) -> None:
        """현재 퀴즈 데이터와 최고 점수를 state.json에 저장한다."""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"⚠️  저장 오류: {e}")

    # ──────────────────────────────────────────
    # 메뉴
    # ──────────────────────────────────────────

    def show_menu(self) -> None:
        """메인 메뉴를 출력한다."""
        print("\n========================================")
        print("         🎯 나만의 퀴즈 게임 🎯")
        print("========================================")
        print("  1. 퀴즈 풀기")
        print("  2. 퀴즈 추가")
        print("  3. 퀴즈 목록")
        print("  4. 점수 확인")
        print("  5. 종료")
        print("========================================")

    def get_menu_choice(self) -> int:
        """메뉴 번호를 입력받아 반환한다. 잘못된 입력은 재요청한다."""
        while True:
            try:
                raw = input("선택: ").strip()
                if not raw:
                    print("⚠️  입력이 비어 있습니다. 1-5 사이의 숫자를 입력하세요.")
                    continue
                choice = int(raw)
                if 1 <= choice <= 5:
                    return choice
                print("⚠️  잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
            except ValueError:
                print("⚠️  잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")

    # ──────────────────────────────────────────
    # 1. 퀴즈 풀기
    # ──────────────────────────────────────────

    def play_quiz(self) -> None:
        """퀴즈를 랜덤 순서로 출제하고 결과를 저장한다."""
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        # 문제 수 선택 (보너스: 문제 수 선택)
        total = self._select_quiz_count()
        if total is None:
            return

        pool = random.sample(self.quizzes, total)
        correct_count = 0

        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")

        for idx, quiz in enumerate(pool, 1):
            quiz.display(idx)
            answer = self._get_answer_input()
            if answer is None:   # Ctrl+C / EOF
                print("\n⚠️  퀴즈가 중단되었습니다.")
                self.save_state()
                return
            if quiz.check_answer(answer):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번이에요.")

        # 결과 출력
        score_pct = int(correct_count / total * 100)
        print(f"\n========================================")
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score_pct}점)")

        # 최고 점수 갱신
        prev_correct = self.best_score.get("correct", 0)
        prev_total = self.best_score.get("total", 0)
        prev_pct = int(prev_correct / prev_total * 100) if prev_total else 0
        if score_pct > prev_pct:
            self.best_score = {"correct": correct_count, "total": total}
            print("🎉 새로운 최고 점수입니다!")
        print("========================================")

        self.save_state()

    def _select_quiz_count(self) -> int | None:
        """풀 문제 수를 선택한다. 취소 시 None 반환."""
        max_count = len(self.quizzes)
        print(f"\n몇 문제를 풀까요? (1~{max_count}, 기본값: {max_count})")
        while True:
            try:
                raw = input(f"문제 수 [Enter = 전체]: ").strip()
                if not raw:
                    return max_count
                count = int(raw)
                if 1 <= count <= max_count:
                    return count
                print(f"⚠️  1~{max_count} 사이의 숫자를 입력하세요.")
            except ValueError:
                print("⚠️  숫자를 입력해 주세요.")
            except (KeyboardInterrupt, EOFError):
                return None

    def _get_answer_input(self) -> int | None:
        """정답 번호(1~4)를 입력받는다. 오류 시 None 반환."""
        while True:
            try:
                raw = input("\n정답 입력 (1-4): ").strip()
                if not raw:
                    print("⚠️  입력이 비어 있습니다. 1~4 사이의 숫자를 입력하세요.")
                    continue
                ans = int(raw)
                if 1 <= ans <= 4:
                    return ans
                print("⚠️  1~4 사이의 숫자를 입력하세요.")
            except ValueError:
                print("⚠️  숫자를 입력해 주세요.")
            except (KeyboardInterrupt, EOFError):
                return None

    # ──────────────────────────────────────────
    # 2. 퀴즈 추가
    # ──────────────────────────────────────────

    def add_quiz(self) -> None:
        """새로운 퀴즈를 등록한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        try:
            question = self._input_required("문제를 입력하세요: ")
            if question is None:
                return

            choices = []
            for i in range(1, 5):
                choice = self._input_required(f"선택지 {i}: ")
                if choice is None:
                    return
                choices.append(choice)

            answer = self._get_answer_index()
            if answer is None:
                return

            new_quiz = Quiz(question=question, choices=choices, answer=answer)
            self.quizzes.append(new_quiz)
            self.save_state()
            print("\n✅ 퀴즈가 추가되었습니다!")

        except (KeyboardInterrupt, EOFError):
            print("\n⚠️  퀴즈 추가가 취소되었습니다.")

    def _input_required(self, prompt: str) -> str | None:
        """공백 제거 후, 비어 있으면 재입력. Ctrl+C 시 None 반환."""
        while True:
            try:
                value = input(prompt).strip()
                if value:
                    return value
                print("⚠️  내용을 입력해 주세요.")
            except (KeyboardInterrupt, EOFError):
                return None

    def _get_answer_index(self) -> int | None:
        """정답 번호(1~4)를 입력받는다."""
        while True:
            try:
                raw = input("정답 번호 (1-4): ").strip()
                if not raw:
                    print("⚠️  번호를 입력해 주세요.")
                    continue
                ans = int(raw)
                if 1 <= ans <= 4:
                    return ans
                print("⚠️  1~4 사이의 숫자를 입력하세요.")
            except ValueError:
                print("⚠️  숫자를 입력해 주세요.")
            except (KeyboardInterrupt, EOFError):
                return None

    # ──────────────────────────────────────────
    # 3. 퀴즈 목록
    # ──────────────────────────────────────────

    def list_quizzes(self) -> None:
        """등록된 퀴즈 목록을 출력한다."""
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("----------------------------------------")
        for i, quiz in enumerate(self.quizzes, 1):
            print(f"  [{i}] {quiz.question}")
        print("----------------------------------------")

    # ──────────────────────────────────────────
    # 4. 점수 확인
    # ──────────────────────────────────────────

    def show_score(self) -> None:
        """최고 점수를 출력한다."""
        correct = self.best_score.get("correct", 0)
        total = self.best_score.get("total", 0)
        if total == 0:
            print("\n🏆 아직 퀴즈를 풀지 않았습니다.")
        else:
            score_str = self._score_str(correct, total)
            print(f"\n🏆 최고 점수: {score_str} ({total}문제 중 {correct}문제 정답)")

    # ──────────────────────────────────────────
    # 유틸리티
    # ──────────────────────────────────────────

    @staticmethod
    def _score_str(correct: int, total: int) -> str:
        if total == 0:
            return "0점"
        return f"{int(correct / total * 100)}점"

    # ──────────────────────────────────────────
    # 메인 루프
    # ──────────────────────────────────────────

    def run(self) -> None:
        """게임 메인 루프를 실행한다."""
        action_map = {
            1: self.play_quiz,
            2: self.add_quiz,
            3: self.list_quizzes,
            4: self.show_score,
        }

        while True:
            try:
                self.show_menu()
                choice = self.get_menu_choice()
                if choice == 5:
                    print("\n👋 게임을 종료합니다. 데이터를 저장했습니다.")
                    self.save_state()
                    break
                action_map[choice]()
            except (KeyboardInterrupt, EOFError):
                print("\n\n⚠️  비정상적인 종료 신호를 감지했습니다. 데이터를 저장하고 종료합니다.")
                self.save_state()
                break
