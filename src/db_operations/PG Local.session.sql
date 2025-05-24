CREATE TABLE IF NOT EXISTS dailysleep (
    sleep_date DATE PRIMARY KEY,
    deep_sleep INT,
    efficiency INT,
    latency INT,
    rem_sleep INT,
    restfulness INT,
    timing INT,
    total_sleep INT,
    score INT
);

CREATE TABLE IF NOT EXISTS sleeproutes (
    sleep_date DATE PRIMARY KEY,
    avg_breath INT,
    avg_heartrate INT,
    avg_hrv INT,
    deepsleep_effic INT,
    bedtime_start VARCHAR(255),
    bedtime_end VARCHAR(255),
    time_in_bed INT,
    awake_time INT,
    totalsleep_dur INT
    
);

CREATE TABLE IF NOT EXISTS sleeptimeroutes (
    day DATE primary KEY,
    day_tz INT,
    start_offset INT,
    end_offset INT,
    recommendation VARCHAR(255),
    daystatus VARCHAR(255)
)