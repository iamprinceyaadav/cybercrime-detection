# ============================================
# CYBERCRIME DETECTION SYSTEM
# Phishing + Fraud - Ek Hi App!
# ============================================
# Run: streamlit run main_app.py
# ============================================

import streamlit as st
import pickle
import numpy as np
import pandas as pd

# ----------------------------------------
# Page Setup
# ----------------------------------------
st.set_page_config(
    page_title="CyberCrime Detection System",
    page_icon="🔐",
    layout="centered"
)

# ----------------------------------------
# Header
# ----------------------------------------
st.title("🔐 CyberCrime Detection System")
st.write("AI-powered system to detect Phishing & Bank Fraud")
st.divider()

# ----------------------------------------
# Tab Banao - Dono Projects Ek Jagah
# ----------------------------------------
tab1, tab2 = st.tabs(["🎣 Phishing Detector", "💳 Bank Fraud Detector"])


# ============================================
# TAB 1 - PHISHING DETECTOR
# ============================================
with tab1:

    st.header("🎣 Phishing URL Detector")
    st.write("URL daalo — AI batayegi safe hai ya phishing!")
    st.divider()

    # Model load karo
    @st.cache_resource
    def load_phishing_model():
        with open('phishing_model.pkl', 'rb') as f:
            return pickle.load(f)

    phishing_model = load_phishing_model()

    # Features nikalne ka function
    def features_nikalo(url):
        features = {}
        features['url_length']   = len(url)
        features['at_count']     = url.count('@')
        features['hyphen_count'] = url.count('-')
        features['has_https']    = 1 if url.startswith('https') else 0
        features['slash_count']  = url.count('/')
        features['dot_count']    = url.count('.')
        features['has_ip']       = 1 if any(
            part.isdigit() for part in url.split('.')
        ) else 0
        return features

    # URL input
    url_input = st.text_input(
        "🔗 URL yahan daalo:",
        placeholder="jaise: http://fake-sbi-login.com/verify"
    )

    # Example URLs
    st.write("**Test ke liye examples:**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ Phishing Example"):
            url_input = "http://paypal.com.secure-login.tk/verify@account"
            st.code(url_input)
    with col2:
        if st.button("✅ Safe Example"):
            url_input = "https://www.google.com"
            st.code(url_input)

    # Check button
    if st.button("🔍 Check Karo", type="primary", key="phishing_btn"):

        if url_input == "":
            st.warning("⚠️ Pehle koi URL daalo!")
        else:
            # Features nikalo
            features = features_nikalo(url_input)
            features_df = pd.DataFrame([features])

            # Predict karo
            prediction = phishing_model.predict(features_df)[0]
            probability = phishing_model.predict_proba(features_df)[0]

            st.divider()

            # Result
            if prediction == 1:
                st.error("🚨 PHISHING URL HAI! MAT KHOLO!")
                st.metric("Fraud Probability", f"{probability[1]*100:.1f}%")
                st.warning("""
                ⚠️ **Kya karo:**
                - Yeh link kisi ko mat bhejo
                - Is website par login mat karo
                - Apna password change karo agar khola ho
                """)
            else:
                st.success("✅ URL Safe Lagti Hai!")
                st.metric("Safe Probability", f"{probability[0]*100:.1f}%")

            # URL Analysis
            st.divider()
            st.subheader("📊 URL Ki Analysis:")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("URL Length", features['url_length'])
                st.metric("@ Symbol", features['at_count'])
            with col2:
                st.metric("HTTPS", "✅" if features['has_https'] else "❌")
                st.metric("Dots", features['dot_count'])
            with col3:
                st.metric("Hyphens", features['hyphen_count'])
                st.metric("IP Address", "⚠️ Haan" if features['has_ip'] else "Nahi")

            # Probability bars
            st.divider()
            st.write("**Safe:**")
            st.progress(float(probability[0]))
            st.write("**Phishing:**")
            st.progress(float(probability[1]))


