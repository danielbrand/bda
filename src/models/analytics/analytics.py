import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import magic
#import matplotlib.pyplot as plt
#import plotly
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import json
import uuid
import src.models.analytics.constants as AnalyticsConstants
from src.common.database import Database


class Dataset(object):
    def __init__(self, data, name, user_email, _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.data = data
        self.name = name
        self.user_email = user_email

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "user_email": self.user_email,
            "data": self.data,
        }

    def save_to_db(self):
        Database.insert(AnalyticsConstants.COLLECTION, self.json())

    @staticmethod
    def save_data(dataset, user_email):
        #file_type = magic.from_file(dataset.seek(0), mime=True)
        #q = "csv"
        #if q in file_type:
        #    data = pd.read_csv(dataset)
        #else:
        #    data = pd.read_excel(dataset)

        data = pd.read_csv(dataset)
        data_json = json.loads(data.to_json(orient='records'))
        Dataset(data_json, dataset.filename, user_email).save_to_db()
        return True

    @staticmethod
    def prediction_score(dataset):
        data = dataset
        data = data.dropna(axis=0)
        X = data.drop("churn", axis=1)
        y = data["churn"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

        rfc = RandomForestClassifier()
        rfc.fit(X_train, y_train)
        return rfc.score(X_test, y_test)

    @staticmethod
    def basic_statistics(dataset):
        data = dataset
        data = data.dropna(axis=0)

        nr_of_columns = len(data.columns)
        nr_of_rows = len(data.index)

        return nr_of_rows, nr_of_columns

    @staticmethod
    def retrieve_data():
        mongo_data = Dataset.list_all()
        overview_list = []
        for md in mongo_data:
            md_name = md.name
            md_id = md._id
            md_user_email = md.user_email

            df = pd.DataFrame.from_records(Database.find(AnalyticsConstants.COLLECTION, {}))
            df2 = pd.DataFrame(columns=df.columns)
            df2_index = 0
            for row in df.iterrows():
                one_row = row[1]
                for list_value in row[1]["data"]:
                    one_row["data"] = list_value
                    df2.loc[df2_index] = one_row
                    df2_index += 1

            df_data = pd.json_normalize(df2["data"])

            pred_acc = Dataset.prediction_score(df_data)
            nr_of_rows, nr_of_columns = Dataset.basic_statistics(df_data)

            overview_list.append({'name': md_name,
                                  'id': md_id,
                                  'user_email': md_user_email,
                                  'acc': pred_acc,
                                  'rows': nr_of_rows,
                                  'columns': nr_of_columns})
        return overview_list

    @classmethod
    def get_by_name(cls, dataset_name):
        return cls(**Database.find_one(AnalyticsConstants.COLLECTION, {"name": dataset_name}))

    @classmethod
    def list_all(cls):
        return [cls(**elem) for elem in Database.find(AnalyticsConstants.COLLECTION, {})]

    @classmethod
    def all(cls):
        return cls(**Database.find(AnalyticsConstants.COLLECTION, {}))

    @classmethod
    def find_by_user_email(cls, user_email):
        return [cls(**elem) for elem in Database.find(AnalyticsConstants.COLLECTION, {'user_email': user_email})]