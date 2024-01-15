from copy import copy
from io import TextIOWrapper
from typing import Union

from bs4 import BeautifulSoup
from bs4.element import Comment

# Remove tags? Like href, title attributes
def tag_visible(element):
    if element.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if not element.parent:
        return False
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body: Union[str, TextIOWrapper], keep_imporant_tags:bool =False):
    soup = BeautifulSoup(body, 'html.parser')
    el_with_texts = soup.findAll(string=True)
    el_with_visible_texts = filter(tag_visible, el_with_texts)
    visible_texts = []
    for element in el_with_visible_texts:
        visible_text = element.strip()
        if keep_imporant_tags and element.parent.name in ['h1', 'h2', 'h3', 'td', 'ul', 'li']:
            visible_text = f'<{element.parent.name}>{visible_text}</{element.parent.name}>'
        visible_texts.append(visible_text)
    return "\n".join(visible_texts)


def text_from_html_preserving_table_html(body: Union[str, TextIOWrapper], keep_imporant_tags:bool =True, preserve_table:bool=True):
    soup = BeautifulSoup(body, 'html.parser')
    els = soup.findAll()
    visible_els = filter(tag_visible, els)
    if preserve_table:
        for element in visible_els:
            if element.name == 'table':
                element.table_structure_string = copy(str(element))
                element.clear()

    els = soup.findAll()
    visible_els = filter(tag_visible, els)
    visible_texts = []

    for element in visible_els:
        visible_text= ''
        try:
            visible_text = element.strip()
            if keep_imporant_tags and element.parent.name in ['h1', 'h2', 'h3', 'td', 'ul', 'li']:
                visible_text = f'<{element.parent.name}>{visible_text}</{element.parent.name}>'
        except:
            if preserve_table and element.name == 'table':
                visible_text = element.table_structure_string
        visible_texts.append(visible_text)
    return "\n".join(visible_texts)

if __name__ == '__main__':
    with open('../data/page.html', 'r') as f:
        body = text_from_html_preserving_table_html(f)
    print('what')

