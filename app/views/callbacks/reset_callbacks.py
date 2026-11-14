import logging
from time import time_ns

from dash import Input, Output, State, no_update
from dash.exceptions import PreventUpdate

from app.services.reset_service import reset_all_data

logger = logging.getLogger(__name__)


def register_reset_callbacks(app):
    @app.callback(
        Output("url-refresh", "href"),
        Output("resilience-recalculate-feedback", "children", allow_duplicate=True),
        Input("reset-all", "n_clicks"),
        State("url", "pathname"),
        prevent_initial_call=True,
    )
    def reset_all(n_clicks, pathname):
        if not n_clicks:
            raise PreventUpdate
        try:
            reset_all_data()
        except Exception:
            logger.exception("Reset All failed")
            return no_update, "Reset failed. Check the application logs; no success was reported."
        path = pathname if pathname and pathname.startswith("/") and not pathname.startswith("//") else "/welcome"
        # Force a full browser refresh to clear edited tables, selections and graphs.
        return f"{path}?reset={time_ns()}", no_update
