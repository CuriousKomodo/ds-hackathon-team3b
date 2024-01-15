import pickle
import json
from datetime import datetime

from utils.get_text import text_from_html


class PageItem:
    """
    This pickle_data class is the output of direct extraction from Confluence API.
    Each page item contains the title of the incident report, the date of creation,
    and the html of the confluence page.
    """
    def __init__(self, id: str, postmortem_id: str, html: str, title: str, creation_date: datetime = None):
        self.id = id
        self.postmortem_id = postmortem_id
        self.html = html
        self.title = title
        self.creation_date = creation_date
        self.text = self.obtain_text()  # Not needed anymore
    def obtain_text(self):
        """Meant to parse only visible string from the html, not needed anymore because
        the html body returned by the API is clean, and give good strutural info about the page"""
        text = ''
        try:
            text = text_from_html(self.html)
        except:
            print(f'Error getting visible text from page with id: {self.id}')
        return text
    def save(self, save_dir: str, format: str ='pickle', html_only:bool =True):
        assert format in ['pickle', 'json'], 'Format must be in pickle or json'
        if format == 'pickle':
            if html_only:
                with open(f'{save_dir}/{self.postmortem_id}.pkl', 'wb') as handle:
                    pickle.dump(self.html, handle, protocol=pickle.HIGHEST_PROTOCOL)
            else:
                with open(f'{save_dir}/{self.postmortem_id}.pkl', 'wb') as handle:
                    pickle.dump(self.__dict__, handle, protocol=pickle.HIGHEST_PROTOCOL)

        elif format == 'json':
            json_object = json.dumps(self.__dict__, indent=4)
            with open(f'{save_dir}/{self.postmortem_id}.json', 'w') as handle:
                handle.write(json_object)


