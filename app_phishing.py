# ============================================
# STEP 4 - Streamlit App (Live Demo!)
# ============================================
# Yeh file run karne ke liye terminal mein likho:
# streamlit run app_phishing.py
# ============================================

import streamlit as st
import pickle
import pandas as pd

# ----------------------------------------
# Page Setup
# ----------------------------------------
st.set_page_config(
    page_title="Phishing URL Detector",
    page_icon="🎣",
    layout="centered"
)

# Title
st.title("🎣 Phishing URL Detector")
st.write("URL daalo — AI batayegi safe hai ya phishing!")
st.divider()

# ----------------------------------------
# Model Load Karo
# ----------------------------------------
@st.cache_resource  # Ek baar load hoga, baar baar nahi
def model_load_karo():
    with open('phishing_model.pkl', 'rb') as f:
        return pickle.load(f)

model = model_load_karo()

# ----------------------------------------
# Features Nikalne Ka Function
# (Step 2 wala hi function)
# ----------------------------------------
def features_nikalo(url):
    features = {}
    features['url_length'] = len(url)
    features['at_count'] = url.count('@')
    features['hyphen_count'] = url.count('-')
    features['has_https'] = 1 if url.startswith('https') else 0
    features['slash_count'] = url.count('/')
    features['dot_count'] = url.count('.')
    features['has_ip'] = 1 if any(
        part.isdigit() for part in url.split('.')
    ) else 0
    return features

# ----------------------------------------
# User Input
# ----------------------------------------
url_input = st.text_input(
    "🔗 URL yahan daalo:",
    placeholder="jaise: http://fake-sbi-login.com/verify"
)

# ----------------------------------------
# Check Button
# ----------------------------------------
if st.button("🔍 Check Karo", type="primary"):

    if url_input == "":
        st.warning("⚠️ Pehle koi URL daalo!")

    else:
        # Features nikalo
        features = features_nikalo(url_input)
        features_df = pd.DataFrame([features])

        # AI se predict karo
        prediction = model.predict(features_df)[0]
        probability = model.predict_proba(features_df)[0]

        st.divider()

        # Result dikhao
        if prediction == 1:
            # PHISHING!
            st.error("🚨 PHISHING URL HAI! MAT KHOLO!")
            st.metric(
                label="Phishing Probability",
                value=f"{probability[1]*100:.1f}%"
            )
            st.write("**Yeh URL dangerous lag rahi hai. Kisi ko mat dena yeh link!**")

        else:
            # SAFE!
            st.success("✅ URL Safe Lagti Hai!")
            st.metric(
                label="Safe Probability",
                value=f"{probability[0]*100:.1f}%"
            )
            st.write("**Yeh URL safe lagti hai. Phir bhi personal info share mat karo!**")

        # Features dikhao
        st.divider()
        st.subheader("📊 URL Ki Analysis:")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("URL Length", features['url_length'])
            st.metric("HTTPS", "✅ Haan" if features['has_https'] else "❌ Nahi")
            st.metric("@ Count", features['at_count'])

        with col2:
            st.metric("Dots", features['dot_count'])
            st.metric("Hyphens", features['hyphen_count'])
            st.metric("IP Address?", "⚠️ Haan" if features['has_ip'] else "Nahi")

# ----------------------------------------
# Footer
# ----------------------------------------
st.divider()
st.caption("Made by Prince Yadav 👨‍💻 | AI-Enabled Cybercrime Detection System")