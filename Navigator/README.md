# Knowledge Navigator



The Knowledge Navigator system is implemented using Streamlit for the user interface. All processes are triggered through interactions with the app.


## Installation Instructions

#### 1.	Clone the Repository
Begin by cloning the repository to your local machine using the following command:

    git clone https://github.com/katzurik/Knowledge_Navigator.git
    cd Knowledge_Navigator/Navigator

#### 2.	Install Dependencies
Install all necessary packages and dependencies listed in the requirements.txt file or use the following command:
    
    conda create -n knowledge_navigator python=3.10 
    conda activate knowledge_navigator
    pip install -r requirements.txt
#### 3. Setting up your API Keys
The Knowledge Navigator system utilizes various API services. For LLMs and embeddings generation, it uses the OpenAI API. For retrieving scientific papers, it relies on either the Semantic Scholar API (default) or Google Scholar via SERPAPI. To run Knowledge Navigator, you must have valid API keys.

Store the API keys in a Keys.py file with the following format:

```python
# For LLMs and embeddings generation
OPENAI_KEY = 'YOUR_KEY' # *Default
CLAUDE_API_KEY = 'YOUR_KEY' # *Optional
# For search, choose one of the following:
SEMANTIC_SCHOLAR_API_KEY = 'YOUR_KEY' # *Default
SERPAPI_KEY = 'YOUR_KEY' # *Optional
```
* We recommend using Claude Sonnet 3.5 for generating queries with the Subtopic Expander.

#### 4. Run the Application
After setting up the environment and dependencies, run the application using Streamlit:

    streamlit run Navigator_app.py 

####	5.	Access the Application
Once the application starts, you can access it in your web browser at the default Streamlit URL:
    
    http://localhost:8501