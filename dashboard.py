"""
STEP 3 — Streamlit Dashboard (Dark Purple Theme)
Reads analysis_results.json and displays an interactive dashboard.

Run: streamlit run step3_dashboard.py
"""

import json
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ── PAGE CONFIG ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Product Review Intelligence",
    page_icon="🦈",
    layout="wide"
)

# ── CUSTOM CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f0a1e; }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1a1035 0%, #2d1b69 100%);
        border: 1px solid #4c1d95;
        border-radius: 12px;
        padding: 16px 20px;
    }
    [data-testid="metric-container"] label {
        color: #c4b5fd !important;
        font-size: 13px !important;
        font-weight: 500;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #f3f0ff !important;
        font-size: 28px !important;
        font-weight: 700;
    }
    [data-testid="stMetricDelta"] { color: #a78bfa !important; }

    /* Section headers */
    h2, h3 { color: #e2d9f3 !important; }

    /* Divider */
    hr { border-color: #2d1b69 !important; }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid #2d1b69 !important;
        border-radius: 8px;
    }

    /* Info boxes (AI summaries) */
    .stAlert {
        background: linear-gradient(135deg, #1a1035 0%, #1e1245 100%) !important;
        border: 1px solid #4c1d95 !important;
        border-radius: 8px !important;
        color: #c4b5fd !important;
    }

    /* Slider */
    [data-testid="stSlider"] { color: #a855f7; }

    /* Caption */
    .stCaption { color: #7c6fa0 !important; }

    /* Feature request bars */
    .feat-bar-bg {
        background: #1a1035;
        border-radius: 4px;
        height: 8px;
        margin-bottom: 10px;
    }
    .feat-bar-fill {
        background: linear-gradient(90deg, #7c3aed, #a855f7);
        height: 8px;
        border-radius: 4px;
    }
    .feat-label {
        color: #c4b5fd;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 3px;
    }
</style>
""", unsafe_allow_html=True)

# ── PLOTLY THEME ──────────────────────────────────────────────────────
PLOT_BG    = "#0f0a1e"
PAPER_BG   = "#0f0a1e"
GRID_COLOR = "#2d1b69"
TEXT_COLOR = "#c4b5fd"

def base_layout():
    return dict(
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(color=TEXT_COLOR, size=12),
        xaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickcolor=TEXT_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickcolor=TEXT_COLOR),
        margin=dict(l=0, r=0, t=10, b=0),
        height=320,
    )

# ── LOAD DATA ─────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    with open("analysis_results.json") as f:
        analysis = json.load(f)
    reviews  = pd.read_csv("reviews.csv")
    products = pd.read_csv("products.csv")
    return analysis, reviews, products

try:
    analysis, reviews_df, products_df = load_data()
except FileNotFoundError:
    st.error("Run generate_data.py and analyze.py first.")
    st.stop()

# ── HEADER ────────────────────────────────────────────────────────────
st.title("🦈 Product Review Intelligence")
st.caption("Powered by Claude AI · Product Reviews")
st.divider()

# ── KPI ROW ───────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
sentiment = analysis["avg_sentiment"]
sentiment_label = "Positive 😊" if sentiment > 0.2 else ("Neutral 😐" if sentiment > -0.2 else "Negative 😟")

col1.metric("Reviews Analyzed",  f"{analysis['total_reviews_analyzed']:,}")
col2.metric("Avg Star Rating",    f"{analysis['avg_rating']} / 5.0")
col3.metric("Overall Sentiment",  sentiment_label, f"{sentiment:+.2f}")
col4.metric("Products Covered",   f"{reviews_df['asin'].nunique():,}")

st.divider()

# ── ROW 1: Complaints + Praises ───────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Top Customer Complaints")
    complaints = pd.DataFrame(analysis["top_complaints"], columns=["Issue", "Count"])
    complaints["Issue"] = complaints["Issue"].str.title()
    fig = px.bar(complaints, x="Count", y="Issue", orientation="h",
                 color="Count", color_continuous_scale=["#4c1d95", "#dc2626"])
    fig.update_layout(**base_layout())
    fig.update_traces(hovertemplate="%{y}: %{x} mentions")
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("🟢 Top Customer Praises")
    praises = pd.DataFrame(analysis["top_praises"], columns=["Aspect", "Count"])
    praises["Aspect"] = praises["Aspect"].str.title()
    fig2 = px.bar(praises, x="Count", y="Aspect", orientation="h",
                  color="Count", color_continuous_scale=["#1e3a5f", "#059669"])
    fig2.update_layout(**base_layout())
    fig2.update_traces(hovertemplate="%{y}: %{x} mentions")
    fig2.update_coloraxes(showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

# ── ROW 2: Sentiment trend + Feature requests ─────────────────────────
col_a, col_b = st.columns([2, 1])

with col_a:
    st.subheader("📈 Sentiment Trend by Batch")
    batch_results = [r for r in analysis["batch_results"] if "error" not in r]
    if batch_results:
        trend_df = pd.DataFrame([{
            "Batch"    : r["batch_index"] + 1,
            "Sentiment": r["overall_sentiment"],
        } for r in batch_results])
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=trend_df["Batch"], y=trend_df["Sentiment"],
            mode="lines+markers", name="Sentiment",
            line=dict(color="#a855f7", width=2),
            marker=dict(color="#c084fc", size=6),
            fill="tozeroy", fillcolor="rgba(168,85,247,0.1)"
        ))
        fig3.add_hline(y=0, line_dash="dash", line_color="#4c1d95", opacity=0.7)
        layout = base_layout()
        layout.update(dict(
            yaxis=dict(range=[-1,1], title="Sentiment Score",
                       gridcolor=GRID_COLOR, linecolor=GRID_COLOR),
            xaxis=dict(title="Review Batch",
                       gridcolor=GRID_COLOR, linecolor=GRID_COLOR),
            height=280
        ))
        fig3.update_layout(**layout)
        st.plotly_chart(fig3, use_container_width=True)

with col_b:
    st.subheader("💡 Feature Requests")
    requests = pd.DataFrame(analysis["feature_requests"], columns=["Feature", "Mentions"])
    requests["Feature"] = requests["Feature"].str.title()
    max_val = requests["Mentions"].max()
    for _, row in requests.iterrows():
        pct = int((row["Mentions"] / max_val) * 100)
        st.markdown(f"""
        <div class="feat-label">{row['Feature']}</div>
        <div class="feat-bar-bg">
          <div class="feat-bar-fill" style="width:{pct}%"></div>
        </div>
        """, unsafe_allow_html=True)

# ── ROW 3: Rating distribution + AI summaries ────────────────────────
st.divider()
col_p, col_q = st.columns([1, 2])

with col_p:
    st.subheader("⭐ Rating Distribution")
    if "rating" in reviews_df.columns:
        rating_counts = reviews_df["rating"].value_counts().sort_index()
        colors = ["#dc2626", "#ea580c", "#ca8a04", "#65a30d", "#7c3aed"]
        fig4 = go.Figure(go.Bar(
            x=rating_counts.index,
            y=rating_counts.values,
            marker_color=colors,
            hovertemplate="⭐ %{x}: %{y} reviews"
        ))
        layout4 = base_layout()
        layout4.update(dict(
            xaxis=dict(title="Stars", gridcolor=GRID_COLOR, linecolor=GRID_COLOR),
            yaxis=dict(title="Reviews", gridcolor=GRID_COLOR, linecolor=GRID_COLOR),
            height=260, showlegend=False
        ))
        fig4.update_layout(**layout4)
        st.plotly_chart(fig4, use_container_width=True)

with col_q:
    st.subheader("🤖 AI Executive Summary")
    summaries = [r.get("summary","") for r in batch_results if r.get("summary")]
    if summaries:
        for i, s in enumerate(summaries[:3], 1):
            st.info(f"**Batch {i}:** {s}")

# ── ROW 4: Raw reviews ────────────────────────────────────────────────
st.divider()
st.subheader("🔍 Explore Raw Reviews")
rating_filter = st.slider("Filter by minimum rating", 1, 5, 1)
filtered = reviews_df[reviews_df["rating"] >= rating_filter].head(50)
if not filtered.empty:
    show_df = filtered[["rating","title","text"]].copy()
    show_df.columns = ["Stars","Review Title","Review Text"]
    show_df["Review Text"] = show_df["Review Text"].str[:200] + "..."
    st.dataframe(show_df, use_container_width=True, height=300)

st.caption("Built with Python · Claude API · Streamlit · Product Reviews")