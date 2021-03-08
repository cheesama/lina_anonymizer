from tqdm import tqdm

import json
import meta_db_client

'''
with open('regex.json', 'r') as regexFile:
    regexes = json.load(regexFile)
    print (regexes[0])

    for regex in regexes:
        item = {}
        item['entity'] = regex['entity']
        item['pattern'] = regex['pattern']
        item['anonymization'] = False

        result = meta_db_client.post('regexes', item)
        print (result)

with open('regex_combination.json', 'r') as regexFile:
    regexes = json.load(regexFile)
    print (regexes[0])

    for regex in regexes:
        item = {}
        item['entity'] = regex['entity']
        item['combination'] = regex['combination']
        item['anonymization'] = False

        result = meta_db_client.post('regex-combinations', item)
        print (result)
'''

with open('personal_information.json', 'r') as regexFile:
    regexes = json.load(regexFile)
    print (regexes[0])

    for regex in regexes:
        item = {}
        item['entity'] = regex['entity']
        item['pattern'] = regex['pattern']
        item['anonymization'] = True

        result = meta_db_client.post('regexes', item)
        print (result)


