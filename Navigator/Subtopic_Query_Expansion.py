import json
from openai import OpenAI
import os
import re



def complex_task_query_generation(cluster_data,query,api_type='OAI'):

    is_title = True
    is_abstract = False

    cluster_information = cluster_data[0]
    papers = cluster_data[1]
    subtopic = cluster_information['Subtopic']
    general_topic = query
    content = f"You are tasked with identifying keywords or terms from a list of scientific paper titles and abstracts specifically relevant to the subtopic \"{subtopic}\". These keywords will be used to generate a query to retrieve documents about this specific subtopic. It's crucial to focus only on this particular aspect of \"{general_topic}\" research and not on the general topic.\n\nHere is the list of titles and abstracts:\n\n"
    content += f"Query Description: {cluster_information['Description']}\n"
    content+=  "<titles_and_abstracts>\n"

    for paper in papers:
        if is_title:
            content += f"Title: {paper['title']}\n"
        if is_abstract:
            content += f"Abstract: {paper['abstract']}\n\n"
    # content += f"Query: {cluster_information['Subtopic']}\n"
    # content += f"Query Description: {cluster_information['Description']}\n"
    content += "\n</titles_and_abstracts>\n\n"
    content+= f"Please follow these steps to complete the task:\n\n1. Carefully read through each title and abstract.\n\n2. As you read, identify words or short phrases that are specifically related to \"{subtopic}\".\n\n3. Pay special attention to recurring terms or concepts across multiple papers, as these are likely to be particularly relevant.\n\n4. Avoid selecting overly general terms related to \"{general_topic}\". Focus on terms that specifically relate to the \"{subtopic}\" aspect.\n\n5. After analyzing all the titles and abstracts, compile a list of the most relevant and frequently occurring keywords or phrases.\n\n6. Present your final list of keywords in order of relevance, with the most important or frequently occurring terms first. Include this list within <keywords> tags.\n\n7. Provide a brief explanation for why you chose each keyword, highlighting its relevance to \"{subtopic}\". Include this explanation within <justification> tags.\n\nRemember, the goal is to identify terms that will help retrieve documents specifically about \"{subtopic}\", not about \"{general_topic}\" in general. Your selected keywords should reflect this focused approach."
    chat_messages = [{"role": "user", "content": [{'type': "text", "text" : content}]}]

    if api_type == 'OAI':
        from Keys import OPENAI_KEY
        oai_client = OpenAI(api_key=OPENAI_KEY)
        response = oai_client.chat.completions.create(model="gpt-4o-2024-05-13",messages=[{"role": "user", "content": content}])
        chat_messages.append({"role": 'user', "content": [{"type": "text", "text": response.choices[0].message.content}]})

        return response.choices[0].message.content , chat_messages

    if api_type == 'Anthropic':
        import anthropic
        from Keys import CLAUDE_API_KEY
        claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        message = claude_client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        messages=chat_messages)
        chat_messages.append({"role": message.role, "content": [ {"type": "text", "text": message.content[0].text}]})
        return message.content[0].text , chat_messages







def extract_keywords(text):
    # Use a regular expression to find the keywords block
    keywords_block = re.search(r'<keywords>(.*?)</keywords>', text, re.DOTALL).group(1)

    # Split the block into lines and remove numbering and leading/trailing whitespace
    keywords = [re.sub(r'^\d+\.\s*', '', line).strip() for line in keywords_block.split('\n') if line.strip()]

    return keywords


def subtopic_expansion_query(query,subtopic_id):
    #load subtopics and clusters
    with open(f"Data/{query}/{query}_clusters_with_subtopics.json") as f:
        subtopics_and_clusters = json.load(f)

    cluster_data = subtopics_and_clusters[subtopic_id]
    claude_output, _  = complex_task_query_generation(cluster_data,query, api_type='Anthropic')
    keywords = extract_keywords(claude_output)
    boolean_query = transform_to_boolean(cluster_data,keywords)
    ## save boolean query in a subfolder of the main subtopic

    subtopic_name = cluster_data[0]['Subtopic']

    if not os.path.exists(f"Data/{query}/{subtopic_name}"):
        os.makedirs(f"Data/{query}/subtopic_expansions/{subtopic_name}")
    with open(f"Data/{query}/subtopic_expansions/{subtopic_name}/{subtopic_name}_boolean_query.json", "w") as f:
        json.dump({"boolean_query": boolean_query}, f)


def transform_to_boolean(cluster_data,keywords):
    # concat subtopic and keywords into a boolean query with AND and OR clauses
    cluster_information = cluster_data[0]
    subtopic = cluster_information['Subtopic']
    boolean_query = f"({subtopic}) AND ({' OR '.join(keywords)})"
    return boolean_query

if __name__ == '__main__':
    query = "Lepidoptera microbiome"
    #subtopic_name ="Sex Hormones and COVID-19 Severity" # "Thyroid Dysfunction in COVID-19" #Impact of COVID-19 on Reproductive Endocrine Health /
    subtopic_name = "Gut Microbiome of Silkworms"
    #load subtopics and clusters
    with open(f"Data/{query}/{query}_clusters_with_subtopics.json") as f:
        subtopics_and_clusters = json.load(f)



    for cluster_id, (subtopic, papers) in subtopics_and_clusters.items():
        if subtopic['Subtopic'] == subtopic_name:
            break


    cluster_data = subtopics_and_clusters[cluster_id]
    output = complex_task_query_generation(cluster_data,query, api_type='Anthropic')
    claude_output, _ = output
    keywords = extract_keywords(claude_output)
    boolean_query = transform_to_boolean(cluster_data,keywords)
    ## save boolean query in a subfolder of the main subtopic
    if not os.path.exists(f"Data/{query}/{subtopic_name}"):
        os.makedirs(f"Data/{query}/subtopic_expansions/{subtopic_name}")
    with open(f"Data/{query}/subtopic_expansions/{subtopic_name}/{subtopic_name}_boolean_query.json", "w") as f:
        json.dump({"boolean_query": boolean_query}, f)

