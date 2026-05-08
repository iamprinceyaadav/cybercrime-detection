# ============================================
# CYBERCRIME DETECTION SYSTEM
# Self-Training App - Streamlit Cloud Ready
# Made by Prince Yadav
# ============================================

import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

# ----------------------------------------
# Page Setup
# ----------------------------------------
st.set_page_config(
    page_title="CyberCrime Detection System",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 CyberCrime Detection System")
st.write("AI-powered system to detect Phishing & Bank Fraud")
st.divider()

# ============================================
# PHISHING MODEL
# ============================================

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

@st.cache_resource
def train_phishing_model():
    data = {
        'url': [
            'https://www.google.com',
            'https://www.youtube.com',
            'https://www.facebook.com',
            'https://www.amazon.com',
            'https://www.wikipedia.org',
            'https://www.github.com',
            'https://www.microsoft.com',
            'https://www.apple.com',
            'https://www.twitter.com',
            'https://www.linkedin.com',
            'https://www.netflix.com',
            'https://www.reddit.com',
            'https://www.instagram.com',
            'https://www.stackoverflow.com',
            'https://www.python.org',
            'https://www.sbi.co.in',
            'https://www.hdfcbank.com',
            'https://www.icicibank.com',
            'https://www.irctc.co.in',
            'https://www.flipkart.com',
            'http://paypal.com.secure-login.tk/verify@account',
            'http://192.168.1.1/bank/login/secure',
            'http://sbi-bank-secure-login.com/verify',
            'http://amazon.com.deals-login.xyz/account',
            'http://secure.paypal.com.phishing.net/login',
            'http://login-facebook.com.fake.tk/auth',
            'http://apple-id.com-verify.net/signin',
            'http://hdfc-bank-login-secure.tk/verify',
            'http://irctc-booking.fake-site.com/login@user',
            'http://flipkart.com.offer-claim.xyz/deal',
            'http://google.com.account-verify.tk/signin',
            'http://netflix.com-login.phish.net/account',
            'http://income-tax-refund.fake.com/claim@now',
            'http://10.0.0.1/login/bank/secure/verify',
            'http://sbi.co.in.secure-login-portal.tk/auth',
            'http://microsoft.com-account.verify.xyz/login',
            'http://free-recharge-offer.fake.tk/claim@prize',
            'http://covid-relief-fund.scam.net/apply@now',
            'http://uidai-aadhar-update.fake.com/verify@id',
            'http://pm-kisan-yojana.scam.tk/apply@benefit',
        ],
        'label': [
            0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,
            1,1,1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,1,1,
        ]
    }

    df = pd.DataFrame(data)
    feature_list = [features_nikalo(str(url)) for url in df['url']]
    X = pd.DataFrame(feature_list)
    y = df['label']

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

@st.cache_resource
def train_fraud_model():
    np.random.seed(42)

    normal        = np.random.normal(0, 1, (1000, 29))
    normal[:, 28] = np.abs(np.random.normal(100, 50, 1000))
    normal_labels = np.zeros(1000)

    fraud         = np.random.normal(0, 1, (200, 29))
    fraud[:, 0]   = np.random.normal(-3, 1, 200)
    fraud[:, 3]   = np.random.normal(-3, 1, 200)
    fraud[:, 28]  = np.abs(np.random.normal(800, 200, 200))
    fraud_labels  = np.ones(200)

    X = np.vstack([normal, fraud])
    y = np.hstack([normal_labels, fraud_labels])

    smote       = SMOTE(random_state=42)
    X_bal, y_bal = smote.fit_resample(X, y)

    scaler         = StandardScaler()
    X_bal[:, 28]   = scaler.fit_transform(
        X_bal[:, 28].reshape(-1, 1)
    ).ravel()

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_bal, y_bal)
    return model, scaler

# ============================================
# MODELS TRAIN KARO
# ============================================
with st.spinner("🤖 AI Models load ho rahe hain... thoda wait karo!"):
    phishing_model          = train_phishing_model()
    fraud_model, scaler     = train_fraud_model()

st.success("✅ AI Models Ready Hain!")
st.divider()

# ============================================
# TABS
# ============================================
tab1, tab2 = st.tabs(["🎣 Phishing Detector", "💳 Bank Fraud Detector"])

