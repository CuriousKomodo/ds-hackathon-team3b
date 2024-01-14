import pickle
import json
from datetime import datetime


class PageItem:
    """
    This data class is the output of direct extraction from Confluence API.
    Each page item contains the title of the incident report, the date of creation,
    and the html of the confluence page.
    """
    def __init__(self, id: str, html: str, title: str, creation_date: datetime = None):
        self.id = id
        self.html = html
        self.title = title
        self.creation_date = creation_date
    def save(self, save_dir: str, format: str ='pickle'):
        assert format in ['pickle', 'json'], 'Format must be in pickle or json'
        if format == 'pickle':
            with open(f'{save_dir}/{self.id}.pkl') as f:
                pickle.dump(self.__dict__, f, 'wb')
        else:
            with open(f'{save_dir}/{self.id}.json') as f:
                json.dump(self.__dict__, f)
