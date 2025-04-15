import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import zoneinfo as ZoneInfo


# Unless the user is logged in, they will not be able to view this page
token = st.session_state.get("access_token", "")
if not token:
    st.error("❌ Oops! You need to be logged in first.")
    st.stop()

st.set_page_config(
    page_title="Prediction History - Group 1 COMP377",
)

st.title("Your Prediction History")
st.sidebar.success(f"Go back to the landing page, make a prediction, or examine our data")

API_BASE = "https://group1-comp377-groupproject-1.onrender.com"

def map_age(age_code):
    age_map = {
        1: "18-24", 2: "25-29", 3: "30-34", 4: "35-39", 5: "40-44",
        6: "45-49", 7: "50-54", 8: "55-59", 9: "60-64", 10: "65-69",
        11: "70-74", 12: "75-79", 13: "80 or older"
    }
    return age_map.get(age_code, str(age_code))

def map_education(edu_code):
    edu_map = {
        1: "No formal education",
        2: "Elementary",
        3: "Some high school",
        4: "High school graduate",
        5: "Some college",
        6: "College graduate"
    }
    return edu_map.get(edu_code, str(edu_code))

def map_income(income_code):
    income_map = {
        1: "Less than $10,000",
        2: "Less than $15,000",
        3: "Less than $20,000",
        4: "Less than $25,000",
        5: "Less than $35,000",
        6: "Less than $50,000",
        7: "Less than $75,000",
        8: "$75,000 or more"
    }
    return income_map.get(income_code, str(income_code))

def map_gen_health(health_code):
    health_map = {
        1: "Excellent",
        2: "Very Good",
        3: "Good",
        4: "Fair",
        5: "Poor"
    }
    return health_map.get(health_code, str(health_code))

def map_boolean(value):
    return "Yes" if value == 1 else "No"

def transform_features(features):
    transformed = features.copy()
    transformed['Age'] = map_age(features['Age'])
    transformed['Education'] = map_education(features['Education'])
    transformed['Income'] = map_income(features['Income'])
    transformed['GenHlth'] = map_gen_health(features['GenHlth'])
    
    boolean_fields = ['HighBP', 'HighChol', 'CholCheck', 'Smoker', 'Stroke', 
                     'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies',
                     'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'DiffWalk', 'Sex']
    
    for field in boolean_fields:
        if field in transformed:
            transformed[field] = map_boolean(transformed[field])
    
    return transformed

try:
    response = requests.get(
        f"{API_BASE}/predictions",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        predictions = response.json()
        
        if not predictions:
            st.info("You haven't made any predictions yet. Go to the Predictions page to make your first prediction!")
        else:
            # Display predictions in a table format
            for pred in predictions:
                with st.expander(f"Prediction from {datetime.strptime(pred['created_at'], '%a, %d %b %Y %H:%M:%S GMT').astimezone(ZoneInfo.ZoneInfo('America/New_York')).strftime('%Y-%m-%d %I:%M:%S %p ET')}", expanded=False):
                    
                    result = "Likely Diabetic" if pred['prediction'] else "Not Diabetic"
                    probability = float(pred['probability']) * 100
                    
                    
                    st.markdown(f"**Result:** {result}")
                    st.markdown(f"**Probability:** {probability:.2f}%")
                    
                    
                    st.markdown("**Features Used:**")
                    transformed_features = transform_features(pred['features'])
                    features_df = pd.DataFrame([transformed_features])
                    st.dataframe(features_df, use_container_width=True)
                    
    else:
        st.error(f"❌ Failed to fetch predictions: {response.json().get('error', 'Unknown error')}")
        
except Exception as e:
    st.error(f"❌ An error occurred: {str(e)}")

if st.session_state.is_logged_in:
    if st.sidebar.button("Logout"):
        st.session_state.access_token = None
        st.session_state.user_email = None
        st.session_state.is_logged_in = False
        st.success("✅ Logged out successfully.")
