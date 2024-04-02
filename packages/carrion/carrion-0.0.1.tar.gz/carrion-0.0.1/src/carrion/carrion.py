import argparse
import colorlog
import csv
import json
import logging
import lxml
import requests
import condor_secrets
import sys
import time
import umpyutl as umpy
import souper as soup

from argparser import create_parser
from bs4 import BeautifulSoup
from datetime import datetime as dt
from datetime import timezone as tz
from logger import create_logger
from pathlib import Path
from scholarly import scholarly
from typing import Any  # had to add this to use Any in typehinting
from urllib.parse import urlencode


BASE_URL: str = "https://scholar.google.com"


def build_url(value: str) -> Path:
    """TODO"""

    return Path(BASE_URL).joinpath(value)


def retrieve_citation(html: str) -> dict:
    """Return citation attributes from passed-in <html>.

    Parameters:
        html (str): chunk of HTML

    Returns:
        dict: dictionary representation of a citation
    """
    # author_affiliations = []
    # for author in select_value_by_key(html.select(".gs_a a"), "href"):
    # author_affiliations.append(author)

    return {
        "title": html.select_one(".gs_rt").text,
        "title_url": select_value_by_key(html.select_one(".gs_rt a"), "href"),
        "pub_info": html.select_one(".gs_a").text,
        "author_affiliation": select_value_by_key(html.select(".gs_a a"), "href"),
        "snippet": html.select_one(".gs_rs").text,
        # "cited_by": select_value_by_key(html.select_one("#gs_res_ccl_mid .gs_nph+ a"), "href"),
        "pdf_url": select_value_by_key(html.select_one(".gs_or_ggsm a:nth-child(1)"), "href"),
        # "related_articles": select_value_by_key(result.select_one("#gs_res_ccl_mid .gs_nph+ a+ a"), "href"),
    }


def select_value_by_key(selector: Any, key: str) -> str:
    """Return a value from a selector object.

    Parameters:
        selector (Any): selector object
        key (str): key to retrieve

    Returns:
        str: value associated with key
    """

    try:
        return selector[key]
    except (KeyError, TypeError):
        return None


def get_links(base_url, params, offset: int, limit: int) -> list:
    """TODO"""
    urls = []
    for i in range(limit):  # need to integrate offset as starting point of range limit
        urls.append(f"{base_url}/scholar?start={i}&q=UMMZ+bird&hl=en&as_sdt=0,23")


def run_async_job(url, json, timeout=10, call_interval=5, max_calls=1000) -> dict:
    # url is scraperapi url, built url is in json
    """TODO"""

    response: requests.Response = requests.post(url=url, json=json, timeout=timeout)
    response.raise_for_status()
    data: dict | list = response.json()
    status: str = data["status"]
    status_url: str = data["statusUrl"]

    calls: int = 0
    while not status == "finished" and calls < max_calls:
        time.sleep(call_interval)
        response: requests.Response = requests.get(status_url, timeout=timeout)
        response.raise_for_status()
        data: dict = response.json()
        status = data["status"].lower()
        calls += 1
    return data

def retrieve_author_links(base_url: str, tag) -> list:
    """Return author citation links from passed-in bs4.Tag object.

    Parameters:
        html (bs4.Tag): Tag object

    Returns:
        list: sequence of author dictionaries
    """

    return [
        {"author_name": element.text, "url_fragment": f"{base_url}{element.get('href')}"}
        for element in tag.find_all("a", href=True)
    ]


