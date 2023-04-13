
#Import Libries
from sklearn.ensemble import RandomForestRegressor
from proccess import process_data
import pickle

# Get Processed Datasets
_, xtrain_data, _, y_train = process_data()
  
# Train model
rfr = RandomForestRegressor(max_depth=80, min_samples_leaf=4, min_samples_split=3, n_estimators=300)
rfr.fit(xtrain_data, y_train)

#Save Module
pickle.dump(rfr, open("model.pkl","wb"))
