import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

import seaborn as sns
from pathlib import Path


csv_path = './data/processed/csv_files/serum_ferritin.csv'
df = pd.read_csv(csv_path)

df['Date'] = pd.to_datetime(df['collect_time'])
df['Result'] = pd.to_numeric(df['serum_ferritin'], errors='coerce')
df = df.sort_values('Date')

plt.figure(figsize=(10, 6))

sns.lineplot(data=df, x='Date', y='Result', markers='o')

plt.axhspan(13, 150, color='green', alpha=0.1, label='Normal Range')

plt.title('Serum Ferritin Trend')
plt.xticks(rotation=45)
plt.tight_layout()

output_img = Path("./test_output/trend_chart.png")
plt.savefig(output_img)