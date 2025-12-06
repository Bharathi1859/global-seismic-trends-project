import streamlit as st
import pandas as pd
import mysql.connector
import numpy as np


# -----------------------------
# Database connection
# -----------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="earthquake_db"
    )

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM earthquake", conn)
    conn.close()
    return df

df = load_data()

# -----------------------------
# Session state for page navigation
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

# -----------------------------
# Sidebar navigation
# -----------------------------
st.sidebar.title("Navigation")
page_option = st.sidebar.radio("Go to Page", ["Home", "Earthquake Tasks"])
st.session_state.page = page_option

# -----------------------------
# Home Page
# -----------------------------
if st.session_state.page == "Home":
    st.title("🌍 Earthquake Dashboard - Data Preview")

    # Filters
    st.sidebar.header("Filters")
    year_list = sorted(df["year"].dropna().unique())
    selected_year = st.sidebar.selectbox("Select Year", ["All"] + year_list)

    country_list = sorted(df["country"].dropna().unique())
    selected_country = st.sidebar.selectbox("Select Country", ["All"] + country_list)

    # Apply filters
    filtered_df = df.copy()
    if selected_year != "All":
        filtered_df = filtered_df[filtered_df["year"] == selected_year]
    if selected_country != "All":
        filtered_df = filtered_df[filtered_df["country"] == selected_country]

    # Data Preview
    st.subheader("📌 Filtered Data Preview")
    st.dataframe(filtered_df.head(50))

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Earthquakes", len(filtered_df))
    col2.metric("Average Magnitude", round(filtered_df["magnitude"].mean(), 2))
    col3.metric("Total Tsunamis", filtered_df["properties_tsunami"].sum())
    col4.metric("Most Active Country", filtered_df["country"].value_counts().idxmax())

