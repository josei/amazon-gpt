# Amazon GPT

![AmazonGPT Demo](amazon-gpt.gif)

## What's this?

This is a Retrieval-Augmented Generator (RAG) that enables you to ask for Amazon product recommendations in natural language.

Note: this is a sample research project not affiliated with Amazon nor ChatGPT in any way. Please use it for research purposes only.

## Why is this interesting?

Amazon search is limited to actual product specifications. AmazonGPT leverages user reviews and lets you find products according to what users say about them.

## How to run it

First, install dependencies:
```
pip install pipenv && pipenv install
```

Shell into the virtual environment:
```
pipenv shell
```

Scrape some Amazon product list to populate the bronze data folder:
```
python scripts/scrape_products.py
```

Convert the scraped product data into individual markdown files to be used in the RAG:
```
python scripts/generate_docs.py
```

Run streamlit server and query the scraped product list:
```
streamlit run scripts/server.py
```

# License

Created by @josei.

MIT License, 2024.