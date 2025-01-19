import os
import dotenv
import praw

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
    query = append_review_to_query(query)  # Ensure "review" is in the query
    reviews = []
    after = None  # To paginate through results
    while len(reviews) < max_results:
        submissions = reddit.subreddit('all').search(query, sort='relevance', limit=1000, params={'after': after})
        submissions_list = list(submissions)  # Convert to list to access elements

        if not submissions_list:
            break  # Exit if no submissions are found
        
        for submission in submissions_list:
            query_words = query.lower().split()
            all_words_exist = all(word in submission.title.lower() for word in query_words)
            all_words_exist2 = all(word in submission.selftext.lower() for word in query_words)

            if submission.selftext.strip() != "" and (all_words_exist or all_words_exist2):
                reviews.append(submission.selftext.strip())  # Only take the text part
            if len(reviews) >= max_results:
                break
        
        # Check if there are more pages to load
        after = submissions_list[-1].fullname if submissions_list else None
        if not after:  # If no more results, stop the loop
            break
    
    # Retry logic if less than 100 reviews are found
    if len(reviews) < max_results:
        print(f"Only {len(reviews)} reviews found, retrying with a broader query...")
        reviews += fetch_reviews_top("review", max_results - len(reviews))  # Retry with a more general "review" query
    
    return reviews[:max_results]

# Function to fetch reviews sorted by "hot"
def fetch_reviews_hot(query, max_results=100):
    query = append_review_to_query(query)  # Ensure "review" is in the query
    reviews = []
    after = None  # To paginate through results
    while len(reviews) < max_results:
        submissions = reddit.subreddit('all').search(query, sort='hot', limit=100, params={'after': after})
        submissions_list = list(submissions)  # Convert to list to access elements

        if not submissions_list:
            break  # Exit if no submissions are found
        
        for submission in submissions_list:
            if submission.selftext.strip() != "" and (query.lower() in submission.title.lower() or query.lower() in submission.selftext.lower()):
                reviews.append(submission.selftext.strip())  # Only take the text part
            if len(reviews) >= max_results:
                break
        
        # Check if there are more pages to load
        after = submissions_list[-1].fullname if submissions_list else None
        if not after:  # If no more results, stop the loop
            break
    
    # Retry logic if less than 100 reviews are found
    if len(reviews) < max_results:
        print(f"Only {len(reviews)} reviews found, retrying with a broader query...")
        reviews += fetch_reviews_hot("review", max_results - len(reviews))  # Retry with a more general "review" query
    
    return reviews[:max_results]

# # Example usage
query = "ola electric"  # You can change this to any product or business name

# Fetch reviews sorted by "top"
top_reviews = fetch_reviews_top(query)
print(f"Total Top Reviews: {len(top_reviews)}")
for review in top_reviews[:5]:  # Print first 5 reviews as an example
    print(review)
    print("-" * 20)

# # Fetch reviews sorted by "hot"
# hot_reviews = fetch_reviews_hot(query)
# print(f"\nTotal Hot Reviews: {len(hot_reviews)}")
# for review in hot_reviews[:5]:  # Print first 5 reviews as an example
#     print(review)
#     print("-" * 20)
