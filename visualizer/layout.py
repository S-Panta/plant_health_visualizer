# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 16:34:52 2026

@author: A02483178

layout.py
This file holds the dashboard UI only. Keeping layout separate from callback 
logic is a common Dash organization pattern and makes the screen structure 
much easier to edit later.
"""

from dash import dcc, html

THRESHOLD = 0.85

def create_layout():
    return html.Div([
        dcc.Store(id="full-data-store"),
        dcc.Store(id="current-index", data=1),

        dcc.Interval(
            id="interval",
            interval=1000,
            n_intervals=0
        ),
        
        dcc.Interval(
            id="forecast-interval",
            interval=30000,
            n_intervals=0
        ),

        html.Div([
            html.Div([
                html.Div([
                    html.H1("Alfalfa  Field Live Dashboard"),
                    html.P("Smart NDVI Monitoring • SQLite Feed • Mimic Real-Time Sensor")
                ], className="title-wrap"),
                html.Div("Live data stream simulation", className="status-pill")
            ], className="top-header"),

            html.Div([
                html.Div([
                    html.Div("Current NDVI", className="kpi-label"),
                    html.Div(id="current-ndvi", className="kpi-value"),
                    html.Div(id="current-ndvi-sub", className="kpi-sub")
                ], className="kpi-card"),

                html.Div([
                    html.Div("Harvest Status", className="kpi-label"),
                    html.Div(id="harvest-status", className="kpi-value"),
                    html.Div(f"Threshold = {THRESHOLD:.2f}", className="kpi-sub")
                ], className="kpi-card"),

                html.Div([
                    html.Div("Last Timestamp", className="kpi-label"),
                    html.Div(id="last-timestamp", className="kpi-value timestamp-value"),
                    html.Div("Latest visible record", className="kpi-sub")
                ], className="kpi-card"),
            ], className="kpi-row"),
            
            html.Div([
                html.Div("7-DAY FORECAST", className="forecast-title"),
                html.Div(id="forecast-table", className="forecast-table")
            ], className="forecast-panel"),

            html.Div([
                dcc.Graph(
                    id="live-graph",
                    className="dash-graph",
                    config={"displayModeBar": True, "scrollZoom": True},
                    style={"height": "68vh"}
                )
            ], className="chart-panel")
        ], className="app-shell")
    ])