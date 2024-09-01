import json
import os
import pickle
from openai import OpenAI
from Keys import OPENAI_KEY
import argparse
from tqdm import tqdm
import numpy as np
client = OpenAI(api_key=OPENAI_KEY)



def generate_outline(subtopic_and_cluster_ids,query,output_dir,number_of_chapters=8):
    #remove subtopics with "Removed" value:
    subtopic_and_cluster_ids = {k: {'Subtopic':v['Subtopic'],'Description':v['Description']} for k, v in subtopic_and_cluster_ids.items() if v != 'Removed' and v['Is Related']=='RELATED'}
    #sys_content = f"""You are an assistant for a scientific literature navigation platform. You are given a dictionary of groups of subtopics of the topic {query}. The dictionary include the group_id, subtopic and its description Group the following subtopics into 5 groups of subtopics and give each cluster a proper name and description. Output must be in json. Each key is the name, values are the list of \"cluster_id\" and \"description\". Dont leave any subtopic out.  Write nothing else."""
    # sys_content = f"""You are given a nested dictionary where each key is a subtopic_id and the value is a dictionary of subtopics of the topic "{query}". Reflect on the subtopics and their descriptions and define {str(number_of_chapters)} clusters of topics that group the subtopics into meaningful research clusters. Those clusters will be used by a user to navigate between different domains of his research topic. give each topic a clear label and describe the subtopics that the cluster is dealing with. Output must be in json. Do not leave any subtopic without a cluster.
    #
    # ## Output
    # - Output a json object with:
    # - clusters: list of dictionaries with digits from '1' to '{str(number_of_chapters)}' of  "cluster_ids", "cluster_title" and "description"
    # - subtopics: dictionary with the subtopic_id as a field  and the appropriate cluster id as a key for each subtopic in the input.
    # """
    sys_content = f"""You are given a nested dictionary where each key is a subtopic_id and the value is a dictionary of subtopics of the topic "{query}". Reflect on the subtopics and their descriptions and define clusters of topics that group the subtopics into meaningful research clusters. Create the clusters as an outline where each cluster is a foundational chapter about  "{query}". Those clusters will be used by a user to navigate between different domains of his research topic. give each topic a clear label and describe the subtopics that the cluster is dealing with. Output must be in json. Do not leave any subtopic without a cluster.
    
    ## Output
    - Output a json object with:
    - clusters: list of dictionaries with digits from '1' to 'N' of  "cluster_ids", "cluster_title" and "description"
    - subtopics: dictionary with the subtopic_id as a field and the appropriate cluster id as a key for each subtopic in the input.
    """
    response = client.chat.completions.create(
              model="gpt-4o-2024-05-13",
              response_format={ "type": "json_object" },
              messages=[
                {"role": "system", "content": sys_content.strip()},
                {"role": "user", "content":  f"Subtopic dictionary: {subtopic_and_cluster_ids}"}
              ]
            )
    outline = json.loads(response.choices[0].message.content)

    return outline

def parse_outline(outline,subtopic_and_cluster):
    map_cluster_id_to_title = {i['cluster_id']:{'title':i['cluster_title'],'description':i['description']} for i in outline['clusters']}
    parsed_outline = {}
    for subtopic_id, cluster_id in outline['subtopics'].items():
        if map_cluster_id_to_title[cluster_id]['title'] not in parsed_outline:
            parsed_outline[map_cluster_id_to_title[cluster_id]['title']] = {'cluster_id':[subtopic_id],
                                                                   'description':map_cluster_id_to_title[cluster_id]['description'],
                                                                   'subtopics':[subtopic_and_cluster[subtopic_id][0]]}
        else:
            parsed_outline[map_cluster_id_to_title[cluster_id]['title']]['cluster_id'].append(subtopic_id)
            parsed_outline[map_cluster_id_to_title[cluster_id]['title']]['subtopics'].append(subtopic_and_cluster[subtopic_id][0])

    return parsed_outline
def get_outline_for_subtopics(subtopic_and_cluster,query,output_dir):

    if not os.path.exists(f"{output_dir}/{query}/{query}_outline.json"):

        id_subtopic_dict = {k: v[0] for k, v in subtopic_and_cluster.items()}
        subtopics_outline = generate_outline(id_subtopic_dict, query, output_dir)
        parsed_outline = parse_outline(subtopics_outline,subtopic_and_cluster)
        # create a new dict of topics and their subtopics from subtopics_outline:
        #subtopics_to_clusters = {}
        # for main_topic, clusters_and_desc in subtopics_outline.items():
        #     subtopics_outline[main_topic]['subtopics'] = [subtopic_and_cluster[cluster_id][0] for cluster_id in
        #                                                   clusters_and_desc['cluster_id']]
        #     if len(subtopics_outline[main_topic]['subtopics']) != len(clusters_and_desc['cluster_id']):
        #         print("Error: The number of subtopics and cluster_ids do not match.")


        with open(f"{output_dir}/{query}/{query}_outline.json", "w") as f:
            json.dump(parsed_outline, f)

    else:
        with open(f"{output_dir}/{query}/{query}_outline.json") as f:
            parsed_outline = json.load(f)

    return parsed_outline



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', dest='query', type=str, help='query to search')
    args = parser.parse_args()

    query = 'Temperature and Cellular Physiology'#args.query
    output_dir = 'Data'

    with open(f"{output_dir}/{query}/{query}_clusters_with_subtopics.json") as f:
        cluster_with_subtopics = json.load(f)

    #outline = get_outline_for_subtopics(cluster_with_subtopics,query,output_dir)
    id_subtopic_dict = {k: v[0] for k, v in cluster_with_subtopics.items()}
    subtopics_outline = generate_outline(id_subtopic_dict,query,output_dir)
    # #create a new dict of topics and their subtopics from subtopics_outline:
    # subtopics_to_clusters = {}
    # for main_topic, clusters_and_desc in subtopics_outline.items():
    #     subtopics_outline[main_topic]['subtopics'] = [cluster_with_subtopics[cluster_id][0] for cluster_id in clusters_and_desc['cluster_id']]
    #     if len(subtopics_outline[main_topic]['subtopics']) != len(clusters_and_desc['cluster_id']):
    #         print("Error: The number of subtopics and cluster_ids do not match.")