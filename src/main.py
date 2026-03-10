import openpyxl
import pandas as pd
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import config

file_path = '../data/MedianPricesofExistingDetachedHomesHistoricalData.xlsx'
wb = load_workbook(filename=file_path)

    
df = pd.read_excel(file_path, sheet_name="Median Price", header=7)

col_means = df.mean(numeric_only=True) #<class 'pandas.core.series.Series'>

bay_area_means = col_means[col_means.index.isin(config.bay_area_counties)]
other_means = col_means[~col_means.index.isin(config.bay_area_counties)]
other_avg = other_means.mean()

# Plotting the mean house prices
plt.figure(figsize=(12, 6))
plt.bar(bay_area_means.index, bay_area_means.values, label='Bay Area Counties')
plt.bar(['Other Counties Average'], [other_avg], color='orange')
plt.title("Mean House Prices by County")
plt.xlabel("County")
plt.ylabel("Mean House Prices ($)")
plt.xticks(rotation=45, ha='right')
plt.legend()
plt.tight_layout()
plt.savefig('../data/output_figures/mean_house_prices_bay_area_vs_other.png')
plt.show()

# Plotting the median house prices over time for Bay Area counties
plt.figure(figsize=(10, 5))
for county in config.bay_area_counties:
    plt.scatter(df["Mon-Yr"],df[county], label=county)
plt.xticks(rotation=45, ha='right')
plt.title("Median House Prices in Bay Area Counties Over Time")
plt.xlabel("Year-Month")
plt.ylabel("Median House Prices ($)")
plt.legend()
plt.savefig('../data/output_figures/over_time_median_house_prices_bay_area.png')
plt.show()



