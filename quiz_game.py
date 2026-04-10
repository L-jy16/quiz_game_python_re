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
            with open(self.state_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            # JSON 데이터를 Quiz 객체로 변환
            quizzes_data = data.get("quizzes", [])
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