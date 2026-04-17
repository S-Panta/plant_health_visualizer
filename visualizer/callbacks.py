# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 16:37:55 2026

@author: A02483178

callbacks.py
This file registers all callbacks through a register_callbacks(app) function,
 which is a common solution for putting Dash callbacks in a separate file 
 without breaking imports.
"""

import pandas as pd
from dash import Input, Output, State
from data import fetch_data
from figure import build_figure, THRESHOLD

def register_callbacks(app):
    @app.callback(
        Output("full-data-store", "data"),
        Input("interval", "n_intervals"),
        State("full-data-store", "data"),
        prevent_initial_call=False
    )
    def load_data_once(n, stored_data):
        if stored_data is None:
            df = fetch_data()
            return df.to_dict("records")
        return stored_data

    @app.callback(
        Output("current-index", "data"),
        Input("interval", "n_intervals"),
        State("current-index", "data"),
        State("full-data-store", "data")
    )
    def advance_index(n, current_index, stored_data):
        if not stored_data:
            return 1

        total_rows = len(stored_data)

        if current_index < total_rows:
            return current_index + 1

        return total_rows

    @app.callback(
        Output("live-graph", "figure"),
        Input("current-index", "data"),
        State("full-data-store", "data")
    )
    def update_graph(current_index, stored_data):
        if not stored_data:
            return build_figure(pd.DataFrame(columns=["DateTimeUTC", "DataValue"]))

        df = pd.DataFrame(stored_data)
        df["DateTimeUTC"] = pd.to_datetime(df["DateTimeUTC"])
        df["DataValue"] = pd.to_numeric(df["DataValue"], errors="coerce")

        visible_df = df.iloc[:current_index].copy()
        return build_figure(visible_df)

    @app.callback(
        Output("current-ndvi", "children"),
        Output("current-ndvi-sub", "children"),
        Output("harvest-status", "children"),
        Output("last-timestamp", "children"),
        Input("current-index", "data"),
        State("full-data-store", "data")
    )
    def update_kpis(current_index, stored_data):
        if not stored_data:
            return "--", "No data loaded", "--", "--"

        df = pd.DataFrame(stored_data)
        df["DateTimeUTC"] = pd.to_datetime(df["DateTimeUTC"])
        df["DataValue"] = pd.to_numeric(df["DataValue"], errors="coerce")

        visible_df = df.iloc[:current_index].copy()

        if visible_df.empty:
            return "--", "No visible data", "--", "--"

        latest_value = visible_df["DataValue"].iloc[-1]
        latest_time = visible_df["DateTimeUTC"].iloc[-1]

        if latest_value >= THRESHOLD:
            status = "Above"
            sub = "Crop is in harvest zone"
        elif latest_value >= THRESHOLD - 0.03:
            status = "Near"
            sub = "Approaching harvest threshold"
        else:
            status = "Below"
            sub = "Below harvest threshold"

        return (
            f"{latest_value:.3f}",
            sub,
            status,
            latest_time.strftime("%Y-%m-%d %H:%M")
        )