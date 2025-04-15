import requests
import streamlit as st


# Unless the user is logged in, they will not be able to view this page
token = st.session_state.get("access_token", "")
if not token:
    st.error("❌ Oops! You need to be logged in first.")
    st.stop()

st.set_page_config(
    page_title="Group 1 COMP377",
    page_icon="🔮",
)

st.sidebar.success("Go back to the landing page, look at your history, or examine our data")

st.write("# Predict on our model with the form below!")

with st.form("my_form"):
    st.write("Notes:")
    st.write("A checkbox indicates a 'Yes' to a yes or no answer. ")


    bmi_val = st.slider("BMI", 0.0, 100.0, 25.0)
    mental_health_val = st.slider("How many days in the past 30 days was your mental health not good?", 0, 30, 0)
    physical_health_val = st.slider("How many days in the past 30 days was your physical health not good (injury/illness)?", 0, 30, 0)
    # 13-level age category (_AGEG5YR see codebook) 1 = 18-24 9 = 60-64 13 = 80 or older
    age_val = st.selectbox("Age", ["18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80 or older"])
    # Education level (EDUCA see codebook) scale 1-6 1 = Never attended school or only kindergarten 2 = Grades 1 through 8 (Elementary) 3 = Grades 9 through 11 (Some high school) 4 = Grade 12 or GED (High school graduate) 5 = College 1 year to 3 years (Some college or technical school) 6 = College 4 years or more (College graduate)
    education_val = st.selectbox("Education Level", ["No formal education", "Elementary", "Some high school", "High school graduate", "Some college", "College graduate"])
    # Income scale (INCOME2 see codebook) scale 1-8 1 = less than $10,000 5 = less than $35,000 8 = $75,000 or more
    income_val = st.selectbox("Income Level", ["Less than $10,000", "Less than $15,000", "Less than $20,000", "Less than $25,000", "Less than $35,000", "Less than $50,000", "Less than $75,000", "$75,000 or more"])
    # scale 1-5 1 = excellent 2 = very good 3 = good 4 = fair 5 = poor
    gen_health_val = st.selectbox("General Health", ["Poor", "Fair", "Good", "Very Good", "Excellent"])


    high_bp_val = st.checkbox("Do you have high blood pressure?")
    high_chol_val = st.checkbox("Do you have high cholesterol?")
    chol_check_val = st.checkbox("Have you had your cholesterol checked in the last 5 years?")
    smoking_val = st.checkbox("Have you smoked more than 100 cigarettes in your life?")
    stroke_val = st.checkbox("Have you ever had a stroke?")
    heart_val = st.checkbox("Have you ever had a heart attack or myocardial infraction?")
    phys_activity_val = st.checkbox("Have you had physical activity in the last 30 days excluding employment?")
    fruits_val = st.checkbox("Do you eat fruit 1+ times a day?")
    veggies_val = st.checkbox("Do you eat vegetables 1+ times a day?")
    hvy_alc_val = st.checkbox("Do you drink 7+ drinks of alcohol a week?")
    any_health_val = st.checkbox("Do you have any kind of health care coverage?")
    no_doc_cost_val = st.checkbox("Have you neglected going to the doctor because of cost in the past 12 months?")
    walking_val = st.checkbox("Do you have serious difficulty walking or climbing a flight of stairs?")
    gender_val = st.checkbox("Is your sex male?")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        # Maps the user input to the format that's expected by our model
        input_data = {
            "BMI": bmi_val,
            "MentHlth": mental_health_val,
            "PhysHlth": physical_health_val,
            "Age": {
                "18-24" : 1,
                "25-29" : 2,
                "30-34" : 3,
                "35-39" : 4,
                "40-44" : 5,
                "45-49" : 6,
                "50-54" : 7,
                "55-59" : 8,
                "60-64" : 9,
                "65-69" : 10,
                "70-74" : 11,
                "75-79" : 12,
                "80 or older" : 13
            }[age_val],
            "Education": {
                "No formal education": 1,
                "Elementary": 2,
                "Some high school": 3,
                "High school graduate": 4,
                "Some college": 5,
                "College graduate": 6
            }[education_val],
            "Income": {
                "Less than $10,000" : 1,
                "Less than $15,000" : 2,
                "Less than $20,000" : 3,
                "Less than $25,000" : 4,
                "Less than $35,000" : 5,
                "Less than $50,000" : 6,
                "Less than $75,000" : 7,
                "$75,000 or more" : 8
            }[income_val],
            "GenHlth": {
                "Excellent": 1,
                "Very Good": 2,
                "Good": 3,
                "Fair": 4,
                "Poor": 5
            }[gen_health_val],
            "HighBP": int(high_bp_val),
            "HighChol": int(high_chol_val),
            "CholCheck": int(chol_check_val),
            "Smoker": int(smoking_val),
            "Stroke": int(stroke_val),
            "HeartDiseaseorAttack": int(heart_val),
            "PhysActivity": int(phys_activity_val),
            "Fruits": int(fruits_val),
            "Veggies": int(veggies_val),
            "HvyAlcoholConsump": int(hvy_alc_val),
            "AnyHealthcare": int(any_health_val),
            "NoDocbcCost": int(no_doc_cost_val),
            "DiffWalk": int(walking_val),
            "Sex": int(gender_val)
        }

        # Get the JWT token from the session
        token = st.session_state.get("access_token", "")
        if not token:
            st.error("❌ No JWT token found. Please log in first.")
            st.stop()

        response = requests.post(
            "https://group1-comp377-groupproject-1.onrender.com/predict",
            headers={"Authorization": f"Bearer {token}"},
            json=input_data
        )

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")

        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ Prediction Complete: {'Likely Diabetic' if result['isDiabetes'] else 'Not Diabetic'}")
            st.write(f"Probability: {100*float(result['probability']):.2f}%")
        else:
            st.error(f"❌ Prediction Failed: {response.json().get('error', 'Unknown error')}")

if st.session_state.is_logged_in:
    if st.sidebar.button("Logout"):
        st.session_state.access_token = None
        st.session_state.user_email = None
        st.session_state.is_logged_in = False
        st.success("✅ Logged out successfully.")
