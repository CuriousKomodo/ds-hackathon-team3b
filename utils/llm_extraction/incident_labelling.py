import pandas as pd
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
import json

from tqdm import tqdm

from utils.load_data import pickle_load
from wise_chain import load_model

from response_conversion import convert_response_to_dict


def get_prompt(document_content):
    response_schemas = [
        ResponseSchema(name="primary_category",
                       description="""up to five words to classify the high-level category of the incident,
                       based on the business impact and teams/stakeholders involved,
                       such as engineering, platform, compliance, fraud, payment operation, KYC, accounting, user-experience, marketing.
                       If not sure, return 'unknown' """),
        ResponseSchema(name="secondary_category",
                       description="""up to five words to summarise the category of the incident,
                       based on the root cause or the part of product involved. If not sure, return 'unknown'
                       """),
        ResponseSchema(name="third_category",
                       description="""up to five words to summarise the category of the incident,
                       based on the root cause or the part of product/technology involved. If not sure, return 'unknown'"""),
        ResponseSchema(name="list_of_tech_involved",
                       description="""a list of technology/microservices/tools that are involved in the root cause of the incident if applicable. If not sure, return 'unknown'"""),
        # ResponseSchema(name="teams_responsible_for_improvement",
        #                description="""a list of technology that are involved in the root cause of the incident if applicable"""),
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    format_instructions = output_parser.get_format_instructions()
    prefix = ('You are a helpful assistant that processes and summarises reports about incidents at a fin-tech company.'
              'You are provided with the html of the incident report, and asked to provide four categories for this incident.'
              'Note that the incidents can occur in different functions of the company, '
              'Please extract p from the report if possible')
    suffix = 'provide output as a json format.'
    full_instruction = f'{prefix} \n {document_content} \n {format_instructions} \n {suffix}'
    return prefix, format_instructions, full_instruction, output_parser


if __name__ == '__main__':
    version = 1
    df = pd.read_csv('../../table_urls_up_to_sev3.csv')

    labels = {}
    # read all files from directory, take only 200 files:
    for post_mortem_id in tqdm(list(df['POSTMORTEM_ID'])):
        try:
            html = pickle_load(f'../../pickle_data_html_only_new/{post_mortem_id}.pkl')
            prefix, format_instructions, full_instruction, output_parser = get_prompt(html)
            llm = load_model("gpt-4", team='hackathon', use_case='incident-labelling')

            answer = llm(full_instruction)
            output = convert_response_to_dict(answer, output_parser)
            labels[post_mortem_id] = {'direct_answer':answer, 'parsed_answer':output}
        except Exception as e:
            print(f'cannot process {post_mortem_id} due to {e}')
    json_object = json.dumps(labels, indent=4)
    with open(f'../../tagging_results/tags_{version}.json', 'w') as handle:
        handle.write(json_object)

    config = {'prefix': prefix, 'full_instruction': format_instructions}
    json_object = json.dumps(config, indent=4)
    with open(f'../../tagging_results/config_{version}.json', 'w') as handle:
        handle.write(json_object)