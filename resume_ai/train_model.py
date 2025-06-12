import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge  
from sklearn.pipeline import Pipeline

df = pd.read_csv('resume_ai/data/resume_dataset.csv')  

X = df['resume_text']
y = df['score']  
model = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('reg', Ridge(alpha=1.0))  
])

model.fit(X, y)

joblib.dump(model, 'resume_ai/model/resume_score_model.pkl')
print("✅ Exact-score regression model trained and saved.")
