class Quiz:
    # 객체가 생성될 때 실행되는 초기화 함수
    def __init__(self, question, choices, answer):
        self.question = question    # 문제
        self.choices = choices  # 선택지
        self.answer = answer    # 정답

    # 퀴즈를 화면에 출력하는 함수
    # number는 문제 번호 (없으면 None)
    def display(self, number=None):
        if number is not None:
            print(f"\n[문제 {number}]")
        print(self.question)
        # 선택지를 하나씩 출력
        # enumerate를 사용하여 번호와 함께 출력
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")

    # 사용자가 입력한 답이 정답인지 확인하는 함수
    def is_correct(self, user_answer):
        # 입력값과 정답이 같으면 True, 아니면 False 반환
        return user_answer == self.answer

    # Quiz 객체를 딕셔너리 형태로 변환하는 함수
    # JSON 파일에 저장하기 위해 사용됨
    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    # 딕셔너리 데이터를 다시 Quiz 객체로 변환하는 함수
    # JSON에서 불러온 데이터를 객체로 만들 때 사용 
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["question"],
            data["choices"],
            data["answer"]
        )