import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import config as cg
import numpy as np

def read_data():
    data = cg.median_prices_dataset
    df = pd.read_excel(data, sheet_name="Median Price", header=7)
    return df


def get_nan_counts(df):
    for county in cg.bay_area_counties:
        nan_count = df[county].isna().sum()
        if nan_count > 0:
            print(f"{county}: {nan_count} NaN values")
    return None

def format_data(df):
    df['Mon-Yr'] = pd.to_datetime(df['Mon-Yr'], format='%b-%y')
    df['Mon-Yr'] = df['Mon-Yr'].map(lambda x: x.toordinal())
    return df


def fit_liner_regression(df, county):
    X = df['Mon-Yr'].values.reshape(-1, 1)
    #option 1: fill NaN values with mean
    y = df[county].fillna(df[county].mean()).values
    # #option 2: fill NaN values with forward fill
    # y = df[county].fillna(method='ffill').values
    # #option3: drop NaN values
    # county_df = df[['Mon-Yr', county]].dropna()
    # #option 4: 
    # if df[county].isna().sum() > 0.2 * len(df):  # skip if >20% missing
    #     print(f"Skipping {county} — too many NaNs")
    #     continue
    
    model = LinearRegression().fit(X, y)
    
    print(county, model.coef_, model.intercept_)
    
    #Get the prediction
    y_pred = model.predict(X)
    
    # Get the fitting metrics
    mape = mean_absolute_error(y, y_pred)
    r2 = r2_score(y,y_pred)
    
    # Get the slope of the trend line
    slope = model.coef_[0]
    
    mean = np.mean(y)
    
    return slope, mape, mean, r2

if __name__ == "__main__":
    median_df = format_data(read_data())
    get_nan_counts(median_df)

    location_dict = {}
    for county in cg.bay_area_counties:
        location_dict[county] = fit_liner_regression(median_df, county)
    lr_df = pd.DataFrame(location_dict).transpose()
    lr_df = lr_df.rename(columns = {0:'gradient',1:'mae',2:'mean',3:'r2_score'})
    lr_df['mape'] = lr_df['mae']/lr_df['mean']

    print(lr_df)