import pandas as pd
from tqdm import tqdm
from get_page_items import fetch_and_store_page_content

if __name__ == '__main__':
    df = pd.read_csv('table_urls_up_to_sev3.csv')
    for index, row in tqdm(df.iterrows()):
        page_id = row['URL'].split('/')[-1]

        fetch_and_store_page_content(page_id=page_id,
                                     save_dir='pickle_data_text_only',
                                     postmortem_id=row['POSTMORTEM_ID']
                                     )

