import pandas as pd

# Lastly, we want to have a look at who is the most improved player in the top 50
# Load year-over-year ranking changes data from sql query output
df_growth = pd.read_csv('winning_rate.csv')

# Calculate the improvement in winning rate
df_growth['win_rate'] = (df_growth['total_wins'].astype(
    float) / df_growth['total_matches']) * 100

# Pivot Data for H1 vs H2 Comparison
# Reshape the data so H1 and H2 win rates are in separate columns
df_pivot = df_growth.pivot_table(
    index=['player_id', 'full_name'],
    columns='half_year',
    values='win_rate'
).reset_index()

# to rnsure both H1 and H2 columns exist, filling missing values (NaN) with 0
df_pivot = df_pivot.fillna(0)

# Growth = H2 Win Rate - H1 Win Rate
df_pivot['win_rate_growth'] = df_pivot['H2'] - df_pivot['H1']

# Filter out players who didn't play in both halves (H1 or H2 win rate is 0)
# And players who only played a minimal amount of matches (e.g., less than 5% win rate in H1)
df_growth_clean = df_pivot[
    (df_pivot['H1'] > 0) & (df_pivot['H2'] > 0)
].copy()

# Identify the most improved player
most_improved_player = df_growth_clean.loc[df_growth_clean['win_rate_growth'].idxmax(
)]
print(
    f"\nMost Improved Player: {most_improved_player['full_name']} with a Winning Rate Growth of {most_improved_player['win_rate_growth']:.2f}%"
)
