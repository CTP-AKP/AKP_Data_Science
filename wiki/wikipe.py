
import requests as rq
import wikipedia
import pandas as pd
from difflib import SequenceMatcher
import urllib.parse

df = pd.read_csv('names-of-game.csv')

similarity_threshold = 0.8

# New DataFrame to store name-content pairs
name_content_df = pd.DataFrame(columns=['name', 'content'])

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

not_found_df = pd.DataFrame(columns=['name'])

def sanitize_title(title):
    # Add or remove characters based on your needs
    forbidden_characters = ['<', '>', '#', '|', '[', ']', '{', '}', '`','™', '®', '©']

    for char in forbidden_characters:
        title = title.replace(char, '')

    return title

# Loop through the titles in the DataFrame
for index, row in df.iloc[15000:].iterrows():
    title = row['Name']

    # Sanitize the title to remove problematic characters
    sanitized_title = sanitize_title(title)

    # Flag to track if a page is found for any alteration
    page_found = False

    # Try the original title first
    try:
        page = wikipedia.page(sanitized_title, auto_suggest=False)
        print(f"Found result for {title}. Original: {title}")
        # If found, store the name-content pair in the new DataFrame
        name_content_df = pd.concat([name_content_df, pd.DataFrame({'name': [title], 'content': [page.content]})], ignore_index=True)
        page_found = True

    except wikipedia.exceptions.DisambiguationError as e:
        # Handle disambiguation pages if needed
        print(f"DisambiguationError: {e.options}")

    except wikipedia.exceptions.HTTPTimeoutError:
        # Handle timeout errors
        print("HTTPTimeoutError: Unable to retrieve page, trying common alterations...")

    except wikipedia.exceptions.PageError:
        # Handle page not found errors for the original title
        print(f"PageError: {title} not found on Wikipedia, trying common alterations...")
    except:
        print(f"Final error on original {title}")
    # If a page is found for the original title, skip the rest of the loop for this iteration
    if page_found:
        continue

    # Try common alterations of the title
    altered_titles = [title.replace(' ', '_'), title.replace(' ', '-')]
    for altered_title in altered_titles:
        try:
            page = wikipedia.page(altered_title, auto_suggest=False)
            print(f"Found result for {altered_title}. Original: {title}")
            # If found, store the name-content pair in the new DataFrame
            name_content_df = pd.concat([name_content_df, pd.DataFrame({'name': [altered_title], 'content': [page.content]})], ignore_index=True)
            page_found = True
            break  # Break the loop if a page is found for altered title

        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation pages if needed
            print(f"DisambiguationError: {e.options}")

            # Continue iterating through options until a valid page is found
            valid_option_found = False
            for option in e.options:
                try:
                    page = wikipedia.page(option, auto_suggest=False)
                    print(f"Found result for {altered_title}. Disambiguation option: {option}. Original: {title}")
                    # If found, store the name-content pair in the new DataFrame
                    name_content_df = pd.concat([name_content_df, pd.DataFrame({'name': [altered_title], 'content': [page.content]})], ignore_index=True)
                    valid_option_found = Trues
                    break  # Break the loop if a valid page is found for the disambiguation option

                except wikipedia.exceptions.PageError:
                    print(f"PageError: {option} not found on Wikipedia, skipping disambiguation option...")
                except wikipedia.exceptions.DisambiguationError:
                    # Handle disambiguation pages if needed
                    print(f"DisambiguationError: Skip")
                    continue


            if valid_option_found:
                page_found = True
                break  # Break the loop if a page is found for altered title
        except:
            continue
    


# Display the new DataFrame with name-content pairs
print(name_content_df)

# Save the not_found_df to a CSV file, handling if the file already exists
try:
    not_found_df_existing = pd.read_csv('not_found_names.csv')
    not_found_df_existing = pd.concat([not_found_df_existing, not_found_df], ignore_index=True)
    not_found_df_existing.to_csv('not_found_names.csv', index=False)
    print("not_found_names.csv already exists. Appending.")
except Exception as e:
    print(f"Error: {e}")
    print("not_found_names.csv not found. Creating new file.")
    not_found_df.to_csv('not_found_names.csv', index=False)

try:
    nc_df2 = pd.read_csv('name_content_2.csv')
    nc_df2 = pd.concat([nc_df2, name_content_df], ignore_index=True)
    nc_df2.to_csv('name_content_2.csv', index=False)
    print("Already made. Appending")
except Exception as e:
    print(f"Error: {e}")
    print("First Run")
    name_content_df.to_csv('name_content_2.csv', index=False)