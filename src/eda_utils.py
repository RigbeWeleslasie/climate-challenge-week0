import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def missing_value_report(df):
    """Generate missing value report."""
    missing = df.isna().sum()
    pct = (missing / len(df)) * 100
    return pd.DataFrame({'Missing Count': missing, 'Missing %': pct})

def detect_outliers(df, cols):
    """Detect outliers using Z-score method."""
    z_scores = np.abs(stats.zscore(df[cols].dropna()))
    outlier_mask = pd.DataFrame(z_scores > 3, columns=cols)
    return outlier_mask.sum()

def plot_temperature_timeseries(df, country):
    """Plot monthly average temperature time series."""
    monthly_temp = df.groupby(df['Date'].dt.to_period('M'))['T2M'].mean()
    monthly_temp.index = monthly_temp.index.to_timestamp()
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(monthly_temp.index, monthly_temp.values, color='tomato', linewidth=1.5)
    warmest = monthly_temp.idxmax()
    coolest = monthly_temp.idxmin()
    ax.annotate(f'Warmest\n{warmest.strftime("%b %Y")}\n{monthly_temp.max():.1f}C',
                xy=(warmest, monthly_temp.max()),
                xytext=(warmest, monthly_temp.max() + 1),
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=9, color='red', ha='center')
    ax.annotate(f'Coolest\n{coolest.strftime("%b %Y")}\n{monthly_temp.min():.1f}C',
                xy=(coolest, monthly_temp.min()),
                xytext=(coolest, monthly_temp.min() - 1),
                arrowprops=dict(arrowstyle='->', color='blue'),
                fontsize=9, color='blue', ha='center')
    ax.set_title(f'{country} - Monthly Average Temperature (2015-2026)')
    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature (C)')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig

def plot_precipitation_barchart(df, country):
    """Plot monthly total precipitation bar chart."""
    monthly_precip = df.groupby(df['Date'].dt.to_period('M'))['PRECTOTCORR'].sum()
    monthly_precip.index = monthly_precip.index.to_timestamp()
    fig, ax = plt.subplots(figsize=(14, 5))
    colors = ['steelblue' if v < monthly_precip.quantile(0.75) else 'darkblue'
              for v in monthly_precip.values]
    ax.bar(monthly_precip.index, monthly_precip.values, color=colors, width=20)
    peak = monthly_precip.idxmax()
    ax.annotate(f'Peak\n{peak.strftime("%b %Y")}\n{monthly_precip.max():.1f}mm',
                xy=(peak, monthly_precip.max()),
                xytext=(peak, monthly_precip.max() + 20),
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=9, color='red', ha='center')
    ax.set_title(f'{country} - Monthly Total Precipitation (2015-2026)')
    ax.set_xlabel('Date')
    ax.set_ylabel('Precipitation (mm)')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    return fig

def plot_correlation_heatmap(df, country):
    """Plot correlation heatmap."""
    cols = ['T2M','T2M_MAX','T2M_MIN','T2M_RANGE',
            'PRECTOTCORR','RH2M','WS2M','WS2M_MAX','PS','QV2M']
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(df[cols].corr(), annot=True, fmt='.2f',
                cmap='RdYlGn', center=0, square=True, ax=ax)
    ax.set_title(f'{country} - Correlation Matrix')
    plt.tight_layout()
    return fig