# -----------------------------
# Tasks Page
# -----------------------------
elif st.session_state.page == "Earthquake Tasks":
    st.title("🧩 Earthquake SQL Tasks")

    # Task list
    tasks_list = [
        "1. Top 10 strongest earthquakes (mag).",
        "2. Top 10 deepest earthquakes (depth_km).",
        "3. Shallow earthquakes < 50 km & mag > 7.5",
        "4. Average depth per continent.",
        "5. Average magnitude per magnitude type (magType).",
        "6. Year with most earthquakes.",
        "7. Month with highest number of earthquakes.",
        "8. Day of week with most earthquakes.",
        "9. Count of earthquakes per hour of day.",
        "10. Most active reporting network (net).",
        "11. Top 5 places with highest casualties.",
        "12. Total estimated economic loss per continent.",
        "13. Average economic loss by alert level.",
        "14. Count of reviewed vs automatic earthquakes (status).",
        "15. Count by earthquake type (type).",
        "16. Number of earthquakes by data type (types).",
        "17. Average RMS and gap per continent.",
        "18. Events with high station coverage (nst > threshold).",
        "19. Number of tsunamis triggered per year.",
        "20. Count earthquakes by alert levels (red, orange, etc.).",
        "21. Find the top 5 countries with the highest average magnitude of earthquakes in the 10 years",       	
  	    "22. Find countries that have experienced both shallow and deep earthquakes within the same month.",
  	    "23. Compute the year-over-year growth rate in the total number of earthquakes globally.",
   	    "24. List the 3 most seismically active regions by combining both frequency and average magnitude.",
        "25. For each country, calculate the average depth of earthquakes within ±5° latitude range of the equator.",
        "26. Identify countries having the highest ratio of shallow to deep earthquakes.",
        "27. Find the average magnitude difference between earthquakes with tsunami alerts and those without.",
        "28. Using the gap and rms columns, identify events with the lowest data reliability (highest average error margins).",
        "29. Find pairs of consecutive earthquakes (by time) that occurred within 50 km of each other and within 1 hour.",
        "30. Determine the regions with the highest frequency of deep-focus earthquakes (depth > 300 km)."
        # Add all tasks up to 30...
    ]

    task = st.selectbox("Select Task", tasks_list)

    # Helper to run SQL
    def run_query(query):
        conn = get_connection()
        df = pd.read_sql(query, conn)
        conn.close()
        return df

    # -----------------------------
    # Task queries
    # -----------------------------
    if task.startswith("1."):
        st.subheader("Top 10 strongest earthquakes (mag).")
        df_task = run_query("SELECT id, magnitude, place, time, depth_km, country FROM earthquake ORDER BY magnitude DESC LIMIT 10")
        st.dataframe(df_task)

    elif task.startswith("2."):
        st.subheader("Top 10 deepest earthquakes (depth_km).")
        df_task = run_query("SELECT id, magnitude, place, time, depth_km, country FROM earthquake ORDER BY depth_km DESC LIMIT 10;")
        st.dataframe(df_task)

    elif task.startswith("3."):
        st.subheader("Shallow earthquakes < 50 km and mag > 7.5.")
        query = f"""
            SELECT 
                    id,
                    magnitude,
                    place,
                    time,
                    depth_km,
                    depth_category,
                    country
                FROM earthquake
                WHERE depth_km < 50
                AND magnitude > 7.5
                ORDER BY magnitude DESC;
        """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("4."):
        st.subheader("Average depth per continent.")
        query = """
                SELECT continent, avg(depth_km) AS avg_depth
                FROM earthquake
                GROUP BY continent
                ORDER BY avg_depth DESC;
                """
        df_task = run_query(query)
        st.bar_chart(df_task.set_index("continent"))

    elif task.startswith("5."):
        st.subheader("Average magnitude per magnitude type (magType).")
        query = """
                SELECT properties_magType AS magType,
                    AVG(magnitude) AS avg_magnitude,
                    COUNT(*) AS total_events
                FROM earthquake
                GROUP BY properties_magType
                ORDER BY avg_magnitude DESC;
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("6."):
        st.subheader("Year with most earthquakes.")
        query = """
                SELECT year,count(*) as Total_earthquakes from earthquake
                group by year 
                order by Total_earthquakes desc
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("7."):
        st.subheader("Month with highest number of earthquakes.")
        query = """
                SELECT month,count(*) as Total_earthquakes from earthquake
                group by month 
                order by Total_earthquakes desc
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("8."):
        st.subheader("Day of week with most earthquakes.")
        query = """
                SELECT day_of_week,count(*) as Total_earthquakes from earthquake
                group by day_of_week
                order by Total_earthquakes desc
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("9."):
        st.subheader("Count of earthquakes per hour of day.")
        query = """
                SELECT hour,count(*) as Total_earthquakes from earthquake
                group by hour
                order by Total_earthquakes desc
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("10."):
        st.subheader("Most active reporting network (net).")
        query = """
                SELECT properties_net, COUNT(*) AS total_reports
                FROM earthquake
                GROUP BY properties_net
                ORDER BY total_reports DESC
                LIMIT 5;
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("11."):
        st.subheader("Top 5 places with highest casualties.")
        query = """
                SELECT place, SUM(properties_felt) AS casualties
                FROM earthquake
                GROUP BY place
                ORDER BY casualties DESC
                limit 5
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("12."):
        st.subheader("Total estimated economic loss per continent.")
        query = """
                SELECT continent, SUM(properties_sig) AS total_economic_loss
                FROM earthquake
                GROUP BY continent
                ORDER BY total_economic_loss DESC;
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("13."):
        st.subheader("Average economic loss by alert level.")
        query = """
                SELECT properties_alert, avg(properties_sig) AS total_economic_loss
                FROM earthquake
                GROUP BY properties_alert
                ORDER BY total_economic_loss DESC;
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("14."):
        st.subheader("Count of reviewed vs automatic earthquakes (status).")
        query = """
                SELECT properties_status, count(*) AS count
                FROM earthquake
                GROUP BY properties_status
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("15."):
        st.subheader("Count by earthquake type (type).")
        query = """
                SELECT properties_type, count(*) AS count
                FROM earthquake
                GROUP BY properties_type
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("16."):
        st.subheader("Number of Earthquakes by Data Type (properties_types)")

    # fetch types column
        query = "SELECT properties_types FROM earthquake;"
        df_types = run_query(query)  # your helper function

        # normalize strings
        s = (df_types['properties_types']
            .fillna('')          # turn None -> ''
            .astype(str)         # ensure string
            .str.strip()         # trim whitespace
            .str.lstrip(',')     # remove leading commas
            .replace('', np.nan) # empty -> NaN
        )

        # split/explode
        df_exploded = (s.dropna()
                        .str.split(',', expand=False)
                        .explode()
                        .str.strip()
                        .to_frame(name='type'))

        # count
        type_counts = df_exploded['type'].value_counts().reset_index()
        type_counts.columns = ['Data Type', 'Count']

        # show table & bar chart
        st.dataframe(type_counts)
        st.bar_chart(type_counts.set_index('Data Type'))


    elif task.startswith("17."):
        st.subheader("Average RMS and gap per continent.")
        query = """
                SELECT 
                    continent,
                    AVG(properties_rms) AS avg_rms,
                    AVG(properties_gap) AS avg_gap
                FROM earthquake
                GROUP BY continent
                ORDER BY continent;
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("18."):
        st.subheader("Events with high station coverage (nst > threshold).")
        query = f"""
                    SELECT 
                        id,
                        magnitude,
                        place,
                        time,
                        properties_nst AS nst,
                        properties_magType,
                        depth_km,
                        country,
                        continent
                    FROM earthquake
                    WHERE properties_nst > 50
                    ORDER BY properties_nst DESC limit 10;
                    """

        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("19."):
        st.subheader("Number of tsunamis triggered per year.")
        query = """
                SELECT 
                    year,
                    COUNT(*) AS total_events,
                    SUM(CASE WHEN properties_tsunami = 1 THEN 1 ELSE 0 END) AS tsunami_events
                FROM earthquake
                GROUP BY year
                ORDER BY year;
                """

        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("20."):
        st.subheader("Count earthquakes by alert levels (red, orange, etc.).")
        query = """
                SELECT 
                    COALESCE(properties_alert, 'no_alert') AS alert_level,
                    COUNT(*) AS count_alerts
                FROM earthquake
                GROUP BY alert_level
                ORDER BY count_alerts DESC;
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("21."):
        st.subheader("Find the top 5 countries with the highest average magnitude of earthquakes in the past 10 years")
        query = """
                SELECT country, avg(magnitude) as avg_mag from earthquake
                group by country
                order by avg_mag 
                limit 5;
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("22."):
        st.subheader("Find countries that have experienced both shallow and deep earthquakes within the same month.")
        query = """
                SELECT DISTINCT e1.country, 
                    e1.year,
                    e1.month
                FROM earthquake e1
                WHERE e1.depth_category = 'Shallow'
                AND EXISTS (
                        SELECT 1
                        FROM earthquake e2
                        WHERE e2.country = e1.country
                        AND e2.year = e1.year
                        AND e2.month = e1.month
                        AND e2.depth_category = 'Deep'
                )
                UNION
                SELECT DISTINCT e2.country, 
                    e2.year,
                    e2.month
                FROM earthquake e2
                WHERE e2.depth_category = 'Deep'
                AND EXISTS (
                        SELECT 1
                        FROM earthquake e3
                        WHERE e3.country = e2.country
                        AND e3.year = e2.year
                        AND e3.month = e2.month
                        AND e3.depth_category = 'Shallow'
                );

                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("23."):
        st.subheader("Compute the year-over-year growth rate in the total number of earthquakes globally.")
        query = """
                WITH yearly_counts AS (
                    SELECT 
                        year,
                        COUNT(*) AS total_quakes
                    FROM earthquake
                    GROUP BY year
                )
                SELECT 
                    y1.year,
                    y1.total_quakes,
                    y2.total_quakes AS previous_year_total,
                    ROUND(
                        ((y1.total_quakes - y2.total_quakes) / y2.total_quakes) * 100,
                        2
                    ) AS yoy_growth_percentage
                FROM yearly_counts y1
                LEFT JOIN yearly_counts y2
                    ON y1.year = y2.year + 1
                ORDER BY y1.year;
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("24."):
        st.subheader("List the 3 most seismically active regions by combining both frequency and average magnitude.")
        query = """
                SELECT 
                    country AS region,
                    COUNT(*) AS total_events,
                    ROUND(AVG(magnitude), 3) AS avg_magnitude,
                    ROUND(COUNT(*) * AVG(magnitude), 3) AS activity_score
                FROM earthquake
                GROUP BY country
                ORDER BY activity_score DESC
                LIMIT 3;
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("25."):
        st.subheader("For each country, calculate the average depth of earthquakes within ±5° latitude range of the equator.")
        query = """
                SELECT 
                    country,
                    ROUND(AVG(depth_km), 3) AS avg_depth_equatorial
                FROM earthquake
                WHERE latitude BETWEEN -5 AND 5
                GROUP BY country
                ORDER BY avg_depth_equatorial DESC;
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("26."):
        st.subheader("Identify countries having the highest ratio of shallow to deep earthquakes.")
        query="""SELECT
                    country,
                    SUM(CASE WHEN depth_category = 'Shallow' THEN 1 ELSE 0 END) AS shallow_count,
                    SUM(CASE WHEN depth_category = 'Deep' THEN 1 ELSE 0 END) AS deep_count,
                    ROUND(
                        SUM(CASE WHEN depth_category = 'Shallow' THEN 1 ELSE 0 END) /
                        NULLIF(SUM(CASE WHEN depth_category = 'Deep' THEN 1 ELSE 0 END), 0),
                        3
                    ) AS shallow_to_deep_ratio
                FROM earthquake
                GROUP BY country
                HAVING deep_count > 0   -- only countries having at least 1 deep earthquake
                ORDER BY shallow_to_deep_ratio DESC;
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("27."):
        st.subheader("Find the average magnitude difference between earthquakes with tsunami alerts and those without.")
        query = """
                SELECT
                    AVG(CASE WHEN properties_tsunami = 1 THEN magnitude END) -
                    AVG(CASE WHEN properties_tsunami = 0 THEN magnitude END)
                    AS avg_magnitude_difference
                FROM earthquake;
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("28."):
        st.subheader("Using the gap and rms columns, identify events with the lowest data reliability (highest average error margins).")
        query = """
                SELECT
                    id,
                    place,
                    magnitude,
                    properties_rms AS rms,
                    properties_gap AS gap,
                    (properties_rms + properties_gap)/2 AS error_score
                FROM earthquake
                ORDER BY error_score DESC
                LIMIT 10;
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("29."):
        st.subheader("Find pairs of consecutive earthquakes (by time) that occurred within 50 km of each other and within 1 hour.")
        query="""SELECT 
                    e1.id AS eq1_id,
                    e2.id AS eq2_id,
                    e1.time AS eq1_time,
                    e2.time AS eq2_time,

                    TIMESTAMPDIFF(MINUTE, e1.time, e2.time) AS time_diff_minutes,

                    6371 * ACOS(
                        COS(RADIANS(e1.latitude)) * COS(RADIANS(e2.latitude)) *
                        COS(RADIANS(e2.longitude) - RADIANS(e1.longitude)) +
                        SIN(RADIANS(e1.latitude)) * SIN(RADIANS(e2.latitude))
                    ) AS distance_km

                FROM earthquake e1
                JOIN earthquake e2
                    ON e2.time > e1.time
                    AND e2.time <= DATE_ADD(e1.time, INTERVAL 1 HOUR)   

                WHERE NOT EXISTS (
                    SELECT 1 
                    FROM earthquake e3
                    WHERE e3.time > e1.time 
                    AND e3.time < e2.time
                )

                HAVING distance_km <= 50
                ORDER BY e1.time;
                """
        df_task = run_query(query)
        st.dataframe(df_task)

    elif task.startswith("30."):
        st.subheader("Determine the regions with the highest frequency of deep-focus earthquakes (depth > 300 km).")
        query="""SELECT 
                    country,
                    COUNT(*) AS deep_focus_count
                FROM earthquake
                WHERE depth_km > 300
                GROUP BY country
                ORDER BY deep_focus_count DESC;
                """
        df_task = run_query(query)
        st.dataframe(df_task)

  

    # Continue for remaining tasks...
