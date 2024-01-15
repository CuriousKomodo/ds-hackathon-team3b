import pandas as pd

from utils.load_data import pickle_load, json_load

summaries_dict = json_load('../../summary_results/summary_1.json')
summaries_df = pd.DataFrame.from_records(summaries_dict)
summaries_df = summaries_df.loc[summaries_df['summary']!='<NULL>']

main_df = pd.read_csv('../../data/incidents_main.csv')

main_df_with_summary = pd.merge(main_df,
                             summaries_df,
                             how='inner',
                             left_on='POSTMORTEM_ID',
                             right_on='postmortem_id')
main_df_with_summary.to_csv('main_df_with_summary_new.csv')