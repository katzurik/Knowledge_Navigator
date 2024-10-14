---
license: cc-by-sa-4.0
language:
- en
size_categories:
- n<1K
---
# CLUSTREC-COVID: A Topical Clustering Benchmark for COVID-19 Scientific Research

## Dataset Summary
**CLUSTREC-COVID** is a modified version of the **TREC-COVID** dataset, transformed into a topical clustering benchmark. The dataset consists of titles and abstracts from scientific papers about COVID-19 research, covering a diverse range of research topics. Each document in the dataset is assigned to a specific subtopic, making it ideal for use in document clustering and topic modeling tasks.

The dataset is useful for researchers aiming to evaluate clustering algorithms and techniques for automatic organization of scientific literature. It can also be used for exploring information retrieval systems that aim to group documents by subtopic or related research areas.

The source of this dataset is the [TREC-COVID](https://ir.nist.gov/trec-covid/) retrieval dataset, which has been adapted for clustering and organization tasks.
****
## Accessing the Dataset on Hugging Face
The dataset is also available on Hugging Face. You can easily load it using the following code:
```python
from datasets import load_dataset

ds = load_dataset("Uri-ka/CLUSTREC-COVID")
```
## Dataset Structure

Each document in the dataset includes the following fields:

- **topic_name** (string): The specific subtopic to which the document has been assigned. (e.g., "coronavirus response to weather changes").
- **topic_id** (string): A unique identifier for the topic. (cluster identifier)
- **title** (string): The title of the scientific paper.
- **abstract** (string): The abstract or summary of the paper.
- **doc_id** (string): A unique document identifier.
### Example Entry
```json
{
  "topic_name": "coronavirus response to weather changes",
  "topic_id": "2",
  "title": "Weather variables impact on COVID-19 incidence",
  "abstract": "We test the hypothesis of COVID-19 contagion being influenced by meteorological parameters such as temperature or humidity.\
              We analysed data at high spatial resolution (regions in Italy and counties in the USA) and found that while at low resolution this might seem the case,\
              at higher resolution no correlation is found. Our results are consistent with a poor outdoors transmission of the disease. However,\
              a possible indirect correlation between good weather and a decrease in disease spread may occur,\
              as people spend longer time outdoors.",
  "doc_id": "hadnxjeo",
}
```
### License
The dataset inherits its license from the original [TREC-COVID](https://ir.nist.gov/trec-covid/) dataset. Please refer to the license of the original dataset for any use restrictions.


### Citation Information
Cite as:
```
@article{katz2024knowledge,
  title={Knowledge Navigator: LLM-guided Browsing Framework for Exploratory Search in Scientific Literature},
  author={Katz, Uri and Levy, Mosh and Goldberg, Yoav},
  journal={arXiv preprint arXiv:2408.15836},
  year={2024}
}
```