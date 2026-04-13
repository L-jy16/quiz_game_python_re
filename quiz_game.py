import json
from quiz import Quiz


class QuizGame:
    def __init__(self):
         # 저장 파일 이름
        self.state_file = "state.json"
        
        # 퀴즈 목록 저장 리스트
        self.quizzes = []
        
        # 최고 점수 저장 변수
        self.best_score = 0
        
        # 프로그램 실행 시 데이터 불러오기
        self.load_state()

    # json 안에 내용이 없을 경우를 위한 기본 데이터
    def get_default_quizzes(self):
        return [
            Quiz("대한민국의 수도는 어디인가요?", ["부산", "서울", "인천", "대전"], 2),
            Quiz("지구에서 가장 큰 대륙은 무엇인가요?", ["아프리카", "유럽", "아시아", "남아메리카"], 3),
            Quiz("물의 화학식은 무엇인가요?", ["CO2", "H2O", "O2", "NaCl"], 2),
            Quiz("태양은 무엇으로 이루어진 천체인가요?", ["고체", "액체", "기체", "플라즈마"], 4),
            Quiz("대한민국의 국기는 무엇인가요?", ["성조기", "유니언잭", "태극기", "오성홍기"], 3),
            Quiz("컴퓨터의 중앙처리장치를 무엇이라고 하나요?", ["RAM", "CPU", "SSD", "GPU"], 2)
        ]

    # JSON 파일에서 데이터 불러오기
    def load_state(self):
        try:
            # state.json이 있을 경우에 state.json파일을 만듦
            # encoding="utf-8"은 한글이 포함되어 있어도 깨지지 않도록 하기 위한 설정
            # save_state()에서 파일을 "w" 모드로 열어 현재 상태 전체를 json.dump()로 저장하는 방식으로 전체를 덮어쓰게 함
            with open(self.state_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            # quizzes가 존하면 값을 가져오고 없을 경우 빈 리스크 반환
            quizzes_data = data.get("quizzes", [])
            # from_dict() = 딕셔너리 1개를 받아 Quiz 객체 1개로 바꿔준다.
            self.quizzes = [Quiz.from_dict(item) for item in quizzes_data]
            
            # 최고 점수 불러오기
            self.best_score = data.get("best_score", 0)
            
            # 퀴즈가 엇으면 기본 데이터 불러와서 사용
            if not self.quizzes:
                print("저장된 퀴즈가 없어 기본 퀴즈를 불러옵니다.")
                self.quizzes = self.get_default_quizzes()
                self.save_state()
            else:
                print(f"저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")

        # 파일 없을 경우
        except FileNotFoundError:
            print("state.json 파일이 없어 기본 퀴즈를 생성합니다.")
            self.quizzes = self.get_default_quizzes()
            self.best_score = 0
            self.save_state()

        # JSON 파일이 손상이 된 경우
        except json.JSONDecodeError:
            print("state.json 파일이 손상되어 기본 퀴즈로 복구합니다.")
            self.quizzes = self.get_default_quizzes()
            self.best_score = 0
            self.save_state()

         # JSON 파일을 불러오는 중에 오류가 발생한 경우 기본 데이터로 불러온다
        except Exception as error:
            print(f"파일을 불러오는 중 오류가 발생했습니다: {error}")
            print("기본 퀴즈로 시작합니다.")
            self.quizzes = self.get_default_quizzes()
            self.best_score = 0

    def save_state(self):
        # 저장할 데이터 만들기
        data = {
            # .to_dict() = 객체를 딕셔너리로 변환하는 병령어
            # self.quizzes = 퀴즈 객체 리스트, quiz = Quiz 객체
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score
        }

        try:
            # 파일 열기
            # with를 쓰는 이유는 자동으로 파일이 닫히기 때문
            
            with open(self.state_file, "w", encoding="utf-8") as file:
                # json.dump = 파이썬을 JSON으로 변환에서 파일에 저장
                # ensure_ascii=False = 한글 안 깨지게 만듦
                # indent=2 = 줄을 맞춤
                json.dump(data, file, ensure_ascii=False, indent=2)
                
        # 저장 중 문제 생기면 프로그램 안 죽고 에러메시자 출력
        except Exception as error:
            print(f"파일 저장 중 오류가 발생했습니다: {error}")
            
    # 숫자 입력을 안전하게 받기 위한 함수
    # prompt = 사용자에게 보여줄 입력 문구
    # min_value = 입력 가능한 최소값
    # max_value = 입력 가능한 최대값
    def get_int_input(self, prompt, min_value, max_value):
        # 올바른 값을 입력할 때까지 계속 반복
        while True:
            try:
                # 사용자 입력을 받고, 앞뒤 공백을 제거함
                user_input = input(prompt).strip()

                # 아무것도 입력하지 않고 엔터만 누른 경우 처리
                if user_input == "":
                    print("빈 입력은 허용되지 않습니다. 다시 입력하세요.")
                    # 다시 입력받기 위해 반복문의 처음으로 돌아감
                    continue
                
                # 입력값을 문자열에서 정수로 변환
                number = int(user_input)

                # 입력한 숫자가 허용 범위를 벗어난 경우 처리
                if number < min_value or number > max_value:
                    print(f"{min_value}부터 {max_value} 사이의 숫자를 입력하세요.")
                    # 다시 입력받기 위해 반복문의 처음으로 돌아감
                    continue
                
                # 위의 모든 조건을 통과하면 올바른 숫자이므로 반환
                return number

            # 문자를 입력해서 숫자로 변환할 수 없는 경우 처리
            except ValueError:
                print("숫자로 입력해야 합니다. 다시 입력하세요.")
                
            # 사용자가 Ctrl + C를 눌러 강제로 입력을 중단한 경우 처리
            except KeyboardInterrupt:
                print("\n입력이 중단되었습니다. 프로그램을 안전하게 종료합니다.")
                # 종료 전에 현재 데이터를 저장
                self.save_state()
                # 프로그램 종료
                raise SystemExit
            
            # 입력 스트림이 종료된 경우 처리
            # 예: Ctrl + D 같은 입력 종료 상황
            except EOFError:
                print("\n입력 스트림이 종료되었습니다. 프로그램을 안전하게 종료합니다.")
                # 종료 전에 현재 데이터를 저장
                self.save_state()

                # 프로그램 종료
                raise SystemExit
            
            
    # 메뉴 출력
    def show_menu(self):
        print("\n========================================")
        print(" 나만의 퀴즈 게임 ")
        print("========================================")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("========================================")

    # 퀴즈 풀기 기능
    def play_quiz(self):
        # 퀴즈 목록이 비어 있으면 퀴즈를 진행할 수 없으므로 안내 메시지 출력
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            # 함수 종료
            return

        # 전체 퀴즈 개수를 보여주면서 퀴즈 시작 안내
        print(f"\n 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        # 맞힌 문제 수를 저장할 변수
        score = 0

        # 퀴즈 목록을 처음부터 끝까지 하나씩 꺼내면서 반복
        # index는 문제 번호, quiz는 Quiz 객체
        for index, quiz in enumerate(self.quizzes, start=1):
            print("----------------------------------------")
            # 현재 문제와 선택지를 화면에 출력
            quiz.display(index)
            # 사용자가 정답 번호를 입력하도록 하고,
            # 1~4 사이의 숫자만 허용하도록 처리
            user_answer = self.get_int_input("정답 입력 (1-4): ", 1, 4)
            
            # 사용자가 입력한 답이 정답인지 확인
            if quiz.is_correct(user_answer):
                print("정답입니다!")
                # 맞힌 개수 1 증가
                score += 1
            else:
                # 오답일 경우 실제 정답 번호에 해당하는 선택지 내용을 가져옴
                # quiz.answer는 1부터 시작하므로 리스트 인덱스에 맞게 -1 해줌
                correct_answer_text = quiz.choices[quiz.answer - 1]
                print(f" 오답입니다. 정답은 {quiz.answer}번 ({correct_answer_text}) 입니다.")
        
        # 전체 퀴즈가 끝난 뒤 점수를 백분율로 계산
        final_score = int((score / len(self.quizzes)) * 100)
        print("========================================")
        # 최종 결과 출력
        print(f"결과: {len(self.quizzes)}문제 중 {score}문제 정답! ({final_score}점)")

        # 이번 점수가 기존 최고 점수보다 높으면 최고 점수 갱신
        if final_score > self.best_score:
            # 최고 점수를 현재 점수로 변경
            self.best_score = final_score
            # 변경된 최고 점수를 state.json에 저장
            self.save_state()
            # 새로운 최고 점수라는 메시지 출력
            print("새로운 최고 점수입니다!")

        print("========================================")

    # 새로운퀴즈를 추가하는 함수
    def add_quiz(self):
        print("\n새로운 퀴즈를 추가합니다.")

        try:
            # 사용자에게 문제를 입력받고 앞뒤 공백을 제거함
            question = input("문제를 입력하세요: ").strip()
            
            # 문제가 비어 있으면 다시 입력받음
            while question == "":
                print("문제는 비워둘 수 없습니다.")
                question = input("문제를 입력하세요: ").strip()

            # 선택지 4개를 저장할 리스트 생성
            choices = []
            
            # 1번부터 4번까지 선택지를 입력받기 위해 반복
            for i in range(1, 5):
                # 각 선택지를 입력받고 앞뒤 공백 제거
                choice = input(f"선택지 {i}: ").strip()
                # 선택지가 비어 있으면 다시 입력받음
                while choice == "":
                    print("선택지는 비워둘 수 없습니다.")
                    choice = input(f"선택지 {i}: ").strip()
                # 입력받은 선택지를 리스트에 추가
                choices.append(choice)

            # 정답 번호를 입력받음
            # 1부터 4 사이의 숫자만 입력 가능하도록 처리
            answer = self.get_int_input("정답 번호 (1-4): ", 1, 4)

            # 입력받은 문제, 선택지, 정답 번호를 이용해 새 Quiz 객체 생성
            new_quiz = Quiz(question, choices, answer)
            # 생성한 퀴즈를 전체 퀴즈 목록에 추가
            self.quizzes.append(new_quiz)
            # 추가된 퀴즈를 state.json 파일에 저장
            self.save_state()

            print("퀴즈가 추가되었습니다!")
        
        # 사용자가 Ctrl + C를 눌러 입력을 중단한 경우 처리
        except KeyboardInterrupt:
            print("\n퀴즈 추가가 중단되었습니다.")
            # 중단되더라도 현재 상태를 저장
            self.save_state()
        # 입력 스트림이 종료된 경우 처리
        except EOFError:
            print("\n퀴즈 추가가 종료되었습니다.")
            # 종료 전 현재 상태를 저장
            self.save_state()

    # 퀴즈 목록을 출력
    def show_quiz_list(self):
        # 퀴즈가 하나도 없을 경우 안내 메시지 출력 후 종료
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        # 현재 저장된 퀴즈 개수와 함께 출력
        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("----------------------------------------")
        
        #퀴즈 목록으 하나씩 반복하면서 문제 출력
        # i는 번호 quiz는 Quiz 객체 
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"[{i}] {quiz.question}")
        print("----------------------------------------")

    # 최고 점수를 출력
    def show_best_score(self):
        # 최고 저수가 없는 경우
        if self.best_score == 0:
            print("아직 기록된 최고 점수가 없습니다.")
        else:
            # 최고 점수가 있는 경우
            print(f"최고 점수: {self.best_score}점")

    # 프로그램의 전체 실행 흐름 담당
    def run(self):
        
        # 프로그램 종료될 때까지 반복
        while True:
            # 메뉴 화면 출력
            self.show_menu()
            # 사용자에게 메뉴 번호 입력받기
            choice = self.get_int_input("선택: ", 1, 5)

            # 사용자가 선택한 번호에 따라 퀴즈 풀기, 퀴즈 추가, 퀴즈 목록 풀기, 최고 점수 보기, 종료 중에 실행
            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quiz_list()
            elif choice == 4:
                self.show_best_score()
            elif choice == 5:
                # 종료 전 현재 데이터 저장
                self.save_state()
                # 반복문 종료 및 프로그램 끝
                print("프로그램을 종료합니다.")
                break