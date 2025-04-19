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

=====================================================
    CVSS METRICS OVERVIEW — FOR CVE ENRICHMENT LOGIC
=====================================================

## ***Common Vulnerability Scoring System SIG***

        References/Resources:
                https://www.first.org/cvss/v4.0/user-guide
                https://www.first.org/cvss/
                https://chandanbn.github.io/cvss/
                https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator
                https://nvd.nist.gov/vuln-metrics/cvss/v4-calculator
                https://gitlab-com.gitlab.io/gl-security/product-security/appsec/cvss-calculator/
                https://learn.habilelabs.io/cvss-calculator-software-vulnerability-scoring-process-25c6a3356751
                https://github.com/RedHatProductSecurity/cvss-v4-calculator
                
### Key Components and Acronyms

CVSS-B: Base Metrics  
Measures the intrinsic characteristics of a vulnerability that are constant over time.

CVSS-BE: Base and Environmental Metrics  
Base metrics plus the Environmental metrics that account for the characteristics unique to a user's environment.

CVSS-BT: Base and Threat Metrics  
Base metrics plus the Threat metrics that reflect the characteristics of a vulnerability that change over time.

CVSS-BTE: Base, Threat, and Environmental Metrics  
The combination of all three metric groups to provide the most comprehensive severity score.

### Metric Groups

#### 1. Base Metrics (Intrinsic)

Reflect the fundamental characteristics of a vulnerability.  
Used universally, regardless of the environment or specific threat intelligence.

Attack Vector (AV):
- Network (N): The attacker exploits the vulnerability remotely via the network.
- Adjacent (A): The attacker needs to be on the same shared physical or logical network.
- Local (L): The attacker needs to have local access to the vulnerable component.
- Physical (P): The attacker must physically interact with the vulnerable component.

Attack Complexity (AC):
- Low (L): Exploitation is straightforward and requires little effort.
- High (H): Exploitation is more complicated and requires additional conditions.

Attack Requirements (AT):
- None (N): No specific prerequisites for the attack.
- Low (L): Some conditions or preparation needed.

Privileges Required (PR):
- None (N): The attacker does not require any privileges to exploit the vulnerability.
- Low (L): The attacker needs low-level privileges.
- High (H): The attacker needs high-level privileges (e.g., root or admin).

User Interaction (UI):
- None (N): No user interaction required.
- Passive (P): The user interacts unknowingly.
- Active (A): The user must actively perform some action.

Vulnerable Confidentiality (VC):
- None (N): No impact on confidentiality.
- Low (L): Partial loss of confidentiality.
- High (H): Complete loss of confidentiality.

Vulnerable Integrity (VI):
- None (N): No impact on integrity.
- Low (L): Partial loss of integrity.
- High (H): Complete loss of integrity.

Vulnerable Availability (VA):
- None (N): No impact on availability.
- Low (L): Partial loss of availability.
- High (H): Complete loss of availability.

Subsequent Systems: Metrics to assess the impact of vulnerabilities on subsequent systems.
- Subsequent Confidentiality (SC)
- Subsequent Integrity (SI)
- Subsequent Availability (SA)

#### 2. Threat Metrics (Temporal)

Reflect the state of a vulnerability that may change over time.

Exploit Maturity (E): Previously known as "Exploit Code Maturity." Describes the availability of exploit code.
- None (N): No exploit available.
- Proof-of-Concept (P): Exploit exists as a proof of concept.
- Functional (F): Exploit is usable and available for attackers.

Threat Report Confidence (RC): Confidence level of the report for the vulnerability.
- Confirmed (C): High confidence that the vulnerability exists.
- Reasonable (R): Moderate confidence in the vulnerability.
- Uncorroborated (U): Low confidence.

#### 3. Environmental Metrics

Reflect how a vulnerability affects a user's specific environment.

Confidentiality Requirement (CR):
- Low (L): Confidentiality is of low importance.
- Medium (M): Confidentiality is of moderate importance.
- High (H): Confidentiality is of high importance.

Integrity Requirement (IR):
- Low (L): Integrity is of low importance.
- Medium (M): Integrity is of moderate importance.
- High (H): Integrity is of high importance.

Availability Requirement (AR):
- Low (L): Availability is of low importance.
- Medium (M): Availability is of moderate importance.
- High (H): Availability is of high importance.

Modified Attack Vector (MAV): Adjusts Attack Vector based on deployment conditions.

#### 4. Supplemental Metrics

Additional metrics that do not modify the score but provide further insight.

- Value Density (VD): Reflects the value of data on the system (Diffuse or Concentrated).
- Safety (S): Safety impact of exploiting a vulnerability.
- Automatable (A): Whether the exploitation can be automated.
- Recovery (R): Describes the system's resilience and recovery post-attack:
    - Automatic (A)
    - User Intervention (U)
    - Irrecoverable (I)

### Key Definitions

- Vulnerable System: The system directly affected by the vulnerability.
- Subsequent System: A system impacted as a result of exploiting the Vulnerable System.
- Chained Vulnerabilities: A scenario where multiple vulnerabilities are exploited in sequence.
- Chained Score: The CVSS score of two or more chained vulnerabilities.

### Scoring Rubrics

- Reasonable Worst-Case: Assessing the maximum plausible damage an attacker can cause given the vulnerability.
- Vulnerability Response Effort (VRE): Effort required to respond to the vulnerability after discovery.

"""
