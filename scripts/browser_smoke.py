"""Browser checks for the local sample-data demo (requires Playwright Chromium)."""
import sys
from playwright.sync_api import sync_playwright, expect

base = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:8000"

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 1050})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("response", lambda response: errors.append(f"HTTP {response.status}: {response.url}")
            if response.url.startswith(base) and response.status >= 500 else None)
    page.goto(base, wait_until="networkidle")
    expect(page.locator(".banner-title")).to_have_text("CyberGators")
    expect(page.get_by_role("link", name="Dashboard", exact=True)).to_be_visible()
    expect(page.get_by_text("Login/Register", exact=True)).to_have_count(0)

    page.get_by_role("link", name="Dashboard", exact=True).click()
    expect(page.get_by_role("heading", name="Dashboard Overview", exact=True)).to_be_visible()
    expect(page.locator("#resilience-pie-chart .js-plotly-plot")).to_be_visible()
    expect(page.locator("#page-content")).to_have_count(1)
    expect(page.locator("#system-resilience-score")).to_contain_text("System Resilience Score")

    page.get_by_role("link", name="System Graph", exact=True).click()
    expect(page.locator("#system-graph")).to_be_visible()
    original_nodes = page.request.get(base + "/api/nodes/").json()
    original_score = page.request.get(base + "/api/resilience").json()["system_resilience_score"]
    # Exercise the actual Remove Node callback with a selected node, then use the
    # real reset menu. This changes only the isolated CI container's sample data.
    for count in (1, 2):
        for index, node in enumerate(original_nodes[:count], start=1):
            response = page.request.post(base + "/_dash-update-component", data={
                "output": "remove-node-feedback.children",
                "outputs": {"id": "remove-node-feedback", "property": "children"},
                "inputs": [{"id": "remove-node-button", "property": "n_clicks", "value": index}],
                "state": [{"id": "system-graph", "property": "tapNodeData",
                           "value": {"id": node["node_id"]}}],
                "changedPropIds": ["remove-node-button.n_clicks"],
            })
            assert response.ok, response.text()
            assert "removed successfully" in response.json()["response"]["remove-node-feedback"]["children"]
        assert len(page.request.get(base + "/api/nodes/").json()) == len(original_nodes) - count
        page.get_by_role("button", name="Refresh Graph", exact=True).click()
        page.get_by_role("button", name="Recalculate Resilience", exact=True).click()
        expect(page.locator("#resilience-recalculate-feedback")).to_contain_text("updated")
        assert page.request.get(base + "/api/resilience").json()["system_resilience_score"] != original_score

        page.get_by_role("button", name="Reset Options", exact=True).click()
        with page.expect_navigation(wait_until="networkidle"):
            page.locator("#reset-all").click()
        expect(page.locator("#system-graph")).to_be_visible()
        assert page.request.get(base + "/api/nodes/").json() == original_nodes
        assert page.request.get(base + "/api/resilience").json()["system_resilience_score"] == original_score

    page.get_by_role("link", name="System Tables", exact=True).click()
    expect(page.locator("#page-content")).to_contain_text("System")
    page.locator("#export-btn").click()
    expect(page.get_by_role("heading", name="Export Data", exact=True)).to_be_visible()
    browser.close()
    if errors:
        raise AssertionError("\n".join(errors))
print("Browser navigation, charts, graph, delete/recalculate/reset cycles and export page passed.")
