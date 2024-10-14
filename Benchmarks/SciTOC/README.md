# SCITOC Benchmark

## Overview

SCITOC is a novel benchmark designed to evaluate the ability of systems to handle complex scientific topics and produce well-organized outputs. The dataset consists of 50 Table of Contents (TOCs) extracted from scientific review papers sourced from 15 diverse peer-reviewed journals, all published by **Annual Reviews**.

The goal of SCITOC is to assess systems' capability to automatically structure large and complex scientific literature, aiding researchers in organizing information into hierarchical formats such as tables of contents.

## Dataset Format

The SCITOC dataset is stored as a JSON file, where each entry corresponds to the TOC of a scientific review article. Each entry is represented as a dictionary with the following structure:

```json
{
  "title": "Toward an Integrated Understanding of the Lepidoptera Microbiome",
  "sections": {
    "INTRODUCTION": [],
    "DIVERSITY OF THE LEPIDOPTERA MICROBIOME": [
      {"Endosymbionts": []},
      {"Gut Microbiome": [
        "Taxonomic diversity of gut bacteria.",
        "Taxonomic diversity of gut fungi.",
        "Toward uncovering a core microbiome."
      ]},
      {"Factors That Influence the Gut Microbiome": [
        "Diet and the environment.",
        "Host phylogeny.",
        "Developmental changes.",
        "Captivity- and rearing-induced changes."
      ]}
    ],
    "IMPACTS OF MICROBES ON THEIR LEPIDOPTERAN HOST": [
      {"Biological Significance of Endosymbionts": []},
      {"Putative Beneficial Relationships Between Lepidoptera and Their Gut Microorganisms": []},
      {"Multitrophic Interactions Mediated by Lepidopteran Microbes": []}
    ],
    "APPLICATION POTENTIAL OF LEPIDOPTERA-ASSOCIATED MICROBES": [],
    "CONCLUSIONS AND OUTLOOK": []
  },
  "doi": "doi:10.1146/annurev-ento-020723-102548",
  "journal_name": "Annual Review of Entomology",
  "url": "https://www.annualreviews.org/content/journals/10.1146/annurev-ento-020723-102548",
  "uuid": "4576a859-903e-47b2-96b0-7854b33c217f",
  "query": "Lepidoptera microbiome"
}
```
### Fields
```yaml
	title: The title of the scientific review article.
	sections: A dictionary representing the hierarchical structure of the paper’s TOC. Each section can contain subsections, which are either empty lists or lists of further subsections or content descriptions.
	doi: The article’s DOI for reference.
	journal_name: The journal from which the review was sourced.
	url: Link to the article’s webpage.
	uuid: A unique identifier for the entry.
	query: The query that was used to retrieve relevant papers in Knowledge Navigator paper.
```

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