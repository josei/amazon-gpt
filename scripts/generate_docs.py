import json
from pathlib import Path

bronze_data_dir = 'data/bronze'

def get_latest_data(folder):
    json_files = list(Path(folder).glob('*.json'))
    json_files.sort()
    with open(json_files[-1], 'r') as file: return json.load(file)

products = get_latest_data(bronze_data_dir)

for product in products:
    id = product['url'].split('/dp/')[1].split('/')[0]
    markdown = '# Product\n'
    markdown += f"Name: {product['title']}\n"
    markdown += f"URL: {product['url']}\n"
    markdown += "\n## Description\n"
    description = product['description'].replace('\n', '\n\n')
    markdown += f"{description}\n"
    markdown += "\n## Reviews\n"
    for review in product['reviews']:
        text = review['text'].replace('\n', ' ').replace('No se ha podido cargar el contenido multimedia.', '').strip()
        markdown += f"- {review['rating']}: {text}\n"
    with open(f'data/silver/{id}.md', 'w') as f: f.write(markdown)

for product in products:
    for i, review in enumerate(product['reviews']):
        id = product['url'].split('/dp/')[1].split('/')[0]
        markdown = '# Product\n'
        markdown += f"Name: {product['title']}\n"
        markdown += f"ID: {id}\n"
        text = review['text'].replace('\n', ' ').replace('No se ha podido cargar el contenido multimedia.', '').strip()
        markdown += f"Review: {review['rating']}: {text}\n"
        with open(f'data/gold/{id}-{i}.md', 'w') as f: f.write(markdown)
