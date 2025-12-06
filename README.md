# global-seismic-trends-project
"A data analytics project on 5-year earthquake dataset including preprocessing, database loading, task execution, and Streamlit dashboard visualization."

# Earthquake Analytics Project

🌍 Earthquake Analytics Dashboard (2019–2024)

A complete end-to-end data analytics project using Python, Pandas, MySQL, SQL, and Streamlit.
This project analyzes global earthquake patterns over the last 5 years and provides an interactive dashboard for visual analytics.

📁 Project Overview

This project performs:

✔ Data Loading

    Earthquake dataset loaded from a public API/URL covering events from the last 5 years.
    
    Converted to Pandas DataFrame for processing.

✔ Data Preprocessing

    Performed several cleaning steps:
    
    Handling missing values
    
    Converting date & time formats
    
    Extracting useful fields (year, month, day, hour)
    
    Cleaning numeric fields
    
    Normalizing categorical columns
    
    Detecting & removing duplicates

✔ Database Creation

    Created a MySQL database named earthquake_db
    
    Designed a table named earthquake
    
    Loaded the cleaned dataset into the database using mysql-connector-python.

✔ 30 Analytical Tasks Executed using SQL + Python

    The analysis includes:
    
    🔹 Magnitude & Depth Analysis
    
        (Top 10 strongest, deepest, average magnitude/type, shallow earthquakes, etc.)
    
    🔹 Time-Based Analysis
    
        (Active year/month/day/hour, reporting networks, trends.)
    
    🔹 Casualties & Economic Impact
    
        (Top 5 locations, total economic loss, alert-level impact.)
    
    🔹 Event Quality & Reliability
    
        (RMS, gap, nst coverage, reviewed vs automatic events.)
    
    🔹 Tsunami & Alerts
    
        (Alert level counts, tsunami-triggered events.)
    
    🔹 Trend & Pattern Modeling
    
        (Year-over-year growth, country analysis, magnitude comparison.)
    
    🔹 Spatial + Depth Analysis
    
        (Equator-based depth, distance-based event pairing, deep-focus earthquakes.)
        
    All 30 tasks were completed using SQL queries + Python transformations.
    
    🎛️ Interactive Streamlit Dashboard
    
A fully functional interactive dashboard includes:

Dashboard Features

    ✔ Home Page (project intro & data overview)
    ✔ Dataset Preview + Filters
    ✔ 30 Task Explorer Page
    ✔ Navigation Sidebar
    ✔ Plotly + Matplotlib charts
    ✔ Searchable & filterable task outputs
    ✔ Dynamic SQL execution
    ✔ Clean UI layout

Pages

    🔹 Home
    
    🔹 Dataset Preview
    
    🔹 Earthquake Tasks
    
    🔹 30 Task Selector (drop-down or click-based)
