from spacy import displacy

import streamlit as st
import requests
import json
import random
import os, sys

query_input = st.text_input('query:')

url = os.getenv('NODERED_ADDR', 'http://localhost:18087') + '/'
headers = {'content-type': 'application/json'}

def add_colormap(labels):
    color_map = {}

    for label in labels:
        #if label not in color_map:
        rand_color = "#"+"%06x" % random.randint(0, 0xFFFFFF)
        color_map[label]=rand_color

    return color_map

# from https://github.com/explosion/spacy-streamlit/util.py#L26
WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""

if query_input != '':
    data = {'text': query_input}
    with st.spinner('Predicting ...'):
        result = requests.post(url + 'query', data=json.dumps(data, ensure_ascii=False).encode('utf8'), headers=headers)

        entity_result = json.loads(result.text)
        for entity in entity_result:
            entity['label'] = entity['entity']

        labels = list(set(entity['entity'] for entity in entity_result))
        color_map = add_colormap(labels)

        bert_doc = {}
        bert_doc['text'] = query_input
        bert_doc['ents'] = entity_result
        bert_doc['title'] = None

        html = displacy.render(bert_doc, manual=True, style="ent", options={"colors": color_map})
        html = html.replace("\n", " ")
        st.write(WRAPPER.format(html), unsafe_allow_html=True)

        st.json(entity_result)

if st.button("Re-load"):
    requests.post(url + 'reload', headers=headers)
    st.write('rule reload finished!')
