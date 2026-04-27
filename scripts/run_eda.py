"""
Main script to run the full climate EDA pipeline.
Usage: python scripts/run_eda.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import load_country_data, load_all_countries
from src.eda_utils import (missing_value_report, detect_outliers,
                           plot_temperature_timeseries,
                           plot_precipitation_barchart)
from src.comparison import (temperature_summary, precipitation_summary,
                            kruskal_wallis_test, vulnerability_ranking)

def main():
    print("Starting Climate EDA Pipeline...")
    print("Loading all country datasets...")
    df_all = load_all_countries('data')

    print("\nTemperature Summary:")
    print(temperature_summary(df_all))

    print("\nPrecipitation Summary:")
    print(precipitation_summary(df_all))

    print("\nKruskal-Wallis Test:")
    stat, p = kruskal_wallis_test(df_all)
    print(f"Statistic: {stat:.4f}, P-value: {p:.10f}")

    print("\nVulnerability Ranking:")
    print(vulnerability_ranking(df_all))
    print("\nEDA Pipeline Complete!")

if __name__ == "__main__":
    main()
