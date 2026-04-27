# -*- coding: utf-8 -*-
"""
RohhBot Enhanced — Live Corporate & ESG Finance Dashboard
Multi-AI Provider | Advanced Analytics & Visualizations
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
import datetime
import uuid
import warnings
warnings.filterwarnings("ignore")

# ── Optional AI SDKs (graceful fallback if not installed) ──────────────────
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    import anthropic as anthropic_sdk
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# ══════════════════════════════════════════════════════════════════════════════
# 1.  PAGE CONFIG & GLOBAL THEME
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="RohhBot · Financial Intelligence",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded",
)

# ── Dark-luxury CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=Outfit:wght@300;400;600;700&display=swap');

  :root {
    --bg:        #0a0c10;
    --surface:   #111318;
    --border:    #1e2330;
    --accent:    #3af0a2;
    --accent2:   #5b8dee;
    --accent3:   #f7c353;
    --text:      #e8eaf0;
    --muted:     #6b7280;
    --red:       #ff5c6a;
  }

  html, body, .stApp { background: var(--bg) !important; color: var(--text); font-family: 'Outfit', sans-serif; }

  /* Sidebar */
  [data-testid="stSidebar"] { background: var(--surface) !important; border-right: 1px solid var(--border); }
  [data-testid="stSidebar"] * { color: var(--text) !important; }

  /* Inputs */
  .stTextInput input, .stSelectbox select, [data-baseweb="select"] * {
    background: #161b25 !important; border: 1px solid var(--border) !important;
    color: var(--text) !important; border-radius: 8px !important; font-family: 'DM Mono', monospace !important;
  }

  /* Metric cards */
  [data-testid="metric-container"] {
    background: linear-gradient(135deg, #111927, #0f141d);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px !important;
    transition: border-color .2s;
  }
  [data-testid="metric-container"]:hover { border-color: var(--accent); }
  [data-testid="metric-container"] label { color: var(--muted) !important; font-size: .75rem; letter-spacing:.08em; text-transform:uppercase; }
  [data-testid="metric-container"] [data-testid="stMetricValue"] { color: var(--accent) !important; font-family:'DM Mono',monospace; font-size:1.6rem; font-weight:500; }
  [data-testid="stMetricDelta"] svg { display:none; }

  /* Titles */
  h1 { font-family:'DM Serif Display',serif !important; font-size:2.2rem !important; color:var(--text) !important; letter-spacing:-.02em; }
  h2,h3 { font-family:'Outfit',sans-serif !important; color:var(--text) !important; }

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] { background:var(--surface); border-radius:12px; padding:4px; gap:4px; border:1px solid var(--border); }
  .stTabs [data-baseweb="tab"] { border-radius:8px; color:var(--muted) !important; font-weight:600; padding:8px 20px; }
  .stTabs [aria-selected="true"] { background:linear-gradient(135deg,#1a2e20,#162840) !important; color:var(--accent) !important; }

  /* Dataframe */
  .stDataFrame { border:1px solid var(--border); border-radius:10px; overflow:hidden; }

  /* Chat */
  [data-testid="stChatMessage"] { background:var(--surface) !important; border:1px solid var(--border); border-radius:12px !important; margin-bottom:8px; }
  .stChatInputContainer { background:var(--surface) !important; border-top:1px solid var(--border) !important; }

  /* Divider */
  hr { border-color: var(--border) !important; }

  /* Section label */
  .section-label {
    font-size:.7rem; font-weight:700; letter-spacing:.15em; text-transform:uppercase;
    color:var(--muted); margin-bottom:8px; padding-left:2px;
  }

  /* Badge */
  .badge {
    display:inline-block; padding:3px 10px; border-radius:20px; font-size:.72rem; font-weight:600;
    background: rgba(58,240,162,.12); color:var(--accent); border:1px solid rgba(58,240,162,.25);
  }

  /* Spinner */
  .stSpinner > div { border-top-color: var(--accent) !important; }

  /* Scrollbar */
  ::-webkit-scrollbar { width:5px; height:5px; }
  ::-webkit-scrollbar-track { background: var(--bg); }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius:4px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 2.  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if "user_id" not in st.session_state:
    st.session_state.user_id = f"user_{str(uuid.uuid4())[:8]}"
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hello! I'm **RohhBot**, your AI financial analyst. I can analyze live stock data, explain metrics, assess risk, and discuss ESG factors. What would you like to explore?"}
    ]

# ══════════════════════════════════════════════════════════════════════════════
# 3.  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🤖 AI Provider")

    ai_provider = st.selectbox(
        "Choose AI Engine",
        ["Google Gemini", "Anthropic Claude", "OpenAI ChatGPT", "Perplexity AI"],
        index=0,
    )

    model_options = {
        "Google Gemini":     ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
        "Anthropic Claude":  ["claude-opus-4-5", "claude-sonnet-4-5", "claude-haiku-4-5"],
        "OpenAI ChatGPT":    ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
        "Perplexity AI":     ["llama-3.1-sonar-large-128k-online", "llama-3.1-sonar-small-128k-online"],
    }
    selected_model = st.selectbox("Model", model_options[ai_provider])

    api_key_label = {
        "Google Gemini":    "Gemini API Key",
        "Anthropic Claude": "Anthropic API Key",
        "OpenAI ChatGPT":   "OpenAI API Key",
        "Perplexity AI":    "Perplexity API Key",
    }
    user_api_key = st.text_input(api_key_label[ai_provider], type="password", placeholder="Paste your key…")
    st.caption(f"Session `{st.session_state.user_id}`")

    st.divider()

    st.markdown("## 🔎 Asset Search")
    popular_tickers = [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
        "WIPRO.NS", "AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "AMZN",
    ]
    selected_ticker = st.selectbox("Quick Select", ["Custom…"] + popular_tickers)
    if selected_ticker == "Custom…":
        target_ticker = st.text_input("Custom Ticker", "RELIANCE.NS").upper()
    else:
        target_ticker = selected_ticker

    # Benchmark
    benchmark_ticker = st.selectbox(
        "Benchmark",
        ["^NSEI", "^BSESN", "^GSPC", "^IXIC", "^DJI"],
        index=0,
    )
    hist_period = st.selectbox("History Window", ["3mo", "6mo", "1y", "2y", "5y"], index=2)

    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# 4.  DATA FETCHING
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600)
def fetch_all_data(ticker, benchmark, period):
    try:
        tk   = yf.Ticker(ticker)
        bm   = yf.Ticker(benchmark)
        info = tk.info

        # ── Financials ──────────────────────────────────────────────────────
        fin = {
            "Name":          info.get("longName", ticker),
            "Sector":        info.get("sector", "N/A"),
            "Industry":      info.get("industry", "N/A"),
            "Country":       info.get("country", "N/A"),
            "Currency":      info.get("currency", "N/A"),
            "Market Cap":    info.get("marketCap", 0),
            "ROE (%)":       round(info.get("returnOnEquity",  0) * 100, 2) if info.get("returnOnEquity")  else None,
            "ROA (%)":       round(info.get("returnOnAssets",  0) * 100, 2) if info.get("returnOnAssets")  else None,
            "Profit Margin": round(info.get("profitMargins",   0) * 100, 2) if info.get("profitMargins")   else None,
            "P/E Ratio":     round(info.get("trailingPE", 0), 2)            if info.get("trailingPE")      else None,
            "P/B Ratio":     round(info.get("priceToBook", 0), 2)           if info.get("priceToBook")     else None,
            "EV/EBITDA":     round(info.get("enterpriseToEbitda", 0), 2)    if info.get("enterpriseToEbitda") else None,
            "Debt/Equity":   round(info.get("debtToEquity", 0), 2)          if info.get("debtToEquity")    else None,
            "Current Ratio": round(info.get("currentRatio", 0), 2)          if info.get("currentRatio")    else None,
            "Beta":          round(info.get("beta", 0), 3)                  if info.get("beta")            else None,
            "52W High":      info.get("fiftyTwoWeekHigh"),
            "52W Low":       info.get("fiftyTwoWeekLow"),
            "Dividend Yield": round(info.get("dividendYield", 0) * 100, 2)  if info.get("dividendYield")   else None,
            "Revenue":       info.get("totalRevenue", 0),
            "EBITDA":        info.get("ebitda", 0),
            "Net Income":    info.get("netIncomeToCommon", 0),
            "Gross Profit":  info.get("grossProfits", 0),
            "Operating CF":  info.get("operatingCashflow", 0),
            "Free CF":       info.get("freeCashflow", 0),
            "Total Debt":    info.get("totalDebt", 0),
            "Total Cash":    info.get("totalCash", 0),
            "Current Price": info.get("currentPrice") or info.get("regularMarketPrice", 0),
        }

        # ── Officers ────────────────────────────────────────────────────────
        officers_list = [
            {
                "Name":             o.get("name", "Unknown"),
                "Age":              o.get("age", None),
                "Title":            o.get("title", "N/A"),
                "Total Pay ($)":    o.get("totalPay", 0),
                "Exercised ($)":    o.get("exercisedValue", 0),
            }
            for o in info.get("companyOfficers", [])
        ]
        df_officers = pd.DataFrame(officers_list) if officers_list else pd.DataFrame()

        # ── Historical prices ────────────────────────────────────────────────
        hist    = tk.history(period=period)
        bm_hist = bm.history(period=period)

        return fin, df_officers, hist, bm_hist
    except Exception as e:
        return None, None, None, None

# ══════════════════════════════════════════════════════════════════════════════
# 5.  CHART HELPERS  (dark theme defaults)
# ══════════════════════════════════════════════════════════════════════════════
DARK = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Outfit", color="#e8eaf0", size=12),
    xaxis=dict(gridcolor="#1e2330", zerolinecolor="#1e2330"),
    yaxis=dict(gridcolor="#1e2330", zerolinecolor="#1e2330"),
    margin=dict(l=10, r=10, t=40, b=10),
)
ACCENT  = "#3af0a2"
ACCENT2 = "#5b8dee"
ACCENT3 = "#f7c353"
RED     = "#ff5c6a"

def fmt_large(n):
    if n is None: return "N/A"
    if abs(n) >= 1e12: return f"{n/1e12:.2f}T"
    if abs(n) >= 1e9:  return f"{n/1e9:.2f}B"
    if abs(n) >= 1e6:  return f"{n/1e6:.2f}M"
    return f"{n:,.0f}"

# ══════════════════════════════════════════════════════════════════════════════
# 6.  AI CALL HELPER
# ══════════════════════════════════════════════════════════════════════════════
def call_ai(provider, model_name, api_key, messages_history, context):
    system = f"""You are RohhBot, an elite AI financial analyst specializing in corporate finance, ESG, and quantitative analysis.
