from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def compute_similarities(articles):
    # Extract the content of the articles for TF-IDF transformation
    contents = [article['content'] for article in articles]

    # Convert the articles into TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(contents)
    
    # Compute cosine similarity between the articles
    cosine_sim = cosine_similarity(tfidf_matrix)
    
    return cosine_sim

def get_recommendations(articles, input_articles_links, top_n=5):
    # Compute similarities
    cosine_sim = compute_similarities(articles)
    
    # Create a link to index mapping
    link_to_idx = {article['link']: idx for idx, article in enumerate(articles)}
    recommendations = []

    for link in input_articles_links:
        idx = link_to_idx[link]
        sim_scores = list(enumerate(cosine_sim[idx]))
        
        # Sort the articles based on similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Exclude the article itself and get the top_n similar articles
        sim_scores = sim_scores[1:top_n+1]

        # Extract the links and scores of the recommended articles
        rec_links = [(articles[i]['link'], score) for i, score in sim_scores]

        for rec_link, score in rec_links:
            recommendations.append({
                'original': link,
                'recommended': rec_link,
                'score': score
            })
    
    return recommendations
