import requests
import os
from dotenv import load_dotenv

load_dotenv()
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
KEY = os.getenv("NVD_API_KEY")

class CVEService:
    """
    Service to fetch CVE details from the NVD API. 
    Returns CVE id and NVD score. 
    """
    
    @staticmethod
    def get_cve_info(cve_id):
        """Fetch CVE details including NVD score from NVD API."""
        
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

            # Extract CVSS score (latest version available)
            metrics = cve_data.get("metrics", {})
            cvss_scores = metrics.get("cvssMetricV40", []) or metrics.get("cvssMetricV31", []) or metrics.get("cvssMetricV30", []) or metrics.get("cvssMetricV2", [])
            
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
