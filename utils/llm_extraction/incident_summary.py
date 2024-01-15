import json

from langchain.chains import LLMChain, SimpleSequentialChain
from langchain_core.prompts import ChatPromptTemplate
from tqdm import tqdm
from wise_chain import load_model
import pandas as pd
from utils.load_data import pickle_load


def get_root_cause_analysis(html):
    prompt =  f"""You are a helpful assistant that processes and summarises reports about incidents at a fin-tech company.
              You are provided with the html of the incident report, and asked to produce a paragraph of less than 200 words to summarise the incident 
               Clearly state the teams involved in the incident.
               If the incident is related to technology, clearly state which AWS infrastructures that are involved.
               The infrastructure can be the database, or an analytics tool, or server, or cluster.  
               If the incident is related to fraud, clearly state the type of fraud (such as chargeback, scam, ATO). 
               if it is related to a banking partner, clearly state the name of the banking partner. 
               If it is related to a third party software, clearly state the name of third party software.. 
               If the given report does not contain enough information for a summary, return <NULL>. 
               \n Incident report: {html}"""
    return prompt


if __name__ == '__main__':
    version = 1

    df = pd.read_csv('../../table_urls_up_to_sev3.csv')
    llm = load_model("gpt-4", team='hackathon', use_case='incident-labelling')
    labels = []

    # read all files from directory, take only 200 files:
    for post_mortem_id in tqdm(list(df['POSTMORTEM_ID'])):
        try:
            html = pickle_load(f'../../pickle_data_html_only_new/{post_mortem_id}.pkl')

            answer = llm(get_root_cause_analysis(html))
            labels.append({'postmortem_id': post_mortem_id, 'summary': answer})
        except Exception as e:
            print(f'Error getting summary from {post_mortem_id} due to {e}')

    json_object = json.dumps(labels, indent=4)
    with open(f'../../summary_results/summary_{version}.json', 'w') as handle:
        handle.write(json_object)


