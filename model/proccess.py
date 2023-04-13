
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def ZScoreCapping(col, thr, dataset):
    
    new_dataset = dataset.copy()
    
    mean = new_dataset[col].mean()
    std = new_dataset[col].std()
    
    upper_bound = mean + thr*std
    lower_bound = mean - thr*std
    
    new_dataset[col] = np.where(new_dataset[col]>upper_bound, upper_bound,
            np.where(new_dataset[col]<lower_bound, lower_bound, new_dataset[col]))
    
    return new_dataset
    
def process_data():
    
    # Get and split dataset into training and test
    df = pd.read_csv("../data/medical-cost.csv")
    x_train, x_test, y_train, y_test = train_test_split(df.drop("charges", axis=1),df["charges"],test_size=0.2,random_state=45,shuffle=True)

    # Handle outlier in bmi feature
    x_train_bmi = ZScoreCapping("bmi", 3, x_train)
    x_test_bmi = ZScoreCapping("bmi", 3, x_test)

    # Preprocess Dataset
    _onehot = Pipeline([("one-hot-encode", OneHotEncoder(sparse=False))])
    _scale_bmi = Pipeline([("scale-bmi", StandardScaler())])    
    _scale_children = Pipeline([("scale-children", MinMaxScaler())])
    _scale_age = Pipeline([("scale-age", MinMaxScaler())])

    col = ColumnTransformer([("onehot-pipeline", _onehot, ["region","smoker","sex"]),("children-pipeline", _scale_children, ["children"]),("bmi-pipeline", _scale_bmi, ["bmi"]),("age-pipeline", _scale_age, ["age"])], remainder="passthrough")

    p_xtrain = col.fit_transform(x_train_bmi)
    p_xtest = col.transform(x_test_bmi)

    # Convert process dataset into Dataframe
    xtrain_data = pd.DataFrame(p_xtrain, columns=['x0_northeast', 'x0_northwest', 'x0_southeast', 'x0_southwest','x1_no', 'x1_yes', 'x2_female', 'x2_male','children','age', 'bmi'])
    xtest_data = pd.DataFrame(p_xtest, columns=['x0_northeast', 'x0_northwest', 'x0_southeast', 'x0_southwest','x1_no', 'x1_yes', 'x2_female', 'x2_male','children','age', 'bmi'])
    
    # Save Dataset
    return xtest_data, xtrain_data, y_test, y_train
