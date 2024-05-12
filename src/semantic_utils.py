import time

import requests

# endpoint and default params
endpoint = "https://api.semanticscholar.org/graph/v1/paper/"
params = {"fields": "title,tldr,abstract,authors"}


def paper_informations(arxiv_url, item=params, tries=20, interval=3):
    """
    take paper informations about arxiv_url
    If you cannot take information within 60 seconds, raise TimeoutError

    Args:
        arxiv_url (str): url in arXiv of paper
        param (dict): items which you want to know
    """

    # get arxiv_id
    arxiv_id = arxiv_url.split("/")[-1]

    # request details of the paper
    result = requests.get(endpoint + "ARXIV:" + arxiv_id, params=item)
    request_time = 0

    # request some times until take information
    while result.status_code != 200:
        if request_time > tries:
            raise TimeoutError("cannot connect to semantic scholar")

        print(str(request_time + 1) + "th request for Semantic Scholar is failed. Bot will re-request soon.")
        time.sleep(interval)
        result = requests.get(endpoint + "ARXIV:" + arxiv_id, params=params)
        request_time += 1

    # return results
    return result.json()
