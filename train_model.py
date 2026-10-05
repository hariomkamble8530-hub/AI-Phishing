import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# load dataset
data = pd.read_csv("spam.csv", encoding="latin-1")

# keep only useful columns
data = data[['v1','v2']]
data.columns = ['label','text']

# convert labels
data['label'] = data['label'].map({'ham':0,'spam':1})

X = data['text']
y = data['label']

# vectorize text
vectorizer = TfidfVectorizer(stop_words='english')
X_vector = vectorizer.fit_transform(X)

# train model
model = MultinomialNB()
model.fit(X_vector, y)

# save model
pickle.dump((model,vectorizer), open("phishing_model.pkl","wb"))

print("Model trained successfully")