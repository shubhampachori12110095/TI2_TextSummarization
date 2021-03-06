#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from IPython.display import display
import re # regex
import numpy as np
from nltk import tokenize


# In[2]:


# Carrega o dataset original da pasta data/
data = pd.read_csv('../data/ted_main.csv')
transcripts = pd.read_csv('../data/transcripts.csv')


# In[3]:


# Dá uma olhada nos dados
print(data.columns)
display(data.head())
display(data.describe())


# In[4]:


# Dá uma olhada nos dados
print(transcripts.columns)
display(transcripts.head())
display(transcripts.describe())


# In[5]:


# Junta os dois (tomando cuidado porque não tem o transcript de todos)

# Inner_join, comparando os urls
merged = pd.merge(data, transcripts, left_on='url', right_on='url', how='inner')


# In[6]:


def remove_tags(transcript):
    # (...)|(...)|(...) = qualquer uma das coisas entre parenteses
    # \( e \) = um parêntese, literalmente (sem o "\" tem outro significado em regex)
    # [^\)]* = qualquer coisa que não for parentese que fecha, n vezes
    regex = re.compile(r"(\(Music[^\)]*\))|(\(Applause[^\)]*\))|(\(Laughter[^\)]*\))", re.IGNORECASE)
    return regex.sub(" ", transcript).strip() #Remove os lugares em que der match com a regex
    
# Deixa só as colunas que nós vamos usar
final_dataset = pd.DataFrame()

final_dataset['transcript'] = merged['transcript'].apply(remove_tags)
final_dataset['summary'] = merged['description']

# Remove as linhas que não tem transcrição ou que não tem o resumo
final_dataset['transcript'].replace('', np.nan, inplace=True)
final_dataset['summary'].replace('', np.nan, inplace=True)
final_dataset = final_dataset.dropna()

display(final_dataset.head())
display(final_dataset.describe())


# In[7]:


# Salva
final_dataset.to_csv('../data/final_dataset.csv')
print("Done")

