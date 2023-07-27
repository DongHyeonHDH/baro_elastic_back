import mysql.connector

# MySQL 연결 정보 설정
config = {
    'host': '13.125.224.184',       # 호스트   
    'port': 50588, 
    'user': 'hdh',   # 사용자 이름
    'password': '4202',   # 비밀번호
    'database': 'baro_grim_practice'    # 사용할 데이터베이스 이름
}

# MySQL 연결
conn = mysql.connector.connect(**config)

# 커서 생성
cursor = conn.cursor()

# 테이블 생성 쿼리
drop_table = 'DROP TABLE IMAGE;'
create_table_query = '''
CREATE TABLE IF NOT EXISTS IMAGE (
    user_id VARCHAR(10),
    name VARCHAR(500) DEFAULT 'temp_key',    
    file_link VARCHAR(500) NOT NULL,    
    prompt TEXT,
    negative_prompt TEXT,
    timestamp DATE,
    steps INT,
    sampler VARCHAR(30),
    cfg_scale INT,
    seed LONG,
    model_hash VARCHAR(10),
    clip_skip INT,
    denoising_strength FLOAT
)
'''
drop_table2 = 'DROP TABLE TEMP;'
create_temp = '''
CREATE TABLE IF NOT EXISTS TEMP (
    user_id VARCHAR(10),
    name VARCHAR(500) DEFAULT 'temp_key',    
    file_link VARCHAR(500) NOT NULL,
    prompt TEXT,
    negative_prompt TEXT,
    timestamp DATE
)
'''


try:
    # 쿼리 실행
    cursor.execute(drop_table)
    cursor.execute(drop_table2)
    cursor.execute(create_table_query)
    cursor.execute(create_temp)
    print("테이블이 성공적으로 생성되었습니다.")
except mysql.connector.Error as err:
    print(f"테이블 생성 오류: {err}")
finally:
    # 커넥션과 커서 닫기
    cursor.close()
    conn.close()