# ============================================
# TAB 2 - BANK FRAUD DETECTOR
# ============================================
with tab2:

    st.header("💳 Bank Fraud Detector")
    st.write("Real transaction examples se test karo!")
    st.divider()

    # Model load karo
    @st.cache_resource
    def load_fraud_model():
        with open('fraud_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('fraud_scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        return model, scaler

    @st.cache_data
    def load_fraud_data():
        return pd.read_csv('creditcard.csv')

    fraud_model, scaler = load_fraud_model()
    df = load_fraud_data()

    # Real examples
    fraud_examples  = df[df['Class'] == 1].head(20)
    normal_examples = df[df['Class'] == 0].head(20)

    # Options
    st.subheader("🎯 Test Karne Ka Tarika Chuno:")
    option = st.radio(
        "Kaunsa transaction?",
        [
            "🚨 Fraud Transaction Example",
            "✅ Normal Transaction Example",
            "🔢 Custom Row Number"
        ],
        key="fraud_radio"
    )

    if option == "🚨 Fraud Transaction Example":
        example_num = st.slider("Fraud Example:", 1, 20, 1, key="fraud_slider")
        selected = fraud_examples.iloc[example_num - 1]
        st.info("💡 Yeh actually ek FRAUD transaction hai!")

    elif option == "✅ Normal Transaction Example":
        example_num = st.slider("Normal Example:", 1, 20, 1, key="normal_slider")
        selected = normal_examples.iloc[example_num - 1]
        st.info("💡 Yeh actually ek NORMAL transaction hai!")

    else:
        idx = st.number_input(
            "Row number (0 to 284806):",
            min_value=0,
            max_value=len(df)-1,
            value=0
        )
        selected = df.iloc[int(idx)]

    # Transaction info
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💰 Amount", f"${selected['Amount']:.2f}")
    with col2:
        actual = "🚨 Fraud" if selected['Class'] == 1 else "✅ Normal"
        st.metric("📋 Actual Label", actual)

    # Check button
    if st.button("🔍 AI Se Check Karo", type="primary", key="fraud_btn"):

        # Features prepare
        amount_normalized = scaler.transform([[selected['Amount']]])[0][0]
        v_cols    = [f'V{i}' for i in range(1, 29)]
        v_features = selected[v_cols].values
        features   = np.append(v_features, amount_normalized).reshape(1, -1)

        # Predict
        prediction  = fraud_model.predict(features)[0]
        probability = fraud_model.predict_proba(features)[0]

        st.divider()
        st.subheader("🤖 AI Ka Result:")

        if prediction == 1:
            st.error("🚨 FRAUD TRANSACTION DETECTED!")
            st.metric("Fraud Probability", f"{probability[1]*100:.1f}%")
            if selected['Class'] == 1:
                st.success("✅ AI Sahi Hai! Yeh actually fraud tha!")
            else:
                st.warning("⚠️ False Alarm — actually normal tha")
        else:
            st.success("✅ Normal Transaction Hai!")
            st.metric("Safe Probability", f"{probability[0]*100:.1f}%")
            if selected['Class'] == 0:
                st.success("✅ AI Sahi Hai! Yeh actually normal tha!")
            else:
                st.error("❌ AI Miss Kar Gayi! Actually fraud tha")

        # Probability bars
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Normal", f"{probability[0]*100:.1f}%")
        with col2:
            st.metric("Fraud",  f"{probability[1]*100:.1f}%")
        st.write("Normal:")
        st.progress(float(probability[0]))
        st.write("Fraud:")
        st.progress(float(probability[1]))

    # Dataset stats
    st.divider()
    st.subheader("📈 Dataset Stats:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total", f"{len(df):,}")
    with col2:
        st.metric("Fraud Cases", f"{int(df['Class'].sum()):,}")
    with col3:
        st.metric("Fraud %", f"{df['Class'].mean()*100:.2f}%")

# ----------------------------------------
# Footer
# ----------------------------------------
st.divider()
st.caption("Made for College Internship 🎓 | AI-Enabled Cybercrime Detection System")
