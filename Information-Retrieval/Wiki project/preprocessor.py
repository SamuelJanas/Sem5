import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

# Download required NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')

# Initialize stemmer and lemmatizer
lemmatizer = WordNetLemmatizer()

# Load stop words
stop_words = set(stopwords.words('english'))

# Helper function to convert NLTK pos to wordnet pos
def nltk_pos_to_wordnet_pos(nltk_pos):
    mapping = {'N': wordnet.NOUN, 'V': wordnet.VERB, 'R': wordnet.ADV, 'J': wordnet.ADJ}
    return mapping.get(nltk_pos[0], wordnet.NOUN)

def preprocess_article(article):
    content = article['content']
    link = article['link']
    
    # Tokenize into sentences, then into words
    sentences = sent_tokenize(content)
    tokens = [word_tokenize(sent) for sent in sentences]
    words = [word for sublist in tokens for word in sublist]

    # Remove stopwords and non-alphabetical tokens for cleaner preprocessing
    words = [word for word in words if word not in stop_words and word.isalpha()]

    # Get POS tagging for the words
    nltk_pos = nltk.pos_tag(words)
    wordnet_pos = [nltk_pos_to_wordnet_pos(pos) for _, pos in nltk_pos]

    # Apply lemmatization
    lemmatized_words = [lemmatizer.lemmatize(word, pos) for word, pos in zip(words, wordnet_pos)]

    preprocessed_content = ' '.join(lemmatized_words)
    
    return {
        'link': link,
        'content': preprocessed_content
    }
