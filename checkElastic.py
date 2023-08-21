from elasticsearch import Elasticsearch
from pocket import pocket

# Elasticsearch 연결 정보
info = pocket()
es_host = info.es_host
es_port = info.es_port
es_username = info.es_username
es_password = info.es_password

es = Elasticsearch(
    [f"{es_host}:{es_port}"],
    basic_auth=(es_username, es_password)    
)

# 매핑 정보 조회 함수 정의
def get_mapping(index_name):
    response = es.indices.get_mapping(index=index_name)
    return response

# 인덱스 이름 설정
index_name = "test_image_prompt"  # 실제 인덱스 이름으로 변경

# 매핑 정보 조회
# mapping_info = get_mapping(index_name)
# 매핑 정보 출력
# print(mapping_info)
def search_with_filter_query(index_name, field_name, query_text):
    query = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        field_name: query_text
                    }
                }
            }
        }
    }
    response = es.search(index=index_name, body = query, timeout="60s")
    return response["hits"]["hits"]


field_to_search = "prompt"  # 검색할 필드 이름
query_text = "red"       # 검색할 텍스트

results = search_with_filter_query(index_name, field_to_search, query_text)
for result in results:
    print(result)

# 클라이언트의 기본 타임아웃 확인
# default_timeout = es.transport.options.timeout
# print("Default Timeout:", default_timeout)