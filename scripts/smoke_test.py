"""Exercise real HTTP APIs and Dash page callbacks with the bundled dataset."""
import json
import sys
from urllib.request import Request, urlopen

base = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:8000"


def fetch(path, payload=None):
    body = json.dumps(payload).encode() if payload is not None else None
    request = Request(base + path, data=body, headers={"Content-Type": "application/json"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


for endpoint in ("/healthz", "/_dash-layout", "/_dash-dependencies",
                 "/api/graph", "/api/resilience", "/api/sue-graph/"):
    fetch(endpoint)
    print("OK", endpoint)

score = fetch("/_dash-update-component", {
    "output": "system-resilience-score.children",
    "outputs": {"id": "system-resilience-score", "property": "children"},
    "inputs": [{"id": "session-user", "property": "data", "value": None}],
    "state": [], "changedPropIds": ["session-user.data"],
})
assert "System Resilience Score" in score["response"]["system-resilience-score"]["children"]
print("OK initial demo resilience score")

pages = ("/", "/welcome", "/dashboard", "/sue-graph", "/system-graph", "/system-tables",
         "/system-tables/cves", "/system-tables/nodes", "/system-tables/software-nodes",
         "/system-tables/software-unique", "/system-tables/critical-functions", "/export",
         "/environmental-factors", "/neo4j-graph", "/work-stations",
         "/node-association-manager", "/apt-simulation", "/cve-simulation", "/fsm-simulation",
         "/about/oz", "/about/jess", "/about/samson", "/about/andrew", "/about/shayan")
for page in pages:
    response = fetch("/_dash-update-component", {
        "output": "page-content.children",
        "outputs": {"id": "page-content", "property": "children"},
        "inputs": [{"id": "url", "property": "pathname", "value": page}],
        "state": [{"id": "session-user", "property": "data", "value": None}],
        "changedPropIds": ["url.pathname"],
    })
    assert "page-content" in response["response"], page
    print("OK page", page)
print("Sample-data demo smoke checks passed.")
