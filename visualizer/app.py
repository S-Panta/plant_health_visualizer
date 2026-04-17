# Use data from sqlite database

"""
app.py
This file only creates the app, loads the layout, registers callbacks, 
and runs the server. That pattern helps avoid circular imports, which is 
one of the main reasons Dash python package apps are split into different files.
"""


# DB_PATH = r"C:\Users\A02483178\OneDrive - USU\Documents\GitHub\plant_health_visualizer\ndvi.sqlite"
# TABLE_NAME = "datavalues"

# import sqlite3
# import pandas as pd
# from dash import Dash, dcc, html, Input, Output, State
# import plotly.graph_objs as go

# DB_PATH = r"C:\Users\A02483178\OneDrive - USU\Documents\GitHub\plant_health_visualizer\ndvi.sqlite"
# TABLE_NAME = "datavalues"

# def fetch_data():
#     conn = sqlite3.connect(DB_PATH)
#     query = f"""
#         SELECT DateTimeUTC, DataValue
#         FROM {TABLE_NAME}
#         WHERE DataValue IS NOT NULL
#           AND DataValue != -9999
#         ORDER BY DateTimeUTC
#     """
#     df = pd.read_sql(query, conn)
#     conn.close()
#     df["DateTimeUTC"] = pd.to_datetime(df["DateTimeUTC"])
#     return df

# app = Dash(__name__)

# app.layout = html.Div([
#     html.H3("NDVI Live Dashboard", style={"color": "white"}),
    
#     dcc.Store(id="full-data-store"),
#     dcc.Store(id="current-index", data=1),

#     dcc.Graph(id="live-graph", animate=False),

#     dcc.Interval(
#         id="interval",
#         interval=1000,   # 1 second
#         n_intervals=0
#     )
# ], style={
#     "backgroundColor": "#031b0b",
#     "padding": "20px"
# })

# @app.callback(
#     Output("full-data-store", "data"),
#     Input("interval", "n_intervals"),
#     State("full-data-store", "data"),
#     prevent_initial_call=False
# )
# def load_data_once(n, stored_data):
#     if stored_data is None:
#         df = fetch_data()
#         return df.to_dict("records")
#     return stored_data

# @app.callback(
#     Output("current-index", "data"),
#     Input("interval", "n_intervals"),
#     State("current-index", "data"),
#     State("full-data-store", "data")
# )
# def advance_index(n, current_index, stored_data):
#     if not stored_data:
#         return 1

#     total_rows = len(stored_data)

#     if current_index < total_rows:
#         return current_index + 1

#     return total_rows

# @app.callback(
#     Output("live-graph", "figure"),
#     Input("current-index", "data"),
#     State("full-data-store", "data")
# )
# def update_graph(current_index, stored_data):
#     if not stored_data:
#         return go.Figure()

#     df = pd.DataFrame(stored_data)
#     df["DateTimeUTC"] = pd.to_datetime(df["DateTimeUTC"])

#     visible_df = df.iloc[:current_index]

#     fig = go.Figure()

#     fig.add_trace(go.Scatter(
#         x=visible_df["DateTimeUTC"],
#         y=visible_df["DataValue"],
#         mode="lines",
#         name="NDVI",
#         line=dict(color="#19e36a", width=3),
#         fill="tozeroy",
#         fillcolor="rgba(25, 227, 106, 0.12)"
#     ))

#     fig.add_hline(
#         y=0.72,
#         line_dash="dash",
#         line_color="#d8b11e",
#         annotation_text="Harvest threshold (0.72)",
#         annotation_position="bottom right"
#     )

#     fig.update_layout(
#         template="plotly_dark",
#         paper_bgcolor="#031b0b",
#         plot_bgcolor="#062a12",
#         font=dict(color="white"),
#         xaxis_title="Date",
#         yaxis_title="NDVI (0-1)",
#         yaxis=dict(range=[0, 1.05], gridcolor="rgba(255,255,255,0.08)"),
#         xaxis=dict(
#             gridcolor="rgba(255,255,255,0.08)",
#             rangeslider=dict(visible=True)
#         ),
#         margin=dict(l=40, r=40, t=40, b=40),
#         showlegend=True
#     )

#     return fig

# if __name__ == "__main__":
#     app.run(debug=True)


from dash import Dash
from layout import create_layout
from callbacks import register_callbacks

app = Dash(__name__)
app.title = "Alfalfa Live Dashboard"

app.layout = create_layout()
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)