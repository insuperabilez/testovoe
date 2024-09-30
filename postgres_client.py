import xml.etree.ElementTree as ET
import psycopg2
import json
from config import settings
import logging
class PostgresClient:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=settings.POSTGRES_DB,
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
                host=settings.POSTGRES_HOST,
                port=settings.POSTGRES_PORT
            )
            self.cursor = self.conn.cursor()
            logging.info("Postgres успешно подключен")
        except Exception as e:
            self.conn = None
            self.cursor = None
            logging.error(f"Ошибка подключения к Postgres: {e}")

    def close(self):
        if self.conn is not None:
            self.cursor.close()
            self.conn.close()
            logging.info("Postgres успешно отключен")

    def load_data_to_postgresql(self,offers):
        if self.conn is None:
            self.connect()
        
        for offer in offers:
            self.cursor.execute("""
                INSERT INTO sku (
                    uuid, marketplace_id, product_id, title, description, brand, seller_id, seller_name,
                    first_image_url, category_id, category_lvl_1, category_lvl_2, category_lvl_3,
                    category_remaining, features, rating_count, rating_value, price_before_discounts,
                    discount, price_after_discounts, bonuses, sales, currency, barcode, similar_sku
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                offer['uuid'], offer['marketplace_id'], offer['product_id'], offer['title'], offer['description'],
                offer['brand'], offer['seller_id'], offer['seller_name'], offer['first_image_url'], offer['category_id'],
                offer['category_lvl_1'], offer['category_lvl_2'], offer['category_lvl_3'], offer['category_remaining'],
                json.dumps(offer['features']), offer['rating_count'], offer['rating_value'],
                offer['price_before_discounts'], offer['discount'], offer['price_after_discounts'], offer['bonuses'],
                offer['sales'], offer['currency'], offer['barcode'], offer['similar_sku']
            ))

        self.conn.commit()
        
        logging.info("Часть данных успешно загружена в Postgres")

    def fetch_data_from_postgresql(self,batch_size=1000):
        if self.conn is None:
            self.connect()
        
        self.cursor.execute("""
            SELECT uuid, category_id, title, price_before_discounts, currency, description
            FROM sku;
        """)

        while True:
            batch = self.cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

        logging.info("Данные успешно получены из Postgres")
    def update_similar_sku_in_postgresql(self, uuid, similar_objects):
        if self.conn is None:
            self.connect()
        uuid = str(uuid) 
        self.cursor.execute("""
            UPDATE sku
            SET similar_sku = %s
            WHERE uuid = %s;
        """, (similar_objects, uuid))

        self.conn.commit()
        

    def fetch_data_for_similarity(self,batch_size=1000):
        if self.conn is None:
            self.connect()
        
        self.cursor.execute("""
            SELECT uuid, title
            FROM sku;
        """)

        while True:
            batch = self.cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
        logging.info("Данные успешно получены из Postgres")
