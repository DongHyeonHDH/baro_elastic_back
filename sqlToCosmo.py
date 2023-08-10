from azure.cosmos import CosmosClient, exceptions

# Azure Cosmos DB 연결 설정
url = "https://connect-for-elastic.documents.azure.com:443/"
key = "S2e2NB7mjEXpclCrehdpZz9P996LFDWFMCEFrjGoh6Q5jvXUWmTLkKNQ0TT9QWauetGN6lG4Wg6ZACDbLTZ0Uw=="

client = CosmosClient(url, credential=key)
database_name = "baro_test"
container_name = "test_elastic"


# 데이터 읽기
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

new_item = {
    "id": "1",
    "name": "John Doe",
    "age": 30
}

# 삭제할 데이터의 ID
document_id_to_delete = "1"

# 데이터 삭제
def data_delete(document_id_to_delete):
    try:
        item = container.read_item(item=document_id_to_delete, partition_key=document_id_to_delete)
        container.delete_item(item, partition_key=document_id_to_delete)
        print(f"Item with ID '{document_id_to_delete}' deleted successfully.")
    except exceptions.CosmosHttpResponseError as e:
        if e.status_code == 404:
            print(f"Item with ID '{document_id_to_delete}' not found.")
        else:
            raise

def data_insert(new_item):
    container.upsert_item(new_item)
    print("Item inserted or updated")


def show_data(query):    
    items = container.query_items(query, enable_cross_partition_query=True)
    for item in items:
        print(item)


if __name__ == "__main__":    
    data_delete(document_id_to_delete)
    