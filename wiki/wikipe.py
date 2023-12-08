
import requests as rq
import wikipedia
import pandas as pd
from difflib import SequenceMatcher

df = pd.read_csv('names-of-game.csv')

similarity_threshold = 0.8

# New DataFrame to store name-content pairs
name_content_df = pd.DataFrame(columns=['name', 'content'])

# Function to calculate similarity between two strings
def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

#2500, Found result for Untitled Goose Game. Original: Untitled Goose Game
# Loop through the titles in the DataFrame
for index, row in df.iloc[12500:].iterrows():
    title = row['Name']

    # Search for similar titles
    search_results = wikipedia.search(title)

    if search_results:
        most_similar_title = search_results[0]

        # Check if the result is above the similarity threshold
        current_similarity = similarity(title.lower(), most_similar_title.lower())

        if current_similarity > similarity_threshold:
            try:
                # Search for the most similar title on Wikipedia
                page = wikipedia.page(most_similar_title)
                print(f"Found result for {most_similar_title}. Original: {title}")
                # If found, store the name-content pair in the new DataFrame
                name_content_df = pd.concat([name_content_df, pd.DataFrame({'name': [most_similar_title], 'content': [page.summary]})], ignore_index=True)

            except wikipedia.exceptions.DisambiguationError as e:
                # Handle disambiguation pages if needed
                print(f"DisambiguationError: {e.options}")

            except wikipedia.exceptions.HTTPTimeoutError:
                # Handle timeout errors
                print("HTTPTimeoutError: Unable to retrieve page, skipping...")

            except wikipedia.exceptions.PageError:
                # Handle page not found errors
                print(f"PageError: {most_similar_title} not found on Wikipedia, skipping...")

# Display the new DataFrame with name-content pairs
print(name_content_df)
try:
    nc_df2 = pd.read_csv('name_content.csv')
    nc_df2 = pd.concat([nc_df2, name_content_df], ignore_index=True)
    nc_df2.to_csv('name_content.csv', index=False)
    print("Already made. Appending")
except Exception as e:
    print(f"Error: {e}")
    print("First Run")
    name_content_df.to_csv('name_content.csv', index=False)