from celery_worker import app
import numpy as np

from db_manager import DbManager
from gmail_mail_sender import send_results, send_email
from rightmove_scraper import get_station_based_initial_search_urls, \
    scrape_individual_house, get_results_pages, get_individual_house_links


@app.task()
def main_task(max_days, stations_list, mail_list):
    properties = []
    property_urls = []
    db_manager = DbManager()
    domain, initial_search_urls = get_station_based_initial_search_urls(
        max_days,
        stations_list
    )
    for initial_search_url in initial_search_urls:
        try:
            results_pages = get_results_pages(domain, initial_search_url)
            for results_page in results_pages:
                domain, individual_house_links = get_individual_house_links(domain, results_page)
                for house_link in individual_house_links:
                    property_data = scrape_individual_house(domain, house_link)
                    db_manager.add_new_property(property_data)
                    if property_data['url'] not in property_urls:
                        properties.append(property_data)
                        property_urls.append(property_data['url'])
        except Exception as e:
            send_email(
                'error@error_email.com',
                f'An error occurred whilst scraping {initial_search_url}: {str(e)}'
            )
            pass


    help_to_buy_filters = ['new', 'luxury', 'help']
    help_to_buy_properties = []
    for item in properties:
        if any(word in item['full_description_text'] for word in help_to_buy_filters) \
            or any(word in item['key_features_text'] for word in help_to_buy_filters):
            help_to_buy_properties.append(item)
            properties.remove(item)

    data = [
        {
            'type': 'Possibly Help to Buy',
            'properties': help_to_buy_properties,
            'number_of_properties': len(help_to_buy_properties),
            'average_price': np.average([item['price'] for item in help_to_buy_properties]),
        },
        {
            'type': 'Other Properties',
            'properties': properties,
            'number_of_properties': len(properties),
            'average_price': np.average([item['price'] for item in properties]),
        }
    ]

    send_results(data, mail_list)


@app.task()
def get_station_based_initial_search_urls_task(max_days: int):
    domain, initial_search_urls = get_station_based_initial_search_urls(max_days)
    return domain, initial_search_urls


@app.task()
def get_results_pages_task(domain_result_url):
    return get_results_pages(domain_result_url)


@app.task()
def get_individual_house_links_task(results_page, domain):
    return get_individual_house_links(domain, results_page)


@app.task()
def scrape_individual_house_task(house_link, domain):
    return scrape_individual_house(domain, house_link)


@app.task()
def save_to_database_task(property_data):
    db_manager = DbManager()
    db_manager.add_new_property(property_data)


@app.task()
def send_results_task():
    send_results()


