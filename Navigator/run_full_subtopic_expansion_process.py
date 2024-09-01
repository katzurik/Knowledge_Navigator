from Subtopic_Query_Expansion import subtopic_expansion_query
from google_scholar_api import get_scholar_papers
import uuid
import os
import json


# function to load the subtopics and clusters given a query and subtopic_id

def subtopic_name_to_id(query,subtopic):
    with open(f"Data/{query}/{query}_clusters_with_subtopics.json") as f:
        subtopics_and_clusters = json.load(f)
    subtopic_name_to_id = {v[0]['Subtopic']:k for k,v in subtopics_and_clusters.items() if v[0] != 'Removed'}
    return subtopic_name_to_id[subtopic]

def load_subtopic_and_expanded_query(query,subtopic_id):
    #extract subtopic name
    with open(f"Data/{query}/{query}_clusters_with_subtopics.json") as f:
        subtopics_and_clusters = json.load(f)
    cluster_data = subtopics_and_clusters[subtopic_id]
    subtopic_name = cluster_data[0]['Subtopic']
    #check of boolean query exists
    if not os.path.exists(f"Data/{query}/subtopic_expansions/{subtopic_name}/{subtopic_name}_boolean_query.json"):
        subtopic_expansion_query(query,subtopic_id)

    return

#load subtopic query

def search_subtopic_query(query,subtopic_id):
    with open(f"Data/{query}/{query}_clusters_with_subtopics.json") as f:
        subtopics_and_clusters = json.load(f)
    cluster_data = subtopics_and_clusters[subtopic_id]
    subtopic_name = cluster_data[0]['Subtopic']


    with open(f"Data/{query}/subtopic_expansions/{subtopic_name}/{subtopic_name}_boolean_query.json") as f:
        boolean_query = json.load(f)['boolean_query']

    papers, organic_raw_results = get_scholar_papers(boolean_query, num_papers=150)



    #save json
    with open(f"Data/{query}/subtopic_expansions/{subtopic_name}/{subtopic_name}_raw.json", 'w') as f:
        json.dump(organic_raw_results, f)

    with open(f"Data/{query}/subtopic_expansions/{subtopic_name}/{subtopic_name}.jsonl", 'w') as file:
        for paper in papers:
            paper_id = str(uuid.uuid4())
            title = paper['title']
            abstract = paper['snippet']
            new_paper_format = {'paperId': paper_id, 'title': title, 'abstract': abstract}
            json.dump(new_paper_format, file)
            file.write('\n')



def expand_subtopic(query,subtopic_id):
    load_subtopic_and_expanded_query(query,subtopic_id)
    search_subtopic_query(query,subtopic_id)
    return

if __name__ == "__main__":
    query = 'Neuroblastoma'
    subtopic_name = 'Epigenetic Therapy in Neuroblastoma'   #subtopic title
    subtopic_id = subtopic_name_to_id(query,subtopic_name)
    load_subtopic_and_expanded_query(query,subtopic_id)
    search_subtopic_query(query,subtopic_id)
    print('done')
