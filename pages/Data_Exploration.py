import streamlit as st
from ucimlrepo import fetch_ucirepo
import pandas as pd
from matplotlib import pyplot as plt
from pathlib import Path
import os

# Unless the user is logged in, they will not be able to view this page
token = st.session_state.get("access_token", "")
if not token:
    st.error("❌ Oops! You need to be logged in first.")
    st.stop()

st.set_page_config(
    page_title="Group 1 COMP377",
    page_icon="👾",
)

st.write("# Data Exploration!")
st.write('A little bit about this dataset: This dataset is from the CDC and contains health indicators for diabetes.'
         ' It has information from all states and territories in the US in 2021 as part of The Behavioral Risk Factor Surveillance System'
         ' which monitors health across The United States of America.')

st.sidebar.success("Go back to the landing page, check out your history, or make predictions")

# fetch dataset (first try local CSV, fallback to UCI ML repo)
df_path = Path("diabetes_012_health_indicators_BRFSS2015.csv")

if df_path.exists():
    df = pd.read_csv(df_path)
    st.write("✅ Loaded dataset from local CSV.")
else:
    st.write("📡 Downloading dataset from UCI ML Repo. This may take a few seconds...")
    try:
        cdc_diabetes_health_indicators = fetch_ucirepo(id=891)
        df = cdc_diabetes_health_indicators.data.original
        df.to_csv(df_path, index=False)
        st.write("📥 Dataset downloaded and saved locally for future runs.")
    except Exception as e:
        st.error("❌ Failed to load dataset from both local file and UCI ML Repo.")
        st.stop()

# data (as pandas dataframes)
with st.container():
    st.write("## Dataframe null check:")
    st.write(df.isnull().sum())

st.write("We have no missing values in our dataset, so we can proceed to look a bit closer at it.")

st.write("## Dataframe head:")
st.write(df.head())

st.write("## Dataframe Types:")
st.write(df.dtypes)

st.write("We can also see by this that the types of data are all numerical, so no real need to process them from\n"
"strings or objects etc. So we can continue on from this. But, it should be noted there are some categorical values\n"
"such as 'Education_Level' and 'Income_Level', so we should be mindful of this when looking at the data.")

cols = [col for col in df.columns if col not in ['Diabetes_binary', 'ID']]

df_median = pd.DataFrame(columns=[cols])

st.write("## What is the median person?")
for col in cols:
    df_median.at[0, col] = round(df[col].median(), 7)

st.table(df_median.T)

st.write("The median person is a man with healthcare coverage, no extreme health issues and is between 55 and 59 years old,"
         " with a BMI of 27.0, eats fruit and vegetables 1+ times a day, has a high school education, and an income of "
         "between \$50,000 and \$75,000 USD")

correlations = {}

for col in cols:
    correlations[col] = df[col].corr(df['Diabetes_binary'])  # Lets add this to a dictionary to take a closer look

weak_correlation = {}
medium_correlation = {}
strong_correlation = {}

for key in correlations:
    if correlations[key] > 0.2 or correlations[key] < -0.2:
        strong_correlation[key] = correlations[key]
    elif correlations[key] > 0.1 or correlations[key] < -0.1:
        medium_correlation[key] = correlations[key]
    else:
        weak_correlation[key] = correlations[key]

st.write("## A closer look at the data:")
with st.container():

    stats = st.checkbox("Show more stats")

    with st.expander("Strong correlations:"):
        for key in strong_correlation:
            st.write(f"{key} has a correlation of {strong_correlation[key]}")
            if stats:
                st.write(f"{key} has a mean of {round(df[key].mean(), 7)} and a standard deviation of {round(df[key].std(), 7)}")
                st.write(f"{key} has a min of {round(df[key].min(), 7)} and a max of {round(df[key].max(), 7)}")
            if key != list(strong_correlation)[-1]:
                st.divider()

    with st.expander("Medium correlations:"):
        for key in medium_correlation:
            st.write(f"{key} has a correlation of {medium_correlation[key]}")
            if stats:
                st.write(f"{key} has a mean of {round(df[key].mean(), 7)} and a standard deviation of {round(df[key].std(), 7)}")
                st.write(f"{key} has a min of {round(df[key].min(), 7)} and a max of {round(df[key].max(), 7)}")
            if key != list(medium_correlation)[-1]:
                st.divider()

    with st.expander("Weak correlations:"):
        for key in weak_correlation:
            st.write(f"{key} has a correlation of {weak_correlation[key]}")
            if stats:
                st.write(f"{key} has a mean of {round(df[key].mean(), 7)} and a standard deviation of {round(df[key].std(), 7)}")
                st.write(f"{key} has a min of {round(df[key].min(), 7)} and a max of {round(df[key].max(), 7)}")
            if key != list(weak_correlation)[-1]:
                st.divider()

    st.write("The general conclusion is that generally stronger indicators of physical health are "
             "more likely to be correlated directly with diabetes or lack thereof, followed by education or income and then life style." \
             " But be mindful that some of these statistics are categorical, such as 'Education_Level' and 'Income_Level', so they may not be " \
             "as reliable as the others.")

st.write("## Outlier Detection in BMI:")
fig, ax = plt.subplots()
ax.boxplot(df["BMI"])
ax.set_title(f"Boxplot for BMI Outliers")
st.pyplot(fig)
st.write("As we can see from the boxplot, there are a some outliers in the BMI column. We used this column because " \
         "it is a good indicator of health and is also continuous, as opposed to a boolean or categorical value.")

# New section added between the two charts

st.write("## Age distribution:")
age_counts = df['Age'].value_counts().sort_index()
x = ["18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80+"]
y = age_counts.values
fig, ax = plt.subplots()
ax.bar(x, y)
ax.set_title("Age distribution")
ax.set_xlabel("Age")
ax.set_ylabel("Count")
ax.set_xticks(range(len(x)))
ax.set_xticklabels(x, rotation=45, ha='right', fontsize=10)
st.pyplot(fig)

st.write("## Education distribution:")
age_counts = df['Education'].value_counts().sort_index()
x = ["No formal education", "Elementary", "Some high school", "High school graduate", "Some college", "College graduate"]
y = age_counts.values
fig, ax = plt.subplots()
ax.bar(x, y)
ax.set_title("Education distribution")
ax.set_xlabel("Education Level")
ax.set_ylabel("Count")
ax.set_xticks(range(len(x)))
ax.set_xticklabels(x, rotation=45, ha='right', fontsize=10)
st.pyplot(fig)

st.write("Education distribution table, lower the number corresponds to lower education:")
edu_table = df['Education'].value_counts()
st.table(edu_table)

st.write("## Income distribution:")
age_counts = df['Income'].value_counts().sort_index()
x = ["Less than $10,000", "Less than $15,000", "Less than $20,000", "Less than $25,000", "Less than $35,000", "Less than $50,000", "Less than $75,000", "$75,000 or more"]
y = age_counts.values
fig, ax = plt.subplots()
ax.bar(x, y)
ax.set_title("Income distribution")
ax.set_xlabel("Income Level")
ax.set_ylabel("Count")
ax.set_xticks(range(len(x)))
ax.set_xticklabels(x, rotation=45, ha='right', fontsize=10)
st.pyplot(fig)

if st.session_state.is_logged_in:
    if st.sidebar.button("Logout"):
        st.session_state.access_token = None
        st.session_state.user_email = None
        st.session_state.is_logged_in = False
        st.success("✅ Logged out successfully.")
