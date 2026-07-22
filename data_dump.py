import pymongo
import pandas as pd
import json

# Provide the mongodb localhost url to connect python to mongodb.
client = pymongo.MongoClient("mongodb+srv://tamimystic:zlA4kFQaXnODGAFa@cluster0.ymql190.mongodb.net/?appName=Cluster0")

DATA_FILE_PATH = "data/ai_student_impact_dataset.csv"
DATABASE_NAME = "AI_Impact_DB"
COLLECTION_NAME = "Students_Collection"

if __name__ == "__main__":
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns: {df.shape}")

    # Convert dataframe to json so that we can dump these record in mongo db
    df.reset_index(drop=True, inplace=True)

    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])
    
    # insert converted json record to mongo db
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    collection.insert_many(json_record)
    print("Data dumped successfully!")
