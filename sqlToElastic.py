# 1. 일단 MYSQL과 ElasticSearch 라이브러리 설치 
# 2. MySQL과 ElasticSearch 포트 연결
# 3. SELECT * from image를 통해 가져오기 아니면 column 마다 한줄씩 주어서 가져와도 될 것 같다.
# 4. 가져온 image 수를 측정을 해서 반복문을 통해 bulk_index로 삽입하기

import mysql.connector
from elasticsearch import Elasticsearch 
from elasticsearch.helpers import bulk
from pocket import pocket

# MySQL 연결 정보 설정
info = pocket()
mysql_host =  info.mysql_host
mysql_port = info.mysql_port
mysql_user = info.mysql_user
mysql_password = info.mysql_password
mysql_database = 'baro_grim_practice'

# Elasticsearch 연결 정보
es_host = info.es_host
es_port = info.es_port
es_username = info.es_username
es_password = info.es_password

# MySQL 데이터 가져오기
def get_data_from_mysql():
    connection = mysql.connector.connect(
        host=mysql_host,
        port = mysql_port,
        user=mysql_user,        
        password=mysql_password,
        database=mysql_database
    )

    query = f"SELECT * FROM IMAGE;"
    cursor = connection.cursor()
    cursor.execute(query)

    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return data

# Elasticsearch에 bulk로 데이터 색인
def index_data_to_elasticsearch(data):
    # TLS 설정을 위한 SSLContext 생성
    # ssl_context = ssl.create_default_context(cafile=ca_certs)

    # Elasticsearch 클라이언트 생성
    es = Elasticsearch(
        [f"{es_host}:{es_port}"],
        http_auth=(es_username, es_password),
        scheme="http",
        # connection_class=RequestsHttpConnection,
        # ssl_context=ssl_context
    )

    # Elasticsearch에 저장할 데이터 변환 (index와 id 필드가 있는 dict 형태로 변환)
    actions = [
        {
            "_index": "test_image-2",
            "_id": doc["file_link"],
            "_source": doc
        }
        for doc in data
    ]

    # Elasticsearch에 bulk 색인 실행
    bulk(es, actions)

if __name__ == "__main__":
    data_from_mysql = get_data_from_mysql()
    index_data_to_elasticsearch(data_from_mysql)

