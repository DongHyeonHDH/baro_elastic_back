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
    'database': info.mysql_database,    # 사용할 데이터베이스 이름         
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


  
try:
    # 쿼리 실행
    # checkserver = 'select * from image LIMIT 10'
    # checkserver = 'DESCRIBE image_post'
    # cursor.execute(checkserver)

    # checkprompt = 'select count(*) from image_prompt'
    # checkprompt = 'DESCRIBE image_prompt'
    # cursor.execute(checkprompt)

    cursor = '''
      SELECT 
          p1.image_id,
          p1.prompt AS prompt,
          p2.prompt AS negative_prompt,
          p1.prompt_time As timestamp     
      FROM image_prompt p1
      JOIN image_prompt p2 ON p1.image_id = p2.image_id
      WHERE p1.image_id = (SELECT 
          p3.image_id
          FROM image p3
          JOIN image_post p4 ON p3.image_post_id = p4.image_post_id
          WHERE p4.subscribe_only = false)
          AND(p1.is_positive = true AND p2.is_positive = false)
    '''

    rows = cursor.fetchall()

    for row in rows:
       print(row)   

    print("테이블 읽기 성공.")

except mysql.connector.Error as err:
    print(f"테이블 읽기 오류: {err}")
finally:
    # 커넥션과 커서 닫기
    cursor.close()
    conn.close()