import json
import requests
from config import configs
from datetime import datetime
from models import write_to_json, get_total_pages, get_id_total_pages
import time
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging

logging.basicConfig(level=logging.DEBUG)

current_date = datetime.now().strftime("%Y%m%d-%H%M%S")

header = {"Authorization": "




def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_all_psts():
    all_psts = []
    for i in range(1, 3):
        s = requests.Session()
        #s = requests.Session()
        s.proxies = {"ht
        resp = s.get("https://us.api.knowbe4.com/v1/phishing/security_tests?page={0}".format(i), headers=header,
                     verify=False).json()
        full_psts = [item['pst_id'] for item in resp]
        all_psts.extend(full_psts)
    return all_psts


# For each pst, get pst recipients
def load_data(pst_list):
    pst_rec_list = []
    print(len(pst_list))
    t0 = time.time()
    s = requests.Session()
    s.proxies = {"http": 

    for obj in pst_list:
        for i in range(1, 1000):
            try:
                response = requests_retry_session(session=s).get(rec_url+'{0}/recipients?page={1}'.format(obj, i),
                                                                 headers=header, verify=False)
                resp = response.json()
            except Exception as e:
                print('It failed :(', e.__class__.__name__)
            else:
                print('It eventually worked', response.status_code)
                if resp:
                    pst_rec_list.extend(resp)
                elif not resp:
                    print("Should stop and go to next object")
                    break
            finally:
                t1 = time.time()
                print('Took', t1 - t0, 'seconds')

    print(len(pst_rec_list))
    print('printing to json file')
    with open(pst_rec_path, 'w', encoding='utf-8') as file:
        json.dump(pst_rec_list, file, ensure_ascii=False, indent=1, sort_keys=False, default=str)


def main():
    pst_list = get_all_psts()
    #get_all_psts()
    load_data(pst_list)


if __name__ == '__main__':
    main()



