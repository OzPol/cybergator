import os
import requests
import pandas as pd
from collections import defaultdict
from dotenv import load_dotenv
from app.services.data_loader import get_nodes, save_nodes_data

load_dotenv()

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
KEY = os.getenv("NVD_API_KEY")


class CVEService:
    """
    A service for handling CVE data:
    - Fetches CVE details from the NVD API.
    - Aggregates internal CVE statistics from node data.
    - Applies patches to remove CVEs from affected nodes.
    """

    @staticmethod
    def get_cve_info(cve_id):
        """Fetch CVE details including NVD score from the NVD API."""
        headers = {}
        if KEY:
            headers["apiKey"] = KEY

        params = {"cveId": cve_id}
        response = requests.get(NVD_API_URL, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            vulnerabilities = data.get("vulnerabilities", [])
            if not vulnerabilities:
                return {"error": f"No data found for {cve_id}"}, 404

            cve_data = vulnerabilities[0].get("cve", {})
            metrics = cve_data.get("metrics", {})
            cvss_scores = (
                metrics.get("cvssMetricV40", []) or 
                metrics.get("cvssMetricV31", []) or 
                metrics.get("cvssMetricV30", []) or 
                metrics.get("cvssMetricV2", [])
            )

            if cvss_scores:
                cvss_data = cvss_scores[0]["cvssData"]
                nvd_score = cvss_data["baseScore"]
            else:
                nvd_score = ""

            return {
                "CVE ID": cve_id,
                "NVD Score": nvd_score,
            }, 200

        return {"error": f"Error fetching CVE data: {response.status_code}"}, response.status_code

    @staticmethod
    def get_unique_cves():
        """Aggregate unique CVEs from all nodes and compute their impact."""
        nodes_data = get_nodes()
        cve_summary = defaultdict(lambda: {"NVD Score": 0, "Nodes": set()})

        for node in nodes_data:
            node_id = node["node_id"]
            for cve_id, nvd_score in node.get("CVE_NVD", {}).items():
                cve_summary[cve_id]["NVD Score"] = nvd_score
                cve_summary[cve_id]["Nodes"].add(node_id)

        records = []
        for cve_id, info in cve_summary.items():
            node_count = len(info["Nodes"])
            nvd = info["NVD Score"]
            records.append({
                "CVE ID": cve_id,
                "Nodes Affected": node_count,
                "Impact Score": round(node_count * nvd, 2),
            })

        df = pd.DataFrame(records)
        df.sort_values("Impact Score", ascending=False, inplace=True)
        return df

    @staticmethod
    def patch_cve(cve_id):
        """Remove the specified CVE from all affected nodes."""
        nodes_data = get_nodes()
        for node in nodes_data:
            if cve_id in node.get("CVE", []):
                node["CVE"].remove(cve_id)
                node.get("CVE_NVD", {}).pop(cve_id, None)
        save_nodes_data(nodes_data)
