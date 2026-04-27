import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kruskal

def temperature_summary(df_all):
    """Summary statistics for temperature across all countries."""
    return df_all.groupby('Country')['T2M'].agg([
        ('Mean', 'mean'),
        ('Median', 'median'),
        ('Std Dev', 'std'),
        ('Min', 'min'),
        ('Max', 'max')
    ]).round(3).sort_values('Mean', ascending=False)

def precipitation_summary(df_all):
    """Summary statistics for precipitation across all countries."""
    return df_all.groupby('Country')['PRECTOTCORR'].agg([
        ('Mean', 'mean'),
        ('Median', 'median'),
        ('Std Dev', 'std'),
        ('Min', 'min'),
        ('Max', 'max')
    ]).round(3).sort_values('Mean', ascending=False)

def kruskal_wallis_test(df_all):
    """Run Kruskal-Wallis test on T2M across all countries."""
    countries = df_all['Country'].unique()
    groups = [df_all[df_all['Country'] == c]['T2M'].dropna().values
              for c in countries]
    stat, p_value = kruskal(*groups)
    return stat, p_value

def vulnerability_ranking(df_all):
    """Rank countries by climate vulnerability."""
    countries = ['Sudan', 'Nigeria', 'Tanzania', 'Kenya', 'Ethiopia']
    data = []
    for country in countries:
        df_c = df_all[df_all['Country'] == country]
        data.append({
            'Country': country,
            'Mean_Temp_C': round(df_c['T2M'].mean(), 2),
            'Precip_Std': round(df_c['PRECTOTCORR'].std(), 2),
            'Extreme_Heat_Days': len(df_c[df_c['T2M_MAX'] > 35]),
            'Dry_Days': len(df_c[df_c['PRECTOTCORR'] < 1])
        })
    df_rank = pd.DataFrame(data)
    df_rank['Vulnerability_Rank'] = range(1, 6)
    return df_rank
