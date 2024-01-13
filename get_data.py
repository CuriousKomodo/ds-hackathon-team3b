import os

import requests
from pprint import pprint
from authentication import authenticate

"""Fetch all the child ids given the parent incident page, 
then fetch the content from each child page"""

api_token = os.getenv('API_TOKEN')
email = os.getenv('EMAIL')
headers = authenticate(email, api_token)

base_url = 'https://transferwise.atlassian.net/wiki'
page_id = "2740585401"  # This is the incident parent page for 2023

def _get_child_ids_from_response(child_page_results):
    child_ids = []
    for page in child_page_results:
        link = page['_links'].get('self')
        child_id = link.split('/')[-1]
        child_ids.append(child_id)
    child_ids = list(set(child_ids))
    return child_ids

def get_ids_of_all_child_page_ids(page_id):
    child_ids_all = []

    base_url = 'https://transferwise.atlassian.net/wiki'

    for i in range(4):
        url = f'{base_url}/rest/api/content/{page_id}/child/page?start={i*1000}&limit={(i+1)*1000}'
        response = requests.get(
            url,
            headers=headers,
        )
        if response.status_code == 200:
            child_page_results = response.json()['results']
            child_ids = _get_child_ids_from_response(child_page_results)
            child_ids_all += child_ids
        else:
            print(f"Failed to retrieve page - at pagination {i}:", response.status_code)
    print('Total number of child pages:', len(child_ids_all))
    return child_ids_all

if __name__ == '__main__':
    get_ids_of_all_child_page_ids(page_id)
