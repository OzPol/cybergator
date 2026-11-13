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
    expect(page.get_by_role("link", name="Dashboard", exact=True)).to_be_visible()
    expect(page.get_by_text("Login/Register", exact=True)).to_have_count(0)

    page.get_by_role("link", name="Dashboard", exact=True).click()
    expect(page.get_by_role("heading", name="Dashboard Overview", exact=True)).to_be_visible()
    expect(page.locator("#resilience-pie-chart .js-plotly-plot")).to_be_visible()
    expect(page.locator("#page-content")).to_have_count(1)
    expect(page.locator("#system-resilience-score")).to_contain_text("System Resilience Score")

    page.get_by_role("link", name="System Graph", exact=True).click()
    expect(page.locator("#system-graph")).to_be_visible()
    page.get_by_role("button", name="Recalculate Resilience", exact=True).click()
    expect(page.locator("#resilience-recalculate-feedback")).to_contain_text("updated")

    page.get_by_role("link", name="System Tables", exact=True).click()
    expect(page.locator("#page-content")).to_contain_text("System")
    page.locator("#export-btn").click()
    expect(page.get_by_role("heading", name="Export Data", exact=True)).to_be_visible()
    browser.close()
    if errors:
        raise AssertionError("\n".join(errors))
print("Browser navigation, charts, graph, recalculation and export page passed.")
