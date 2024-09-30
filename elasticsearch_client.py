from elasticsearch import Elasticsearch
import uuid as uuid_lib
from elasticsearch.helpers import bulk
from config import settings
import logging
class ElasticSearchClient:
    def __init__(self):
        self.client = None
        
    
    def connect(self):
        try:
            self.client = Elasticsearch([{'host': str(settings.ELASTICSEARCH_HOST), 
                                          'port': int(settings.ELASTICSEARCH_PORT), 
                                          'scheme':'http'}], request_timeout=60)
            logging.info("Elasticsearch успешно подключен")
        except Exception as e:
            self.client = None
            logging.error(f"Ошибка подключения к Elasticsearch: {e}")
    
    def load_data_to_elasticsearch(self, data_generator):
        if self.client is None:
            logging.info("Подключение к Elasticsearch")
            self.connect() 
        
        for batch in data_generator:
            actions = [
                {
                    "_index": "sku_index",
                    "_id": uuid,
                    "_source": {
                        "category_id": category_id,
                        "title": title,
                        "price_before_discounts": price_before_discounts,
                        "currency": currency,
                        "description": description
                    }
                }
                for uuid, category_id, title, price_before_discounts, currency, description in batch
            ]
            logging.info(self.client)
            bulk(self.client, actions)
        logging.info("Данные успешно загружены в Elasticsearch")
        
    def find_similar_objects(self, uuid, title):
        if self.client is None:
            self.connect()
        query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "more_like_this": {
                            "fields": ["title"],
                            "like": [
                                {
                                    "_index": 'sku_index',
                                    "_id": str(uuid)
                                }
                            ],
                            "min_term_freq": 1,
                            "max_query_terms": 12,
                            "minimum_should_match": "30%",
                            "boost": 1
                        }
                    }
                ],
                "must_not": [
                    {
                        "term": {
                            "title": "none"
                        }
                    }
                ]
            }
        },
        "size": 6
    }

        response = self.client.search(index="sku_index", body=query)
        hits = response['hits']['hits']

        # Удаляем сам объект из результатов
        similar_objects = [uuid_lib.UUID(hit['_id']) for hit in hits if hit['_id'] != uuid][:5]

        return similar_objects
    
    