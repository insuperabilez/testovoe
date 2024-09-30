from postgres_client import PostgresClient
from elasticsearch_client import ElasticSearchClient
import psycopg2.extras
import xml.etree.ElementTree as ET
import uuid
import argparse
import logging
import time

logging.basicConfig(level=logging.INFO)

def parse_yml(file_path, batch_size=1000):
    context = ET.iterparse(file_path, events=("start", "end"))
    context = iter(context)
    event, root = next(context)
    batch = []

    for event, elem in context:
        if event == "end" and elem.tag == "offer":
            offer_data = {
                'uuid': str(uuid.uuid4()),
                'marketplace_id': 1,  #  
                'product_id': elem.get('id') if elem.get('id') is not None else None,
                'title': elem.find('name').text if elem.find('name') is not None else None,
                'description': elem.find('description').text if elem.find('description') is not None else None,
                'brand': elem.find('vendor').text if elem.find('vendor') is not None else None,
                'seller_id': 1,  #  
                'seller_name': 'Example Seller',  #  
                'first_image_url': elem.find('picture').text if elem.find('picture') is not None else None,
                'category_id': elem.find('categoryId').text if elem.find('categoryId') is not None else None,  #  
                'category_lvl_1': None,
                'category_lvl_2': None,
                'category_lvl_3': None,
                'category_remaining': None,
                'features': {},  #  
                'rating_count': 0,  #  
                'rating_value': 0.0,  #  
                'price_before_discounts': float(elem.find('price').text) if elem.find('price') is not None else None,
                'discount': 0.0,  #  
                'price_after_discounts': float(elem.find('price').text) if elem.find('price') is not None else None,
                'bonuses': 0,  #  
                'sales': 0,  #  
                'currency': elem.find('currencyId').text if elem.find('currencyId') is not None else None,
                'barcode': elem.find('barcode').text if elem.find('barcode') is not None else None,  #  
                'similar_sku': []  #  
            }
            batch.append(offer_data)
            root.clear()  # Освобождаем память

            if len(batch) >= batch_size:
                yield batch
                
                batch = []

    if batch:
        logging.info('xml файл обработан')
        yield batch
        


def main():
    parser = argparse.ArgumentParser(description="Process XML data and load it to PostgreSQL and/or Elasticsearch.")
    parser.add_argument('--load_to_postgres', type=int, default=1, help="Load data to PostgreSQL")
    parser.add_argument('--load_to_elastic', type=int, default=1, help="Load data to Elasticsearch")
    parser.add_argument('--file_size', type=str, default='5k', help="Size of the XML file to process")
    parser.add_argument('--find_similar', type=int, default=1, help="Find similar objects in ElasticSearch")
    args = parser.parse_args()
    logging.info(args)
    psycopg2.extras.register_uuid()

    if args.file_size == '5k':
        file_path = '5k.xml'
    else:
        file_path = '50k.xml'

    batch_size = 1000

    postgres_client = PostgresClient()
    elasticsearch_client = ElasticSearchClient()

    if args.load_to_postgres or args.find_similar or args.load_to_elastic:
        postgres_client.connect()
        time.sleep(10)
        
    if args.load_to_postgres:
        #парсим и загружаем в postgres
        
        for batch in parse_yml(file_path, batch_size):
            postgres_client.load_data_to_postgresql(batch)

    if args.load_to_elastic or args.find_similar: 
        elasticsearch_client.connect()
        time.sleep(10)

    if args.load_to_elastic:
        #загружаем в elasticsearch
        
        data = postgres_client.fetch_data_from_postgresql(batch_size)
        elasticsearch_client.load_data_to_elasticsearch(data)
    
    if args.find_similar:
        data = postgres_client.fetch_data_for_similarity(batch_size)
        i=1
        for batch in data:
            for uuid, title in batch:
                if i%500==0:
                    logging.info(f"Обработано {i} объектов")
                if title is None:
                    title = ""
                similar_objects = elasticsearch_client.find_similar_objects(uuid, title)
                postgres_client.update_similar_sku_in_postgresql(uuid, similar_objects)
                if i==1:
                    logging.info(f"Объект с UUID {uuid} имеет следующие похожие объекты: {similar_objects}")
                i+=1
        postgres_client.close()
if __name__ == "__main__":
    main()