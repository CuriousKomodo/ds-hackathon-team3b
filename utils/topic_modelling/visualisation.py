from scipy.cluster import hierarchy as sch
import datamapplot
import re
import matplotlib.pyplot as plt

from umap import UMAP
import pandas as pd

import seaborn as sns


# https://medium.com/@ashwin_rachha/topic-modeling-with-quantized-large-language-models-llms-a-comprehensive-guide-9331c6936073
def visualise_basic_results(topic_model, main_df, save_dir):
    docs = main_df['SUMMARY']

    del main_df['SUMMARY']

    document_info = topic_model.get_document_info(docs, main_df)
    document_info.to_csv(f'{save_dir}/document_info.csv', index=False)
    topics = document_info['Topic']
    linkage_function = lambda x: sch.linkage(x, 'single', optimal_ordering=True)
    hierarchical_topics = topic_model.hierarchical_topics(docs, linkage_function=linkage_function)

    fig = topic_model.visualize_hierarchy(hierarchical_topics=hierarchical_topics)
    fig.show()

    fig2 = topic_model.visualize_topics(topics)
    fig2.show()
    return document_info

def visualise_topics_over_time(topic_model, docs, timestamps):
    topics_over_time = topic_model.topics_over_time(docs, timestamps)
    fig = topic_model.visualize_topics_over_time(topics_over_time, top_n_topics=20)
    fig.show()

def visualise_financial_loss_over_time(document_info, df=None):
    # visualise the financial loss per topic?
    # join the main_df with topics predicted
    document_info['CREATED_DATE'] = pd.to_datetime(document_info['CREATED_DATE'])
    sns.lineplot(x='CREATED_DATE', y='FINANCIAL_LOSS', hue='Topic', data=document_info)
    plt.show()

# TODO: visualise severity


def visualise_clusters(topic_model, embeddings, topics, subtitle=''):
    # Create a label for each document
    llm_labels = [re.sub(r'\\W+', ' ', label[0][0].split("\\n")[0].replace('"', '')) for label in
                  topic_model.get_topics(full=True)["Main"].values()]
    llm_labels = [label if label else "Unlabelled" for label in llm_labels]
    all_labels = [llm_labels[topic + topic_model._outliers] if topic != -1 else "Unlabelled" for topic in topics]
    # Run the visualization
    # Pre-reduce embeddings for visualization purposes
    reduced_embeddings = UMAP(n_neighbors=15, n_components=2, min_dist=0.0, metric='cosine',
                              random_state=42).fit_transform(embeddings)

    fig, _ = datamapplot.create_plot(
        reduced_embeddings,
        all_labels,
        label_font_size=11,
        title="BERTopic + LLM - Incident topic modelling",
        sub_title=subtitle,
        label_wrap_width=20,
        use_medoids=True,
        logo=None,
    )
    fig.savefig("clustering.png", bbox_inches="tight")