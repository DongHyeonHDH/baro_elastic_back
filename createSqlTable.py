import mysql.connector
from mysql.connector import errorcode
from pocket import pocket
# MySQL 연결 정보 설정
info = pocket()
config = {
    'host': info.mysql_host,       # 호스트   
    'port': info.mysql_port, 
    'user': info.mysql_user,   # 사용자 이름
    'password': info.mysql_password,   # 비밀번호
    'database': 'baro_test_image',    # 사용할 데이터베이스 이름         
}

# Construct connection string
try:
   conn = mysql.connector.connect(**config)
   print("Connection established")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with the user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cursor = conn.cursor()

# 테이블 생성 쿼리
drop_prompt ='DROP TABLE IMAGE_PROMPT;' 
drop_table = 'DROP TABLE IMAGE;'
create_table_query = '''
CREATE TABLE IF NOT EXISTS IMAGE (
    image_id VARCHAR(10) PRIMARY KEY,
    user VARCHAR(10),    
    image_file VARCHAR(500) NOT NULL,            
    seed LONG,
    steps INT,
    sampler VARCHAR(30),
    cfg_scale INT,
    model_hash VARCHAR(10),   
    clip_skip INT,
    denoising_strength FLOAT,
    image_time TIMESTAMP,
    adult BOOL
)
'''
create_prompt_query ='''
CREATE TABLE IF NOT EXISTS IMAGE_PROMPT (
    image_id VARCHAR(10),    
    prompt TEXT,
    is_positive BOOL,
    prompt_time TIMESTAMP,    
    FOREIGN KEY(image_id)
    REFERENCES IMAGE(image_id) ON UPDATE CASCADE
)
'''

# drop_temp = 'DROP TABLE TEMP;'
# create_temp = '''
# CREATE TABLE IF NOT EXISTS TEMP (
#     user_id VARCHAR(10),
#     name VARCHAR(500) DEFAULT 'temp_key',    
#     file_link VARCHAR(500) NOT NULL,
#     prompt TEXT,
#     negative_prompt TEXT,
#     timestamp TIMESTAMP
# )
# '''
# drop_log = 'DROP TABLE LOG;'
# create_log = '''
# CREATE TABLE IF NOT EXISTS LOG (
#     log_id VARCHAR(10),    
#     data TEXT,
#     timestamp TIMESTAMP
# )
# '''

try:
    # 쿼리 실행
    cursor.execute(drop_prompt)
    cursor.execute(drop_table)
    # cursor.execute(drop_temp)
    # cursor.execute(drop_log)
    cursor.execute(create_table_query)
    cursor.execute(create_prompt_query)
    # cursor.execute(create_temp)
    # cursor.execute(create_log)
    print("테이블이 성공적으로 생성되었습니다.")
except mysql.connector.Error as err:
    print(f"테이블 생성 오류: {err}")
finally:
    # 커넥션과 커서 닫기
    cursor.close()
    conn.close()
