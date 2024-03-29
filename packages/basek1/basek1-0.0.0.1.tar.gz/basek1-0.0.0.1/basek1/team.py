# project/team_info/team.py

import pymysql
from tabulate import tabulate

def get_team_info(year, team_name=None):
    try:
        # MySQL 연결 설정
        conn = pymysql.connect(
            user="root",
            password="1233",
            host="MySQL_서버_IP",  # 여기에 MySQL 서버의 공인 IP 주소를 입력합니다.
            database="baseball_stat",
            charset='utf8'
        )

        # 커서 생성
        cursor = conn.cursor()

        # 쿼리 생성
        if team_name:
            query = f"SELECT * FROM regular_team_{year} WHERE `team_name` = '{team_name}'"
        else:
            query = f"SELECT * FROM regular_team_{year} ORDER BY `rank`"

        # 쿼리 실행
        cursor.execute(query)

        # 결과 가져오기
        team_info = cursor.fetchall()

        # 데이터 가공
        processed_team_info = []
        for info in team_info:
            rank, team, game, win, lose, draw, win_ratio, game_difference, recent_10_games, streak, home, visit = info
            processed_info = {
                '순위': rank,
                '팀명': team,
                '경기수': game,
                '승': win,
                '패': lose,
                '무': draw,
                '승률': win_ratio,
                '게임차': game_difference,
                '최근10경기': recent_10_games,
                '연속': streak,
                '홈': home,
                '방문': visit
            }
            processed_team_info.append(processed_info)

        return processed_team_info

    except pymysql.Error as err:
        print(f"MySQL 오류: {err}")

    finally:
        if 'conn' in locals() and conn.open:
            cursor.close()
            conn.close()

            
def get_team_wl(year, team1=None):
    try:
        # MySQL 연결 설정
        conn = pymysql.connect(
            user="root",
            password="1233",
            host="MySQL_서버_IP",  # 여기에 MySQL 서버의 공인 IP 주소를 입력합니다.
            database="baseball_stat",
            charset='utf8'
        )

        # 커서 생성
        cursor = conn.cursor()

        # 쿼리 생성
        if team1:  # 특정 팀의 승패표를 가져오는 경우
            query = f"SELECT * FROM regular_team_WL_{year} WHERE `team_name` = '{team1}'"
        else:  # 전체 팀의 승패표를 가져오는 경우
            query = f"SELECT * FROM regular_team_WL_{year}"

        # 쿼리 실행
        cursor.execute(query)

        # 컬럼 이름 가져오기
        columns = [col[0] for col in cursor.description]

        # 결과 가져오기
        team_wl = cursor.fetchall()

        # 테이블 형태로 출력하기 위한 데이터 가공
        data = [columns]  # 헤더 추가
        for wl in team_wl:
            data.append(list(wl))

        # 테이블 형태로 출력
        print(tabulate(data, tablefmt="grid"))

    except pymysql.Error as err:
        print(f"MySQL 오류: {err}")

    finally:
        if 'conn' in locals() and conn.open:
            cursor.close()
            conn.close()
