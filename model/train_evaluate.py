
#Import Libries
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error

#Import custom function
from proccess import process_data

def evaluate_model(ypred, ytest):
        
    """
    This method suppose to evaluate our models
    and return its results.
    Args:
        ypred: The predicted values
        ytest: The actual test value
    """
    #Evaluate mean absolute error
    mae = round(mean_absolute_error(y_true=ytest, y_pred=ypred), 3)
        
    #Evaluate mean absolute percentage error
    mape = round(mean_absolute_percentage_error(y_true=ytest,y_pred=ypred),3)
        
    #Evaluate r2
    r_squared = round(r2_score(y_true=ytest, y_pred=ypred),3)
    
    #Return results
    return mae, mape, r_squared

def train_model():
    
    # Get Datasets
    xtest_data, xtrain_data, y_test, y_train = process_data()
  
    # Train model
    rfr = RandomForestRegressor(max_depth=80, min_samples_leaf=4, min_samples_split=3, n_estimators=300)
    rfr.fit(xtrain_data, y_train)
    ypred = rfr.predict(xtest_data)

    #Evaluate model
    mae, mape, r2 = evaluate_model(ypred=ypred, ytest=y_test)
    evaluated_results = {"mae": mae, "mape": mape, "r2": r2}

    return evaluated_results

print(train_model())