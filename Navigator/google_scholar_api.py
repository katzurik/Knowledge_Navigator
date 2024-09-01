import requests
import json
import time
import os
import uuid
from Keys import SERPAPI_KEY



# Your SerpAPI key
API_KEY = SERPAPI_KEY

# Function to get papers from Google Scholar using SerpAPI
def get_scholar_papers(query, num_papers=1000):
    papers = []
    start = 0
    organic_raw_results = []
    request_counter = 0
    print(f"Extracting {num_papers} papers for query: {query}")
    while len(papers) < num_papers:
        params = {
            'engine': 'google_scholar',
            'q': query,
            'api_key': API_KEY,
            'start': start,
            "num":"20"
        }

        response = requests.get('https://serpapi.com/search', params=params)
        request_counter += 1
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            break

        results = response.json()

        if 'error' in results:
            print(f"Error: {results['error']}")
            break

        organic_results = results.get('organic_results', [])
        if not organic_results:
            print("No more results available")
            break

        for paper in organic_results:
            if len(papers) >= num_papers:
                break
            papers.append({
                'title': paper.get('title'),
                'link': paper.get('link'),
                'snippet': paper.get('snippet')
            })
        organic_raw_results.extend(organic_results)

        start += 20  # Google Scholar returns 10 results per page
        if len(papers) % 100 == 0:
            print(f"Extracted {len(papers)} papers")
        #time.sleep(2)  # Sleep for 2 seconds to avoid hitting rate limits
    print(f"request counter: {request_counter}")
    return papers,organic_raw_results

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
    papers = get_scholar_papers(query)
    save_to_jsonl(papers, os.path.join(f"{output_dir}/{query}"),query)
    print(f"Total {len(papers)} papers")
    return papers




if __name__ == "__main__":
    query = 'tool use in animals'
    topic_name = 'tool use in animals'
    output_dir = 'Data'
    papers,organic_raw_results = get_scholar_papers(query)

    dir_name = os.path.join(output_dir, topic_name)
    # Check if the directory exists, if not create it
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    #save json
    with open(os.path.join(dir_name,f'{topic_name}_raw.json'), 'w') as f:
        json.dump(organic_raw_results, f)

    with open(os.path.join(dir_name,f'{topic_name}.jsonl'), 'w') as file:
        for paper in papers:
            paper_id = str(uuid.uuid4())
            title = paper['title']
            abstract = paper['snippet']
            new_paper_format = {'paperId': paper_id, 'title': title, 'abstract': abstract}
            json.dump(new_paper_format, file)
            file.write('\n')


