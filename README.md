# tennis_performance_analysis
A data engineering and analytics project combining SQL (data cleaning & transformation) and Python (statistical analysis & visualization) to investigate performance trends among ATP Top 50 players in 2023.

The project answers three key questions:

Which surface rewards high-quality serving the most?

Does age/experience influence clutch performance?

Who is the most improved player (H1 → H2 winning-rate growth)?

Only ATP Masters 1000 and Grand Slam matches are included, and only matches where at least one player finished 2023 in the ATP Top 50.

structure: 
├── data/
│   ├── raw/
│   │   ├── atp_matches_2023.csv
│   │   ├── atp_players_2023.csv
│   │   └── atp_rankings_2023.csv
│   │
│   └── cleaned/
│       ├── service_surface_data.csv
│       ├── age_performance_data.csv
│       └── winning_rate.csv
│
├── sql/
│   └── data_cleaning.sql
│
├── python.analysis/
│   ├── service_surface_analysis.ipynb
│   ├── age_clutch_analysis.ipynb
│   └── improvement_analysis.ipynb
│
└── README.md

# Cleaning and filtering (SQL)
Cleaning steps:
1. Joined matches + players + rankings
2. Filtered tournaments to Masters 1000 & Grand Slams only
3. Included only players who finished 2023 in ATP Top 50

Created three final datasets:

-- service_surface_data.csv — for serve × surface analysis

-- age_performance.csv — for clutch performance analysis

-- winning_rate.csv — for H1 vs H2 win-rate comparison

# Analysis (Python)
1. Serve Quality on Different Surfaces:
Evaluates how serve performance indicators vary across grass, clay, and hard courts.

Metrics:

- 2nd Serve Win %
- 1st Serve Win %
- Total Service Points Won

Outputs include tables.
=> Grass favours strong service the most, followed by hard.

2. Age & Clutch Performance
Assesses whether older players (more exprienced) perform better under pressure using:

- Break points saved % (BPS%)
- Break points converted % (BPC%)
- A computed “pressure performance index”
- 2023 subtracted players' birth year as their estimated age

=> No significant correlation was found between age and clutch performer,
   However the most clutch was found from one of the most exprienced player on tour:
=> the overall best clutch performer (highest mean BPS% and BPC%) is Novak Djokovic -- our Year End number 1!

3. Most Improved Player
Looks for the player with winning rate improving the most from first half of the seaon to the second.

Only players with at least 10 matches in both halves of the season are included.

=> the most improved player is Alex De Minaur, he made his atp finals debut the next year!


