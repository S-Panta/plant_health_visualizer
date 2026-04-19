# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 16:37:55 2026

@author: A02483178

callbacks.py
This file registers all callbacks through a register_callbacks(app) function,
which is a common solution for putting Dash callbacks in a separate file
without breaking imports.
"""

import random
from datetime import datetime, timedelta

import pandas as pd
from dash import Input, Output, State, html

from data import fetch_data
from figure import build_figure, THRESHOLD


def random_forecast_rows():
    conditions = [
        ("☀️", "Sunny"),
        ("⛅", "Partly cloudy"),
        ("☁️", "Overcast"),
        ("🌦", "Light drizzle"),
        ("🌧", "Heavy showers"),
        ("🌩", "Storms"),
    ]

    today = datetime.today()
    rows = []

    for i in range(7):
        date_obj = today + timedelta(days=i)

        if i == 0:
            day_label = "Today"
        else:
            day_label = date_obj.strftime("%a %b %d")

        icon, condition = random.choice(conditions)
        high_temp = random.randint(50, 92)
        low_temp = high_temp - random.randint(8, 18)
        rain = random.choice([0, 0, 0, 0.02, 0.05, 0.08, 0.15, 0.24])

        rows.append(
            html.Div([
                html.Div(day_label, className="forecast-day"),
                html.Div([
                    html.Span(icon, className="forecast-icon"),
                    html.Span(condition, className="forecast-condition")
                ], className="forecast-condition-wrap"),
                html.Div(f'{rain:.2f}"' if rain > 0 else "", className="forecast-rain"),
                html.Div([
                    html.Span(f"{high_temp}°", className="forecast-high"),
                    html.Span(f" / {low_temp}°", className="forecast-low")
                ], className="forecast-temp")
            ], className="forecast-row")
        )

    return rows


def _prepare_df(stored_data):
    df = pd.DataFrame(stored_data)
    df["DateTimeUTC"] = pd.to_datetime(df["DateTimeUTC"], errors="coerce")
    df["DataValue"] = pd.to_numeric(df["DataValue"], errors="coerce")
    df = df.dropna(subset=["DateTimeUTC", "DataValue"]).reset_index(drop=True)
    return df


def register_callbacks(app):
    @app.callback(
        Output("full-data-store", "data"),
        Input("url", "pathname"),
        State("full-data-store", "data"),
        prevent_initial_call=False
    )
    def load_data_once(pathname, stored_data):
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

        df = _prepare_df(stored_data)
        total_rows = len(df)

        if total_rows == 0:
            return 1

        if current_index is None or current_index < 1:
            current_index = 1

        if current_index < total_rows:
            return current_index + 1

        return 1

    @app.callback(
        Output("live-graph", "figure"),
        Input("current-index", "data"),
        State("full-data-store", "data")
    )
    def update_graph(current_index, stored_data):
        if not stored_data:
            return build_figure(pd.DataFrame(columns=["DateTimeUTC", "DataValue"]))

        df = _prepare_df(stored_data)

        if df.empty:
            return build_figure(pd.DataFrame(columns=["DateTimeUTC", "DataValue"]))

        if current_index is None or current_index < 1:
            current_index = 1

        current_index = min(current_index, len(df))
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
        df["DateTimeUTC"] = pd.to_datetime(df["DateTimeUTC"], errors="coerce")
        df["DataValue"] = pd.to_numeric(df["DataValue"], errors="coerce")
        df = df.dropna(subset=["DateTimeUTC", "DataValue"]).reset_index(drop=True)
    
        if df.empty:
            return "--", "No valid data", "--", "--"
    
        if current_index is None or current_index < 1:
            current_index = 1
    
        current_index = min(current_index, len(df))
    
        current_row = df.iloc[current_index - 1]
        current_value = current_row["DataValue"]
        current_time = current_row["DateTimeUTC"]
    
        if current_value >= THRESHOLD:
            status = "Above"
            sub = "Crop is in harvest zone"
        elif current_value >= THRESHOLD - 0.03:
            status = "Near"
            sub = "Approaching harvest threshold"
        else:
            status = "Below"
            sub = "Below harvest threshold"
    
        return (
            f"{current_value:.6f}",
            sub,
            status,
            current_time.strftime("%Y-%m-%d %H:%M:%S")
        )

    @app.callback(
        Output("forecast-table", "children"),
        Input("forecast-interval", "n_intervals")
    )
    def update_forecast(n):
        return random_forecast_rows()