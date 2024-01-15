import pandas as pd

from utils.load_data import pickle_load

tags_df = pd.read_json('../tagging_results/tags_1.json', orient='index')
tags_df['POSTMORTEM_ID'] = tags_df.index

tags_results = []
for index, row in tags_df.iterrows():
    try:
        tag_result = {'POSTMORTEM_ID': row['POSTMORTEM_ID']}
        tag_result.update(row['parsed_answer'])
        tags_results.append(tag_result)
    except:
        print(f'error with {row["POSTMORTEM_ID"]}')

tags_results_df = pd.DataFrame(tags_results)
main_df = pd.read_csv('../data/incidents_main.csv')

summary_dict = pickle_load('../data/all_summaries_gpt4_dict.pkl')

summary_df = pd.DataFrame.from_dict(summary_dict, orient='index')

summary_df['POSTMORTEM_ID'] = summary_df.index.astype(float)

main_df_with_tags = pd.merge(main_df,
                             summary_df,
                             how='right',
                             left_on='POSTMORTEM_ID',
                             right_on='POSTMORTEM_ID')
main_df_with_tags.to_csv('data/main_df_with_summary.csv')