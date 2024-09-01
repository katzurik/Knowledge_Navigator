import json
import os
import pickle
from openai import OpenAI
from Keys import OPENAI_KEY
import streamlit as st
import argparse
from tqdm import tqdm
import numpy as np
client = OpenAI(api_key=OPENAI_KEY)



def generate_subtopic_aspects(clusters,
                              query,
                              model="gpt-4o-2024-05-13"):
    SYSTEM_PROMPT = """
# Task Overview:
You are provided with a general topic and a set of scientific papers retrieved by a lexical search system using this topic as a query. Your task is to analyze how the papers relate to the topic and categorize their relevance.

# Instructions:

Evaluate Relevance: Determine if the papers are directly related to the research topic.

- If they are not related to the research domain or do not address the topic directly, mark them as "NOT RELATED."
- If they are a genuine subtopic of the main topic, mark them as "RELATED."
- If the papers would not be relevant to a user searching for the main topic, consider them not related.
- IF the papers do not address an explicit relation to the topic, consider them not related.

#Output Requirements:
Output should be a json with the following fields:
Description: Write a summary describing the common subtopic reflected in the research theme of the papers in the group in relation to the Topic. 
Subtopic: Give a title for the group of papers that represents a meaningful subtopic of the Topic.
Relatedness: Rate the relatedness on a scale from 1 to 5, where 1 means not relevant at all, and 5 indicates the papers deal directly with the topic.
Is Related: State whether the papers are "RELATED" or "NOT RELATED" based on their relevance to the original topic.
- Write nothing else
"""


    is_title = True
    is_abstract = True

    subtopics = []
    progress_text = f"Generating {query} Aspects. Please wait."
    progress_bar = st.progress(0, text=progress_text)
    for cl,(cluster_id,papers) in enumerate(clusters.items()):
        if len(papers)> 3:
          papers_list = ''
          for i,paper in enumerate(papers):
            line = ''
            if is_title:
              line+=f"\n{i}:{paper['title']}"
            if is_abstract:
              line+=f"\nAbstract:{paper['abstract']}"

            papers_list+=line

          content = f"Topic: {query}\nPapers:{papers_list}"
          response = client.chat.completions.create(
              model=model,
              response_format={ "type": "json_object" },
              messages=[
                {"role": "system", "content": SYSTEM_PROMPT.strip()},
                {"role": "user", "content": content}
              ]
            )
          subtopics.append(response.choices[0].message.content)
          progress_bar.progress(cl + 1, text=progress_text)
        else:
          subtopics.append('Removed')
          progress_bar.progress(cl + 1, text=progress_text)

    for i,(cluster_id,titles) in enumerate(clusters.items()):
        if subtopics[i] != 'Removed':
            clusters[cluster_id] = (json.loads(subtopics[i]),titles)
        else:
            clusters[cluster_id] = ('Removed',titles)

    return clusters


def name_the_clusters(clusters,query,output_dir):
    if not os.path.exists(f"{output_dir}/{query}/{query}_clusters_with_subtopics.json"):
        clusters_with_subtopics =  generate_subtopic_aspects(clusters,query)

        with open(f"{output_dir}/{query}/{query}_clusters_with_subtopics.json", "w") as f:
            json.dump(clusters_with_subtopics, f)
    else:
        with open(f"{output_dir}/{query}/{query}_clusters_with_subtopics.json") as f:
            clusters_with_subtopics = json.load(f)
    return clusters_with_subtopics


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', dest='query', type=str, help='query to search')
    args = parser.parse_args()

    #query = args.query
    query = "Neuroblastoma"
    output_dir = 'Data'

    with open(f"{output_dir}/{query}/{query}_cluster.json") as f:
        cluster_output = json.load(f)
    clusters_with_subtopics = generate_subtopic_aspects(cluster_output,query)