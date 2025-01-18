import pandas as pd
import os

# Load train and test datasets
train_path = "data/amazon_reviews/train.csv"
test_path = "data/amazon_reviews/test.csv"

train_df = pd.read_csv(train_path)
test_df = pd.read_csv(test_path)

# Display basic information
print("Train Dataset Shape:", train_df.shape)
print("Test Dataset Shape:", test_df.shape)
print("Train Sample:")
print(train_df.head())

print("Test Sample:")
print(test_df.head())
