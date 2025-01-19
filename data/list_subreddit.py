import os
import dotenv
import praw
import re

# Function to ensure all words from the query are present in the text (strict matching)
def contains_all_query_words(text, query):
    """
    Check if a text contains all words from the query (case-insensitive).

    Parameters:
        text (str): The text to search.
        query (str): The query containing words to match.

    Returns:
        bool: True if all words are found, False otherwise.
    """
    query_words = query.lower().split()
    text_lower = text.lower()
    return all(re.search(r"\\b" + re.escape(word) + r"\\b", text_lower) for word in query_words)

# Load environment variables from .env
dotenv.load_dotenv()

# Reddit API credentials
client_id = os.environ.get("reddit_client_id")
client_secret = os.environ.get("reddit_client_secret")
user_agent = os.environ.get("reddit_user_agent")

# Initialize Reddit client
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

# Function to ensure "review" is added to the query if not already present
def append_review_to_query(query):
    if "review" not in query.lower():
        query += " review"
    return query

# Function to fetch reviews sorted by "top"
def fetch_reviews_top(query, max_results=100):
    """
    Fetch top reviews from Reddit subreddits containing the word 'review' in their name.
    
    Parameters:
        query (str): The search term for reviews.
        max_results (int): The maximum number of reviews to fetch.
    
    Returns:
        list: A list of review texts matching the query.
    """
    # Append "review" to the query if not already included
    original_query = query  # Store the original query
    query = append_review_to_query(query)

    reviews = []

    # Dynamically fetch subreddits with "review" in their name
    
    subreddits_list = [sub.display_name for sub in reddit.subreddits.search(original_query)]
    print(subreddits_list)
    for sub in subreddits_list:
        print(f"Fetching reviews from r/{sub}...")
        print(len(reviews))
        if len(reviews) >= max_results:
            break
        # Fetch submissions from the subreddit
        submissions = reddit.subreddit(sub).search(query, sort='relevance', limit=100)
        # submissions_list = list(submissions)  # Convert to list

        # if not submissions_list:
        #     break  # Exit if no submissions are found
        
        for submission in submissions:
            if len(reviews) >= max_results:
                break

            # Check strict matching in both title and body
            if (contains_all_query_words(submission.title, original_query) or
                contains_all_query_words(submission.selftext, original_query)):
                reviews.append(submission.selftext.strip())
    
    # Retry with a broader query if fewer than max_results are found
    if len(reviews) < max_results:
        print(f"Only {len(reviews)} reviews found. Retrying with a broader query...")
        reviews += fetch_reviews_top("review", max_results - len(reviews))
    
    return reviews[:max_results]
import csv

def export_reviews_to_csv(reviews, filename="reviews.csv"):
    """
    Export a list of reviews to a CSV file.

    Parameters:
        reviews (list): List of reviews to be saved.
        filename (str): Name of the CSV file to save the reviews.
    """
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Review"])  # Add a header row
        for review in reviews:
            writer.writerow([review])  # Write each review in a new row

    print(f"Reviews successfully saved to {filename}")


# Example usage
query = "ola electric"  # Replace with your desired query

# Fetch reviews sorted by "top"
top_reviews = fetch_reviews_top(query)

# Export reviews to CSV
export_reviews_to_csv(top_reviews, filename="top_reviews.csv")

# # Example usage
query = "ola electric"  # You can change this to any product or business name

# Fetch reviews sorted by "top"
top_reviews = fetch_reviews_top(query)
print(f"Total Top Reviews: {len(top_reviews)}")
for review in top_reviews[:5]:  # Print first 5 reviews as an example
    print(review)
    print("-" * 20)