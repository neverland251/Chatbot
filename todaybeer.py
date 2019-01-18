class todaybeer():
    def __init__(self):
        self.vocabulary = self.pd.read_csv("색인사전.csv", engine="python", encoding="utf-8")

        self.vocabulary = self.vocabulary.to_dict(orient="records")[0]
        self.model = self.models.load_model("chatbot.model")
        self.model.trainable = False
        self.model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

    def engine(self, corpus):
        ### 문장 판단 부분 ###
        self.morphsVectored = list()
        corpusList = list()
        temporailyList = list()

        self.tests = self.twitter_tag.nouns(corpus)

        for i in self.tests:
            try:
                temporailyList.append(self.vocabulary[i])
            except KeyError:
                temporailyList.append(0)
        corpusList.append(temporailyList)
        self.vectorized_seq = self.sequence.pad_sequences(corpusList, maxlen=50)
        return_classes = self.model.predict_classes(self.vectorized_seq)
        return return_classes

    def save_corpus(self, corpus, return_classes):
        dbList = self.pd.read_csv("corpusDb.csv", engine="python", encoding="utf-8")
        userReturn = input("결과")
        raw = self.pd.DataFrame([{"text": corpus, "target": return_classes[0], "user_return": userReturn}])
        dbList = self.pd.concat([raw, dbList])
        dbList.to_csv("corpusDb.csv", encoding="utf-8", index=False)


class todaybeer_main(todaybeer):

    def __init__(self):
        from keras import models

        from keras.models import Sequential
        from keras.layers import Dense
        from keras.layers import Flatten
        from keras.layers import Embedding
        from keras.layers.convolutional import Conv1D
        from keras.layers.convolutional import MaxPooling1D
        from keras.layers import Dropout
        from keras.preprocessing import sequence
        from keras.layers import LSTM
        from keras.utils import np_utils
        from sklearn.model_selection import train_test_split
        from sklearn.feature_extraction.text import CountVectorizer
        import pandas as pd

        from pandas import DataFrame, Series
        import numpy as np

        import re

        import matplotlib as mpl
        import matplotlib.pyplot as plt
        import matplotlib.font_manager as fm

        import copy

        from konlpy.tag import Okt

        def vect_tokenizer(text):
            return twitter_tag.nouns(text)

        self.models = models
        self.twitter_tag = Okt()
        self.pd = pd
        self.sequence = sequence
        todaybeer.__init__(self)



