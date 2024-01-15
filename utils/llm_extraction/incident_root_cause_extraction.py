from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.prompts import ChatPromptTemplate
from wise_chain import load_model

from utils.llm_extraction.response_conversion import convert_response_to_dict
from utils.load_data import pickle_load


def get_root_cause_analysis():
    prompt = ChatPromptTemplate.from_template('You are a helpful assistant that processes and summarises reports about incidents at a fin-tech company.'
              'You are provided with the html of the incident report, and asked to perform root cause analysis.'
              'Please produce a paragraph of less than 200 words to describe the root cause.'
             """
               If the incident is related to technology, clearly state which AWS infrastructures that are involved, 
               the internal names of the infrastructure that we give.  
               The infrastructure can be the database, or an analytics tool, or server, or cluster. 
               If not sure, return <NULL>. \n Incident report: {html}""")
    return prompt

def extract_infra():
    response_schemas = [
        ResponseSchema(name="name_of_infra",
                       description=""""""),
        ResponseSchema(name="internal_name_of_infra",
                       description=""" 
                       """),
        ResponseSchema(name="problem_summary",
                       description="""Up to 5 words to describe the problem of the infrastrcture"""),
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    format_instructions = output_parser.get_format_instructions()

    prefix = f"""You are a senior engineer that reads and summarises root causes of incidents. '
              'Your job is to identify AWS infrastructures that are involved so other engineers can fix them.'
                'Given the root cause report of the incident, {format_instructions} """

    prompt = ChatPromptTemplate.from_template(
        'You are a senior engineer that reads and summarises root causes of incidents. '
              'Your job is to identify AWS infrastructures that are involved so other engineers can fix them.'
                """Given the root cause report of the incident, {format_instructions}
                produce a json that contain the AWS infrastructure with their internal 
                names. Each dictionary has the following fields: 
                name_of_infra, internal_name_of_infra, problem_description 
                       \n 
                       Root cause: {root_cause}""")
    return prompt

def extract_timeline():
    return None

if __name__ == '__main__':
    version = 1
    post_mortem_id=2777
    html = pickle_load(f'../../pickle_data_html_only_new/{post_mortem_id}.pkl')

    llm = load_model("gpt-4", team='hackathon', use_case='incident-labelling')

    chain_one = LLMChain(llm=llm, prompt=get_root_cause_analysis())
    chain_two = LLMChain(llm=llm, prompt=extract_infra())
    overall_simple_chain = SimpleSequentialChain(chains=[chain_one, chain_two],
                                                 verbose=True
                                                 )
    result = overall_simple_chain.run(html)
    print(result)


