# quiz_game.py 파일에 있는 QuizGame 클래스를 가져옴
from quiz_game import QuizGame


# 프로그램의 시작 함수 (메인 함수)
def main():

    # QuizGame 객체 생성 (게임 시작 준비)
    game = QuizGame()

    # 게임 실행 (메뉴 출력 + 전체 흐름 시작)
    game.run()


# 이 파일이 직접 실행될 때만 main() 함수 실행
if __name__ == "__main__":

    # 프로그램 시작
    main()