#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from IPython.display import display
import re #regex


# In[2]:


# Carrega o dataset original
data = pd.read_csv('ted_main.csv')
transcripts = pd.read_csv('transcripts.csv')


# In[3]:


print(data.columns)
display(data.head())
display(data.describe())


# In[4]:


print(transcripts.columns)
display(transcripts.head())
display(transcripts.describe())


# In[5]:


# Junta os dois (tomando cuidado porque não tem o transcript de todas)

# Inner_join, comparando os urls
merged = pd.merge(data, transcripts, left_on='url', right_on='url')


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

# Remove linhas que não tem transcrição ou que não tem o resumo
final_dataset.dropna()

display(final_dataset.head())
display(final_dataset.describe())


# In[7]:


# Salva
final_dataset.to_csv('../summarization/tedtalks.csv')
print("Done")

