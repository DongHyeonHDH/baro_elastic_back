from azure.cosmos import CosmosClient, exceptions, PartitionKey
from datetime import datetime

class Cosmosup():
    # Azure Cosmos DB 연결 설정
    url = "https://connect-for-elastic.documents.azure.com:443/"
    key = "S2e2NB7mjEXpclCrehdpZz9P996LFDWFMCEFrjGoh6Q5jvXUWmTLkKNQ0TT9QWauetGN6lG4Wg6ZACDbLTZ0Uw=="

    client = CosmosClient(url, credential=key)
    database_name = "baro_test"
    container_name = "cosmos"

    # 데이터 읽기
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    @staticmethod
    def data_delete(document_id_to_delete):
        try:
            item = Cosmosup.container.read_item(item=document_id_to_delete, partition_key=document_id_to_delete)
            Cosmosup.container.delete_item(item, partition_key=document_id_to_delete)
            print(f"Item with ID '{document_id_to_delete}' deleted successfully.")
        except exceptions.CosmosHttpResponseError as e:
            if e.status_code == 404:
                print(f"Item with ID '{document_id_to_delete}' not found.")
            else:
                raise

    @staticmethod
    def data_insert(new_item):
        Cosmosup.container.upsert_item(new_item)
        print("Item inserted or updated")

    @staticmethod
    def show_data(query):
        items = Cosmosup.container.query_items(query, enable_cross_partition_query=True)
        for item in items:
            print(item)

if __name__ == "__main__":
    cosmos = Cosmosup()
    
    # Create a new Cosmos DB database and container if they don't exist
    cosmos.client.create_database_if_not_exists(id=cosmos.database_name)
    cosmos.database.create_container_if_not_exists(id=cosmos.container_name, partition_key=PartitionKey(path="/partitionKey"))
    
    dt = datetime.now()
    new_item = {
        "id": "1",  # You can use a unique identifier as the item ID
        "image_id": "1",
        "prompt": "john",
        "negative_prompt": "done",
        "prompt_time": dt.strftime("%Y-%m-%d %H:%M:%S")
    }

    cosmos.data_insert(new_item)

    query = "SELECT * FROM c"
    cosmos.show_data(query)
