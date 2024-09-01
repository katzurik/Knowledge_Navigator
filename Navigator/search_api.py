import json
import requests
import os
import time
import argparse
from Keys import SEMANTIC_SCHOLAR_API_KEY

def fetch_title(title):
    api_key = SEMANTIC_SCHOLAR_API_KEY
    headers = {'x-api-key': api_key}
    fields = "title,abstract,year"
    url = f"https://api.semanticscholar.org/graph/v1/paper/search/match?query={title}&fields={fields}"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data


def fetch_papers(query, max_results=2000):
    api_key = SEMANTIC_SCHOLAR_API_KEY
    headers = {'x-api-key': api_key}
    fields = "title,abstract,year,url"
    offset = 0
    limit = 100  # Adjust based on API's maximum limit per request

    papers = []

    while len(papers) < max_results:
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&fields={fields}&offset={offset}&limit={limit}&sort=relevance"
        response = requests.get(url, headers=headers)
        data = response.json()
        if 'data' not in data:
          print(data)
          break

        papers.extend(data['data'])
        offset += limit

        if len(papers) >= max_results or len(data['data']) < limit:
          print('hey ho lets go')
          break

    #change the field "url" to "link"
    for paper in papers:
        paper['link'] = paper.pop('url')

    return papers[:max_results]

def save_to_jsonl(papers, dir_name,query):
    # Extract the directory name from the filename

    # Check if the directory exists, if not create it
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # Save the papers to the file in the (now existing) directory
    with open(os.path.join(dir_name,f'{query}.jsonl'), 'w') as file:
        for paper in papers:
            json.dump(paper, file)
            file.write('\n')


def search_papers_in_semantic_scholar(query,output_dir, max_results=1000):
    papers = fetch_papers(query, max_results)
    save_to_jsonl(papers, os.path.join(f"{output_dir}/{query}"),query)
    print(f"Total {len(papers)} papers")
    return papers

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', dest='query', type=str, help='query to search')
    parser.add_argument('--output_dir', dest='output_dir', type=str, help='output directory to save the papers')
    parser.add_argument('--max_results', dest='max_results', default=1000, type=int, help='maximum number of papers to fetch')
    args = parser.parse_args()
    search_papers_in_semantic_scholar(args.query, args.output_dir, args.max_results)