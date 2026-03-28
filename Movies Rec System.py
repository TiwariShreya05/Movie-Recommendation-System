
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


movies=pd.read_csv('tmdb_5000_movies.csv.csv')
credits=pd.read_csv('tmdb_5000_credits.csv.csv')


# In[3]:


movies.head(1)


# In[4]:


credits.head(1)


# In[5]:


movies=movies.merge(credits,on='title')


# In[6]:


movies.head(1)


# In[ ]:


print(type(movies))
print(type(credits))


# In[8]:


movies['original_language'].value_counts()


# In[9]:


movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]


# In[10]:


movies.head(5)


# In[13]:


movies.isnull().sum()


# In[12]:


movies.dropna(inplace=True)


# In[14]:


movies.duplicated().sum()


# In[15]:


movies.iloc[0].genres


# In[ ]:


import ast
ast.literal_eval('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')


# In[26]:


def convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L    
        


# In[21]:


import ast
ast.literal_eval('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')


# In[37]:


movies['genres']=movies['genres'].apply(convert)


# In[29]:


movies.head()


# In[31]:


movies['keywords']=movies['keywords'].apply(convert)


# In[32]:


movies.head()


# In[78]:


def convert3(obj):
    L = []
    counter = 0
    try:
        for i in ast.literal_eval(obj):
            if counter == 3:
                break
            L.append(i['name'])
            counter += 1
        return L
    except:
        return []


# In[79]:


movies['cast'] = movies['cast'].apply(convert3)


# In[69]:


movies.head()


# In[82]:


def fetch_director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            L.append(i['name'])
            break
    return L   


# In[83]:


movies['crew']=movies['crew'].apply(fetch_director)


# In[84]:


movies.head()


# In[85]:


movies['overview']=movies['overview'].apply(lambda x:x.split())


# In[86]:


movies.head()


# In[87]:


movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])


# In[88]:


movies.head()


# In[89]:


movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']


# In[90]:


movies.head()


# In[91]:


new_df=movies[['movie_id','title','tags']]


# In[92]:


new_df


# In[93]:


new_df['tags']=new_df['tags'].apply(lambda x:" ".join(x))


# In[94]:


new_df.head()


# In[95]:


new_df['tags'][0]


# In[100]:


new_df['tags']=new_df['tags'].apply(lambda x:x.lower())


# In[101]:


new_df.head()


# In[118]:


get_ipython().system('pip install nltk')


# In[120]:


import nltk


# In[122]:


from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()


# In[123]:


def stem(text):
    y=[]
    
    for i in text.split():
        y.append(ps.stem(i))
        
    return " ".join(y)    


# In[131]:


new_df['tags']=new_df['tags'].apply(stem)


# In[132]:


new_df['tags'][0]


# In[133]:


from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000,stop_words='english')


# In[134]:


vectors=cv.fit_transform(new_df['tags']).toarray()


# In[135]:


vectors


# In[136]:


vectors[0]


# In[137]:


len(cv.get_feature_names())


# In[138]:


cv.get_feature_names()


# In[129]:


stem('in the 22nd century, a paraplegic marine is dispatched to the moon pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization. action adventure fantasy sciencefiction cultureclash future spacewar spacecolony society spacetravel futuristic romance space alien tribe alienplanet cgi marine soldier battle loveaffair antiwar powerrelations mindandsoul 3d jamescameron')


# In[140]:


from sklearn.metrics.pairwise import cosine_similarity


# In[142]:


similarity=cosine_similarity(vectors).shape


# In[143]:


similarity=cosine_similarity(vectors)


# In[155]:



sorted(list(enumerate(similarity[1])),reverse=True,key=lambda x:x[1])[1:11]


# In[150]:


new_df[new_df['title']=='Avatar'].index[0]


# In[151]:


new_df[new_df['title']=='Batman Begins'].index[0]


# In[158]:


def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    
    for i in movies_list:
        print(i[0])


# In[159]:


recommend('Avatar')


# In[160]:


new_df.iloc[1216].title


# In[188]:


def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    for i in movies_list:
        print(new_df.iloc[i[0]].title)
        


# In[189]:


recommend('Avatar')


# In[190]:


recommend('Batman Begins')


# In[191]:


import pickle


# In[192]:


pickle.dump(new_df,open('movies.pkl','wb'))


# In[193]:


new_df['title'].values


# In[194]:


new_df.to_dict()


# In[195]:


pickle.dump(new_df.to_dict(),open('movies_dict.pkl','wb'))


# In[196]:


pickle.dump(similarity, open('similarity.pkl', 'wb'))


# In[197]:


import pickle
import pandas as pd

print("Pandas version:", pd.__version__)

# Recreate pickle files
movies_dict = new_df.to_dict()

with open('movies.pkl', 'wb') as f:
    pickle.dump(movies_dict, f, protocol=4)

with open('similarity.pkl', 'wb') as f:
    pickle.dump(similarity, f, protocol=4)

# Show where files were saved
import os
print("Files saved in:", os.getcwd())


# In[198]:


# Save as CSV instead of pickle
new_df.to_csv('movies.csv', index=False)

# For similarity, save as numpy
import numpy as np
np.save('similarity.npy', similarity)


# In[3]:


def precision_at_k(recommended_list, true_relevant_list, k=5):
    top_k = recommended_list[:k]
    relevant_in_top_k = [m for m in top_k if m in true_relevant_list]
    return len(relevant_in_top_k) / k

# Example Usage:
true_matches = ["The Dark Knight", "The Dark Knight Rises", "Batman", "Batman v Superman: Dawn of Justice"]
recommended = ["The Dark Knight", "Batman", "10th & Wolf", "Synecdoche, New York", "Batman"]
print(f"Precision@5: {precision_at_k(recommended, true_matches, k=5)}")


# In[17]:


import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

ConfusionMatrixDisplay.from_predictions(y_true, y_pred)
plt.show()


# In[14]:




