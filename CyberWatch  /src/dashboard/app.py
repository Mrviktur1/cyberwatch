# src/dashboard/app.py
import streamlit as st
from src.data_ingestion.cve_fetcher import fetch_recent_cves
from src.data_ingestion.otx_client import get_pulse_indicators

st.set_page_config(layout="wide")
st.title("CyberThreatWatch - Live Threat Intelligence")

# Data Refresh
if st.button("Refresh Data"):
    with st.spinner("Loading threat data..."):
        cve_data = fetch_recent_cves(st.secrets["nvd_api_key"])
        otx_data = get_pulse_indicators(st.secrets["otx_api_key"])

# Display Data
col1, col2 = st.columns(2)
with col1:
    st.subheader("Recent CVEs")
    st.dataframe(cve_data, height=500)
with col2:
    st.subheader("Malware Indicators")
    st.dataframe(otx_data, height=500)