def main() -> None:
    """Orchestrates program workflow.

    Parameters:
        None

    Returns:
        None
    """

    # https://scholar.google.com/scholar?start=10&q=UMMZ+bird&hl=en&as_sdt=0,23
    # with date: https://scholar.google.com/scholar?q=UMMZ%2Baves&hl=en&as_sdt=0%2C23&as_ylo=1970&as_yhi=1990

    color_format = (
        "%(log_color)s%(levelname)s%(reset)s: %(blue)s%(filename)s:%(lineno)s%(reset)s |"
        " %(process)d | %(log_color)s%(message)s%(reset)s"
    )
    format = "%(levelname)s: %(message)s"
    filepath = (
        Path(__file__).parent.absolute().joinpath("condor_log_scraperAPI").with_suffix(".log")
    )
    print(f"\nfilepath={filepath}")
    logger = create_logger(filepath, format, color_format=color_format)

    logger.info(f"Run starting {dt.now().isoformat()}.")

    parser = create_parser("Condor (Scraper API)")
    args = parser.parse_args()

    citations: list = []
    authors: list = []
    # TODO: Add offset
    limit: int = args.limit
    query: str = args.query
    offset: int = args.offset
    start: int = args.start
    end: int = args.end

    for i in range(offset, limit):
        params: dict = {"start": i, "q": query, "hl": "en", "as_sdt": "0, 23", "as_ylo": start, "as_yhi": end}
        gs_url: str = f"{BASE_URL}/scholar" + "?" + urlencode(params)
        json = {
            'apiKey': condor_secrets.SCRAPERAPI_KEY,
            'url': gs_url
         }
        scraper_url = "https://async.scraperapi.com/jobs"

        data = run_async_job(scraper_url, json)
        umpy.write.to_json("scraperapi_{i}.json", data)

        html: str = data["response"]["body"]
        filename: str = f"{query}-html-{i}-{dt.now().strftime('%Y%m%dT%H%M')}.html"
        filepath: str = Path(__file__).parent.absolute().joinpath("output", filename)
        print(f"\nfilepath={filepath}")
        umpy.write.to_txt(filepath, [html])

        # authors.extend(retrieve_author_links(BASE_URL, html.find("div", {"class": "gs_a"})))

        citations.extend(soup.SoupScraper(BASE_URL, html).scrape())
        for citation in citations:
            author_links = citation.get("author_links", [])

            if author_links:
                for author_link in author_links:
                    if "author_name" in author_link and author_link["author_name"]:
                        name = author_link["author_name"]
                        if name not in authors:
                            authors.append(name)
        logger.info(f"Citation successfully retrieved and appended to list.")

    logger.info(f"Starting scholarly search.")

    # for name in authors:
    #     print(f"\nauthor={name}")
    #     try:
    #         search_query = scholarly.search_author(name)
    #         author_data = next(search_query)
    #         scholarly.fill(author_data, sections=['basic'])
    #         print(f"\nauthor={name}")
    #         scholar_id = author_data['scholar_id']
    #         filename: str = f"condor-author-{scholar_id}-{dt.now().strftime('%Y%m%dT%H%M')}.json"
    #         filepath: str = Path(__file__).parent.absolute().joinpath("output", filename)
    #         print(f"\nfilepath={filepath}")
    #         umpy.write.to_json(filepath, author_data)
    #     except StopIteration:
    #         logger.info(f"Author not found: {name}")
    #         continue
    #     except Exception as e:
    #         logger.error(f"Error retrieving author: {name} | {e}")
    #         continue

    all_authors_data = []  # List to store all authors' data
    unique_author_ids = set()  # Set to store unique author IDs

    for author_name in authors:
        try:
            search_query = scholarly.search_author(author_name)
            author = next(search_query)
            scholarly.fill(author, sections=['basic'])

        # Check for duplicates based on author ID
            if author['scholar_id'] not in unique_author_ids:
                all_authors_data.append(author)
                unique_author_ids.add(author['scholar_id'])
            else:
                print(f"Duplicate author found and skipped: {author_name}")
        except StopIteration:
            print(f"Author not found: {author_name}")
            continue
        except Exception as e:
            print(f"Error retrieving author: {author_name} | {e}")
            continue

# Write all authors' data to a single JSON file
    filename = f"./output/{query}-{start}-{end}-authors{dt.now().strftime('%Y%m%dT%H%M')}.json"

    umpy.write.to_json(filename, all_authors_data)

    print(f"All authors' data have been written to {filename}")

    logger.info(f"Run ending {dt.now().isoformat()}.")

    # print(f"\ncitation = {citations}")
    filename: str = f"{query}-{start}-{end}-{dt.now().strftime('%Y%m%dT%H%M')}-{limit}.json"
    filepath: str = Path(__file__).parent.absolute().joinpath("output", filename)
    print(f"\nfilepath={filepath}")
    umpy.write.to_json(filepath, citations)
    logger.info(f"Citations written to {filepath}.")

    logger.info(f"Saving authors to file.")

    filename: str = f"condor-authors-{start}-{end}-{dt.now().strftime('%Y%m%dT%H%M')}.csv"
    filepath: str = Path(__file__).parent.absolute().joinpath("output", filename)
    print(f"\nfilepath={filepath}")
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for author in authors:
            writer.writerow([author])

    logger.info(f"Authors written to {filepath}.")

if __name__ == "__main__":
    main()
