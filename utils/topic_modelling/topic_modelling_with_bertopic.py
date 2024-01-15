from scipy.cluster import hierarchy as sch
from dotenv import load_dotenv
from utils.load_data import pickle_load, json_load
from utils.topic_modelling.get_topic_model import get_topic_model
import os, datetime
import pandas as pd

from utils.topic_modelling.visualisation import (
    visualise_basic_results,
    visualise_clusters,
    visualise_topics_over_time,
    visualise_financial_loss_over_time
)

load_dotenv()

timestamp_dir = os.path.join('topic_models/', datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
os.makedirs(timestamp_dir)

if __name__ == '__main__':
    model_version = 'amazon.titan-embed-g1-text-02'
    #model_version = 'default'
    main_df = pd.read_csv('main_df_with_summary_new.csv')
    docs = list(main_df['summary'])

    topic_model, custom_embedder = get_topic_model(model_version)
    topics, probs = topic_model.fit_transform(docs)

    document_info = visualise_basic_results(topic_model, main_df, save_dir=timestamp_dir)
    embeddings = custom_embedder.embed(docs)


    topic_model.save(f"{timestamp_dir}/topic_model_with_{model_version}", serialization="pickle")

    visualise_clusters(topic_model, embeddings, topics,
                       subtitle=f'embedding model={model_version}')

    timestamps = main_df['CREATED_DATE']
    visualise_topics_over_time(topic_model, docs, timestamps)

    financial_losses = main_df['FINANCIAL_LOSS'].fillna(0).astype(int)
    visualise_financial_loss_over_time(document_info)

