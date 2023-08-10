import mysql.connector
from elasticsearch import Elasticsearch 
from pocket import pocket

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
    es = Elasticsearch(
        [f"{es_host}:{es_port}"],
        http_auth=(es_username, es_password),
        scheme="http"        
    )
    
    #frequency 담을 dictionary 생성
    term_freq_dic ={}

    mterm_body = [
        {
            "_index": "test_image-2",
            "_id": doc["file_link"],         
            "fields": ["prompt"]            
        }
        for doc in data
    ]
   

    response = es.mtermvectors(        
       body ={
            "docs": mterm_body,
            "parameters": {
                "fields": ["prompt"]
            }
        }
    )    

    # Elasticsearch에 mtermvectors 실행
    if 'docs' in response:
        for doc in response['docs']:
            if 'term_vectors' in doc:
                term_vectors = doc['term_vectors']
                if "prompt" in term_vectors:
                    # 역색인 정보를 사용하여 원하는 작업을 수행합니다.
                    print(f"Document ID: {doc['_id']}")
                    for term, info in term_vectors["prompt"]['terms'].items():                                                                  
                        if term in term_freq_dic:
                            temp = term_freq_dic.get(term)
                            term_freq_dic[term] = temp + info['term_freq']
                        else:
                            if isinstance(term,float) == True:
                                continue
                            elif isinstance(term, int) == True:
                                continue
                            else:                                
                                term_freq_dic[term] = info['term_freq']                                             
                                                   
            else:
                print(f"No term vectors found for Document ID: {doc['_id']}")        
    else:
        print("No documents found.")

    # for t, val in term_freq_dic.items():
    #     print(f"Term: {t}, Frequency: {val}")
    # frequency 값을 기준으로 딕셔너리를 빈도 값이 높은 순으로 정렬합니다.
    sorted_frequency = sorted(term_freq_dic.items(), key=lambda x: x[1], reverse=True)
    print(len(term_freq_dic.keys()))
    # 상위 100개의 아이템을 출력합니다.
    top_100_items = sorted_frequency[:50]    
    print(top_100_items)

    
    

if __name__ == "__main__":    
    data=get_data_from_mysql()
    index_data_to_elasticsearch(data)