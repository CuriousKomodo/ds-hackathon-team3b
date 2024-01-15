from bertopic import BERTopic
from umap import UMAP
from wise_chain import load_model
from sklearn.feature_extraction.text import CountVectorizer
from bertopic.vectorizers import ClassTfidfTransformer
from utils.topic_modelling.custom_embedder_class import WiseLLMEmbedder

ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True)
vectorizer_model = CountVectorizer(stop_words="english")
umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine')

def get_topic_model(model_version):
    custom_embedder=None
    if model_version == 'default':
        topic_model = BERTopic(
            embedding_model="all-MiniLM-L6-v2",
            vectorizer_model=vectorizer_model,
            ctfidf_model=ctfidf_model,
            min_topic_size=3,
            umap_model=umap_model
        )
    elif 'gpt' in model_version or 'titan' in model_version or 'ada' in model_version:
        llm = load_model(model_version, team='hackathon', use_case='incidents')
        custom_embedder = WiseLLMEmbedder(embedding_model=llm)
        topic_model = BERTopic(
            embedding_model=custom_embedder,
            vectorizer_model=vectorizer_model,
            ctfidf_model=ctfidf_model,
            min_topic_size=5,
            umap_model=umap_model
        )
    else:
        raise Exception('Unknown model: {}'.format(model_version))
    return topic_model, custom_embedder