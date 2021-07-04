from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from sklearn.neighbors import KNeighborsClassifier
nltk.download('punkt')

model = None
counter = 0

class Model:
    def __init__(self):
        self.model_pipeline_status = Pipeline([
            ("vectorizer", TfidfVectorizer(tokenizer=lambda x: self.tokenize_sentence(x))),
            ("model", LogisticRegression(random_state=0))
        ])
        self.model_pipeline_rating = Pipeline([
            ("vectorizer", TfidfVectorizer(tokenizer=lambda x: self.tokenize_sentence(x))),
            ("model", KNeighborsClassifier(n_neighbors=8))
        ]
        )
        self.stop_words = []
        with open(r'imdb.vocab', 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.stop_words.append(line.strip())

    def tokenize_sentence(self, sentence: str):
        global counter
        snowball = SnowballStemmer(language="english")
        tokens = word_tokenize(sentence, language="english")
        tokens = [snowball.stem(i) for i in tokens if i not in string.punctuation]
        counter += 1
        print("Iteration:", counter)
        return tokens

    def train(self):
        train_df = pd.read_csv(r'df_train.csv', sep=',')
        train_df['rating'].apply(int)
        train_df['status'].apply(int)

        self.model_pipeline_rating.fit(train_df["comment"], train_df['rating'])
        self.model_pipeline_status.fit(train_df["comment"], train_df["status"])

    def comment_checking(self, comment):
        res = self.model_pipeline_status.predict([comment])
        if res == [0]:
            return "Status: negative", "Rating: " + str(self.model_pipeline_rating.predict([comment])[0])
        elif res == [1]:
            return "Status: positive", 'Rating: ' + str(self.model_pipeline_rating.predict([comment])[0])
        else:
            return "Error"
