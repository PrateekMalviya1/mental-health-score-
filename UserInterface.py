import streamlit as st
import requests
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

# Page Configuration

st.set_page_config(
    page_title="Mental Health Score Prediction",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# FastAPI Configuration

API_URL = os.getenv("API_URL")
if not API_URL:
    api_host = os.getenv("API_HOST")
    API_URL = (
        f"https://{api_host.rstrip('/')}/predict"
        if api_host
        else "http://127.0.0.1:8000/predict"
    )


# Load Custom CSS

CSS_PATH = Path(__file__).parent / "style.css"

with open(CSS_PATH, encoding="utf-8") as css_file:
    st.markdown(
        f"<style>{css_file.read()}</style>",
        unsafe_allow_html=True
    )


# Header

st.markdown(""" <div> <h1 class="section-heading"> Mental Health Score Prediction </h1> </div> """, unsafe_allow_html=True)
    
# Prediction Form

with st.form("mental_health_form"):

    # Personal Information
    st.markdown(
        '<div class="section-heading"> Personal Information</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        Age = st.number_input(
            "Age",
            min_value=10,
            max_value=100,
            value=22,
            step=1,
            help="Enter an age between 10 and 100."
        )

    with col2:
        Gender = st.selectbox(
            "Gender",
            options=["Male", "Female"]
        )

    with col3:
        Country = st.text_input(
            "Country",
            placeholder="e.g. India",
            max_chars=100
        )

    col4, col5 = st.columns(2)

    with col4:
        Academic_Level = st.selectbox(
            "Academic Level",
            options=[
                "High School",
                "Undergraduate",
                "Graduate"
            ]
        )

    with col5:
        Purpose_Of_Use = st.selectbox(
            "Purpose of Use",
            options=[
                "Networking",
                "Entertainment",
                "Education",
                "News"
            ]
        )

    st.write("")

    # Social Media Information
    st.markdown(
        '<div class="section-heading">Social Media Usage</div>',
        unsafe_allow_html=True
    )

    Most_Used_Platform = st.selectbox(
        "Most Used Platform",
        options=[
            "Facebook",
            "LinkedIn",
            "Instagram",
            "Snapchat",
            "Twitter",
            "YouTube",
            "TikTok",
            "LINE",
            "KakaoTalk",
            "VKontakte",
            "WhatsApp",
            "WeChat"
        ]
    )

    col6, col7 = st.columns(2)

    with col6:
        Avg_Daily_Usage_Hours = st.number_input(
            "Average Daily Usage (Hours)",
            min_value=0.0,
            max_value=24.0,
            value=3.0,
            step=0.5,
            help="Average hours spent using social media daily."
        )

    with col7:
        Daily_Unlocks = st.number_input(
            "Daily Phone Unlocks",
            min_value=0,
            max_value=10000,
            value=50,
            step=1
        )

    st.write("")

    # Lifestyle Information
    st.markdown(
        '<div class="section-heading">Lifestyle & Well-being</div>',
        unsafe_allow_html=True
    )

    col8, col9, col10 = st.columns(3)

    with col8:
        Study_Hours = st.number_input(
            "Study Hours Per Day",
            min_value=0.0,
            max_value=24.0,
            value=4.0,
            step=0.5
        )

    with col9:
        Physical_Activity_Hours = st.number_input(
            "Physical Activity (Hours/Day)",
            min_value=0.0,
            max_value=24.0,
            value=1.0,
            step=0.5
        )

    with col10:
        Sleep_Hours_Per_Night = st.number_input(
            "Sleep Hours Per Night",
            min_value=0.0,
            max_value=24.0,
            value=8.0,
            step=0.5
        )

    Stress_Level = st.select_slider(
        "Current Stress Level",
        options=[
            "Low",
            "Medium",
            "High",
            "Very High"
        ],
        value="Medium",
        help="Select the stress level that best describes you."
    )

    stress_labels = {
        "Low": "🟢 Low",
        "Medium": "🟡 Medium",
        "High": "🟠 High",
        "Very High": "🔴 Very High"
    }

    st.caption(
        f"Selected stress level: {stress_labels[Stress_Level]}"
    )

    st.write("")

    # Submit
    submitted = st.form_submit_button(
        "Predict Mental Health Score",
        use_container_width=True
    )


# Send Data to FastAPI

if submitted:

    if not Country.strip():
        st.error("Please enter your country.")

    else:
        payload = {
            "Age": int(Age),
            "Gender": Gender,
            "Country": Country.strip(),
            "Academic_Level": Academic_Level,
            "Most_Used_Platform": Most_Used_Platform,
            "Purpose_Of_Use": Purpose_Of_Use,
            "Avg_Daily_Usage_Hours": float(
                Avg_Daily_Usage_Hours
            ),
            "Daily_Unlocks": int(Daily_Unlocks),
            "Study_Hours": float(Study_Hours),
            "Physical_Activity_Hours": float(
                Physical_Activity_Hours
            ),
            "Sleep_Hours_Per_Night": float(
                Sleep_Hours_Per_Night
            ),
            "Stress_Level": Stress_Level
        }

        try:
            with st.spinner(
                "Analyzing your information..."
            ):
                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=60
                )

            if response.ok:
                result = response.json()

                st.markdown(
                    '<div class="result-heading">'
                    'Prediction Result'
                    '</div>',
                    unsafe_allow_html=True
                )

                prediction = result.get(
                    "predicted_mental_health_score",
                    result.get("mental_health_score", result.get("prediction"))
                )

                if prediction is not None:
                    st.markdown(
                        f"""
                        <div class="result-card">
                            <p class="result-label">
                                Predicted Mental Health Score
                            </p>
                            <h2>{prediction}</h2>
                            <p class="result-description">
                                This is a model-generated estimate,
                                not a clinical assessment.
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.warning(
                        "The API returned a response, but no "
                        "prediction field was found."
                    )

                with st.expander("View submitted information"):
                    st.json(payload)

                with st.expander("View complete API response"):
                    st.json(result)

            else:
                st.error(
                    f"API Error: {response.status_code}"
                )

                try:
                    st.json(response.json())
                except ValueError:
                    st.text(response.text[:1000])

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to the prediction API. "
                "Check API_URL or API_HOST and make sure the backend is running."
            )

        except requests.exceptions.Timeout:
            st.error(
                "The request took too long. Please try again."
            )

        except requests.exceptions.RequestException as error:
            st.error(f"Request failed: {error}")


# Footer

st.markdown(
    """
    <div class="footer">
        Built with Streamlit, FastAPI & Machine Learning
        <br>
    </div>
    """,
    unsafe_allow_html=True
)
