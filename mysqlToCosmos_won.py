import logging
#import azure.functions as func
import mysql.connector
#from azure.cosmos import CosmosClient
from pocket import pocket

# MySQL 연결 정보 설정
info = pocket()
mysql_host =  info.mysql_host
mysql_user = info.mysql_user
mysql_password = info.mysql_password
mysql_database = info.mysql_database



#def main(event: func.EventGridEvent):
    # Azure MySQL 연결 설정
mysql_connection = mysql.connector.connect(
    host=info.mysql_host,
    user=info.mysql_user,
    password=info.mysql_password,
    database=info.mysql_database
)
# MySQL에서 데이터 읽어오기
cursor = mysql_connection.cursor()

prompt_combine = '''
    SELECT
        ip.image_id,
        p1.prompt AS positive_prompt,
        p2.prompt AS negative_prompt,
        ip.prompt_time
    FROM image_prompt ip
    JOIN image_prompt p1 ON ip.image_id = p1.image_id AND p1.is_positive = true
    JOIN image_prompt p2 ON ip.image_id = p2.image_id AND p2.is_positive = false
    '''

cursor.execute(prompt_combine)
rows = cursor.fetchall()

for row in rows:
    item = {"image_id": str(row[0]), "prompt": row[1], "negative_prompt": row[2], "prompt_time": row[3]}
    print(item)