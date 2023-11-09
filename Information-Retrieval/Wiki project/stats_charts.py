import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# set seed for the sample
np.random.seed(0)

# Load the preprocessed articles data
df = pd.read_csv("csv/processed_file.csv")

# Most frequent words
words = ' '.join(df['content']).split()
word_counts = pd.Series(words).value_counts()
print(f"Number of unique words: {len(word_counts)}")
most_frequent_words = word_counts.head(10)

# Histogram of word frequencies
plt.figure(figsize=(10, 6))
most_frequent_words.plot(kind='bar', color='skyblue')
plt.title('Top 10 Most Frequent Words')
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.xticks(rotation=45)

# take 30 random articles from the dataset
df = df.sample(20)

# Calculate cosine similarities between documents
contents = df['content']
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(contents)
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# take the link of the articles as labels
labels = df['link']
# split by '/' and take the last element of the list
labels = [label.split('/')[-1] for label in labels]

# Create a heatmap for document similarities
plt.figure(figsize=(10, 6))
plt.imshow(cosine_sim, cmap='Blues')
plt.colorbar()
plt.xticks(np.arange(len(labels)), labels, rotation=90)
plt.yticks(np.arange(len(labels)), labels)
plt.title('Document Similarities')
plt.tight_layout()
plt.show()
