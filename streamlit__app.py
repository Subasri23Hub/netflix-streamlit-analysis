import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("📺 NETFLIX DATA ANALYSIS IN STREAMLIT")
upload_file = st.file_uploader("Upload Netflix CSV File", type=['csv'])

if upload_file:

    df = pd.read_csv(upload_file)

    st.subheader("Dataset Preview")
    st.dataframe(df)

    st.sidebar.header("Filters")

    # Filter by Type
    if "type" in df.columns:
        selected_type = st.sidebar.selectbox(
            "Select Content Type",
            df["type"].dropna().unique()
        )
        df = df[df["type"] == selected_type]

    # Filter by Country
    if "country" in df.columns:
        country_list = df["country"].dropna().unique()
        selected_country = st.sidebar.selectbox(
            "Select Country",
            country_list
        )
        df = df[df["country"] == selected_country]

    # Filter by Rating
    if "rating" in df.columns:
        rating_list = df["rating"].dropna().unique()
        selected_rating = st.sidebar.selectbox(
            "Select Rating",
            rating_list
        )
        df = df[df["rating"] == selected_rating]

    st.subheader("Filtered Data")
    st.dataframe(df)

    numeric_columns = df.select_dtypes(include=np.number).columns.tolist()

    selected_column = st.sidebar.selectbox(
        "Select Numeric Column",
        numeric_columns
    )

    min_val = float(df[selected_column].min())
    max_val = float(df[selected_column].max())

    range_values = st.sidebar.slider(
        "Select Range",
        min_val,
        max_val,
        (min_val, max_val)
    )

    filtered_df = df[
        (df[selected_column] >= range_values[0]) &
        (df[selected_column] <= range_values[1])
    ]

    st.subheader("Range Filtered Data")
    st.dataframe(filtered_df)

    st.subheader("NumPy Statistics")

    mean_val = np.mean(filtered_df[selected_column])
    median_val = np.median(filtered_df[selected_column])
    std_val = np.std(filtered_df[selected_column])

    col1, col2, col3 = st.columns(3)

    col1.write(f"Mean: {round(mean_val, 2)}")
    col2.write(f"Median: {round(median_val, 2)}")
    col3.write(f"Standard Deviation: {round(std_val, 2)}")

    # CHART TYPE
   
    st.subheader("Select Chart Type")

    chart_type = st.radio(
        "",
        ["Line", "Bar", "Histogram"]
    )

    if chart_type == "Line":
        st.line_chart(filtered_df[selected_column])

    elif chart_type == "Bar":
        st.bar_chart(filtered_df[selected_column])

    elif chart_type == "Histogram":
        fig, ax = plt.subplots()
        ax.hist(filtered_df[selected_column], bins=20)
        ax.set_title("Histogram")
        ax.set_xlabel(selected_column)
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