The user is viewing live financial data for a stock. Here is the live context:
{context}
Be concise, data-driven and insightful. Use bullet points and markdown. Reference specific numbers from the data."""

    if provider == "Google Gemini":
        if not GEMINI_AVAILABLE:
            return "Install `google-generativeai` to use Gemini."
        genai.configure(api_key=api_key)
        m = genai.GenerativeModel(model_name)
        full = system + "\n\nChat History:\n" + "\n".join(
            f"{x['role'].capitalize()}: {x['content']}" for x in messages_history
        )
        resp = m.generate_content(full)
        return resp.text

    elif provider == "Anthropic Claude":
        if not CLAUDE_AVAILABLE:
            return "Install `anthropic` to use Claude."
        client = anthropic_sdk.Anthropic(api_key=api_key)
        chat_msgs = [{"role": x["role"], "content": x["content"]} for x in messages_history if x["role"] != "system"]
        resp = client.messages.create(
            model=model_name, max_tokens=1024,
            system=system, messages=chat_msgs,
        )
        return resp.content[0].text

    elif provider == "OpenAI ChatGPT":
        if not OPENAI_AVAILABLE:
            return "Install `openai` to use ChatGPT."
        client = OpenAI(api_key=api_key)
        msgs = [{"role": "system", "content": system}] + [
            {"role": x["role"], "content": x["content"]} for x in messages_history
        ]
        resp = client.chat.completions.create(model=model_name, messages=msgs, max_tokens=1024)
        return resp.choices[0].message.content

    elif provider == "Perplexity AI":
        if not OPENAI_AVAILABLE:
            return "Install `openai` (used as Perplexity client) to use Perplexity."
        client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")
        msgs = [{"role": "system", "content": system}] + [
            {"role": x["role"], "content": x["content"]} for x in messages_history
        ]
        resp = client.chat.completions.create(model=model_name, messages=msgs, max_tokens=1024)
        return resp.choices[0].message.content

    return "Unknown provider."

# ══════════════════════════════════════════════════════════════════════════════
# 7.  LOAD DATA
# ══════════════════════════════════════════════════════════════════════════════
with st.spinner(f"Loading live data for **{target_ticker}** vs **{benchmark_ticker}**…"):
    fin_data, df_officers, hist, bm_hist = fetch_all_data(target_ticker, benchmark_ticker, hist_period)

if fin_data is None:
    st.error(f"❌ Could not fetch data for `{target_ticker}`. Check the ticker symbol.")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# 8.  MAIN LAYOUT
# ══════════════════════════════════════════════════════════════════════════════
left, right = st.columns([2, 1], gap="large")

# ─────────────────────────────────────────────────────────────────────────────
with left:
    # ── Header ──────────────────────────────────────────────────────────────
    st.markdown(f"## {fin_data['Name']}")
    st.markdown(
        f"<span class='badge'>{fin_data['Sector']}</span>&nbsp;"
        f"<span class='badge'>{fin_data['Industry']}</span>&nbsp;"
        f"<span class='badge'>{fin_data['Country']}</span>&nbsp;"
        f"<span class='badge'>{target_ticker} · {fin_data['Currency']}</span>",
        unsafe_allow_html=True,
    )
    st.markdown("")

    # ── KPI Row ─────────────────────────────────────────────────────────────
    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    kpi1.metric("Price",         f"{fin_data.get('Current Price','N/A')}")
    kpi2.metric("Market Cap",    fmt_large(fin_data["Market Cap"]))
    kpi3.metric("P/E Ratio",     fin_data["P/E Ratio"] or "N/A")
    kpi4.metric("ROE %",         fin_data["ROE (%)"] or "N/A")
    kpi5.metric("Beta",          fin_data["Beta"] or "N/A")
    kpi6.metric("Div Yield %",   fin_data["Dividend Yield"] or "N/A")

    st.markdown("---")

    # ── Tabs ────────────────────────────────────────────────────────────────
    tabs = st.tabs([
        "📈 Price & Returns",
        "📊 Valuation",
        "💰 P&L Waterfall",
        "⚖️ Risk & Regression",
        "🏛️ Capital Structure",
        "🎯 KPI Scorecard",
        "👥 Governance",
    ])

    # ════════════════════════════════════════════════════════════════════════
    # TAB 1 — Price & Monthly Returns
    # ════════════════════════════════════════════════════════════════════════
    with tabs[0]:
        if hist is not None and not hist.empty:
            col_a, col_b = st.columns([3, 2])

            with col_a:
                # Candlestick
                fig_price = go.Figure(data=[go.Candlestick(
                    x=hist.index, open=hist["Open"], high=hist["High"],
                    low=hist["Low"],  close=hist["Close"],
                    increasing_line_color=ACCENT, decreasing_line_color=RED,
                    increasing_fillcolor=ACCENT, decreasing_fillcolor=RED,
                    name="Price",
                )])
                # 50 & 200 day MA
                hist["MA50"]  = hist["Close"].rolling(50).mean()
                hist["MA200"] = hist["Close"].rolling(200).mean()
                fig_price.add_trace(go.Scatter(x=hist.index, y=hist["MA50"],  name="MA50",  line=dict(color=ACCENT3,  width=1.5)))
                fig_price.add_trace(go.Scatter(x=hist.index, y=hist["MA200"], name="MA200", line=dict(color=ACCENT2,  width=1.5)))
                fig_price.update_layout(**DARK, title="Price + Moving Averages", height=350, showlegend=True,
                                        legend=dict(bgcolor="rgba(0,0,0,0)"))
                st.plotly_chart(fig_price, use_container_width=True)

            with col_b:
                # Monthly return comparison
                monthly_close = hist["Close"].resample("ME").last()
                monthly_ret   = monthly_close.pct_change().dropna() * 100
                colors        = [ACCENT if r >= 0 else RED for r in monthly_ret]
                fig_monthly   = go.Figure(go.Bar(
                    x=monthly_ret.index.strftime("%b %Y"), y=monthly_ret.values,
                    marker_color=colors, name="Monthly Return %",
                ))
                fig_monthly.update_layout(**DARK, title="Monthly Returns (%)", height=350,
                                          xaxis_tickangle=-45)
                st.plotly_chart(fig_monthly, use_container_width=True)

            # Cumulative return vs benchmark
            ret_stock = hist["Close"].pct_change().dropna()
            cum_stock = (1 + ret_stock).cumprod() - 1

            fig_cum = go.Figure()
            fig_cum.add_trace(go.Scatter(x=cum_stock.index, y=cum_stock * 100,
                                         name=target_ticker, line=dict(color=ACCENT, width=2.5)))
            if bm_hist is not None and not bm_hist.empty:
                ret_bm  = bm_hist["Close"].pct_change().dropna()
                cum_bm  = (1 + ret_bm).cumprod() - 1
                fig_cum.add_trace(go.Scatter(x=cum_bm.index, y=cum_bm * 100,
                                             name=benchmark_ticker, line=dict(color=ACCENT2, width=2, dash="dot")))
            fig_cum.update_layout(**DARK, title="Cumulative Return vs Benchmark (%)", height=280)
            st.plotly_chart(fig_cum, use_container_width=True)

            # Volume
            fig_vol = go.Figure(go.Bar(x=hist.index, y=hist["Volume"],
                                       marker_color=ACCENT2, opacity=0.6, name="Volume"))
            fig_vol.update_layout(**DARK, title="Trading Volume", height=180)
            st.plotly_chart(fig_vol, use_container_width=True)

        else:
            st.info("No historical price data available.")

    # ════════════════════════════════════════════════════════════════════════
    # TAB 2 — Valuation Comparison (Bullet / Bar)
    # ════════════════════════════════════════════════════════════════════════
    with tabs[1]:
        metrics_vals = {
            "P/E Ratio":     fin_data["P/E Ratio"],
            "P/B Ratio":     fin_data["P/B Ratio"],
            "EV/EBITDA":     fin_data["EV/EBITDA"],
            "Debt/Equity":   fin_data["Debt/Equity"],
            "Current Ratio": fin_data["Current Ratio"],
            "ROE (%)":       fin_data["ROE (%)"],
            "ROA (%)":       fin_data["ROA (%)"],
            "Profit Margin": fin_data["Profit Margin"],
        }

        # ── Bullet Charts (KPI-style progress bars) ──────────────────────
        BENCHMARKS = {
            "P/E Ratio":     (0, 40,  15),
            "P/B Ratio":     (0, 10,   3),
            "EV/EBITDA":     (0, 30,  12),
            "Debt/Equity":   (0, 200,  80),
            "Current Ratio": (0,  5,   1.5),
            "ROE (%)":       (0, 40,  15),
            "ROA (%)":       (0, 20,   5),
            "Profit Margin": (0, 50,  10),
        }
        st.markdown("### 🎯 Bullet Charts — Metric vs Sector Benchmark")
        fig_bullet = go.Figure()
        for i, (metric, val) in enumerate(metrics_vals.items()):
            if val is None: continue
            lo, hi, target = BENCHMARKS[metric]
            fig_bullet.add_trace(go.Bar(
                x=[hi * 0.75], y=[metric], orientation="h",
                marker_color="rgba(30,35,48,0.9)", name="", showlegend=False,
                width=0.5,
            ))
            fig_bullet.add_trace(go.Bar(
                x=[val if val <= hi else hi], y=[metric], orientation="h",
                marker_color=ACCENT if val <= target else ACCENT3 if val <= hi * 1.2 else RED,
                name="", showlegend=False, width=0.3,
            ))
            fig_bullet.add_shape(type="line",
                x0=target, x1=target, y0=i - 0.35, y1=i + 0.35,
                line=dict(color=RED, width=2, dash="dot"),
            )
        fig_bullet.update_layout(**DARK, title="Bullet Chart — Value (bar) vs Benchmark (dotted line)",
                                  height=420, barmode="overlay",
                                  xaxis=dict(visible=False), yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_bullet, use_container_width=True)

        # ── Radar / Spider ───────────────────────────────────────────────
        radar_labels = ["ROE", "ROA", "Profit Margin", "Current Ratio", "Div Yield"]
        radar_sector_avg = [12, 6, 8, 1.5, 2.0]
        radar_vals = [
            fin_data["ROE (%)"]       or 0,
            fin_data["ROA (%)"]       or 0,
            fin_data["Profit Margin"] or 0,
            min((fin_data["Current Ratio"] or 0) * 10, 100),
            fin_data["Dividend Yield"] or 0,
        ]
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=radar_sector_avg + [radar_sector_avg[0]],
                                             theta=radar_labels + [radar_labels[0]],
                                             fill="toself", name="Sector Avg",
                                             line_color=ACCENT2, fillcolor="rgba(91,141,238,.15)"))
        fig_radar.add_trace(go.Scatterpolar(r=radar_vals + [radar_vals[0]],
                                             theta=radar_labels + [radar_labels[0]],
                                             fill="toself", name=target_ticker,
                                             line_color=ACCENT, fillcolor="rgba(58,240,162,.15)"))
        fig_radar.update_layout(**DARK, polar=dict(
                                    bgcolor="rgba(0,0,0,0)",
                                    radialaxis=dict(visible=True, gridcolor="#1e2330", color="#6b7280"),
                                    angularaxis=dict(gridcolor="#1e2330")),
                                 title="Efficiency Radar — Company vs Sector Avg", height=380)
        st.plotly_chart(fig_radar, use_container_width=True)

    # ════════════════════════════════════════════════════════════════════════
    # TAB 3 — P&L Waterfall
    # ════════════════════════════════════════════════════════════════════════
    with tabs[2]:
        rev  = fin_data["Revenue"]     or 0
        gp   = fin_data["Gross Profit"] or 0
        ebit = fin_data["EBITDA"]      or 0
        ni   = fin_data["Net Income"]  or 0
        ocf  = fin_data["Operating CF"] or 0
        fcf  = fin_data["Free CF"]     or 0

        waterfall_labels = ["Revenue", "COGS", "Gross Profit", "OpEx & D&A", "EBITDA", "Tax & Int.", "Net Income"]
        cogs   = -(rev  - gp)
        opex   = -(gp   - ebit)
        taxint = -(ebit - ni)

        waterfall_vals   = [rev, cogs, gp, opex, ebit, taxint, ni]
        waterfall_meas   = ["absolute", "relative", "total", "relative", "total", "relative", "total"]
        bar_colors       = [ACCENT, RED, ACCENT, RED, ACCENT2, RED, ACCENT3]

        fig_wf = go.Figure(go.Waterfall(
            name="P&L", measure=waterfall_meas,
            x=waterfall_labels,
            y=waterfall_vals,
            connector=dict(line=dict(color=ACCENT2, dash="dot", width=1)),
            increasing_marker_color=ACCENT,
            decreasing_marker_color=RED,
            totals_marker_color=ACCENT3,
            text=[fmt_large(v) for v in waterfall_vals],
            textposition="outside",
        ))
        fig_wf.update_layout(**DARK, title="P&L Waterfall — Revenue to Net Income", height=420)
        st.plotly_chart(fig_wf, use_container_width=True)

        # Cash Flow comparison
        cf_labels = ["Operating CF", "Free CF", "Net Income", "EBITDA"]
        cf_vals   = [ocf, fcf, ni, ebit]
        fig_cf = go.Figure(go.Bar(
            x=cf_labels, y=cf_vals,
            marker_color=[ACCENT, ACCENT2, ACCENT3, ACCENT3],
            text=[fmt_large(v) for v in cf_vals], textposition="outside",
        ))
        fig_cf.update_layout(**DARK, title="Cash Flow Overview", height=320)
        st.plotly_chart(fig_cf, use_container_width=True)

    # ════════════════════════════════════════════════════════════════════════
    # TAB 4 — Risk & Regression
    # ════════════════════════════════════════════════════════════════════════
    with tabs[3]:
        if hist is not None and not hist.empty and bm_hist is not None and not bm_hist.empty:
            daily_ret  = hist["Close"].pct_change().dropna()
            daily_bm   = bm_hist["Close"].pct_change().dropna()
            merged     = pd.concat([daily_ret, daily_bm], axis=1, join="inner")
            merged.columns = [target_ticker, benchmark_ticker]

            # Risk stats
            vol_ann   = daily_ret.std() * np.sqrt(252) * 100
            bm_vol    = daily_bm.std()  * np.sqrt(252) * 100
            sharpe    = (daily_ret.mean() * 252) / (daily_ret.std() * np.sqrt(252))
            max_dd    = (hist["Close"] / hist["Close"].cummax() - 1).min() * 100
            x_arr = merged[benchmark_ticker].values
            y_arr = merged[target_ticker].values
            slope, intercept = np.polyfit(x_arr, y_arr, 1)
            ss_res = np.sum((y_arr - (slope * x_arr + intercept)) ** 2)
            ss_tot = np.sum((y_arr - np.mean(y_arr)) ** 2)
            r_val  = np.sqrt(1 - ss_res / ss_tot) if ss_tot != 0 else 0
            beta_calc  = slope
            alpha_calc = (intercept * 252) * 100

            r_kpi1, r_kpi2, r_kpi3, r_kpi4 = st.columns(4)
            r_kpi1.metric("Annualised Vol %", f"{vol_ann:.2f}")
            r_kpi2.metric("Sharpe Ratio",     f"{sharpe:.2f}")
            r_kpi3.metric("Max Drawdown %",   f"{max_dd:.2f}")
            r_kpi4.metric("Beta (calc)",       f"{beta_calc:.3f}")

            col_r1, col_r2 = st.columns(2)
            with col_r1:
                # Scatter + OLS Regression
                x_line = np.linspace(merged[benchmark_ticker].min(), merged[benchmark_ticker].max(), 100)
                y_line = intercept + slope * x_line
                fig_reg = go.Figure()
                fig_reg.add_trace(go.Scatter(
                    x=merged[benchmark_ticker], y=merged[target_ticker],
                    mode="markers", name="Daily Returns",
                    marker=dict(color=ACCENT, opacity=0.5, size=5),
                ))
                fig_reg.add_trace(go.Scatter(
                    x=x_line, y=y_line, mode="lines", name=f"OLS (β={beta_calc:.2f}, R²={r_val**2:.2f})",
                    line=dict(color=RED, width=2.5),
                ))
                fig_reg.update_layout(**DARK, title="OLS Regression — Stock vs Benchmark", height=380)
                st.plotly_chart(fig_reg, use_container_width=True)

            with col_r2:
                # Rolling Beta (60-day)
                roll_cov  = daily_ret.rolling(60).cov(daily_bm)
                roll_var  = daily_bm.rolling(60).var()
                roll_beta = (roll_cov / roll_var).dropna()
                fig_rbeta = go.Figure(go.Scatter(
                    x=roll_beta.index, y=roll_beta.values,
                    line=dict(color=ACCENT3, width=2), fill="tozeroy",
                    fillcolor="rgba(247,195,83,.1)", name="Rolling 60-day Beta",
                ))
                fig_rbeta.add_hline(y=1, line_dash="dot", line_color=RED, annotation_text="Market Beta=1")
                fig_rbeta.update_layout(**DARK, title="Rolling 60-Day Beta", height=380)
                st.plotly_chart(fig_rbeta, use_container_width=True)

            # Return Distribution
            fig_dist = go.Figure()
            fig_dist.add_trace(go.Histogram(x=merged[target_ticker]*100, nbinsx=60,
                                             marker_color=ACCENT, opacity=0.7, name=target_ticker))
            fig_dist.add_trace(go.Histogram(x=merged[benchmark_ticker]*100, nbinsx=60,
                                             marker_color=ACCENT2, opacity=0.7, name=benchmark_ticker))
            fig_dist.update_layout(**DARK, title="Daily Return Distribution (%)", barmode="overlay", height=280)
            st.plotly_chart(fig_dist, use_container_width=True)

            # Drawdown
            drawdown_series = (hist["Close"] / hist["Close"].cummax() - 1) * 100
            fig_dd = go.Figure(go.Scatter(
                x=drawdown_series.index, y=drawdown_series.values,
                fill="tozeroy", fillcolor="rgba(255,92,106,.15)",
                line=dict(color=RED, width=1.5), name="Drawdown %",
            ))
            fig_dd.update_layout(**DARK, title="Drawdown from Peak (%)", height=220)
            st.plotly_chart(fig_dd, use_container_width=True)
        else:
            st.info("Not enough data to compute risk metrics.")

    # ════════════════════════════════════════════════════════════════════════
    # TAB 5 — Capital Structure (Stacked Column)
    # ════════════════════════════════════════════════════════════════════════
    with tabs[4]:
        total_assets  = (fin_data["Total Debt"] or 0) + (fin_data["Total Cash"] or 0)
        total_debt    = fin_data["Total Debt"]  or 0
        total_cash    = fin_data["Total Cash"]  or 0
        net_debt      = total_debt - total_cash
        market_cap    = fin_data["Market Cap"]  or 0
        enterprise_v  = market_cap + net_debt

        cap1, cap2, cap3, cap4 = st.columns(4)
        cap1.metric("Total Debt",    fmt_large(total_debt))
        cap2.metric("Total Cash",    fmt_large(total_cash))
        cap3.metric("Net Debt",      fmt_large(net_debt))
        cap4.metric("Enterprise Val",fmt_large(enterprise_v))

        # Stacked bar — capital vs cash
        fig_cap = go.Figure()
        fig_cap.add_trace(go.Bar(name="Market Cap",  x=["Capital Structure"], y=[market_cap],  marker_color=ACCENT))
        fig_cap.add_trace(go.Bar(name="Net Debt",    x=["Capital Structure"], y=[max(net_debt,0)], marker_color=RED))
        fig_cap.add_trace(go.Bar(name="Cash Buffer", x=["Capital Structure"], y=[total_cash],  marker_color=ACCENT3))
        fig_cap.update_layout(**DARK, barmode="stack", title="Capital Structure (Stacked)", height=340)
        st.plotly_chart(fig_cap, use_container_width=True)

        # Debt vs Cash vs Revenue comparison
        compare_labels = ["Revenue", "EBITDA", "Net Income", "Total Debt", "Total Cash", "Free CF"]
        compare_vals   = [
            fin_data["Revenue"]      or 0,
            fin_data["EBITDA"]       or 0,
            fin_data["Net Income"]   or 0,
            total_debt,
            total_cash,
            fin_data["Free CF"]      or 0,
        ]
        bar_clrs = [ACCENT, ACCENT2, ACCENT3, RED, ACCENT, ACCENT2]
        fig_comp = go.Figure(go.Bar(
            x=compare_labels, y=compare_vals,
            marker_color=bar_clrs,
            text=[fmt_large(v) for v in compare_vals], textposition="outside",
        ))
        fig_comp.update_layout(**DARK, title="Key Financial Comparisons", height=360)
        st.plotly_chart(fig_comp, use_container_width=True)

    # ════════════════════════════════════════════════════════════════════════
    # TAB 6 — KPI Scorecard
    # ════════════════════════════════════════════════════════════════════════
    with tabs[5]:
        st.markdown("### 🎯 Comprehensive KPI Scorecard")

        def score_metric(val, good_threshold, bad_threshold, higher_is_better=True):
            if val is None: return "⚪ N/A", "#6b7280"
            if higher_is_better:
                if val >= good_threshold: return "🟢 Strong",  ACCENT
                if val >= bad_threshold:  return "🟡 Moderate", ACCENT3
                return "🔴 Weak", RED
            else:
                if val <= good_threshold: return "🟢 Strong",  ACCENT
                if val <= bad_threshold:  return "🟡 Moderate", ACCENT3
                return "🔴 Weak", RED

        scorecard_data = [
            ("Profitability",  "ROE (%)",       fin_data["ROE (%)"],       15, 8,   True),
            ("Profitability",  "ROA (%)",       fin_data["ROA (%)"],       8,  3,   True),
            ("Profitability",  "Profit Margin", fin_data["Profit Margin"], 10, 5,   True),
            ("Valuation",      "P/E Ratio",     fin_data["P/E Ratio"],     20, 35,  False),
            ("Valuation",      "P/B Ratio",     fin_data["P/B Ratio"],     3,  6,   False),
            ("Valuation",      "EV/EBITDA",     fin_data["EV/EBITDA"],     12, 20,  False),
            ("Solvency",       "Debt/Equity",   fin_data["Debt/Equity"],   80, 150, False),
            ("Liquidity",      "Current Ratio", fin_data["Current Ratio"], 2,  1,   True),
            ("Risk",           "Beta",          fin_data["Beta"],          0.8, 1.3, False),
        ]

        df_score = pd.DataFrame(
            [(cat, m, v, score_metric(v, g, b, h)[0]) for cat, m, v, g, b, h in scorecard_data],
            columns=["Category", "Metric", "Value", "Signal"],
        )
        df_score["Value"] = df_score["Value"].apply(lambda x: "N/A" if x is None else str(x))

        # Group by category
        for cat in df_score["Category"].unique():
            st.markdown(f"**{cat}**")
            sub = df_score[df_score["Category"] == cat][["Metric", "Value", "Signal"]]
            st.dataframe(sub, use_container_width=True, hide_index=True)

        # Gauge: Overall Score
        valid_scores  = [score_metric(v, g, b, h) for _, _, v, g, b, h in scorecard_data if v is not None]
        strong_count  = sum(1 for s, _ in valid_scores if "Strong" in s)
        overall_pct   = (strong_count / len(valid_scores) * 100) if valid_scores else 0

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=overall_pct,
            title=dict(text="Overall Health Score (%)", font=dict(color=ACCENT, size=16)),
            delta=dict(reference=50),
            gauge=dict(
                axis=dict(range=[0, 100], tickcolor="#6b7280"),
                bar=dict(color=ACCENT),
                bgcolor="rgba(0,0,0,0)",
                steps=[
                    dict(range=[0, 33],  color="rgba(255,92,106,.15)"),
                    dict(range=[33, 66], color="rgba(247,195,83,.15)"),
                    dict(range=[66, 100],color="rgba(58,240,162,.15)"),
                ],
                threshold=dict(line=dict(color=RED, width=3), thickness=0.75, value=50),
            ),
            number=dict(font=dict(color=ACCENT, size=36, family="DM Mono")),
        ))
        fig_gauge.update_layout(**DARK, height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)

    # ════════════════════════════════════════════════════════════════════════
    # TAB 7 — Governance
    # ════════════════════════════════════════════════════════════════════════
    with tabs[6]:
        if df_officers is not None and not df_officers.empty:
            st.dataframe(df_officers, use_container_width=True, hide_index=True)

            df_age = df_officers.dropna(subset=["Age"]).copy()
            df_age["Age"] = pd.to_numeric(df_age["Age"], errors="coerce")
            df_age = df_age.dropna(subset=["Age"])

            if not df_age.empty:
                fig_gov = px.bar(df_age, x="Name", y="Age", color="Title",
                                 title="Executive Age Distribution",
                                 color_discrete_sequence=px.colors.qualitative.Set2)
                fig_gov.update_layout(**DARK, height=320, xaxis_tickangle=-30)
                st.plotly_chart(fig_gov, use_container_width=True)

            df_pay = df_officers[df_officers["Total Pay ($)"] > 0]
            if not df_pay.empty:
                fig_pay = go.Figure(go.Bar(
                    x=df_pay["Name"], y=df_pay["Total Pay ($)"],
                    marker_color=ACCENT3, text=[fmt_large(v) for v in df_pay["Total Pay ($)"]],
                    textposition="outside",
                ))
                fig_pay.update_layout(**DARK, title="Executive Compensation", height=320, xaxis_tickangle=-30)
                st.plotly_chart(fig_pay, use_container_width=True)
        else:
            st.info("No governance data available.")

# ─────────────────────────────────────────────────────────────────────────────
# RIGHT COLUMN — CHATBOT
# ─────────────────────────────────────────────────────────────────────────────
with right:
    ai_icons = {
        "Google Gemini":    "✦",
        "Anthropic Claude": "◈",
        "OpenAI ChatGPT":   "⬡",
        "Perplexity AI":    "⬢",
    }
    st.markdown(f"## {ai_icons.get(ai_provider,'🤖')} {ai_provider} Analyst")
    st.caption(f"Model: `{selected_model}` · Stock: `{target_ticker}`")

    chat_container = st.container(height=520)
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if prompt := st.chat_input("Ask about financials, risk, ESG, governance…"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                if user_api_key:
                    with st.spinner("Analysing…"):
                        context = (
                            f"Company: {fin_data['Name']} ({target_ticker})\n"
                            f"Sector: {fin_data['Sector']} | Industry: {fin_data['Industry']}\n"
                            f"Financials: {fin_data}\n"
                            f"Officers:\n{df_officers.to_string() if df_officers is not None and not df_officers.empty else 'N/A'}"
                        )
                        try:
                            answer = call_ai(ai_provider, selected_model, user_api_key,
                                             st.session_state.messages, context)
                            st.markdown(answer)
                            st.session_state.messages.append({"role": "assistant", "content": answer})
                        except Exception as e:
                            err = f"❌ Error: {e}"
                            st.error(err)
                            st.session_state.messages.append({"role": "assistant", "content": err})
                else:
                    msg = f"⚠️ Please enter your **{ai_provider}** API key in the sidebar."
                    st.warning(msg)
                    st.session_state.messages.append({"role": "assistant", "content": msg})
