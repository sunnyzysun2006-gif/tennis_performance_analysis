from scipy.stats import pearsonr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Next, we want to analyze how age correlates with clutch performance

# Load clutch performance data from sql query output
df_clutch = pd.read_csv('age_performance.csv')

# Break Points Saved Percentage (BPS%)
df_clutch['BPS_pct'] = (
    df_clutch['total_bp_saved'].astype('float') /
    df_clutch['total_bp_faced_as_server']
) * 100

# Break Points Converted Percentage (BPC%)
df_clutch['BPC_pct'] = (
    df_clutch['total_bp_converted'].astype('float') /
    df_clutch['total_bp_opportunities']
) * 100

# Calculate Pearson correlation between age and BPS%
corr_bps, p_bps = pearsonr(df_clutch['age_estimate'], df_clutch['BPS_pct'])

# Calculate Pearson correlation between age and BPC%
corr_bpc, p_bpc = pearsonr(df_clutch['age_estimate'], df_clutch['BPC_pct'])

if p_bps < 0.05 or p_bpc < 0.05:
    print("\nOverall Conclusion: At least one clutch metric has a statistically significant linear relationship with age.")
else:
    print("\nOverall Conclusion: There is NO statistically significant linear relationship between age and clutch performance in these major matches.")

# best clutch performer based on BPS%
best_bps_player = df_clutch.loc[df_clutch['BPS_pct'].idxmax()]
print(
    f"\nBest Clutch Performer (BPS%): {best_bps_player['full_name']} with BPS% of {best_bps_player['BPS_pct']:.2f}%")

# best clutch performer based on BPC%
best_bpc_player = df_clutch.loc[df_clutch['BPC_pct'].idxmax()]
print(
    f"Best Clutch Performer (BPC%): {best_bpc_player['full_name']} with BPC% of {best_bpc_player['BPC_pct']:.2f}%")

# best overall clutch performer based on average of BPS% and BPC%
df_clutch['avg_clutch_pct'] = (df_clutch['BPS_pct'] + df_clutch['BPC_pct']) / 2
best_overall_clutch_player = df_clutch.loc[df_clutch['avg_clutch_pct'].idxmax(
)]
print(
    f"Best Overall Clutch Performer: {best_overall_clutch_player['full_name']} with Average Clutch% of {best_overall_clutch_player['avg_clutch_pct']:.2f}%")
