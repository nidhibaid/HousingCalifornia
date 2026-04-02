from trend import read_data, get_nan_counts, format_data
import config as cg
import matplotlib.pyplot as plt

def plot_boxplot(df):
    plt.figure(figsize=(18, 6))
    df[cg.bay_area_counties].boxplot()
    plt.title("Box Plot of Median House Prices in Bay Area Counties")
    plt.ylabel("Median House Prices ($)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('../data/output_figures/box_plot_median_house_prices_bay_area.png')
    plt.show()

if __name__ == "__main__":
    median_df = format_data(read_data())
    get_nan_counts(median_df)
    
    print(median_df[cg.bay_area_counties].describe())

    plot_boxplot(median_df)
    

    
    
    