"""
Cooper River Deal Finder
A single-page Streamlit dashboard for tracking, filtering, and evaluating
resale/auction deals across CTBids, eBay, HiBid, Facebook Marketplace,
Mercari, Chairish, and Etsy.

Run locally (optional, no terminal needed for deployment - see DEPLOY.md):
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
from datetime import date, datetime
import io

# --------------------------------------------------------------------------
# PAGE CONFIG + GLOBAL STYLE
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Cooper River Deal Finder",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded",
)

DARK_CSS = """
<style>
    /* ---- base ---- */
    .stApp {
        background: linear-gradient(180deg, #0b0f14 0%, #10151c 100%);
        color: #e6e9ef;
    }
    section[data-testid="stSidebar"] {
        background: #0d1117;
        border-right: 1px solid #1f2733;
    }
    h1, h2, h3, h4 { color: #f2f4f8 !important; letter-spacing: -0.02em; }

    /* ---- KPI cards ---- */
    .kpi-card {
        background: linear-gradient(145deg, #141a23, #0f141b);
        border: 1px solid #232c38;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.25);
    }
    .kpi-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #8b96a5;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #f7f9fc;
    }
    .kpi-sub { font-size: 0.8rem; color: #67e8a4; margin-top: 2px; }
    .kpi-sub.neg { color: #f2607a; }

    /* ---- pills / badges ---- */
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }
    .badge-hot { background: #37260f; color: #f5a524; border: 1px solid #f5a52440;}
    .badge-good { background: #0f2e22; color: #22c98c; border: 1px solid #22c98c40;}
    .badge-pass { background: #2b1418; color: #f2607a; border: 1px solid #f2607a40;}

    /* buttons */
    .stButton>button {
        border-radius: 10px;
        border: 1px solid #2a3441;
        background: #1a212b;
        color: #e6e9ef;
        font-weight: 600;
    }
    .stButton>button:hover { border-color: #4d7cff; color: #4d7cff; }

    /* dataframe */
    div[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }

    /* metric containers spacing */
    .block-container { padding-top: 1.6rem; }

    hr { border-color: #232c38; }
</style>
"""
st.markdown(DARK_CSS, unsafe_allow_html=True)

PLATFORMS = ["CTBids", "eBay", "HiBid", "Facebook Marketplace", "Mercari", "Chairish", "Etsy", "Estate Sale", "Curbside"]
CATEGORIES = ["Gold/Silver Jewelry", "Sterling Flatware", "Watches", "Furniture", "Electronics", "Coins/Currency", "Collectibles", "Other"]
STATUSES = ["Watching", "Bid Placed", "Won/Purchased", "Listed", "Sold", "Passed"]

# --------------------------------------------------------------------------
# SESSION STATE INIT
# --------------------------------------------------------------------------
if "deals" not in st.session_state:
    st.session_state.deals = pd.DataFrame([
        {
            "Date Added": date.today().isoformat(),
            "Item": "14k Gold Chain Lot (Sample)",
            "Platform": "CTBids",
            "Category": "Gold/Silver Jewelry",
            "Cost": 85.00,
            "Est. Resale Value": 240.00,
            "Status": "Won/Purchased",
            "Notes": "Sample row \u2014 edit or delete me",
        }
    ])

if "editor_key" not in st.session_state:
    st.session_state.editor_key = 0


def recalc(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived profit columns to the deals dataframe."""
    df = df.copy()
    df["Cost"] = pd.to_numeric(df["Cost"], errors="coerce").fillna(0)
    df["Est. Resale Value"] = pd.to_numeric(df["Est. Resale Value"], errors="coerce").fillna(0)
    df["Gross Profit"] = df["Est. Resale Value"] - df["Cost"]
    df["ROI %"] = df.apply(
        lambda r: (r["Gross Profit"] / r["Cost"] * 100) if r["Cost"] > 0 else 0, axis=1
    )
    return df


# --------------------------------------------------------------------------
# SIDEBAR — ADD DEAL / IMPORT / EXPORT
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🪙 Cooper River Deal Finder")
    st.caption("Sourcing dashboard for the whole household")

    st.markdown("---")
    st.markdown("#### ➕ Add a Deal")
    with st.form("add_deal_form", clear_on_submit=True):
        item = st.text_input("Item description")
        c1, c2 = st.columns(2)
        with c1:
            platform = st.selectbox("Platform", PLATFORMS)
            cost = st.number_input("Cost ($)", min_value=0.0, step=1.0, format="%.2f")
        with c2:
            category = st.selectbox("Category", CATEGORIES)
            resale = st.number_input("Est. resale value ($)", min_value=0.0, step=1.0, format="%.2f")
        status = st.selectbox("Status", STATUSES, index=0)
        notes = st.text_area("Notes", height=68, placeholder="Karat, weight, condition, auction end time...")
        submitted = st.form_submit_button("Add to dashboard", use_container_width=True)

        if submitted:
            if not item.strip():
                st.warning("Give the item a name first.")
            else:
                new_row = pd.DataFrame([{
                    "Date Added": date.today().isoformat(),
                    "Item": item.strip(),
                    "Platform": platform,
                    "Category": category,
                    "Cost": cost,
                    "Est. Resale Value": resale,
                    "Status": status,
                    "Notes": notes.strip(),
                }])
                st.session_state.deals = pd.concat(
                    [st.session_state.deals, new_row], ignore_index=True
                )
                st.session_state.editor_key += 1
                st.success(f"Added: {item.strip()}")

    st.markdown("---")
    st.markdown("#### 📥 Import / 📤 Export")

    uploaded = st.file_uploader("Import deals from CSV", type=["csv"])
    if uploaded is not None:
        try:
            imported = pd.read_csv(uploaded)
            required = {"Item", "Platform", "Category", "Cost", "Est. Resale Value", "Status"}
            if required.issubset(set(imported.columns)):
                if "Date Added" not in imported.columns:
                    imported["Date Added"] = date.today().isoformat()
                if "Notes" not in imported.columns:
                    imported["Notes"] = ""
                st.session_state.deals = pd.concat(
                    [st.session_state.deals, imported], ignore_index=True
                )
                st.success(f"Imported {len(imported)} rows.")
            else:
                st.error(f"CSV must include columns: {', '.join(required)}")
        except Exception as e:
            st.error(f"Couldn't read that file: {e}")

    csv_buffer = io.StringIO()
    st.session_state.deals.to_csv(csv_buffer, index=False)
    st.download_button(
        "Download all deals as CSV",
        data=csv_buffer.getvalue(),
        file_name=f"cooper_river_deals_{date.today().isoformat()}.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.markdown("---")
    st.caption("Note: this app resets its data if the free hosting instance restarts. Download a CSV backup regularly, then re-import it next session.")


# --------------------------------------------------------------------------
# HEADER + KPI ROW
# --------------------------------------------------------------------------
st.markdown("## Cooper River Deal Finder")
st.caption(f"Live dashboard — updated {datetime.now().strftime('%b %d, %Y %I:%M %p')}")

df = recalc(st.session_state.deals)

active_mask = ~df["Status"].isin(["Passed", "Sold"])
total_invested = df.loc[df["Status"] != "Passed", "Cost"].sum()
total_est_profit = df.loc[active_mask, "Gross Profit"].sum()
sold_profit = df.loc[df["Status"] == "Sold", "Gross Profit"].sum()
deal_count = int(active_mask.sum())

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Active Deals</div>
        <div class="kpi-value">{deal_count}</div></div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Total Invested</div>
        <div class="kpi-value">${total_invested:,.2f}</div></div>""", unsafe_allow_html=True)
with k3:
    cls = "kpi-sub" if total_est_profit >= 0 else "kpi-sub neg"
    st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Est. Profit (Active)</div>
        <div class="kpi-value">${total_est_profit:,.2f}</div>
        <div class="{cls}">{'↑ projected' if total_est_profit>=0 else '↓ projected'}</div></div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Realized Profit (Sold)</div>
        <div class="kpi-value">${sold_profit:,.2f}</div></div>""", unsafe_allow_html=True)

st.write("")

# --------------------------------------------------------------------------
# TABS — DASHBOARD / PROFIT CALCULATOR
# --------------------------------------------------------------------------
tab_dash, tab_calc = st.tabs(["📊  Deal Dashboard", "🧮  Profit Calculator"])

with tab_dash:
    st.markdown("#### Filters")
    f1, f2, f3, f4 = st.columns([1.2, 1.2, 1.2, 2])
    with f1:
        platform_filter = st.multiselect("Platform", PLATFORMS, default=[])
    with f2:
        category_filter = st.multiselect("Category", CATEGORIES, default=[])
    with f3:
        status_filter = st.multiselect("Status", STATUSES, default=[])
    with f4:
        search = st.text_input("Search item / notes", placeholder="e.g. Seiko, 14k, Bombay...")

    filtered = df.copy()
    if platform_filter:
        filtered = filtered[filtered["Platform"].isin(platform_filter)]
    if category_filter:
        filtered = filtered[filtered["Category"].isin(category_filter)]
    if status_filter:
        filtered = filtered[filtered["Status"].isin(status_filter)]
    if search:
        s = search.lower()
        filtered = filtered[
            filtered["Item"].str.lower().str.contains(s, na=False)
            | filtered["Notes"].str.lower().str.contains(s, na=False)
        ]

    st.markdown(f"#### Deals ({len(filtered)})")
    st.caption("Edit any cell directly. Add rows with the ➕ button in the sidebar, delete by selecting a row and pressing the trash icon.")

    edited = st.data_editor(
        filtered.drop(columns=["Gross Profit", "ROI %"]),
        num_rows="dynamic",
        use_container_width=True,
        height=420,
        column_config={
            "Cost": st.column_config.NumberColumn(format="$%.2f"),
            "Est. Resale Value": st.column_config.NumberColumn(format="$%.2f"),
            "Platform": st.column_config.SelectboxColumn(options=PLATFORMS),
            "Category": st.column_config.SelectboxColumn(options=CATEGORIES),
            "Status": st.column_config.SelectboxColumn(options=STATUSES),
        },
        key=f"editor_{st.session_state.editor_key}",
    )

    # push edits made in the filtered view back into the master dataframe
    if not edited.equals(filtered.drop(columns=["Gross Profit", "ROI %"])):
        st.session_state.deals.update(edited)
        # handle any newly added rows from the data editor
        if len(edited) > len(filtered):
            extra_rows = edited.iloc[len(filtered):]
            st.session_state.deals = pd.concat([st.session_state.deals, extra_rows], ignore_index=True)

    st.markdown("---")
    st.markdown("#### Quick profit view per deal (30/70 · 50/50)")
    quick = recalc(edited) if len(edited) else df.iloc[0:0]
    if len(quick):
        quick["30/70 (Cooper River share @70%)"] = quick["Gross Profit"] * 0.70
        quick["50/50 (each share)"] = quick["Gross Profit"] * 0.50
        st.dataframe(
            quick[["Item", "Platform", "Cost", "Est. Resale Value", "Gross Profit",
                   "30/70 (Cooper River share @70%)", "50/50 (each share)"]],
            use_container_width=True,
            column_config={
                "Cost": st.column_config.NumberColumn(format="$%.2f"),
                "Est. Resale Value": st.column_config.NumberColumn(format="$%.2f"),
                "Gross Profit": st.column_config.NumberColumn(format="$%.2f"),
                "30/70 (Cooper River share @70%)": st.column_config.NumberColumn(format="$%.2f"),
                "50/50 (each share)": st.column_config.NumberColumn(format="$%.2f"),
            },
        )
    else:
        st.info("No deals match the current filters.")

with tab_calc:
    st.markdown("#### Standalone Profit Calculator")
    st.caption("Punch in a purchase cost and expected resale value to see both split scenarios instantly — handy for evaluating a lot in real time during a live auction.")

    cc1, cc2 = st.columns(2)
    with cc1:
        calc_cost = st.number_input("Purchase / bid cost ($)", min_value=0.0, step=1.0, format="%.2f", key="calc_cost")
    with cc2:
        calc_resale = st.number_input("Estimated resale value ($)", min_value=0.0, step=1.0, format="%.2f", key="calc_resale")

    with st.expander("Optional: factor in platform fees / buyer's premium"):
        fee_pct = st.slider("Fees as % of resale value (marketplace + payment processing)", 0.0, 30.0, 13.0, 0.5)
        premium_pct = st.slider("Buyer's premium at purchase (e.g. CTBids 18%)", 0.0, 25.0, 18.0, 0.5)

    true_cost = calc_cost * (1 + premium_pct / 100)
    net_resale = calc_resale * (1 - fee_pct / 100)
    gross_profit = net_resale - true_cost
    roi = (gross_profit / true_cost * 100) if true_cost > 0 else 0

    st.markdown("---")
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-label">True Cost (w/ premium)</div>
            <div class="kpi-value">${true_cost:,.2f}</div></div>""", unsafe_allow_html=True)
    with r2:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Net Resale (after fees)</div>
            <div class="kpi-value">${net_resale:,.2f}</div></div>""", unsafe_allow_html=True)
    with r3:
        cls = "kpi-sub" if gross_profit >= 0 else "kpi-sub neg"
        st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Net Profit</div>
            <div class="kpi-value">${gross_profit:,.2f}</div>
            <div class="{cls}">{roi:,.1f}% ROI</div></div>""", unsafe_allow_html=True)
    with r4:
        badge = "badge-good" if roi >= 50 else ("badge-hot" if roi >= 15 else "badge-pass")
        label = "STRONG DEAL" if roi >= 50 else ("WORTH IT" if roi >= 15 else "THIN MARGIN")
        st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Verdict</div>
            <div style="margin-top:6px;"><span class="badge {badge}">{label}</span></div></div>""", unsafe_allow_html=True)

    st.markdown("### Split Scenarios")
    s1, s2 = st.columns(2)
    with s1:
        st.markdown("##### 30 / 70 Split")
        st.write(f"**Partner A (30%):** ${gross_profit*0.30:,.2f}")
        st.write(f"**Partner B (70%):** ${gross_profit*0.70:,.2f}")
    with s2:
        st.markdown("##### 50 / 50 Split")
        st.write(f"**Partner A (50%):** ${gross_profit*0.50:,.2f}")
        st.write(f"**Partner B (50%):** ${gross_profit*0.50:,.2f}")

st.markdown("---")
st.caption("Cooper River Deal Finder · built for CTBids / eBay / HiBid / FB Marketplace / Mercari / Chairish / Etsy sourcing")
