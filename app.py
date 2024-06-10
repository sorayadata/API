# Import packages
import numpy as np
#!/Users/soraya/Desktop/dernier/API/env/bin/python

import pandas as pd
from flask import Flask, jsonify, request
import pickle
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)


# Scaler instance
scaler = StandardScaler()

# CHARGEMENT DES DONNEES
data = pd.read_csv('test_df_sample.csv', nrows=10000)
data_scaled = data.copy()
numeric_columns = data_scaled.iloc[:, 1:].select_dtypes(include=[np.number]).columns
data_scaled[numeric_columns] = scaler.fit_transform(data_scaled[numeric_columns])

model = pickle.load(open('model.pkl', 'rb'))

# API welcome function
@app.route("/")
def welcome():
    res = "Hello world! Welcome to the falask API!"
    return jsonify(res)

# Function returning all client IDs
@app.route("/client_list", methods=["GET"])
def load_client_id_list():
    id_list = data["SK_ID_CURR"].tolist()
    return jsonify(id_list)

# # Function returning personal informaton of a given client (age, annuity amount, credit amount, total income amount)
@app.route("/client", methods=["GET"])
def load_client():
    
    client_id = int(request.args.get("id"))
    client = data[data["SK_ID_CURR"] == int(client_id)]
    
    if(client.size>0):
    
        DAYS_BIRTH = client['DAYS_BIRTH']
        AMT_INCOME_TOTAL = client['AMT_INCOME_TOTAL']
        AMT_CREDIT = client['AMT_CREDIT']
        AMT_ANNUITY = client['AMT_ANNUITY']
        
        return jsonify(DAYS_BIRTH=int(DAYS_BIRTH), AMT_INCOME_TOTAL=float(AMT_INCOME_TOTAL), AMT_CREDIT=float(AMT_CREDIT), AMT_ANNUITY=float(AMT_ANNUITY))


# Function returning, for a given informaton, the values of all clients (age, annuity amount, credit amount, total income amount)
@app.route("/data", methods=["GET"])
def load_data():
    col = request.args.get("col")
    data_col = data[col]
    data_list = data_col.tolist()
    return jsonify(data_list)

# Function returning, for a given client, the default probabiliy (in terms of percentage of default/no default)
@app.route("/predict_default", methods=["GET"])
def predict_default():
    
    id_client = int(request.args.get("id_client"))
    
    client = data_scaled.loc[data_scaled["SK_ID_CURR"] == id_client]
    client = client.iloc[:,1:]
    if(client.shape[0]==1):
        X = client.to_numpy()
        proba = model.predict_proba(X)[0]
        proba_0 = proba[0]  # No default
        proba_1 = proba[1]  # Default
        
        res = dict({'proba_0':proba_0, 'proba_1':proba_1})
        
    return jsonify(res)
    
if __name__ == "__main__":     
    app.run(host="127.0.0.1", port=5000)   
    
                                        