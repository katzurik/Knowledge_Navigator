import json
import os
import pickle
from openai import OpenAI
from Keys import OPENAI_KEY
import streamlit as st
import argparse
from Navigator_utils import load_papers
import numpy as np
client = OpenAI(api_key=OPENAI_KEY)

def is_title_already_in_data(doc,data):
  title = doc['title'].lower().strip()
  for d in data:
    if title == d['title'].lower().strip():
      return False
  return True

def embed_and_save_papers_with_openai(papers,query, output_dir):
    search_output_path = f'{output_dir}/{query}/{query}.jsonl'
    data = []
    for paper in papers:
        if paper['title'] and paper['abstract'] and is_title_already_in_data(paper,data):
            data.append(paper)

    st.write(f"Embedding {len(data)} papers about {query}")


    data_for_embedding = [f"Title: {d['title'].strip()} ; Abstract: {d['abstract'].strip()}" for d in data]

    response = client.embeddings.create(
        input=data_for_embedding,
        model="text-embedding-3-large"
    )

    text_embedding_tuplist = [(text['title'], text['abstract'],text['link'], np.array(embedding_obj.embedding)) for text, embedding_obj in zip(data, response.data)]

    pickle_output_path = f'{output_dir}/{query}/{query}_embeddings.pkl'
    # Save the data to a file
    with open(pickle_output_path, 'wb') as f:
        pickle.dump(text_embedding_tuplist, f)

    st.write(f"Text Embedding Done!")
    return text_embedding_tuplist

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', dest='query', type=str, help='query to search')
    args = parser.parse_args()

    query = args.query
    output_dir = 'Data'
    papers = load_papers(query,output_dir)
    embed_and_save_papers_with_openai(papers,query,output_dir)