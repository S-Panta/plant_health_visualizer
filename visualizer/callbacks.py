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


def register_callbacks(app):
    @app.callback(
        Output("full-data-store", "data"),
        Input("forecast-interval", "n_intervals"),
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
            print("advance_index: no stored data")
            return 1
    
        total_rows = len(stored_data)
        print("advance_index before:", current_index, "of", total_rows)
    
        if current_index < total_rows:
            next_index = current_index + 1
        else:
            next_index = 1   # loop for demo, use total_rows if you want it to stop
    
        print("advance_index after:", next_index)
        return next_index

    @app.callback(
        Output("live-graph", "figure"),
        Input("current-index", "data"),
        State("full-data-store", "data")
    )
    def update_graph(current_index, stored_data):
        if not stored_data:
            print("update_graph: no stored data")
            return build_figure(pd.DataFrame(columns=["DateTimeUTC", "DataValue"]))
    
        df = pd.DataFrame(stored_data)
        df["DateTimeUTC"] = pd.to_datetime(df["DateTimeUTC"], errors="coerce")
        df["DataValue"] = pd.to_numeric(df["DataValue"], errors="coerce")
    
        visible_df = df.iloc[:current_index].copy()
    
        print("update_graph current_index:", current_index)
        print("graph rows visible:", len(visible_df))
    
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

    @app.callback(
    Output("forecast-table", "children"),
    Input("forecast-interval", "n_intervals")
    )
    def update_forecast(n):
        return random_forecast_rows()