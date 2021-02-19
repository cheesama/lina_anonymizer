import streamlit as st
import requests
import json

query_input = st.text_input('query:')

url = 'http://localhost:1881/query'
headers = {'content-type': 'application/json'}

if query_input != '':
    data = {'text': query_input}
    print (query_input)
    result = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode('utf8'), headers=headers)
    st.json(json.loads(result.text))


st.button("Re-load")
