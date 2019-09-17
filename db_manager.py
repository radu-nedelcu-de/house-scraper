import neo4j
import os
from neo4j.v1 import GraphDatabase


class DbManager(object):
    def __init__(self):
        self._driver = GraphDatabase.driver(
            f'bolt://{os.environ["NEO4J_SERVER"]}:7687',
            auth=('neo4j', 'password')
        )

    def add_new_property(
            self,
            property_data
    ):
        with self._driver.session() as session:
            result = session.run(
                """
                MERGE (property_data:PROPERTY_DATA {
                    url: {url}
                })
                ON CREATE SET property_data.key_features_text = {key_features_text}
                ON CREATE SET property_data.full_description_text = {full_description_text}
                WITH property_data 
                MERGE (price:PRICE {
                    price: {price}
                })
                WITH property_data, price
                MERGE (property_data)-[:HAS_PRICE {timestamp: {timestamp}}]->(price)
                WITH property_data, price, {stations_list} as stations_list
                UNWIND stations_list as station
                MERGE (station_data:STATION {station_name: station.station_name})
                MERGE (property_data)-[:HAS_DISTANCE {
                    distance: station.distance,
                    timestamp: {timestamp}
                
                }]->
                (station_data)
                RETURN count(*)
                """,
                property_data
            )

            if (isinstance(result, list)
                    or isinstance(result, neo4j.v1.BoltStatementResult)) \
                    and result:
                for item in result:
                    if item['count(*)'] != len(property_data['stations_list']):
                        print('Unsuccessful creation of data')
            else:
                pass


if __name__ == '__main__':
    db_manager = DbManager()
    import time
    property_data = {
        'url': 'www.test.com',
        "price": '-3',
        "key_features_text": 'test',
        "full_description_text": 'test',
        "stations_list": [{'station_name': 'test_station_2', 'distance': '-2'}],
        "timestamp": time.time()

    }
    db_manager.add_new_property(property_data)
