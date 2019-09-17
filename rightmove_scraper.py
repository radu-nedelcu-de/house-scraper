import json
import math
import re
import time
from random import randint

import requests
import io

from fake_useragent import UserAgent
from lxml import etree


def scrape_individual_house(domain, house_url):
    house_html = get_page(domain + house_url)
    house_parser = etree.HTMLParser()
    house_tree = etree.parse(io.StringIO(house_html.text), house_parser)

    key_features_text = house_tree.xpath(
        'string(//ul[@class="list-two-col list-style-square"])'
    )

    full_description_text = house_tree.xpath(
        'string(//p[@itemprop="description"])'
    )

    long_price = house_tree.xpath(
        'string(//p[@id="propertyHeaderPrice"])'
    )

    found_price = re.findall("(?<=£)(\d+,\d+)", long_price)

    if isinstance(found_price, list) and len(found_price) > 0:
        # remove the comma
        price = int(found_price[0].replace(',', ''))
    else:
        price = None

    stations_list = []

    for li_tag in house_tree.xpath(
        '//ul[@class="stations-list"]/li'
    ):
        new_station = {
            'station_name': li_tag.xpath('span/text()')[0],
            'distance': float(li_tag.xpath('small/text()')[0][1:-4])
        }

        if new_station not in stations_list:
            stations_list.append(new_station)

    images = []
    for media in house_tree.xpath(
        '//meta[@itemprop="contentUrl"]/@content'
    ):
        images.append(media)

    property_data = {
        'url': domain + house_url,
        'price': price if price is not None else 0,
        'key_features_text': key_features_text,
        'full_description_text': full_description_text,
        'stations_list': stations_list,
        'timestamp': time.time(),
        'images': images
    }

    return property_data


# Gather list of results for an individual station.
def get_results_pages(domain, results_url):
    results_pages = []
    results_url = domain + results_url
    html = get_page(results_url)

    parser = etree.HTMLParser()
    tree = etree.parse(io.StringIO(html.text), parser)

    number_of_results_str = tree.xpath('//span[@class="searchHeader-resultCount"]/text()')
    number_of_results = int(number_of_results_str[0])
    # is there any point in scraping this at all?
    if number_of_results != 0:
        number_of_pages = math.ceil(number_of_results / 24)

        # add the first page to scrape
        results_pages.append(results_url)

        number_of_results_per_page = 24

        for page in range(1, number_of_pages):
            # 24 result per page
            number_of_results = page * number_of_results_per_page
            results_link = results_url + f"&index={number_of_results}"
            results_pages.append(results_link)

    return results_pages


def get_page(results_url):
    time.sleep(randint(3, 15))
    ua = UserAgent()
    html = requests.get(results_url, headers={'User-Agent': str(ua.random)})
    return html


def get_individual_house_links(domain, results_url):
    html = get_page(results_url)
    parser = etree.HTMLParser()
    tree = etree.parse(io.StringIO(html.text), parser)
    house_links = tree.xpath('//a[@class="propertyCard-link"]/@href')
    # remove duplicates and empty data
    house_links = set([house_link for house_link in house_links if house_link != ''])
    return domain, house_links


def get_station_based_initial_search_urls(max_days: int, stations_list):
    min_price = 200000
    max_price = 375000
    min_bedrooms = 1
    radius_miles = 1.0

    domain = 'http://www.rightmove.co.uk'
    initial_search_urls = []

    with open(stations_list) as stations_file:
        stations_list = json.load(stations_file)

    for station in stations_list:
        if station['code']:
            print('Scraping %s' % station['name'])
            station_id = station['code']

            initial_search_url = \
                f'/property-for-sale/find.html' \
                f'?locationIdentifier=STATION%{station_id}' \
                f'&minPrice={min_price}' \
                f'&maxPrice={max_price}' \
                f'&minBedrooms={min_bedrooms}' \
                f'&displayPropertyType=' \
                f'&oldDisplayPropertyTypes' \
                f'&radius={radius_miles}' \
                f'&dontShow=retirement%2CsharedOwnership' \
                f'&maxDaysSinceAdded={max_days}'

            initial_search_urls.append(initial_search_url)

    return domain, initial_search_urls


if __name__ == '__main__':
    # domain, initial_search_urls = get_station_based_initial_search_urls(1)
    # for initial_search_url in initial_search_urls:
    #     results_pages = get_results_pages(domain, initial_search_url)
    #     for results_page in results_pages:
    #         domain, individual_house_links = get_individual_house_links(domain, results_page)
    #         for house_link in individual_house_links:
    #             property_data = scrape_individual_house(domain, house_link)
    #             db_manager = DbManager()
    #             db_manager.add_new_property(property_data)
    #
    # send_results()
    scrape_individual_house('http://www.rightmove.co.uk', '/property-for-sale/property-70852871.html')
