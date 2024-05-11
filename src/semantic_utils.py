import time

import requests
from semanticscholar import SemanticScholar

# set client
sch = SemanticScholar()

endpoint = "https://api.semanticscholar.org/graph/v1/paper/"
params = {"fields": "title,tldr,abstract"}


def title_tldr_and_abstract(arxiv_url):

    # get arxiv_id
    arxiv_id = arxiv_url.split("/")[-1]

    # request details of the paper
    result = requests.get(endpoint + "ARXIV:" + arxiv_id, params=params)
    while result.status_code != 200:
        time.sleep(5)
        print("request")
        result = requests.get(endpoint + "ARXIV:" + arxiv_id, params=params)

    # return results
    result = result.json()
    return result["title"], result["tldr"]["text"], result["abstract"]
