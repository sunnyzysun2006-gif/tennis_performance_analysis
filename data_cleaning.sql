-- data-cleaning

CREATE TABLE top_50_atp_players (
     player_id INT,
    `rank` INT PRIMARY KEY,
     points INT
    );
    
-- To focus only on players finishing the season as top 50
INSERT INTO top_50_atp_players (player_id, `rank`, points)
SELECT
    player AS player_id,
    `rank`,
    points
FROM
    atp_rankings_current
LIMIT 50; 

CREATE OR REPLACE VIEW top_50_bio AS
SELECT 
    p.player_id, 
    CONCAT(name_first, ' ', name_last) AS full_name,
    hand,
    dob AS birth_date,
    ioc AS country,
    height,
    `rank`
FROM atp_players p
RIGHT JOIN top_50_atp_players USING(player_id)
ORDER BY `rank` ASC;

-- Filter out lower-level tournaments so we focus on masters matches and grand slams
CREATE OR REPLACE VIEW major_matches AS
SELECT *
FROM atp_matches_2023
WHERE tourney_level LIKE 'M' OR tourney_level LIKE 'G';

-- to focus on the matches where at least one of the players is from the top 50
CREATE VIEW top_matches AS
SELECT
    m.*
FROM
    major_matches m
WHERE
    m.winner_id IN (SELECT player_id FROM top_50_bio)
    OR
    m.loser_id IN (SELECT player_id FROM top_50_bio)
ORDER BY tourney_date ASC;



-- we want to see tennis games on which surface depends on players' serving quality the most
SELECT
    surface,
    winner_id AS player_id,
    winner_name,
    SUM(w_svpt) AS total_serve_points,
    SUM(w_1stWon) AS total_1st_serve_won,
    SUM(w_2ndWon) AS total_2nd_serve_won
FROM
    top_matches
GROUP BY
    surface, winner_id, winner_name;
    


-- next, we are interested in whether experience on tour (operationalised as age) 
   -- would influence players' clutch performance (operationalised as breakpoints-saved rate and conversion rate)
CREATE OR REPLACE VIEW age_performance AS
WITH MatchStats AS (
SELECT
-- when the player won the match
        winner_id AS player_id,
        -- stats when facing break points
        w_bpSaved AS total_bp_saved,
        w_bpFaced AS total_bp_faced_as_server,
        -- stats when having break points opportunities
        l_bpFaced AS total_bp_opportunities,
        (l_bpFaced - l_bpSaved) AS total_bp_converted
FROM top_matches
UNION ALL
SELECT
-- stats when the player lost the match
        loser_id AS player_id,
        l_bpSaved AS total_bp_saved,
        l_bpFaced AS total_bp_faced_as_server,
        w_bpFaced AS total_bp_opportunities,
        (w_bpFaced - w_bpSaved) AS total_bp_converted
FROM top_matches)
SELECT
    t.player_id,
    t.full_name,
    t.birth_date,
    SUM(m.total_bp_saved) AS total_bp_saved,
    SUM(m.total_bp_faced_as_server) AS total_bp_faced_as_server,
    SUM(m.total_bp_opportunities) AS total_bp_opportunities,
    SUM(m.total_bp_converted) AS total_bp_converted
FROM MatchStats m
JOIN top_50_bio t ON 
     m.player_id = t.player_id
GROUP BY t.player_id, t.full_name, t.birth_date;

SELECT ap.*,
    -- estimate players' Age
    (2023 - LEFT(ap.birth_date, 4)) AS age_estimate
FROM age_performance ap;



-- lastly, we want to know which are the players that improved the most improved player this year
SELECT
    t.player_id,
    t.full_name,
    -- Determine the half of the year (H2 starts on 20230701)
    CASE
        WHEN m.tourney_date >= 20230701 THEN 'H2'
        ELSE 'H1'
    END AS half_year,
    -- Count Total Wins
    SUM(CASE WHEN m.winner_id = t.player_id THEN 1 ELSE 0 END) AS total_wins,
    -- Count Total Losses
    SUM(CASE WHEN m.loser_id = t.player_id THEN 1 ELSE 0 END) AS total_losses,
    -- Total Matches Played
    COUNT(m.tourney_id) AS total_matches
FROM top_matches m
JOIN top_50_bio t ON 
      m.winner_id = t.player_id OR m.loser_id = t.player_id
GROUP BY t.player_id, t.full_name, half_year
HAVING
    -- Only consider players with significant matches
    COUNT(m.tourney_id) > 10 
ORDER BY t.player_id, half_year;



    
