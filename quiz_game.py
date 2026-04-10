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
        