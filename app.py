import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import requests
import os

# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Credit Risk Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        font-size: 0.95rem;
        padding: 6px 0;
    }

    /* Main background */
    .main { background-color: #f8fafc; }

    /* KPI Cards */
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 20px 24px;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 8px;
    }
    .kpi-card.red { border-left-color: #ef4444; }
    .kpi-card.green { border-left-color: #10b981; }
    .kpi-card.amber { border-left-color: #f59e0b; }
    .kpi-card.purple { border-left-color: #8b5cf6; }

    .kpi-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: black;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.9rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1;
        font-family: 'JetBrains Mono', monospace;
    }
    .kpi-sub {
        font-size: 0.78rem;
        color: #94a3b8;
        margin-top: 4px;
    }

    /* Section headers */
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: white;
        margin: 24px 0 12px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #e2e8f0;
    }

    /* Insight cards */
    .insight-card {
        background: white;
        border-radius: 10px;
        padding: 16px 20px;
        margin: 8px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.07);
        border-left: 3px solid #3b82f6;
        font-size: 0.9rem;
        color: black;
        line-height: 1.5;
    }
    .insight-card.warning { border-left-color: #f59e0b; }
    .insight-card.danger  { border-left-color: #ef4444; }
    .insight-card.success { border-left-color: #10b981; }

    /* Chat messages */
    .chat-user {
        background: #3b82f6;
        color: white;
        padding: 12px 16px;
        border-radius: 16px 16px 4px 16px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 0.9rem;
    }
    .chat-assistant {
        background: white;
        color: #1e293b;
        padding: 14px 18px;
        border-radius: 16px 16px 16px 4px;
        margin: 8px 0;
        max-width: 85%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.6;
        border: 1px solid #e2e8f0;
    }
    .chat-label {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94a3b8;
        margin-bottom: 4px;
    }

    /* Page title */
    .page-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e40af 100%);
        color: white;
        padding: 28px 32px;
        border-radius: 14px;
        margin-bottom: 24px;
    }
    .page-header h1 {
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0 0 4px 0;
        color: white;
    }
    .page-header p {
        font-size: 0.88rem;
        color: #93c5fd;
        margin: 0;
    }

    /* Hide streamlit defaults */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# def apply_chart_theme(fig):
#     fig.update_layout(
#         font=dict(color="black"),
#         xaxis=dict(
#             tickfont=dict(color="black"),
#             title_font=dict(color="black")
#         ),
#         yaxis=dict(
#             tickfont=dict(color="black"),
#             title_font=dict(color="black")
#         ),
#         legend=dict(font=dict(color="black"))
#     )

#     fig.update_traces(
#         textfont=dict(color="black")
#     )

#     return fig
def apply_chart_theme(fig):
    fig.update_layout(
        font=dict(color="black"),

        xaxis=dict(
            tickfont=dict(color="black"),
            title_font=dict(color="black")
        ),

        yaxis=dict(
            tickfont=dict(color="black"),
            title_font=dict(color="black")
        ),

        legend=dict(
            font=dict(color="black")
        )
    )

    return fig

# ── Data Loading ──────────────────────────────────────────────
# @st.cache_data
# def load_data():
#     # Try local path first, then Google Drive path
#     paths = [
#         "app_final.csv",
#         os.path.expanduser("~/Desktop/financial_assistant/app_final.csv"),
#     ]
#     for path in paths:
#         if os.path.exists(path):
#             df = pd.read_csv(path)
#             return df
#     st.error("❌ Could not find app_final.csv. Please place it in the same folder as app.py")
#     st.stop()


@st.cache_data
def load_data():
    return pd.read_csv("app_final.csv")

@st.cache_data
def load_summary():
    paths = [
        "summary_stats.json",
        os.path.expanduser("~/Desktop/financial_assistant/summary_stats.json"),
    ]
    for path in paths:
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
    return {}

df = load_data()
summary = load_summary()
if 'AGE_GROUP' not in df.columns and 'AGE_YEARS' in df.columns:
    df['AGE_GROUP'] = pd.cut(
        df['AGE_YEARS'],
        bins=[20, 30, 40, 50, 60, 70],
        labels=['20-30', '30-40', '40-50', '50-60', '60-70']
    )

# Ensure derived columns exist
# if 'AGE_GROUP' not in df.columns:
#     df['AGE_YEARS'] = (df['DAYS_BIRTH'] / 365).round(1)
#     df['AGE_GROUP'] = pd.cut(df['AGE_YEARS'],
#                               bins=[20, 30, 40, 50, 60, 70],
#                               labels=['20-30', '30-40', '40-50', '50-60', '60-70'])
if 'CREDIT_INCOME_RATIO' not in df.columns:
    df['CREDIT_INCOME_RATIO'] = df['AMT_CREDIT'] / df['AMT_INCOME_TOTAL']
if 'ANNUITY_INCOME_RATIO' not in df.columns:
    df['ANNUITY_INCOME_RATIO'] = df['AMT_ANNUITY'] / df['AMT_INCOME_TOTAL']

# ── Sidebar Navigation ────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏦 Credit Risk Intelligence")
    st.markdown("*Home Credit Default Analysis*")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["📊 Executive Overview", "🔍 Risk Segmentation", "📈 Credit Behavior", "🤖 AI Assistant"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("**Dataset**")
    st.markdown(f"- {df.shape[0]:,} applicants")
    st.markdown(f"- {df.shape[1]} features")
    st.markdown(f"- 5 source tables merged")
    st.markdown("---")
    st.markdown("**Global Filters**")
    gender_filter = st.multiselect(
        "Gender", options=df['CODE_GENDER'].unique().tolist(),
        default=df['CODE_GENDER'].unique().tolist()
    )
    loan_type_filter = st.multiselect(
        "Loan Type", options=df['NAME_CONTRACT_TYPE'].unique().tolist(),
        default=df['NAME_CONTRACT_TYPE'].unique().tolist()
    )
    age_range = st.slider("Age Range", 20, 70, (20, 70))

# ── Apply Filters ─────────────────────────────────────────────
filtered = df[
    df['CODE_GENDER'].isin(gender_filter) &
    df['NAME_CONTRACT_TYPE'].isin(loan_type_filter) &
    df['AGE_YEARS'].between(age_range[0], age_range[1])
].copy()

total = len(filtered)
defaults = filtered['TARGET'].sum()
default_rate = defaults / total * 100 if total > 0 else 0

# ════════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE OVERVIEW
# ════════════════════════════════════════════════════════════════
if page == "📊 Executive Overview":
    st.markdown("""
    <div class="page-header">
        <h1>📊 Executive Overview</h1>
        <p>Portfolio-level credit risk summary · Home Credit Default Dataset · 307,511 applicants</p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""<div class="kpi-card blue">
            <div class="kpi-label">Total Applicants</div>
            <div class="kpi-value">{total:,}</div>
            <div class="kpi-sub">filtered selection</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card red">
            <div class="kpi-label">Default Rate</div>
            <div class="kpi-value">{default_rate:.1f}%</div>
            <div class="kpi-sub">{int(defaults):,} defaults</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        avg_credit = filtered['AMT_CREDIT'].mean()
        st.markdown(f"""<div class="kpi-card green">
            <div class="kpi-label">Avg Loan Amount</div>
            <div class="kpi-value">${avg_credit:,.0f}</div>
            <div class="kpi-sub">per applicant</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        avg_income = filtered['AMT_INCOME_TOTAL'].mean()
        st.markdown(f"""<div class="kpi-card amber">
            <div class="kpi-label">Avg Annual Income</div>
            <div class="kpi-value">${avg_income:,.0f}</div>
            <div class="kpi-sub">per applicant</div>
        </div>""", unsafe_allow_html=True)
    with c5:
        avg_age = filtered['AGE_YEARS'].mean()
        st.markdown(f"""<div class="kpi-card purple">
            <div class="kpi-label">Avg Applicant Age</div>
            <div class="kpi-value">{avg_age:.1f}</div>
            <div class="kpi-sub">years old</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="section-title">Loan Default Distribution</div>', unsafe_allow_html=True)
        fig = go.Figure(go.Pie(
            labels=['Repaid', 'Defaulted'],
            values=[total - defaults, defaults],
            hole=0.6,
            marker_colors=['#10b981', '#ef4444'],
            textinfo='label+percent',
            textfont_size=13,
        ))
        fig.update_layout(
            showlegend=False, height=300,
            margin=dict(t=10, b=10, l=10, r=10),
            annotations=[dict(text=f'{default_rate:.1f}%<br>Default', x=0.5, y=0.5,
                            font_size=16, showarrow=False, font_color='#0f172a')]
        )
        # st.plotly_chart(fig, use_container_width=True)
        apply_chart_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Loan Amount Distribution</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Histogram(
            x=filtered[filtered['TARGET']==0]['AMT_CREDIT'].clip(0, 1500000),
            name='Repaid', marker_color='#10b981', opacity=0.7, nbinsx=50
        ))
        fig2.add_trace(go.Histogram(
            x=filtered[filtered['TARGET']==1]['AMT_CREDIT'].clip(0, 1500000),
            name='Defaulted', marker_color='#ef4444', opacity=0.7, nbinsx=50
        ))
        fig2.update_layout(
            barmode='overlay', height=300,
            margin=dict(t=10, b=40, l=40, r=10),
            xaxis_title='Loan Amount ($)',
            yaxis_title='Count',
            legend=dict(orientation='h', y=1.1),
            plot_bgcolor='white', paper_bgcolor='white'
        )
        # st.plotly_chart(fig2, use_container_width=True)
        apply_chart_theme(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Key Insights
    st.markdown('<div class="section-title">🔑 Key Findings</div>', unsafe_allow_html=True)
    i1, i2, i3 = st.columns(3)
    with i1:
        st.markdown("""<div class="insight-card danger">
            <strong>🔴 Extreme Risk Segment</strong><br>
            Applicants on maternity leave default at <strong>40%</strong> — nearly 5× the portfolio average.
            Unemployed applicants follow at <strong>36.4%</strong>.
        </div>""", unsafe_allow_html=True)
    with i2:
        st.markdown("""<div class="insight-card warning">
            <strong>🟡 Age-Driven Risk</strong><br>
            Borrowers aged <strong>20–30</strong> show an 11.4% default rate — the highest of any age group.
            Risk declines steadily with age.
        </div>""", unsafe_allow_html=True)
    with i3:
        st.markdown("""<div class="insight-card success">
            <strong>🟢 Best Predictor</strong><br>
            <strong>EXT_SOURCE_2 & EXT_SOURCE_3</strong> (external credit scores) are the strongest
            predictors — higher scores consistently mean lower default risk.
        </div>""", unsafe_allow_html=True)

    # ── Default by Income Type
    st.markdown('<div class="section-title">Default Rate by Income Type</div>', unsafe_allow_html=True)
    income_def = filtered.groupby('NAME_INCOME_TYPE')['TARGET'].mean().reset_index()
    income_def.columns = ['Income Type', 'Default Rate']
    income_def['Default Rate'] = (income_def['Default Rate'] * 100).round(2)
    income_def = income_def.sort_values('Default Rate', ascending=True)
    income_def['Color'] = income_def['Default Rate'].apply(
        lambda x: '#ef4444' if x > 20 else '#f59e0b' if x > 8 else '#10b981'
    )
    # fig3 = go.Figure(go.Bar(
    #     x=income_def['Default Rate'], y=income_def['Income Type'],
    #     orientation='h', marker_color=income_def['Color'],
    #     text=income_def['Default Rate'].apply(lambda x: f'{x:.1f}%'),
    #     textposition='outside'
    fig3 = go.Figure(go.Bar(
    x=income_def['Default Rate'],
    y=income_def['Income Type'],
    orientation='h',
    marker_color=income_def['Color'],
    text=income_def['Default Rate'].apply(lambda x: f'{x:.1f}%'),
    textposition='outside',
    textfont=dict(color='black')
    ))
    fig3.update_layout(
        height=320, margin=dict(t=10, b=10, l=10, r=60),
        xaxis_title='Default Rate (%)', plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(gridcolor='#f1f5f9')
    )
    apply_chart_theme(fig3)
    st.plotly_chart(fig3, use_container_width=True)
    # st.plotly_chart(fig3, use_container_width=True)


# ════════════════════════════════════════════════════════════════
# PAGE 2 — RISK SEGMENTATION
# ════════════════════════════════════════════════════════════════
elif page == "🔍 Risk Segmentation":
    st.markdown("""
    <div class="page-header">
        <h1>🔍 Risk Segmentation</h1>
        <p>Deep-dive into how demographics, education, and family status drive default risk</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Education
        st.markdown('<div class="section-title">Default Rate by Education</div>', unsafe_allow_html=True)
        edu = filtered.groupby('NAME_EDUCATION_TYPE')['TARGET'].mean().reset_index()
        edu.columns = ['Education', 'Default Rate']
        edu['Default Rate'] = (edu['Default Rate'] * 100).round(2)
        edu = edu.sort_values('Default Rate', ascending=True)
        fig = px.bar(edu, x='Default Rate', y='Education', orientation='h',
                     color='Default Rate', color_continuous_scale=['#10b981', '#f59e0b', '#ef4444'],
                     text=edu['Default Rate'].apply(lambda x: f'{x:.1f}%'))
        fig.update_traces(textposition='outside')
        fig.update_layout(height=280, margin=dict(t=10, b=10, l=10, r=60),
                         coloraxis_showscale=False, plot_bgcolor='white', paper_bgcolor='white')
        # st.plotly_chart(fig, use_container_width=True)
        apply_chart_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Family Status
        st.markdown('<div class="section-title">Default Rate by Family Status</div>', unsafe_allow_html=True)
        fam = filtered.groupby('NAME_FAMILY_STATUS')['TARGET'].mean().reset_index()
        fam.columns = ['Family Status', 'Default Rate']
        fam['Default Rate'] = (fam['Default Rate'] * 100).round(2)
        fam = fam.sort_values('Default Rate', ascending=True)
        fig2 = px.bar(fam, x='Default Rate', y='Family Status', orientation='h',
                      color='Default Rate', color_continuous_scale=['#10b981', '#f59e0b', '#ef4444'],
                      text=fam['Default Rate'].apply(lambda x: f'{x:.1f}%'))
        fig2.update_traces(textposition='outside')
        fig2.update_layout(height=280, margin=dict(t=10, b=10, l=10, r=60),
                          coloraxis_showscale=False, plot_bgcolor='white', paper_bgcolor='white')
        apply_chart_theme(fig2)
        st.plotly_chart(fig2, use_container_width=True)
        # st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        # Age Group
        st.markdown('<div class="section-title">Default Rate by Age Group</div>', unsafe_allow_html=True)
        age_def = filtered.groupby('AGE_GROUP', observed=True)['TARGET'].mean().reset_index()
        age_def.columns = ['Age Group', 'Default Rate']
        age_def['Default Rate'] = (age_def['Default Rate'] * 100).round(2)
        colors_age = ['#ef4444', '#f59e0b', '#10b981', '#10b981', '#10b981']
        fig3 = go.Figure(go.Bar(
            x=age_def['Age Group'].astype(str), y=age_def['Default Rate'],
            marker_color=colors_age,
            text=age_def['Default Rate'].apply(lambda x: f'{x:.1f}%'),
            textposition='outside'
        ))
        fig3.update_layout(height=280, margin=dict(t=30, b=10, l=10, r=10),
                          yaxis_title='Default Rate (%)', plot_bgcolor='white',
                          paper_bgcolor='white', yaxis=dict(gridcolor='#f1f5f9'))
        apply_chart_theme(fig3)
        st.plotly_chart(fig3, use_container_width=True)
        # st.plotly_chart(fig3, use_container_width=True)

    with col4:
        # Housing Type
        st.markdown('<div class="section-title">Default Rate by Housing Type</div>', unsafe_allow_html=True)
        hous = filtered.groupby('NAME_HOUSING_TYPE')['TARGET'].mean().reset_index()
        hous.columns = ['Housing Type', 'Default Rate']
        hous['Default Rate'] = (hous['Default Rate'] * 100).round(2)
        hous = hous.sort_values('Default Rate', ascending=True)
        fig4 = px.bar(hous, x='Default Rate', y='Housing Type', orientation='h',
                      color='Default Rate', color_continuous_scale=['#10b981', '#f59e0b', '#ef4444'],
                      text=hous['Default Rate'].apply(lambda x: f'{x:.1f}%'))
        fig4.update_traces(textposition='outside')
        fig4.update_layout(height=280, margin=dict(t=10, b=10, l=10, r=60),
                          coloraxis_showscale=False, plot_bgcolor='white', paper_bgcolor='white')
        apply_chart_theme(fig4)
        st.plotly_chart(fig4, use_container_width=True)
        # st.plotly_chart(fig4, use_container_width=True)

    # Risk Matrix
    st.markdown('<div class="section-title">📊 Risk Heatmap — Education × Family Status</div>',
                unsafe_allow_html=True)
    pivot = filtered.pivot_table(values='TARGET', index='NAME_EDUCATION_TYPE',
                                  columns='NAME_FAMILY_STATUS', aggfunc='mean') * 100
    fig5 = px.imshow(pivot.round(1), color_continuous_scale='RdYlGn_r',
                     text_auto=True, aspect='auto')
    fig5.update_layout(height=320, margin=dict(t=10, b=10, l=10, r=10),
                       coloraxis_colorbar=dict(title='Default %'))
    apply_chart_theme(fig5)
    st.plotly_chart(fig5, use_container_width=True)
    # st.plotly_chart(fig5, use_container_width=True)
    st.caption("💡 Darker red = higher default risk. Use this to identify compounding risk factors.")


# ════════════════════════════════════════════════════════════════
# PAGE 3 — CREDIT BEHAVIOR
# ════════════════════════════════════════════════════════════════
elif page == "📈 Credit Behavior":
    st.markdown("""
    <div class="page-header">
        <h1>📈 Credit Behavior Analysis</h1>
        <p>How income, loan amounts, repayment history, and bureau data reveal default patterns</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Income vs Loan Amount</div>', unsafe_allow_html=True)
        sample = filtered.sample(min(5000, len(filtered)), random_state=42)
        fig = px.scatter(
            sample, x='AMT_INCOME_TOTAL', y='AMT_CREDIT',
            color=sample['TARGET'].map({0: 'Repaid', 1: 'Defaulted'}),
            color_discrete_map={'Repaid': '#10b981', 'Defaulted': '#ef4444'},
            opacity=0.4, size_max=4
        )
        fig.update_layout(height=320, margin=dict(t=10, b=40, l=40, r=10),
                         xaxis_range=[0, 1000000], yaxis_range=[0, 3000000],
                         plot_bgcolor='white', paper_bgcolor='white',
                         xaxis=dict(gridcolor='#f1f5f9'), yaxis=dict(gridcolor='#f1f5f9'),
                         legend=dict(orientation='h', y=1.08))
        # st.plotly_chart(fig, use_container_width=True)
        apply_chart_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Credit-to-Income Ratio by Default Status</div>',
                    unsafe_allow_html=True)
        fig2 = go.Figure()
        for target, name, color in [(0, 'Repaid', '#10b981'), (1, 'Defaulted', '#ef4444')]:
            fig2.add_trace(go.Violin(
                y=filtered[filtered['TARGET']==target]['CREDIT_INCOME_RATIO'].clip(0, 15),
                name=name, fillcolor=color, line_color=color, opacity=0.7, box_visible=True
            ))
        fig2.update_layout(height=320, margin=dict(t=10, b=10, l=10, r=10),
                          yaxis_title='Credit / Income Ratio',
                          plot_bgcolor='white', paper_bgcolor='white')
        # st.plotly_chart(fig2, use_container_width=True)
        apply_chart_theme(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-title">EXT_SOURCE Scores vs Default</div>',
                    unsafe_allow_html=True)
        fig3 = go.Figure()
        for source in ['EXT_SOURCE_2', 'EXT_SOURCE_3']:
            for target, name, color in [(0, 'Repaid', '#10b981'), (1, 'Defaulted', '#ef4444')]:
                sub = filtered[filtered['TARGET']==target][source].dropna()
                fig3.add_trace(go.Box(
                    y=sub, name=f'{source[-1]} – {name}',
                    marker_color=color, opacity=0.8,
                    boxmean=True
                ))
        fig3.update_layout(height=320, margin=dict(t=10, b=10, l=10, r=10),
                          yaxis_title='External Credit Score',
                          plot_bgcolor='white', paper_bgcolor='white',
                          showlegend=False)
        # st.plotly_chart(fig3, use_container_width=True)
        apply_chart_theme(fig3)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-title">Bureau Loan Count vs Default Rate</div>',
                    unsafe_allow_html=True)
        if 'BUREAU_LOAN_COUNT' in filtered.columns:
            filtered['BUREAU_LOAN_BUCKET'] = pd.cut(
                filtered['BUREAU_LOAN_COUNT'],
                bins=[-1, 0, 2, 5, 10, 100],
                labels=['0 loans', '1-2 loans', '3-5 loans', '6-10 loans', '10+ loans']
            )
            bureau_def = filtered.groupby('BUREAU_LOAN_BUCKET', observed=True)['TARGET'].mean().reset_index()
            bureau_def['Default Rate'] = (bureau_def['TARGET'] * 100).round(2)
            fig4 = go.Figure(go.Bar(
                x=bureau_def['BUREAU_LOAN_BUCKET'].astype(str),
                y=bureau_def['Default Rate'],
                marker_color='#8b5cf6',
                text=bureau_def['Default Rate'].apply(lambda x: f'{x:.1f}%'),
                textposition='outside'
                
            ))
            fig4.update_layout(height=320, margin=dict(t=30, b=10, l=10, r=10),
                              yaxis_title='Default Rate (%)',
                              plot_bgcolor='white', paper_bgcolor='white',
                              yaxis=dict(gridcolor='#f1f5f9'))
            # st.plotly_chart(fig4, use_container_width=True)
            apply_chart_theme(fig4)
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("Bureau data not available in filtered selection.")

    # Annuity burden
    st.markdown('<div class="section-title">Monthly Payment Burden (Annuity/Income) Distribution</div>',
                unsafe_allow_html=True)
    fig5 = go.Figure()
    for target, name, color in [(0, 'Repaid', '#10b981'), (1, 'Defaulted', '#ef4444')]:
        fig5.add_trace(go.Histogram(
            x=filtered[filtered['TARGET']==target]['ANNUITY_INCOME_RATIO'].clip(0, 0.5),
            name=name, marker_color=color, opacity=0.65,
            nbinsx=60, histnorm='percent'
        ))
    fig5.update_layout(
        barmode='overlay', height=280,
        margin=dict(t=10, b=40, l=40, r=10),
        xaxis_title='Monthly Payment / Annual Income',
        yaxis_title='% of Applicants',
        plot_bgcolor='white', paper_bgcolor='white',
        legend=dict(orientation='h', y=1.08),
        xaxis=dict(gridcolor='#f1f5f9'), yaxis=dict(gridcolor='#f1f5f9')
    )
    # st.plotly_chart(fig5, use_container_width=True)
    apply_chart_theme(fig5)
    st.plotly_chart(fig5, use_container_width=True)
    st.caption("💡 Defaulters tend to have a higher payment-to-income ratio, indicating financial overextension.")


# ════════════════════════════════════════════════════════════════
# PAGE 4 — AI ASSISTANT
# ════════════════════════════════════════════════════════════════
elif page == "🤖 AI Assistant":
    st.markdown("""
    <div class="page-header">
        <h1>🤖 AI Financial Data Assistant</h1>
        <p>Ask questions about the dataset in plain English · Powered by Grok AI</p>
    </div>
    """, unsafe_allow_html=True)

    # Example questions
    col_ex1, col_ex2, col_ex3 = st.columns(3)
    with col_ex1:
        st.markdown("""<div class="insight-card success">
            <strong>✅ Try asking:</strong><br>
            "What is the default rate for male vs female applicants?"<br><br>
            "Which income type has the highest default risk?"<br><br>
            "How many applicants have more than 5 bureau loans?"
        </div>""", unsafe_allow_html=True)
    with col_ex2:
        st.markdown("""<div class="insight-card warning">
            <strong>✅ Also works well:</strong><br>
            "What percentage of applicants are aged 20-30?"<br><br>
            "Compare cash loans vs revolving loans default rate"<br><br>
            "What is the average income of defaulted applicants?"
        </div>""", unsafe_allow_html=True)
    with col_ex3:
        st.markdown("""<div class="insight-card danger">
            <strong>⚠️ Known limitations:</strong><br>
            "Predict if this new customer will default" — needs ML model<br><br>
            "Show me trends over time" — dataset has no dates<br><br>
            "Why did customer X default?" — no individual-level causality
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Build dataset context for AI
    def build_context(df):
        default_rate = df['TARGET'].mean() * 100
        income_def = df.groupby('NAME_INCOME_TYPE')['TARGET'].mean() * 100
        edu_def = df.groupby('NAME_EDUCATION_TYPE')['TARGET'].mean() * 100
        gender_def = df.groupby('CODE_GENDER')['TARGET'].mean() * 100
        age_def = df.groupby('AGE_GROUP', observed=True)['TARGET'].mean() * 100
        loan_def = df.groupby('NAME_CONTRACT_TYPE')['TARGET'].mean() * 100
        housing_def = df.groupby('NAME_HOUSING_TYPE')['TARGET'].mean() * 100
        family_def = df.groupby('NAME_FAMILY_STATUS')['TARGET'].mean() * 100

        context = f"""
You are a financial data analyst assistant. You have access to the Home Credit Default Risk dataset.

DATASET SUMMARY:
- Total applicants: {len(df):,}
- Total defaults: {int(df['TARGET'].sum()):,}
- Overall default rate: {default_rate:.2f}%
- Average loan amount: ${df['AMT_CREDIT'].mean():,.0f}
- Average income: ${df['AMT_INCOME_TOTAL'].mean():,.0f}
- Average age: {df['AGE_YEARS'].mean():.1f} years

DEFAULT RATES BY SEGMENT:

By Income Type:
{income_def.round(2).to_string()}

By Education:
{edu_def.round(2).to_string()}

By Gender:
{gender_def.round(2).to_string()}

By Age Group:
{age_def.round(2).to_string()}

By Loan Type:
{loan_def.round(2).to_string()}

By Housing Type:
{housing_def.round(2).to_string()}

By Family Status:
{family_def.round(2).to_string()}

KEY STATISTICS:
- Highest risk income type: Maternity leave (40.0%)
- Lowest risk income type: Student (0.0%), Businessman (0.0%)
- Highest risk age group: 20-30 years (11.4%)
- Highest risk education: Lower secondary (10.9%)
- Strongest predictors: EXT_SOURCE_2 (corr -0.160), EXT_SOURCE_3 (corr -0.156), AGE_YEARS (corr -0.078)
- Rented apartment applicants default at 12.3% vs house owners at 7.8%

ADDITIONAL COUNTS:
- Male applicants: {(df['CODE_GENDER']=='M').sum():,} ({(df['CODE_GENDER']=='M').mean()*100:.1f}%)
- Female applicants: {(df['CODE_GENDER']=='F').sum():,} ({(df['CODE_GENDER']=='F').mean()*100:.1f}%)
- Cash loans: {(df['NAME_CONTRACT_TYPE']=='Cash loans').sum():,}
- Revolving loans: {(df['NAME_CONTRACT_TYPE']=='Revolving loans').sum():,}
- Applicants aged 20-30: {((df['AGE_YEARS']>=20) & (df['AGE_YEARS']<30)).sum():,}
- Applicants with bureau history: {(df.get('BUREAU_LOAN_COUNT', pd.Series([0]*len(df))) > 0).sum():,}

Answer questions clearly and specifically. Always cite which data segment you're referring to.
When you give a number, mention what it means for the business.
If a question cannot be answered from the data, say so clearly and explain why.
Keep answers concise but insightful — 3 to 6 sentences is ideal.
        """
        return context

    # Chat interface
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            'role': 'assistant',
            'content': "Hello! I'm your Credit Risk Data Assistant. I have full access to the Home Credit dataset with 307,511 applicants. Ask me anything about default rates, demographics, loan behavior, or risk patterns."
        })

    # Display chat history
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            st.markdown(f"""
            <div style="display:flex; justify-content:flex-end; margin:8px 0">
                <div>
                    <div class="chat-label" style="text-align:right">You</div>
                    <div class="chat-user">{msg['content']}</div>
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="margin:8px 0">
                <div class="chat-label">🤖 Assistant</div>
                <div class="chat-assistant">{msg['content']}</div>
            </div>""", unsafe_allow_html=True)

    # Input
    # user_input = st.chat_input("Ask a question about the credit risk data...")
    st.markdown("### Ask a Question")

    user_input = st.text_input(
    "Enter your question:",
    placeholder="Example: Which income type has the highest default rate?")

    ask_button = st.button("Ask")

    # if user_input:
    if ask_button and user_input:
        st.session_state.messages.append({'role': 'user', 'content': user_input})

        with st.spinner("Analyzing data..."):
            try:
                context = build_context(filtered)
                conversation = [{"role": "user", "content": context + f"\n\nUser question: {user_input}"}]

                # Add previous turns (last 6 messages for context)
                if len(st.session_state.messages) > 2:
                    conversation = []
                    conversation.append({"role": "user", "content": context})
                    conversation.append({"role": "assistant", "content": "Understood. I'm ready to answer questions about this credit risk dataset."})
                    for m in st.session_state.messages[-6:]:
                        conversation.append({"role": m['role'], "content": m['content']})

                # api_key = os.environ.get("GROK_API_KEY", "")
                try:
                     api_key = st.secrets["GROQ_API_KEY"]
                except:
                     api_key = os.getenv("GROQ_API_KEY", "")
                if not api_key:
                    reply = "⚠️ GROK_API_KEY not found. Please set it in your terminal before running the app."
                else:
                    response = requests.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {api_key}"
                        },
                        json={
                            "model": "llama-3.3-70b-versatile",
                            "max_tokens": 1000,
                            "messages": [
                                {
                                    "role": "system",
                                    "content": "You are a financial data analyst assistant embedded in a credit risk dashboard. Be specific, cite exact numbers, and always connect your answer to business implications. Be concise."
                                },
                                *conversation
                            ]
                        },
                        timeout=30
                    )

                    if response.status_code == 200:
                        data = response.json()
                        reply = data['choices'][0]['message']['content']
                    else:
                        reply = f"API error {response.status_code}: {response.text}. Please check your GROK_API_KEY."

            except Exception as e:
                reply = f"Connection error: {str(e)}. Make sure you set your GROK_API_KEY in the terminal."

        st.session_state.messages.append({'role': 'assistant', 'content': reply})
        st.rerun()

    # Clear chat
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
