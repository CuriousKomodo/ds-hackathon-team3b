from langchain.output_parsers import ResponseSchema, StructuredOutputParser


def create_langchain_full_instruction(document_content):
    response_schemas = [
        ResponseSchema(name="business_impact",
                       description="""Identify the paragraph describing the impact of the incident, in terms of financial loss, 
                       or impact to customer experience and compliance. 
                       If there is financial loss, please include the financial loss figure in the corresponding currency code.
                       If there is any quantity associated with impact estimation please clearly state the figures."""),
        ResponseSchema(name="root_cause",
                       description="""Identify the paragraph describing the root cause.
                       If applicable, include a list of technology/platforms that are involved, and how they are related to the incident.
                       """),
        ResponseSchema(name="incident_timeline",
                       description="""Identify the paragraph describing the """),
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    format_instructions = output_parser.get_format_instructions()
    prefix = 'You are a helpful assistant in reviewing verification documents from customers. The following is the parsed text from a PDF document of a bank statement.'
    suffix = 'provide output as a json format'
    full_instruction = f'{prefix} \n {document_content} \n {format_instructions} \n {suffix}'
    return full_instruction, output_parser