# ============================================
# TAB 1 - PHISHING DETECTOR
# ============================================
with tab1:
    st.header("🎣 Phishing URL Detector")
    st.write("URL daalo — AI batayegi safe hai ya phishing!")
    st.divider()

    url_input = st.text_input(
        "🔗 URL yahan daalo:",
        placeholder="jaise: http://fake-sbi-login.com/verify"
    )

    st.write("**Test ke liye examples:**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ Phishing Example", key="p1"):
            url_input = "http://sbi-bank-secure-login.tk/verify@account"
            st.code(url_input)
    with col2:
        if st.button("✅ Safe Example", key="p2"):
            url_input = "https://www.google.com"
            st.code(url_input)

    if st.button("🔍 Check Karo", type="primary", key="phishing_btn"):
        if url_input == "":
            st.warning("⚠️ Pehle koi URL daalo!")
        else:
            features    = features_nikalo(url_input)
            features_df = pd.DataFrame([features])
            prediction  = phishing_model.predict(features_df)[0]
            probability = phishing_model.predict_proba(features_df)[0]

            st.divider()
            if prediction == 1:
                st.error("🚨 PHISHING URL HAI! MAT KHOLO!")
                st.metric("Phishing Probability", f"{probability[1]*100:.1f}%")
                st.warning("""
                ⚠️ **Kya karo:**
                - Yeh link kisi ko mat bhejo
                - Is website par login mat karo
                - Apna password change karo agar khola ho
                """)
            else:
                st.success("✅ URL Safe Lagti Hai!")
                st.metric("Safe Probability", f"{probability[0]*100:.1f}%")

            st.divider()
            st.subheader("📊 URL Ki Analysis:")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("URL Length", features['url_length'])
                st.metric("@ Symbol",   features['at_count'])
            with col2:
                st.metric("HTTPS", "✅" if features['has_https'] else "❌")
                st.metric("Dots",  features['dot_count'])
            with col3:
                st.metric("Hyphens",    features['hyphen_count'])
                st.metric("IP Address", "⚠️ Haan" if features['has_ip'] else "Nahi")

            st.write("Safe:")
            st.progress(float(probability[0]))
            st.write("Phishing:")
            st.progress(float(probability[1]))

# ============================================
# TAB 2 - FRAUD DETECTOR
# ============================================
with tab2:
    st.header("💳 Bank Fraud Detector")
    st.write("Transaction details daalo — AI batayegi fraud hai ya nahi!")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input(
            "💰 Amount (₹)",
            min_value=0.0,
            max_value=100000.0,
            value=500.0,
            step=100.0
        )
    with col2:
        hour = st.slider("🕐 Time (Hour)", 0, 23, 14)

    st.subheader("Transaction Pattern:")
    col1, col2 = st.columns(2)
    with col1:
        v1 = st.slider(
            "Spending Pattern",
            min_value=-5.0,
            max_value=5.0,
            value=0.0,
            step=0.1,
            help="Normal: 0 ke paas | Fraud: -3 ke paas"
        )
    with col2:
        v4 = st.slider(
            "Location Pattern",
            min_value=-5.0,
            max_value=5.0,
            value=0.0,
            step=0.1,
            help="Normal: 0 ke paas | Fraud: -3 ke paas"
        )

    st.write("**Quick Test:**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚨 Fraud Example", key="f1"):
            st.info("Amount: ₹8000 | Spending: -3.5 | Location: -3.0")
    with col2:
        if st.button("✅ Normal Example", key="f2"):
            st.info("Amount: ₹500 | Spending: 0.0 | Location: 0.0")

    if st.button("🔍 Fraud Check Karo", type="primary", key="fraud_btn"):
        features        = np.zeros(29)
        features[0]     = v1
        features[3]     = v4
        features[28]    = scaler.transform([[amount]])[0][0]
        features_reshaped = features.reshape(1, -1)

        prediction  = fraud_model.predict(features_reshaped)[0]
        probability = fraud_model.predict_proba(features_reshaped)[0]

        st.divider()
        st.subheader("🤖 AI Ka Result:")

        if prediction == 1:
            st.error("🚨 FRAUD TRANSACTION DETECTED!")
            st.metric("Fraud Probability", f"{probability[1]*100:.1f}%")
            st.warning("""
            ⚠️ **Kya karo:**
            - Apna card turant block karo
            - Bank helpline call karo
            - Transaction authorize mat karo
            """)
        else:
            st.success("✅ Normal Transaction Hai!")
            st.metric("Safe Probability", f"{probability[0]*100:.1f}%")

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

        st.divider()
        st.subheader("📊 Transaction Summary:")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Amount", f"₹{amount:,.0f}")
        with col2:
            st.metric("Time", f"{hour}:00")
        with col3:
            risk = "High 🔴" if probability[1] > 0.5 else "Low 🟢"
            st.metric("Risk", risk)

# ----------------------------------------
# Footer
# ----------------------------------------
st.divider()
st.caption("Made by Prince Yadav 👨‍💻 | AI-Enabled Cybercrime Detection System")
