import os
import pandas as pd

basePath = "./data/output/data/"
uploadPath = "./data/latents/"

# def toJson(data):
#     return {
#         "success": True,
#         "data": data
#     }
def getALlData():
    files = os.listdir(basePath)

    merged_df = None
    for each in files:
        df = pd.read_csv(os.path.join(basePath, each))

        if merged_df is None: merged_df = df
        else: merged_df = pd.concat([merged_df, df], ignore_index=True)
    
    grouped_df = merged_df.groupby(['methods', 'datasets']).mean().reset_index()
    grouped_df = grouped_df.fillna(0)
    for col in grouped_df.select_dtypes(include=['float']).columns:
        grouped_df[col] = grouped_df[col].round(4)

    data =  grouped_df.to_dict(orient='records')
    return data

def getList(datatype):
    if datatype == "Integration Accuracy":
        file = "integration_accuracy.csv"
    elif datatype == "Batch Correction":
        file = "batch.csv"
    elif datatype == "Bio Conservation":
        file = "biomarker.csv"
    

    path = os.path.join(basePath, file)
    df = pd.read_csv(path)
    df["object_type"] = datatype
    data =  df.to_dict(orient='records')
    return data

def getListByName(file, name):
    path = os.path.join(basePath, file)
    df = pd.read_csv(path)
    filtered_records = df[df['methods'] == name]
    data =  filtered_records.to_dict(orient='records')
    return data

def uploadFile(uploadFiles):
    for file in uploadFiles:
        save_path = os.path.join(uploadPath, file.filename)
        file.save(save_path)
    