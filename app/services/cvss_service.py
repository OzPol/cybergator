import requests
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

# API Setup
NVD_API_KEY = os.getenv("NVD_API_KEY")
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

HEADERS = {
    "User-Agent": "CyberResilienceResearchTool/1.0",
    "apiKey": NVD_API_KEY
} if NVD_API_KEY else {"User-Agent": "CyberResilienceResearchTool/1.0"}

# Where to save CVSS results
CVSS_CACHE_PATH = os.path.join("app", "data", "nvd_results.json")

# Extract unique CVEs from system nodes
def extract_unique_cves(nodes):
    cve_set = set()
    for node in nodes:
        for cve in node.get("CVE", []):
            if isinstance(cve, str) and cve.startswith("CVE-"):
                cve_set.add(cve.strip())
    return sorted(cve_set)

# Query NVD API for metadata
def fetch_cvss_metadata(cve_list, delay=0.3):
    results = {}

    for cve_id in cve_list:
        try:
            params = {"cveId": cve_id}
            response = requests.get(NVD_API_URL, headers=HEADERS, params=params)
            response.raise_for_status()
            data = response.json()
            vulnerabilities = data.get("vulnerabilities", [])

            if not vulnerabilities:
                results[cve_id] = {"error": "No data returned"}
                time.sleep(delay)
                continue

            cve_data = vulnerabilities[0].get("cve", {})
            metrics = cve_data.get("metrics", {})
            cvss = None
            version_used = None

            for version_key in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
                if version_key in metrics and metrics[version_key]:
                    metric = metrics[version_key][0]
                    if "cvssData" in metric:
                        cvss = metric["cvssData"]
                        version_used = version_key.replace("cvssMetric", "CVSS ")
                        break

            if cvss:
                results[cve_id] = {
                    "base_score": cvss.get("baseScore"),
                    "attack_vector": cvss.get("attackVector", cvss.get("accessVector")),
                    "privileges_required": cvss.get("privilegesRequired") if version_used != "CVSS V2" else "NA",
                    "user_interaction": cvss.get("userInteraction") if version_used != "CVSS V2" else "NA",
                    "vector_string": cvss.get("vectorString"),
                    "cvss_version": version_used,
                    "error": None
                }
            else:
                results[cve_id] = {"error": "No CVSS data found"}

        except Exception as e:
            results[cve_id] = {"error": str(e)}

        time.sleep(delay)

    return results

# Save results to file
def write_cvss_cache(cache_path, data):
    with open(cache_path, "w") as f:
        json.dump(data, f, indent=4)





"""
cvss_service.py

This service queries the NVD (National Vulnerability Database) CVE 2.0 API
to extract structured CVSS metadata for known vulnerabilities (CVEs)
present in the system's nodes.

▶ PURPOSE
- Support attack simulation, reachability analysis, and resilience scoring
- Dynamically retrieve and structure per-CVE CVSS data for runtime use

▶ INPUT
- List of nodes (from Nodes_Complete.json)
- Each node may contain a list of CVE IDs under its "CVE" field

▶ OUTPUT
- Dictionary: {CVE ID → CVSS metadata}, where metadata includes:
    - Base Score
    - Attack Vector
    - Privileges Required
    - User Interaction
    - Vector String
    - CVSS Version

▶ API DETAILS
- Source: https://services.nvd.nist.gov/rest/json/cves/2.0
- Rate limited (1 request/sec), API key required via .env file:
    NVD_API_KEY

▶ USAGE
    from app.services.cvss_service import get_cvss_metrics_by_cve
    cve_lookup = get_cvss_metrics_by_cve(nodes_data)
"""
