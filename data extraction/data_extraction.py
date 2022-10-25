# get 'jobs' table from CrunchBase
# using CrunchBase API
# save as dataframe (.csv file)

import requests
import json
import pandas as pd
from datetime import datetime

entities = []

user_key = 'hidden'

headers = {
    'accept': 'application/json',
    'X-cb-user-key': user_key,
}

json_data = {
    'field_ids': [
        'uuid',
        'title',
        'is_current',
        'started_on',
        'ended_on',
        'created_at',
        'updated_at',
        'job_type',
        'person_identifier',
    ],
    'order': [
        {
            'field_id': 'uuid',
            'sort': 'asc',
            'nulls': 'last',
        },
    ],
    'limit': 1000,
}

columns = {'uuid', 'title', 'is_current', 'started_on', 'ended_on', 'created_at', 'updated_at', 'job_type', 'person_identifier'}
datetime_format1 = "%Y-%m-%dT%H:%M:%SZ"
datetime_format2 = "%Y-%m-%d"

now = datetime.now()
file_name = str(now.date()) + '.csv'
print(file_name)

while True:
    response = requests.post('https://api.crunchbase.com/api/v4/searches/jobs', headers=headers, json=json_data)

    json_result = json.loads(response.text)
    json_data['after_id'] = json_result['entities'][-1]['uuid']

    entities = entities + json_result['entities']
    print(len(entities), len(json_result['entities']))

    if len(json_result['entities']) < 1000:
        result = []
        for i in range(len(entities)):
            each_data = entities[i]['properties']
            dict_data = {}
            for c in columns:
                if c in each_data:
                    if c == 'person_identifier':
                        if 'uuid' in each_data[c]:
                            dict_data[c] = each_data[c]['uuid']
                        else:
                            dict_data[c] = None
                    elif str(type(each_data[c])) == "<class 'dict'>":
                        if 'value' in each_data[c]:
                            # save only date (without precision)
                            dict_data[c] = each_data[c]['value']
                        else:
                            dict_data[c] = None
                    else:    
                        dict_data[c] = each_data[c]

                    if dict_data[c]:
                        if c == 'started_on' or c == 'ended_on' or c == 'created_at' or c == 'updated_at':
                            if 'T' in dict_data[c]:
                                dict_data[c] = datetime.strptime(dict_data[c], datetime_format1)
                            else:
                                # save only date
                                dict_data[c] = datetime.strptime(dict_data[c], datetime_format2)
                else:
                    dict_data[c] = None
            result.append(dict_data)

        # save file as dataframe
        df_result = pd.DataFrame(result)
        df_result.to_csv(file_name)

        break
