
import os
import pickle
from usermodel import UsersData
from azure.storage.blob import BlobClient
from sklearn.preprocessing import StandardScaler
from azure.identity import DefaultAzureCredential

token_credential = DefaultAzureCredential()

#Set Environment Variables
STORAGE_ACCOUNT_URL=os.getenv("STORAGE_ACCOUNT_URL")
STORAGE_ACCOUNT_CONTAINER_NAME=os.getenv("STORAGE_ACCOUNT_CONTAINER_NAME")

class PredictCharges:
    
    @staticmethod
    def download_model():

        #Initialize Blob client
        blob_client = BlobClient(STORAGE_ACCOUNT_URL,container_name=STORAGE_ACCOUNT_CONTAINER_NAME, blob_name="model.pkl", credential=token_credential)

        # Download model
        with open("./model.pkl", "wb") as my_blob:
            blob_data = blob_client.download_blob()
            blob_data.readinto(my_blob)
    
    @staticmethod
    def prepare_dataset(usr:UsersData):
        
        # Does User Smokes
        if usr.Smoker == "no":
            x1_no = 1
            x1_yes = 0
        else:
            x1_no = 0
            x1_yes = 1
    
        # Get region user belongs to
        if usr.Region == "northeast":
            x0_northeast = 1
            x0_northwest = 0
            x0_southeast = 0
            x0_southwest = 0

        elif usr.Region == "northwest":
            x0_northeast = 0
            x0_northwest = 1
            x0_southeast = 0
            x0_southwest = 0
    
        elif usr.Region == "southeast":
            x0_northeast = 0
            x0_northwest = 0
            x0_southeast = 1
            x0_southwest = 0
    
        else:
            x0_northeast = 0
            x0_northwest = 0
            x0_southeast = 0
            x0_southwest = 1

        # Get users Gender
        if usr.Gender == "male":
            x2_female = 1
            x2_male = 0

        else:
            x2_female = 0
            x2_male = 1
    
        # Prepare dataset for prediction
        scl = StandardScaler()
        scaled_dataset = scl.fit_transform([[usr.Children, usr.Age, usr.Bmi]])

        children = scaled_dataset[0][0]
        age = scaled_dataset[0][1]
        bmi = scaled_dataset[0][2]

        data = [[x0_northeast, 
                 x0_northwest, 
                 x0_southeast, 
                 x0_southwest, 
                 x1_no,x1_yes, 
                 x2_female, 
                 x2_male, 
                 children, 
                 age,bmi]]

        return data
    
    @classmethod
    def make_prediction(cls, dataset):

        if os.path.exists("model.pkl"):

            #Load model to make prediction
            model = pickle.load(open("model.pkl","rb"))

        else:

            cls.download_model()
            model = pickle.load(open("model.pkl","rb"))

        #Make prediction
        response = model.predict(dataset)
        print(response)

        #Return results
        os.remove("model.pkl")
        return {"Predicted": round(response[0],3)} 
        