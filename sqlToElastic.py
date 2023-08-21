# 1. 일단 MYSQL과 ElasticSearch 라이브러리 설치 
# 2. MySQL과 ElasticSearch 포트 연결
# 3. SELECT * from image를 통해 가져오기 아니면 column 마다 한줄씩 주어서 가져와도 될 것 같다.
# 4. 가져온 image 수를 측정을 해서 반복문을 통해 bulk_index로 삽입하기

import mysql.connector
from elasticsearch import Elasticsearch 
from elasticsearch.helpers import bulk
from pocket import pocket
from datetime import datetime

# MySQL 연결 정보 설정
info = pocket()
mysql_host =  info.mysql_host
mysql_port = info.mysql_port
mysql_user = info.mysql_user
mysql_password = info.mysql_password
mysql_database = info.mysql_database

# Elasticsearch 연결 정보
es_host = info.es_host
es_port = info.es_port
es_username = info.es_username
es_password = info.es_password

es = Elasticsearch(
    [f"{es_host}:{es_port}"],
    http_auth=(es_username, es_password)    
)


def convert_to_iso8601_format(dt):    
    return dt.strftime('%Y-%m-%d %H:%M:%S')


connection = mysql.connector.connect(
    host=mysql_host,
    port = mysql_port,
    user=mysql_user,        
    password=mysql_password,
    database=mysql_database
)

cursor = connection.cursor()

# prompt_combine = '''
# SELECT
#     p1.image_id,
#     p1.prompt AS prompt,
#     p2.prompt AS negative_prompt,
#     p1.prompt_time As timestamp
# FROM image_prompt p1
# JOIN image_prompt p2 ON p1.image_id = p2.image_id
# WHERE p1.is_positive = true AND p2.is_positive = false
# '''


# prompt_combine subscribe 안된 것들 중에 adult 정보도 elastic으로 넘겨주게 수정
prompt_combine = '''
    SELECT 
        p1.image_id,
        p1.prompt AS prompt,
        p2.prompt AS negative_prompt,
        p1.prompt_time As timestamp,
        p3.adult AS adult 
    FROM image_prompt p1
    JOIN image_prompt p2 ON p1.image_id = p2.image_id
    JOIN image_table p3 ON p1.image_id = p3.image_id
    JOIN image_post p4 ON p3.image_post_id = p4.image_post_id
    WHERE (p1.image_id IN (
        SELECT 
        p3.image_id
        FROM image_table p3
        JOIN image_post p4 ON p3.image_post_id = p4.image_post_id
        WHERE p4.subscribe_only = false))
        AND(p1.is_positive = true AND p2.is_positive = false)
    LIMIT 6
'''    
cursor.execute(prompt_combine)    

# query = f"SELECT * FROM IMAGE_PROMPT;"

# cursor.execute(query)

columns = [column[0] for column in cursor.description]
data = [dict(zip(columns, row)) for row in cursor.fetchall()]

cursor.close()
connection.close()

#Elasticsearch에 저장할 데이터 변환 (index와 id 필드가 있는 dict 형태로 변환)
actions = [
    {
        "_index": "test_image_prompt",
        "_id": doc["image_id"],            
        "_source": {
            "image_id" : doc["image_id"],
            "prompt" : doc["prompt"],
            "negative_prompt" : doc["negative_prompt"],                
            "timestamp":f'{convert_to_iso8601_format(doc["timestamp"])}'                
        }
    }
    for doc in data
]

# Elasticsearch에 bulk 색인 실행
bulk(es, actions)
