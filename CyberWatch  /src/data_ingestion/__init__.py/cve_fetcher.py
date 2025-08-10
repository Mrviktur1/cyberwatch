# src/data_ingestion/cve_fetcher.py
import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_recent_cves(api_key=None, days=7):
    url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
    params = {
        "pubStartDate": (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S:000 UTC-00:00"),
        "resultsPerPage": 50
    }
    headers = {"apiKey": api_key} if api_key else {}
    
    response = requests.get(url, params=params, headers=headers)
    return pd.DataFrame([
        {
            "CVE_ID": item["cve"]["CVE_data_meta"]["ID"],
            "Description": item["cve"]["description"]["description_data"][0]["value"],
            "Severity": item["impact"].get("baseMetricV3", {}).get("cvssV3", {}).get("baseSeverity", "UNKNOWN"),
            "Published": item["publishedDate"]
        }
        for item in response.json()["result"]["CVE_Items"]
    ])