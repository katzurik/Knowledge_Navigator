import os
import json
import pickle


def check_if_query_exists(query,output_dir):
    # Check if the query exists in the output directory
    if os.path.exists(os.path.join(f"{output_dir}/{query}/{query}.jsonl")):
        return True
    else:
        return False

def check_if_embedding_exists(query,output_dir):
    # Check if the embeddings exist in the output directory
    if os.path.exists(os.path.join(f"{output_dir}/{query}/{query}_embeddings.pkl")):
        return True
    else:
        return False


def load_papers(query,output_dir):
    # Load the papers from the file
    papers = []
    with open(os.path.join(f"{output_dir}/{query}/{query}.jsonl"), 'r') as file:
        for line in file:
            papers.append(json.loads(line))
    return papers

def load_embeddings(query,output_dir):
    # Load the embeddings from the file
    with open(os.path.join(f"{output_dir}/{query}/{query}_embeddings.pkl"), 'rb') as file:
        embeddings = pickle.load(file)
    return embeddings

def get_list_of_dir_names(output_dir):
    for f in os.listdir(output_dir):
        if not f.startswith('.'):
            yield f
    # Get the list of directories in the output directory
    return list(f)



if __name__ == "__main__":
    dirs = get_list_of_dir_names('Data')