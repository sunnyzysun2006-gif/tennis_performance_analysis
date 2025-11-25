import pandas as pd
import matplotlib.pyplot as plt

# first, we want to know which surface is most favorable to servers
# Load the service statistics data from sql query output
df_serve_stats = pd.read_csv('service_surface_data.csv')

# Calculate total points won on serve
df_serve_stats['total_points_won'] = (
    df_serve_stats['total_1st_serve_won'] +
    df_serve_stats['total_2nd_serve_won']
)
# Calculate the SPW percentage ((Total Points Won / Total Points Served) * 100)
df_serve_stats['SPW_pct'] = (
    df_serve_stats['total_points_won'].astype('float') /
    df_serve_stats['total_serve_points']
) * 100

# group by surface and calculate median SPW%
# The surface with the highest median SPW% is the most serve-dependent.
surface_dominance = df_serve_stats.groupby(
    'surface')['SPW_pct'].median().sort_values(ascending=False)

print("Median Serve Points Won % by Surface:")
print(surface_dominance)

# Visualize the SPW% distribution by surface using boxplots
plt.figure(figsize=(8, 6))

df_serve_stats.boxplot(
    column='SPW_pct',
    by='surface',
    figsize=(8, 6)
)

plt.title("Serve Points Won % by Surface (ATP Top 50, 2023)")
plt.suptitle("")  # Removes the default pandas title
plt.xlabel("Surface")
plt.ylabel("SPW%")
plt.tight_layout()

plt.savefig("surface_serve_strength_boxplot.png", dpi=300)
surface_dominance.to_csv('surface_dominance_summary.csv', index=True)
