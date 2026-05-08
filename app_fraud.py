# ============================================
# BANK FRAUD DETECTOR - Fixed App
# ============================================
# Run: streamlit run app_fraud.py
# ============================================

import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Page Setup
st.set_page_config(
    page_title="Bank Fraud Detector",
    page_icon="💳",
    layout="centered"
)

st.title("💳 Bank Fraud Detector")
st.write("Real transaction examples se test karo!")
st.divider()

# ----------------------------------------
# Model Load Karo
# ----------------------------------------
@st.cache_resource
def load_model():
    with open('fraud_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('fraud_scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    return model, scaler

@st.cache_data
def load_data():
    df = pd.read_csv('creditcard.csv')
    return df

model, scaler = load_model()
df = load_data()

# ----------------------------------------
# Real Examples Dataset Se Lo
# ----------------------------------------
fraud_examples = df[df['Class'] == 1].head(20)
normal_examples = df[df['Class'] == 0].head(20)

# ----------------------------------------
# User Ko Options Do
# ----------------------------------------
st.subheader("🎯 Test Karne Ka Tarika Chuno:")

option = st.radio(
    "Kaunsa transaction test karna hai?",
    [
        "🚨 Fraud Transaction Example",
        "✅ Normal Transaction Example",
        "🔢 Custom Row Number Daalo"
    ]
)

if option == "🚨 Fraud Transaction Example":
    example_num = st.slider("Fraud Example Number:", 1, 20, 1)
    selected = fraud_examples.iloc[example_num - 1]
    st.info("💡 Yeh actually ek FRAUD transaction hai dataset mein")

elif option == "✅ Normal Transaction Example":
    example_num = st.slider("Normal Example Number:", 1, 20, 1)
    selected = normal_examples.iloc[example_num - 1]
    st.info("💡 Yeh actually ek NORMAL transaction hai dataset mein")

else:
    idx = st.number_input(
        "Dataset mein row number daalo (0 to 284806):",
        min_value=0,
        max_value=len(df)-1,
        value=0
    )
    selected = df.iloc[int(idx)]

# Transaction details dikhao
st.divider()
col1, col2 = st.columns(2)
with col1:
    st.metric("💰 Amount", f"${selected['Amount']:.2f}")
with col2:
    actual = "🚨 Fraud" if selected['Class'] == 1 else "✅ Normal"
    st.metric("📋 Actual Label", actual)

# ----------------------------------------
# Predict Button
# ----------------------------------------
if st.button("🔍 AI Se Check Karo", type="primary"):

    # Amount normalize karo
    amount_normalized = scaler.transform([[selected['Amount']]])[0][0]

    # V1-V28 features lo directly dataset se
    v_cols = [f'V{i}' for i in range(1, 29)]
    v_features = selected[v_cols].values

    # Final input banao
    features = np.append(v_features, amount_normalized).reshape(1, -1)

    # AI se predict karo
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]

    st.divider()
    st.subheader("🤖 AI Ka Result:")

    if prediction == 1:
        st.error("🚨 FRAUD TRANSACTION DETECTED!")
        st.metric("Fraud Probability", f"{probability[1]*100:.1f}%")

        if selected['Class'] == 1:
            st.success("✅ AI Sahi Hai! Yeh actually fraud tha!")
        else:
            st.warning("⚠️ AI Galat Hai! False Alarm tha")

    else:
        st.success("✅ Normal Transaction Hai!")
        st.metric("Safe Probability", f"{probability[0]*100:.1f}%")

        if selected['Class'] == 0:
            st.success("✅ AI Sahi Hai! Yeh actually normal tha!")
        else:
            st.error("❌ AI Miss Kar Gayi! Yeh actually fraud tha")

    # Probability bars
    st.divider()
    st.subheader("📊 Probability Breakdown:")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Normal", f"{probability[0]*100:.1f}%")
    with col2:
        st.metric("Fraud", f"{probability[1]*100:.1f}%")

    st.write("Normal:")
    st.progress(float(probability[0]))
    st.write("Fraud:")
    st.progress(float(probability[1]))

# ----------------------------------------
# Dataset Stats
# ----------------------------------------
st.divider()
st.subheader("📈 Dataset Stats:")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Transactions", f"{len(df):,}")
with col2:
    st.metric("Fraud Cases", f"{int(df['Class'].sum()):,}")
with col3:
    st.metric("Fraud %", f"{df['Class'].mean()*100:.2f}%")

st.divider()
st.caption("Made by Prince Yadav 👨‍💻 | AI-Enabled Cybercrime Detection System")