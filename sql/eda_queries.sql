-- SpaceY Launch Intelligence: SQL EDA queries
-- Import data/spacex_launches_demo.csv into a table named launches.
-- Dataset is synthetic demonstration data; do not interpret as official SpaceX history.

-- 1. Overall sample size and reuse rate
SELECT COUNT(*) AS launch_records,
       ROUND(AVG(first_stage_reused) * 100, 1) AS reuse_rate_pct
FROM launches;

-- 2. Reuse rate by orbit
SELECT orbit, COUNT(*) AS launches,
       ROUND(AVG(first_stage_reused) * 100, 1) AS reuse_rate_pct
FROM launches
GROUP BY orbit
ORDER BY reuse_rate_pct DESC;

-- 3. Reuse rate by launch site
SELECT launch_site, COUNT(*) AS launches,
       ROUND(AVG(first_stage_reused) * 100, 1) AS reuse_rate_pct
FROM launches
GROUP BY launch_site
ORDER BY reuse_rate_pct DESC;

-- 4. Payload mass bands
SELECT CASE WHEN payload_mass_kg < 3000 THEN 'Low (<3t)'
            WHEN payload_mass_kg < 8000 THEN 'Medium (3–8t)'
            ELSE 'High (>=8t)' END AS payload_band,
       COUNT(*) AS launches,
       ROUND(AVG(first_stage_reused) * 100, 1) AS reuse_rate_pct
FROM launches
GROUP BY payload_band
ORDER BY payload_band;

-- 5. Annual trend
SELECT SUBSTR(date_utc, 1, 4) AS launch_year,
       COUNT(*) AS launches,
       ROUND(AVG(first_stage_reused) * 100, 1) AS reuse_rate_pct
FROM launches
GROUP BY launch_year
ORDER BY launch_year;
