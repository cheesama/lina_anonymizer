from tqdm import tqdm
from datetime import datetime
from fastapi import FastAPI
from itertools import product

import os, sys
import random
import re
import json
import requests
import multiprocessing
import operator

headers = {'accept': 'application/json', 'content-type': 'application/json'}

endpoint = os.getenv('META_ENDPOINT')
assert endpoint is not None

def request_to_server(method="get", url=None, data=None, headers=None):
    assert method in ["get", "post", "put", "delete"]

    data = json.loads(json.dumps(data))
    
    if method == "get":
        response = requests.get(endpoint + url, headers=headers)
    elif method == "put":
        response = requests.put(endpoint + url, headers=headers, json=data)
    elif method == "post":
        response = requests.post(endpoint + url, headers=headers, json=data)
    elif method == "delete":
        response = requests.delete(endpoint + url, headers=headers)

    response.encoding = None
        
    return json.loads(response.text)

# get data from url(table)
def get(url, max_num=-1):
    cnt = request_to_server('get', '{}/count'.format(url))
    if cnt == 'Not Found':
        raise ConnectionError("Strapi api failed")

    res = []
    start, iter_num = 0, 50
    len_ = 0
    pbar = tqdm(total=cnt, position=0, leave=True, desc="Downloading data : " +  url)
    while len_ < int(cnt):
        tmp_ids = request_to_server('get', url='{}?_start={}&_limit={}'.format(url, start, iter_num))
        res.extend(tmp_ids)
        start += iter_num
        len_ += len(tmp_ids)
        pbar.update(len(tmp_ids))

        if 0 < max_num and max_num < len_:
            break

    pbar.close()

    return res

app = FastAPI()
is_ready = False

patterns = {}
patterns_anonymization_flag = {}
model_version = datetime.today().strftime("%Y-%m-%d")

def load_rules():
    global patterns
    global patterns_anonymization_flag
    global model_version

    ## collect single pattern
    single_patterns = get("regexes")
    for pattern in single_patterns:
        patterns[pattern["entity"]['entity']] = pattern["pattern"]
        patterns_anonymization_flag[pattern['entity']['entity']] = pattern['anonymization']

    ## collect combination pattern
    combination_patterns = get("regex-combinations")
    for combination in combination_patterns:
        gen_regex_comb = []
        for _, pattern_list in combination["combination"].items():
            gen_regex = []
            for each_pattern in pattern_list:
                gen_regex.append(patterns[each_pattern].split("|"))
            gen_regex_comb += ["\\s*".join(regex) for regex in list(product(*gen_regex))]

        patterns[combination["entity"]['entity']] = "|".join(gen_regex_comb)
        patterns_anonymization_flag[combination['entity']['entity']] = combination['anonymization']

    print(f"total patterns: {len(patterns)}")
    for k, v in patterns.items():
        print(f"{k}:\t{v}")

    model_version = datetime.today().strftime("%Y-%m-%d")
    is_ready = True

load_rules()

# endpoints
@app.get("/")
async def health():
    if is_ready:
        output = {"code": 200}
    else:
        output = {"code": 500}

    return output

@app.post("/reload")
async def reload_rules():
    try:
        load_rules()
        return {"code":200}
    except:
        return {"code":500}

@app.post("/predict")
async def match_rule_entities(text: str):
    extracted = []

    print (f'query: {text}')

    print (patterns)

    for k, v in patterns.items():
        matches = re.finditer(pattern=v, string=text)
        for match in matches:
            entity = {
                "start": match.start(),
                "end": match.end(),
                "value": match.group(),
                "confidence": 1.0,
                "entity": k,
                "extractor": "rule-entity-extractor",
                "model_version": model_version,
                "anonymization": patterns_anonymization_flag[k]
            }
            extracted.append(entity)

    if len(extracted) == 1:
        return extracted

    # organize overlapped entities
    remove_overlapped = []
    extracted.sort(key=lambda x: len(x.get("value")), reverse=True)
    for i, target_entity in enumerate(extracted):
        for j, compare_entity in enumerate(extracted):
            #if i == j: continue

            if (
                compare_entity["start"] <= target_entity["start"]
                and target_entity["end"] < compare_entity["end"]
            ) or (
                compare_entity["start"] < target_entity["start"]
                and target_entity["end"] <= compare_entity["end"]
            ):
                break

            if j == len(extracted) - 1:
                remove_overlapped.append(target_entity)

    remove_overlapped.sort(key=operator.itemgetter('start'))
    print (remove_overlapped)

    return remove_overlapped
