'''
This script takes as input a CSV with company names under the heading "Company"
and outputs the CSV with the companies' snippets from Google search results.
The script uses the Google Custom Search API to search for each company name
and extract the snippet from the search results.

PREREQUISITES:
Set your Google API key and Search Engine ID as environment variables.
'''

import os
import requests
import pandas as pd
import time
import shutil

# Constants
google_api_key = os.environ.get('GOOGLE_API_KEY')
search_engine_id =  os.environ.get('SEARCH_ENGINE_ID')
url = 'https://www.googleapis.com/customsearch/v1'
chunk_size = 100 # Number of rows processed at a time
progress_log = './data/processed/progress_descriptions.txt' # Progress log file
input_csv = './data/raw/Top2000CompaniesGlobally.csv'
output_csv = './data/processed/Top2000CompaniesGlobally_descriptions.csv'

def get_snippets_for_chunk(chunk):
    snippets = []
    for company_name in chunk['Company']:
        params = {
            'q': company_name,
            'key': google_api_key,
            'cx': search_engine_id
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status() # Raises HTTPError for bad responses
            results = response.json()
            if 'items' in results:
                snippet = results['items'][0]['snippet']
            else:
                snippet = 'No results found'
        except Exception as e:
            print(f'Error processing {company_name}: {e}')
            snippet = 'Error'
        snippets.append(snippet)
        time.sleep(0.4) # Delay to avoid hitting API rate limit
    chunk['Snippet'] = snippets
    return chunk

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# Check progress from the log
try:
    with open(progress_log, 'r', encoding='utf-8') as file:
        start_chunk = int(file.read())
        first_chunk = False
except (FileNotFoundError, ValueError):
    start_chunk = 0
    first_chunk = True
    
# Process CSV in chunks
for i, chunk in enumerate(pd.read_csv(input_csv,
                                      chunksize=chunk_size,
                                      encoding='ISO-8859-1'),
                          start=1):
    # If a chunk has already been processed, skip it
    if i <= start_chunk:
        continue
    
    print(f'Processing chunk {i} ...')
    
    processed_chunk = get_snippets_for_chunk(chunk)
    
    if i>1:
        # Make backup copy of output file before appending to it
        shutil.copy(output_csv,
                    output_csv.rsplit('.', 1)[0] \
                        + '_backup1.' \
                        + output_csv.rsplit('.', 1)[1])
        
    # Append to output file, without header if it's not the first chunk
    processed_chunk.to_csv(output_csv, 
                           mode='a',
                           header=first_chunk, 
                           index=False)
    first_chunk = False
    
    # Make backup copy of putput file after appending to it
    shutil.copy(output_csv,
                output_csv.rsplit('.', 1)[0] \
                    + '_backup2.' \
                    + output_csv.rsplit('.', 1)[1])
    
    # Update progress log
    with open(progress_log, 'w', encoding='utf-8') as file:
        file.write(str(i))
