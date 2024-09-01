import streamlit as st
# Assuming these are your custom modules for fetching and processing papers
from search_api import search_papers_in_semantic_scholar
from get_paper_embeddings import embed_and_save_papers_with_openai
from cluster_subtopics import run_cluster_subtopics
from subtopic_aspect_generation import name_the_clusters
from outline_creation import get_outline_for_subtopics
from run_full_subtopic_expansion_process import expand_subtopic
from Navigator_utils import *

# Set Streamlit page configuration
st.set_page_config(page_title="Knowledge Navigator", layout="centered", page_icon="🐋")

# Placeholder for the directory where queries and related data are stored
queries_dir = 'Data'
example_queries =  ["Enter your own query"] + list(get_list_of_dir_names(queries_dir))


def ui_setup():
    # Assuming you have a list of example queries

    c1, c2 = st.columns([1, 2])

    with c1:
        # Assuming the image path is correct and accessible
        st.image("images/whale3.png", width=200)

    with c2:
        st.caption("")
        st.title("**:blue[Knowledge Navigator]**")
        st.subheader("Navigate the ocean of scientific knowledge with ease.")

    # Add an option for custom query input in the example queries list
    query_selection = st.sidebar.selectbox('Select a query:', example_queries, index=0)

    custom_query = ""
    # If the user selects "Enter your own query", enable text input for custom query
    if query_selection == "Enter your own query":
        custom_query = st.sidebar.text_input('Enter a scientific topic search query. For example: "DNA methylation" or "covid-19"')
        search_query = custom_query
    else:
        search_query = query_selection

    return search_query


def main():
    query = ui_setup()
    if query:
        with st.spinner(f"Processing '{query}'..."):
            with st.expander("processing", True):
                papers = fetch_papers(query, queries_dir)
                embeddings = generate_embeddings(papers, query, queries_dir)
                clusters = cluster_embeddings(embeddings, query, queries_dir)
                named_clusters = name_clusters(clusters, query, queries_dir)
                outline = create_cluster_outline(named_clusters, query, queries_dir)
                st.subheader(f"**{query}**")
                st.session_state['outline'] = outline
                st.session_state['named_clusters'] = named_clusters
            full_outline = dict()
            # create a unified dictionary of outline and named_clusters:
            for main_topic, clusters_and_desc in outline.items():
                topic_subtopic_dict = dict()
                cluster_ids_in_topic = clusters_and_desc['cluster_id']
                for cluster_id in cluster_ids_in_topic:
                    cluster_items = named_clusters[cluster_id]
                    if cluster_items[0] == 'Removed':
                        continue
                    topic_subtopic_dict[cluster_items[0]['Subtopic']] = {'Description':cluster_items[0]['Description'],'papers':cluster_items[1],'subtopic_id':cluster_id}
                full_outline[main_topic] = topic_subtopic_dict
            st.session_state['query'] = query
            st.session_state['full_outline'] = full_outline
            display_outline()


# Define functions for each step in the process
def fetch_papers(query, output_dir, max_results=1000):
    is_query_exists = check_if_query_exists(query, output_dir)
    if not is_query_exists:
        st.write(f"Searching the literature about {query}")
        papers = search_papers_in_semantic_scholar(query,output_dir, max_results)
        st.write(f"Done! Found {len(papers)} papers.")
    else:
        papers = load_papers(query,output_dir)
        st.write(f"Done! Found {len(papers)} papers.")

    return papers


def generate_embeddings(papers, query, output_dir):
    is_embedding_exists = check_if_embedding_exists(query,output_dir)
    if not is_embedding_exists:
        papers_and_embeddings = embed_and_save_papers_with_openai(papers,query,output_dir)
    else:
        papers_and_embeddings = load_embeddings(query,output_dir)
        st.write(f"Embedding {len(papers_and_embeddings)} papers about {query}")
    return papers_and_embeddings


def cluster_embeddings(papers_and_embeddings, query, output_dir):
    st.write(f"Constructing a map of {query} subtopics...")
    cluster_output = run_cluster_subtopics(papers_and_embeddings,query,output_dir)
    return cluster_output

def name_clusters(clusters, query, output_dir):
    st.write(f"Navigating {query} subtopics... It may take a while.")
    clusters_with_subtopics = name_the_clusters(clusters,query,queries_dir)
    #st.header(f"**:blue[{query}]**")
    st.markdown(f"**Subtopics for {query} generated successfully.**")
    st.write()
    subtopics_to_papers = {}
    for cluster_id, cluster_outputs in clusters_with_subtopics.items():
        subtopic = cluster_outputs[0]
        papers = cluster_outputs[1]
        if subtopic != 'Removed':
            subtopics_to_papers[subtopic['Subtopic']] = papers

    return clusters_with_subtopics

def expand_cluster(query, subtopic, subtopic_id):
    st.write(f"**Subtopic Expander is not implemented yet in the UI, for details on how to run it manually please refer to the github page.**")
    # st.write(f"Expanding the subtopic '{subtopic}'...")
    # expand_subtopic(query, subtopic_id)
    # st.write(f"Subtopic '{subtopic}' expanded successfully.")

def create_cluster_outline(named_clusters, query, output_dir):
    st.write(f"Creating an outline for {query} subtopics...")
    outline = get_outline_for_subtopics(named_clusters,query,output_dir)
    return outline


def display_outline():
    if 'outline' not in st.session_state:
        st.write("No outline to display. Please select a query.")
        return

    outline = st.session_state['outline']
    for topic, details in outline.items():
        caption = f"**{topic}**\n\n**Description**: {details['description']}"
        if st.sidebar.button(caption, key=f"topic_{topic}"):
            st.session_state['selected_topic'] = topic

    if 'selected_topic' in st.session_state:
        selected_topic = st.session_state['selected_topic']
        display_subtopic_details(selected_topic)


def display_subtopic_details(topic):
    named_clusters = st.session_state['full_outline']
    if topic in named_clusters:
        st.header(f"**{topic}**")
        st.divider()
        for subtopic, papers_and_desc in named_clusters[topic].items():
            st.subheader(f"{subtopic}")
            st.markdown(f"**Description**: {papers_and_desc['Description']}")
            if st.button("Expand", key=f"expand_{papers_and_desc['subtopic_id']}"):
                expand_cluster(st.session_state['query'], subtopic, papers_and_desc['subtopic_id'])
            with st.expander("Papers in this Subtopic"):
                for paper in papers_and_desc['papers']:
                    # with st.popover(f":page_facing_up: **Title**: {paper['title']}"):
                    #     st.markdown(f"**Abstract**: {paper['abstract']}")
                    #make the title a link to the paper
                    popover_html = f"""
                    <details>
                        <summary><a href="{paper['link']}" target="_blank">{paper['title']}</a></summary>
                        <p><strong>Abstract:</strong> {paper['abstract']}</p>
                    </details>
                    """
                    st.markdown(popover_html, unsafe_allow_html=True)
                    st.divider()



if __name__ == "__main__":
    main()
