import scraper
import preprocessor
import similarity
import pandas as pd
import argparse
from config import CSV_FILE_PATH

def main(args):
    if args.read_csv:
        # Read from CSV
        df = pd.read_csv(CSV_FILE_PATH)
        preprocessed_articles = df.to_dict(orient='records')
    else:
        # Scrape
        articles = scraper.scrape()
        # Preprocess
        preprocessed_articles = [preprocessor.preprocess_article(article) for article in articles]
        # Save to CSV
        df = pd.DataFrame(preprocessed_articles)
        df.to_csv(CSV_FILE_PATH, index=False)
        print(f"Saved preprocessed articles to {CSV_FILE_PATH}")

    # For demonstration, let's use the links of the first 5 articles as input_articles_links
    input_articles_links = [article['link'] for article in preprocessed_articles[:5]]

    recommendations = similarity.get_recommendations(preprocessed_articles, input_articles_links, top_n=3)

    for rec in recommendations:
        print(f"Based on {rec['original']}, we recommend {rec['recommended']} with a score of {rec['score']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Wikipedia Article Recommender System')
    parser.add_argument('--read-csv', action='store_true', help='Use this flag to read data from CSV instead of scraping again')
    args = parser.parse_args()
    main(args)
