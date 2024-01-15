import re

def process_output(output):
    output = re.sub(r'\\n', '', output)
    output = re.sub(r'\\t', '', output)
    output = re.sub(r'\\', '', output)
    return output

def extract_inside_key_and_comma(key_name, test_str, key_value_end_substring =','):
    sub1 = f'"{key_name}"'
    sub2 = key_value_end_substring

    # getting index of substrings
    idx1 = test_str.index(sub1)
    idx2 = test_str[idx1:].index(sub2) + idx1

    res = ''
    # getting elements in between
    for idx in range(idx1 + len(sub1) + 1, idx2):
        res = res + test_str[idx]
    return res

def convert_response_to_dict(output, output_parser):
    match_dict = {}
    try:
        match_dict = output_parser.parse(output)
    except Exception as e:
        output = process_output(output)
        for key_name in ['tag1', 'tag2', 'tag3']:
            match_dict[key_name] = extract_inside_key_and_comma(
                key_name=key_name,
                test_str=output,
                key_value_end_substring=','
            )
    return match_dict
