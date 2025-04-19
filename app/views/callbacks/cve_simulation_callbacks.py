from dash import Input, Output, State, ctx, ALL
from dash.exceptions import PreventUpdate
from app.views.pages.cve_simulation import get_unique_cves, patch_cve, build_cve_row

def register_cve_simulation_callbacks(app):
    @app.callback(
        Output("cve-sim-table-body", "children"),
        Output("patched-status-msg", "children"),
        Output("patched-cves-store", "data"),
        Output("page-indicator", "children"),
        Output("prev-page-btn", "disabled"),
        Output("next-page-btn", "disabled"),
        Input("all-cves-data", "data"),
        Input({"type": "patch-btn", "index": ALL}, "n_clicks"),
        Input("prev-page-btn", "n_clicks"),
        Input("next-page-btn", "n_clicks"),
        State("patched-cves-store", "data"),
        State("current-page", "data"),
    )
    def update_table(data, patch_clicks, prev_clicks, next_clicks, patched, current_page):
        page_size = 10
        triggered = ctx.triggered_id
        status_msg = ""

        filtered = [cve for cve in data if cve["CVE ID"] not in patched]
        total_pages = max((len(filtered) - 1) // page_size + 1, 1)

        # Handle patch
        if isinstance(triggered, dict) and triggered.get("type") == "patch-btn":
            index = triggered["index"]
            global_index = current_page * page_size + index
            if 0 <= global_index < len(filtered):
                cve_id = filtered[global_index]["CVE ID"]
                if cve_id not in patched:
                    patched.append(cve_id)
                    patch_cve(cve_id)
                    status_msg = f"Patched {cve_id}."
            filtered = [cve for cve in data if cve["CVE ID"] not in patched]
            total_pages = max((len(filtered) - 1) // page_size + 1, 1)

        # Pagination controls
        if triggered == "prev-page-btn" and current_page > 0:
            current_page -= 1
        elif triggered == "next-page-btn" and current_page < total_pages - 1:
            current_page += 1

        paginated = filtered[current_page * page_size: (current_page + 1) * page_size]
        rows = [build_cve_row(cve, i) for i, cve in enumerate(paginated)]

        return (
            rows,
            status_msg,
            patched,
            f"Page {current_page + 1} of {total_pages}",
            current_page == 0,
            current_page >= total_pages - 1,
        )

    @app.callback(
        Output("current-page", "data"),
        Input("prev-page-btn", "n_clicks"),
        Input("next-page-btn", "n_clicks"),
        State("current-page", "data"),
        prevent_initial_call=True
    )
    def update_page_store(prev_clicks, next_clicks, page):
        triggered = ctx.triggered_id
        if triggered == "prev-page-btn" and page > 0:
            return page - 1
        elif triggered == "next-page-btn":
            return page + 1
        return page
