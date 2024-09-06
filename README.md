Forked from [this project that assigns NAICS codes to Kickstarter projects](https://github.com/UtrechtUniversity/kickstarter).

Changes:

- Added ability to extract company descriptions using Google Custom Search API
- Updated syntax to work with version 0.28 of the *openai* library
- Updated default model to gpt-4o-mini

# Assigning NAICS codes to companies using OpenAI's ChatGPT API

## Introduction

This project assigns NAICS codes to companies by extracting company descriptions from their websites using the Google Custom Search API before using the ChatGPT API to determine the most appropriate NAICS based on the company name and description.

[NAICS](https://www23.statcan.gc.ca/imdb/p3VD.pl?Function=getVD&TVD=1369825) (North American Industry Classification System) is a numeric identifier for industries.

Let's use as an example [this dataset on the top 2000 global companies](https://www.kaggle.com/datasets/joebeachcapital/top-2000-companies-globally) in terms of revenue, profits, assets, and market value.

## Input

The input is a CSV file containing company data. At minimum it should contain company names. Here is an example of the first few rows and columns of our top 2000 global companies dataset.

| Global Rank | Company | Sales ($billion) |                                                                                                           
|--|--|--
1 | ICBC | 134.8 |
2 | China Construction Bank | 113.1 |
3 | JPMorgan Chase | 108.2 |

## Output

### extract_descriptions.py

The output of the *extract_descriptions.py* script is the inputted CSV file with company descriptions ("snippets") added from Google search results.

| Global Rank | Company | Sales ($billion)| Snippet                                                                                                    
|--|--|--|--
1 | ICBC | 134.8 | At ICBC, our job is making sure the auto insurance system works for all road users.
2 | China Construction Bank | 113.1 | Address of headquarters:No.25, Finance Street, Xicheng District, Beijing, China, Postcode 100033 Mobile website: m.ccb.com
3 | JPMorgan Chase | 108.2 | Committed to service, innovation and growth. JPMorganChase serves millions of customers, clients and communities in over 100 global markets.

### assign_naics_code.py

The output of the *assign_naics_code.py* script is the company data CSV file with NAICS codes added. It also contains the number of input and output tokens used in the API call.

| Global Rank | Company | Sales ($billion)| Snippet | NAICS | Input Tokens | Output Tokens                                                                                                   
|--|--|--|--|--|--|---
1 | ICBC | 134.8 | At ICBC, our job is making sure the auto insurance system works for all road users. | 5241 | 93 | 2
2 | China Construction Bank | 113.1 | Address of headquarters:No.25, Finance Street, Xicheng District, Beijing, China, Postcode 100033 Mobile website: m.ccb.com | 5221 |  108 | 2
3 | JPMorgan Chase | 108.2 | Committed to service, innovation and growth. JPMorganChase serves millions of customers, clients and communities in over 100 global markets. | 5221 | 104 | 2

## Requirements

- *pandas*, *openai*, *requests* libraries downloaded. Type in the terminal:

  `pip install -r requirements.txt`

- Google Custom Search Engine ID. Obtainable [here](https://programmablesearchengine.google.com/about/). Set the search engine ID as an environment variable.
  - On Linux/MacOS type in the terminal:

    `export SEARCH_ENGINE_ID=your_engine_id`

  - On Windows type in the terminal:

    `setx SEARCH_ENGINE_ID "your_engine_id"`


- Google API key with Custom Search API enabled. Free trials are available. [Google Cloud](https://cloud.google.com/). Set the API key as an environment variable.
  - On Linux/MacOS type in the terminal:

    `export GOOGLE_API_KEY=your_api_key`

  - On Windows type in the terminal:

    `setx GOOGLE_API_KEY "your_api_key"`


- OpenAI API key with credits loaded. Set the API key as an environment variable.
  - On Linux/MacOS type in the terminal:

    `export OPENAI_API_KEY=your_api_key`

  - On Windows type in the terminal:

    `setx OPENAI_API_KEY "your_api_key"`

## Run the program

Run the program from the terminal.

`python src/extract_descriptions.py`

`python src/assign_naics_code.py`
