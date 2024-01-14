from langchain.output_parsers import ResponseSchema, StructuredOutputParser


def create_langchain_full_instruction(document_content):
    response_schemas = [
        ResponseSchema(name="business_impact",
                       description="""Identify the paragraph describing the impact of the incident, in terms of financial loss, 
                       or impact to customer experience and compliance. 
                       If there is financial loss, please clearly state the loss figure in the corresponding currency code.
                       If there is any quantity associated with impact estimation please clearly state the figures."""),
        ResponseSchema(name="account_holder_name",
                       description="""Identify the """),
        ResponseSchema(name="account_number",
                       description=""""""),
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    format_instructions = output_parser.get_format_instructions()
    prefix = 'You are a helpful assistant in reviewing verification documents from customers. The following is the parsed text from a PDF document of a bank statement.'
    suffix = 'provide output as a json format'
    full_instruction = f'{prefix} \n {document_content} \n {format_instructions} \n {suffix}'
    return full_instruction, output_parser
