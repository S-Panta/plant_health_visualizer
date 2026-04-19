# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 16:37:10 2026

@author: A02483178

figure.py
This file is only for building the Plotly figure. Separating chart creation 
like this makes the callback file much smaller and easier to read.
"""

import pandas as pd
import plotly.graph_objs as go

THRESHOLD = 0.85

CUT_DATES = [
    "2025-10-01 01:00:00",
    "2025-10-02 15:00:00"
]

def build_figure(visible_df):
    fig = go.Figure()

    if visible_df.empty:
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#041b11",
            plot_bgcolor="#072915",
            font=dict(color="#F3FFF7"),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[
                dict(
                    text="Waiting for data...",
                    x=0.5,
                    y=0.5,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=20, color="#9BC3A9")
                )
            ]
        )
        return fig

    fig.add_trace(go.Scatter(
        x=visible_df["DateTimeUTC"],
        y=visible_df["DataValue"],
        mode="lines",
        name="NDVI",
        line=dict(color="#1EE66E", width=3),
        fill="tozeroy",
        fillcolor="rgba(30, 230, 110, 0.16)",
        hovertemplate="<b>%{x}</b><br>NDVI: %{y:.3f}<extra></extra>"
    ))

    fig.add_hline(
        y=THRESHOLD,
        line_dash="dash",
        line_color="#D8B11E",
        line_width=2,
        annotation_text=f"Harvest threshold ({THRESHOLD:.2f})",
        annotation_position="bottom right",
        annotation_font_color="#E6C54A"
    )

    cut_dates = pd.to_datetime(CUT_DATES)

    for i, cut_date in enumerate(cut_dates, start=1):
        if cut_date <= visible_df["DateTimeUTC"].max():
            fig.add_vline(
                x=cut_date,
                line_dash="dot",
                line_color="#FF6B6B",
                line_width=1.5
            )

            nearest_idx = (visible_df["DateTimeUTC"] - cut_date).abs().idxmin()
            nearest_row = visible_df.loc[nearest_idx]

            fig.add_trace(go.Scatter(
                x=[nearest_row["DateTimeUTC"]],
                y=[nearest_row["DataValue"]],
                mode="markers",
                name="Cut events" if i == 1 else None,
                marker=dict(
                    color="#FF6B6B",
                    size=12,
                    symbol="triangle-down",
                    line=dict(color="white", width=1)
                ),
                showlegend=(i == 1),
                hovertemplate=f"<b>Cut #{i}</b><br>%{{x}}<br>NDVI: %{{y:.3f}}<extra></extra>"
            ))

            fig.add_annotation(
                x=cut_date,
                y=1.0,
                text=f"Cut #{i}",
                showarrow=False,
                yanchor="bottom",
                font=dict(color="#FF7A7A", size=12)
            )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#041b11",
        plot_bgcolor="#072915",
        font=dict(color="#F3FFF7"),
        margin=dict(l=60, r=40, t=30, b=40),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)"
        ),
        xaxis=dict(
            title="Date",
            gridcolor="rgba(255,255,255,0.08)",
            showline=True,
            linecolor="rgba(255,255,255,0.25)",
            rangeslider=dict(
                visible=True,
                bgcolor="#0A2A18",
                bordercolor="#1C5C39",
                borderwidth=1
            ),
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title="NDVI (0-1)",
            range=[0, 1.05],
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=False,
            tickfont=dict(size=12)
        )
    )

    return fig