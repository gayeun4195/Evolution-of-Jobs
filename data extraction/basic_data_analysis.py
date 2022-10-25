# basic analysis of saved table 'jobs'

import pandas as pd

file_name = 'hidden'
data = pd.read_csv(file_name, low_memory = False)

print(data.columns)
print(data.head(5))

# size of whole dataset
print('size of whole dataset: ', end = "")
print(len(data))
print()

# number of different titles
print('number of different titles: ', end = "")
print(len(data.title.unique()))

# top 10 titles
print('top 10 titles')
print(data['title'].value_counts().tail(20))
print()

# number of different user ids
print('number of different user ids: ', end = "")
print(len(data.person_identifier.unique()))

# top 10 users
print('top 10 users')
print(data['person_identifier'].value_counts().head(10))
print()

# number of valid data of 1) created_at 2) started_on 3) ended_on
print('created_at, started_on, ended_on: ', end = "")
print(len(data.loc[data['created_at']==data['created_at']]), len(data.loc[data['started_on']==data['started_on']]), len(data.loc[data['ended_on']==data['ended_on']]))

# number of current jobs
print(len(data.loc[data['is_current'] == True]))

print(data.loc[data['person_identifier']=='2c2e2af0-a4e7-e66f-6dbf-7526f7b537bc']['title'])