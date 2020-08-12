import json
import requests
from config import my_proxy


def write_to_json(the_list: str, path: str) -> str:
    """
    The purpose of this function is the write knowbe4 data to a json file dynamically.
    :param the_list: This parameters is the knowbe4 data that will be written to the json file.
    :param path: This parameter is the path the knowbe4 data will be written to.
    """
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(the_list, file, ensure_ascii=False, indent=1, sort_keys=False, default=str)


def get_total_pages(the_url: str, api_header: str) -> str:
    """
    This function dynamically gets the total number of pages in an endpoint so we can dynamically get the range for\
    each endpoint.
    :param the_url: The URL of the specific knowbe4 endpoint
    :param api_header: The knowbe4 API header that will be used (API_KEY needed)
    :return: The total number of pages that the endpoint has...(100 per page)
    """
    new = []
    for i in range(1, 5000):
        s = requests.Session()
        s.proxies = my_proxy
        resp = s.get(the_url+"?page={0}".format(i), headers=api_header,
                     verify=False).json()
        if not resp:
            new.extend(str(i))
            break
    total_pages = int(new[0])
    return total_pages

'''
def get_id_total_pages(the_url: str, api_header: str, objj=None) -> str:
    """
    This function dynamically gets the total number of pages in an endpoint so we can dynamically get the range for\
    each endpoint.
    :param objj:
    :param the_url: The URL of the specific knowbe4 endpoint
    :param api_header: The knowbe4 API header that will be used (API_KEY needed)
    :return: The total number of pages that the endpoint has...(100 per page)
    """

    for obj in objj:
        new = []
        for i in range(1, 5000):
            s = requests.Session()
            s.proxies = my_proxy
            resp = s.get(the_url+"{0}/recipients?page={1}".format(obj, i), headers=api_header,
                         verify=False).json()
            if not resp:
                new.extend(str(i))
                break
        total_pages = int(new[0])
        return total_pages
'''