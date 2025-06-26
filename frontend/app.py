import streamlit as st
import requests

# Page configuration
st.set_page_config(page_title="AI Wedding Planner", layout="centered")

# 💄 CSS Styling for background, input, and button
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1597157639073-69284dc0fdaf?q=80&w=2074&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    .main > div {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(0,0,0,0.1);
    }

    h1, h2, h3, h4, h5 {
        color: #800000;
    }

    .stTextInput > div > input {
        color: black !important;
        background-color: #fdf5f5 !important;
        border: 1px solid #ccc;
    }

    .stButton>button {
        background-color: #800000;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        transition: 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #a83232;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App Title
st.title("💒 AI Wedding Planner Assistant")

# Backend API URL
BASE_URL = "http://127.0.0.1:8000"

# User input
user_query = st.text_input("Ask a question (e.g. best venue in Madurai)", placeholder="Type your question...")

# AI response
if st.button("Get Answer") and user_query.strip() != "":
    with st.spinner("Thinking..."):
        try:
            res = requests.post(f"{BASE_URL}/ask", params={"query": user_query})

            # Show raw response for debug
            st.subheader("🔍 Raw Response")
            st.code(res.text)

            # Parse and display
            response_json = res.json()
            st.subheader("💡 AI Wedding Suggestion")
            st.success(response_json["response"])

        except Exception as e:
            st.error(f"⚠️ Error: Could not get a proper response.\n\n{e}")

# Budget Estimator
st.markdown("---")
st.subheader("🧮 Wedding Budget Estimator")

guest_count = st.number_input("Number of guests", min_value=0, step=10)
venue_cost = st.number_input("Venue cost (₹)", min_value=0)
catering_cost = st.number_input("Cost per plate (₹)", min_value=0)
photo_cost = st.number_input("Photography package (₹)", min_value=0)
invite_cost = st.number_input("Invitation printing (₹ for 100 cards)", min_value=0)

if st.button("Calculate Total Budget"):
    total = venue_cost + (guest_count * catering_cost) + photo_cost + invite_cost
    st.success(f"💰 Estimated Total Wedding Cost: ₹{total:,}")
