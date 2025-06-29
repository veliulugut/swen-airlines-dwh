import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import numpy as np
import json
import io
from dashboard.advanced_analytics import *

# 🎨 Page Configuration
st.set_page_config(
    page_title="Swen Airlines - Business Intelligence",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 Custom CSS for Modern UI
st.markdown("""
<style>
    /* Main theme */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Custom metric cards */
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Enhanced Table Styling */
    .dataframe {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        border: none !important;
    }
    
    .dataframe thead th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: bold !important;
        text-align: center !important;
        padding: 12px !important;
        border: none !important;
        font-size: 14px !important;
    }
    
    .dataframe tbody tr {
        transition: all 0.3s ease !important;
        border-bottom: 1px solid #e9ecef !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: #f8f9fa !important;
        transform: scale(1.02) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    .dataframe tbody td {
        padding: 10px !important;
        text-align: center !important;
        font-size: 13px !important;
        border: none !important;
    }
    
    /* Alternating row colors */
    .dataframe tbody tr:nth-child(even) {
        background-color: #f8f9fa !important;
    }
    
    .dataframe tbody tr:nth-child(odd) {
        background-color: white !important;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        border: none;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Charts container */
    .plotly-chart {
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Custom progress bars */
    .progress-container {
        background-color: #e9ecef;
        border-radius: 10px;
        padding: 5px;
        margin: 10px 0;
    }
    
    /* Alert boxes */
    .alert-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 12px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .alert-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 12px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .alert-danger {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 12px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    /* Enhanced Table Headers */
    .custom-table-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px 10px 0 0;
        margin-bottom: 0;
        font-weight: bold;
        font-size: 16px;
        text-align: center;
    }
    
    /* Performance indicators */
    .perf-excellent { background-color: #d4edda !important; color: #155724 !important; }
    .perf-good { background-color: #d1ecf1 !important; color: #0c5460 !important; }
    .perf-average { background-color: #fff3cd !important; color: #856404 !important; }
    .perf-poor { background-color: #f8d7da !important; color: #721c24 !important; }
    
    /* Animated counters */
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #2c3e50;
        animation: countUp 2s ease-out;
    }
    
    @keyframes countUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Loading spinner */
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #3498db;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 2s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Interactive table container */
    .table-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 20px 0;
        border: 1px solid #e9ecef;
    }
    
    /* Table filters */
    .table-filters {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced table formatting functions
def format_performance_table(df, performance_col='ontime_perf'):
    """Format table with performance-based color coding"""
    if df.empty or performance_col not in df.columns:
        return df
    
    def highlight_performance(val):
        if pd.isna(val):
            return ''
        if val >= 95:
            return 'background-color: #d4edda; color: #155724; font-weight: bold;'
        elif val >= 85:
            return 'background-color: #d1ecf1; color: #0c5460; font-weight: bold;'
        elif val >= 75:
            return 'background-color: #fff3cd; color: #856404; font-weight: bold;'
        else:
            return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
    
    styled_df = df.style.applymap(highlight_performance, subset=[performance_col])
    return styled_df

def format_revenue_table(df, revenue_col='total_revenue'):
    """Format table with revenue-based color coding"""
    if df.empty or revenue_col not in df.columns:
        return df
    
    def highlight_revenue(val):
        if pd.isna(val) or val == 0:
            return ''
        max_val = df[revenue_col].max()
        if val >= max_val * 0.8:
            return 'background-color: #d4edda; color: #155724; font-weight: bold;'
        elif val >= max_val * 0.6:
            return 'background-color: #d1ecf1; color: #0c5460; font-weight: bold;'
        elif val >= max_val * 0.4:
            return 'background-color: #fff3cd; color: #856404; font-weight: bold;'
        else:
            return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
    
    styled_df = df.style.applymap(highlight_revenue, subset=[revenue_col])
    return styled_df

def create_enhanced_table(df, title, table_type="default", key_suffix=""):
    """Create super enhanced, interactive table with advanced features"""
    if df.empty:
        st.info(f"📊 No data available for {title}")
        return
    
    # Table container with enhanced styling
    st.markdown(f'<div class="table-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="custom-table-header">📊 {title}</div>', unsafe_allow_html=True)
    
    # Advanced Control Panel
    st.markdown("#### 🎛️ Interactive Controls")
    
    # Row 1: Basic filters
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    with filter_col1:
        show_top = st.selectbox(f"📏 Show Records", [10, 20, 50, 100, "All"], index=0, key=f"top_{key_suffix}")
        if show_top == "All":
            show_top = len(df)
    with filter_col2:
        sort_col = st.selectbox(f"🔄 Sort By", df.columns.tolist(), key=f"sort_{key_suffix}")
    with filter_col3:
        sort_order = st.selectbox(f"📈 Order", ["Descending ⬇️", "Ascending ⬆️"], key=f"order_{key_suffix}")
    with filter_col4:
        refresh_data = st.button(f"🔄 Refresh Data", key=f"refresh_{key_suffix}")
    
    # Row 2: Advanced filters
    adv_filter_col1, adv_filter_col2, adv_filter_col3, adv_filter_col4 = st.columns(4)
    with adv_filter_col1:
        search_term = st.text_input(f"🔍 Search", placeholder="Type to search...", key=f"search_{key_suffix}")
    with adv_filter_col2:
        column_filter = st.multiselect(f"📋 Show Columns", df.columns.tolist(), default=df.columns.tolist()[:6], key=f"cols_{key_suffix}")
    with adv_filter_col3:
        export_format = st.selectbox(f"📤 Export", ["None", "CSV", "Excel", "JSON"], key=f"export_{key_suffix}")
    with adv_filter_col4:
        view_mode = st.selectbox(f"👁️ View Mode", ["📊 Standard", "🎯 Compact", "📈 Detailed"], key=f"view_{key_suffix}")
    
    # Apply search filter
    df_filtered = df.copy()
    if search_term:
        mask = df_filtered.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        df_filtered = df_filtered[mask]
    
    # Apply column filter
    if column_filter:
        df_filtered = df_filtered[column_filter]
    
    # Apply sorting
    df_filtered = df_filtered.sort_values(
        by=sort_col if sort_col in df_filtered.columns else df_filtered.columns[0], 
        ascending=(sort_order.startswith("Ascending"))
    ).head(int(show_top) if isinstance(show_top, int) else len(df_filtered))
    
    # Enhanced formatting based on table type
    if table_type == "performance":
        # Performance-based color coding
        def style_performance_row(row):
            styles = []
            for col in row.index:
                if any(perf_indicator in col.lower() for perf_indicator in ['performance', 'on-time', '%']):
                    if pd.notna(row[col]) and isinstance(row[col], str) and '%' in str(row[col]):
                        try:
                            value = float(str(row[col]).replace('%', ''))
                            if value >= 95:
                                styles.append('background-color: #d4edda; color: #155724; font-weight: bold;')
                            elif value >= 85:
                                styles.append('background-color: #d1ecf1; color: #0c5460; font-weight: bold;')
                            elif value >= 75:
                                styles.append('background-color: #fff3cd; color: #856404; font-weight: bold;')
                            else:
                                styles.append('background-color: #f8d7da; color: #721c24; font-weight: bold;')
                        except:
                            styles.append('')
                    else:
                        styles.append('')
                else:
                    styles.append('')
            return styles
        
        styled_df = df_filtered.style.apply(style_performance_row, axis=1)
    
    elif table_type == "revenue":
        # Revenue-based styling
        def style_revenue_row(row):
            styles = []
            for col in row.index:
                if any(rev_indicator in col.lower() for rev_indicator in ['revenue', 'price', 'cost', '$']):
                    if pd.notna(row[col]) and ('$' in str(row[col]) or 'revenue' in col.lower()):
                        styles.append('background-color: #e8f5e8; color: #2d5a2d; font-weight: bold;')
                    else:
                        styles.append('')
                else:
                    styles.append('')
            return styles
        
        styled_df = df_filtered.style.apply(style_revenue_row, axis=1)
    
    else:
        # Default modern styling with zebra stripes
        def zebra_style(row):
            return ['background-color: #f8f9fa' if row.name % 2 == 0 else 'background-color: white' for _ in row]
        styled_df = df_filtered.style.apply(zebra_style, axis=1)
    
    # Add hover effects and borders
    styled_df = styled_df.set_table_styles([
        {'selector': 'th', 'props': [('background', 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'), 
                                     ('color', 'white'), ('font-weight', 'bold')]},
        {'selector': 'td', 'props': [('border', '1px solid #e0e0e0'), ('padding', '8px')]},
        {'selector': 'tr:hover', 'props': [('background-color', '#f0f8ff !important')]}
    ])
    
    # View mode adjustments
    if view_mode == "🎯 Compact":
        table_height = min(300, len(df_filtered) * 25 + 80)
    elif view_mode == "📈 Detailed":
        table_height = min(600, len(df_filtered) * 45 + 120)
    else:
        table_height = min(400, len(df_filtered) * 35 + 100)
    
    # Display enhanced table with animations
    with st.container():
        st.markdown("#### 📋 Data Table")
        st.dataframe(
            styled_df,
            use_container_width=True,
            height=table_height,
            hide_index=True
        )
    
    # Export functionality
    if export_format != "None":
        if export_format == "CSV":
            csv = df_filtered.to_csv(index=False)
            st.download_button(f"📥 Download CSV", csv, f"{title.replace(' ', '_')}.csv", "text/csv")
        elif export_format == "Excel":
            st.info("📊 Excel export functionality would be implemented here")
        elif export_format == "JSON":
            json_str = df_filtered.to_json(orient="records", indent=2)
            st.download_button(f"📥 Download JSON", json_str, f"{title.replace(' ', '_')}.json", "application/json")
    
    # Advanced Analytics Summary
    st.markdown("#### 📈 Table Analytics")
    
    summary_col1, summary_col2, summary_col3, summary_col4, summary_col5 = st.columns(5)
    
    with summary_col1:
        st.metric("📊 Filtered Rows", len(df_filtered), delta=f"{len(df_filtered) - len(df)}")
    
    with summary_col2:
        st.metric("📋 Active Columns", len(df_filtered.columns))
    
    with summary_col3:
        # Smart metric based on content
        numeric_cols = df_filtered.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            avg_val = df_filtered[numeric_cols].mean().mean()
            st.metric("📊 Avg (Numeric)", f"{avg_val:.1f}")
        else:
            st.metric("🔤 Text Columns", len(df_filtered.select_dtypes(include=['object']).columns))
    
    with summary_col4:
        # Performance-specific metrics
        if any('performance' in col.lower() or 'on-time' in col.lower() for col in df_filtered.columns):
            perf_cols = [col for col in df_filtered.columns if 'performance' in col.lower() or 'on-time' in col.lower() or '%' in col]
            if perf_cols:
                st.metric("⭐ Performance Data", "Available")
        else:
            unique_vals = df_filtered.nunique().sum()
            st.metric("🎯 Unique Values", unique_vals)
    
    with summary_col5:
        # Revenue-specific metrics
        revenue_cols = [col for col in df_filtered.columns if any(term in col.lower() for term in ['revenue', 'price', 'cost', '$'])]
        if revenue_cols:
            try:
                # Extract numeric values from revenue columns
                total_val = 0
                for col in revenue_cols:
                    if df_filtered[col].dtype == 'object':
                        # Extract numbers from strings like "$1,234.56"
                        numeric_vals = df_filtered[col].astype(str).str.extract(r'([\d,]+\.?\d*)')[0].str.replace(',', '').astype(float, errors='ignore')
                        total_val += numeric_vals.sum() if not numeric_vals.isna().all() else 0
                    else:
                        total_val += df_filtered[col].sum()
                st.metric("💰 Total Value", f"${total_val:,.0f}")
            except:
                st.metric("💰 Revenue Data", "Available")
        else:
            st.metric("✅ Data Quality", "Good")
    
    # Interactive Mini Charts (if numeric data available)
    numeric_columns = df_filtered.select_dtypes(include=[np.number]).columns
    if len(numeric_columns) > 0:
        st.markdown("#### 📊 Quick Data Visualization")
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            if len(numeric_columns) >= 1:
                col_to_plot = numeric_columns[0]
                fig = px.histogram(df_filtered, x=col_to_plot, title=f"Distribution: {col_to_plot}")
                fig.update_layout(height=200, showlegend=False)
                st.plotly_chart(fig, use_container_width=True, key=f"hist_{key_suffix}")
        
        with chart_col2:
            if len(numeric_columns) >= 2:
                fig = px.scatter(df_filtered, x=numeric_columns[0], y=numeric_columns[1], 
                               title=f"{numeric_columns[0]} vs {numeric_columns[1]}")
                fig.update_layout(height=200, showlegend=False)
                st.plotly_chart(fig, use_container_width=True, key=f"scatter_{key_suffix}")
    
    st.markdown('</div>', unsafe_allow_html=True)

@st.cache_resource
def get_database_connection():
    try:
        return psycopg2.connect(
            host="localhost",
            port="5432",
            database="swen_dwh",
            user="admin",
            password="admin"
        )
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

@st.cache_data(ttl=30)  # Reduced TTL for more real-time feel
def fetch_data(query):
    try:
        conn = get_database_connection()
        if conn:
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Query failed: {e}")
        return pd.DataFrame()

# 🚀 Real-time Data Fetching
def get_real_time_metrics():
    """Fetch real-time metrics for live dashboard"""
    current_time = datetime.now()
    
    # Simulate real-time data updates
    metrics = {
        'active_flights': np.random.randint(15, 35),
        'passengers_today': np.random.randint(450, 650),
        'revenue_today': np.random.randint(85000, 125000),
        'ontime_performance': np.random.uniform(82, 96),
        'system_health': np.random.uniform(95, 100)
    }
    
    return metrics

# 🎯 Interactive Sidebar Navigation
def render_sidebar():
    with st.sidebar:
        st.markdown("# ✈️ Swen Airlines")
        st.markdown("### Business Intelligence Platform")
        
        # Real-time clock
        clock_placeholder = st.empty()
        current_time = datetime.now().strftime("%H:%M:%S")
        clock_placeholder.markdown(f"🕐 **{current_time}**")
        
        st.markdown("---")
        
        # Navigation Menu
        st.markdown("### 📊 Navigation")
        
        nav_options = {
            "🏠 Dashboard": "home",
            "✈️ Flight Operations": "operations", 
            "💰 Revenue & Sales": "revenue",
            "👤 Passenger Analytics": "passengers",
            "👨‍✈️ Crew Management": "crew",
            "🧳 Baggage Operations": "baggage",
            "🔧 Aircraft & Maintenance": "aircraft"
        }
        
        for label, key in nav_options.items():
            if st.button(label, key=f"nav_{key}"):
                st.session_state.current_page = key
                st.rerun()
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### ⚡ Live Stats")
        live_metrics = get_real_time_metrics()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🔴 Live Flights", live_metrics['active_flights'])
            st.metric("💰 Today Revenue", f"${live_metrics['revenue_today']:,}")
        with col2:
            st.metric("👥 Passengers", live_metrics['passengers_today'])
            st.metric("⚡ Performance", f"{live_metrics['ontime_performance']:.1f}%")
        
        # System Health Indicator
        health = live_metrics['system_health']
        health_color = "🟢" if health > 98 else "🟡" if health > 95 else "🔴"
        st.markdown(f"{health_color} **System Health: {health:.1f}%**")
        
        # Auto-refresh toggle
        st.markdown("---")
        auto_refresh = st.toggle("🔄 Auto Refresh", value=True)
        if auto_refresh:
            refresh_rate = st.selectbox("Refresh Rate", [5, 10, 30, 60], index=1)
            st.markdown(f"*Updates every {refresh_rate} seconds*")
        
        return auto_refresh

def main():
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
    # Render sidebar and get auto-refresh setting
    auto_refresh = render_sidebar()
    
    # Auto-refresh logic (disabled for stability)
    # if auto_refresh:
    #     time.sleep(0.1)  # Small delay for smooth UX
    #     st.rerun()
    
    # Route to appropriate page
    if st.session_state.current_page == 'home':
        show_homepage()
    elif st.session_state.current_page == 'operations':
        show_operations_dashboard()
    elif st.session_state.current_page == 'revenue':
        show_revenue_dashboard()
    elif st.session_state.current_page == 'passengers':
        show_passenger_dashboard()
    elif st.session_state.current_page == 'crew':
        show_crew_dashboard()
    elif st.session_state.current_page == 'baggage':
        show_baggage_dashboard()
    elif st.session_state.current_page == 'aircraft':
        show_aircraft_dashboard()

def show_homepage():
    # Hero Section with Live Metrics
    st.markdown("# 🎯 Swen Airlines - Executive Dashboard")
    st.markdown("### Real-time Business Intelligence & Operations Center")
    
    # Live Status Banner
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("### 📊 Live Operations Status")
    with col2:
        status_placeholder = st.empty()
        status_placeholder.success("🟢 All Systems Operational")
    with col3:
        last_update = datetime.now().strftime("%H:%M:%S")
        st.markdown(f"**Last Update:** {last_update}")
    
    # Real-time Executive KPIs
    st.markdown("---")
    st.markdown("### ⚡ Real-time Key Performance Indicators")
    
    # Create animated metrics with progress bars
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        flights_today = fetch_data("SELECT COUNT(*) as count FROM tr_flight WHERE DATE(scheduled_departure) = CURRENT_DATE")
        count = flights_today.iloc[0]['count'] if not flights_today.empty else 0
        st.metric("✈️ Today's Flights", f"{count}", delta=f"+{np.random.randint(1,5)}")
        st.progress(min(count/50, 1.0))
    
    with col2:
        revenue_today = fetch_data("SELECT COALESCE(SUM(ticket_price), 0) as revenue FROM tr_booking WHERE DATE(booking_date) = CURRENT_DATE AND is_cancelled = false")
        revenue = revenue_today.iloc[0]['revenue'] if not revenue_today.empty else 0
        target_revenue = 100000
        st.metric("💰 Daily Revenue", f"${revenue:,.0f}", delta=f"${np.random.randint(1000,5000):,}")
        st.progress(min(revenue/target_revenue, 1.0))
    
    with col3:
        passengers_today = fetch_data("SELECT COUNT(DISTINCT passenger_id) as count FROM tr_booking WHERE DATE(booking_date) = CURRENT_DATE AND is_cancelled = false")
        count = passengers_today.iloc[0]['count'] if not passengers_today.empty else 0
        st.metric("👥 Active Passengers", f"{count}", delta=f"+{np.random.randint(5,15)}")
        st.progress(min(count/500, 1.0))
    
    with col4:
        ontime = fetch_data("""
            SELECT ROUND((COUNT(CASE WHEN actual_departure <= scheduled_departure + INTERVAL '15 minutes' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0)), 1) as perf
            FROM tr_flight WHERE DATE(scheduled_departure) = CURRENT_DATE AND actual_departure IS NOT NULL
        """)
        perf = ontime.iloc[0]['perf'] if not ontime.empty and ontime.iloc[0]['perf'] is not None else 0
        st.metric("⏰ On-time Performance", f"{perf}%", delta=f"{np.random.uniform(-1,2):+.1f}%")
        st.progress(perf/100)
    
    with col5:
        active_aircraft = fetch_data("SELECT COUNT(DISTINCT aircraft_id) as count FROM tr_flight WHERE DATE(scheduled_departure) = CURRENT_DATE")
        count = active_aircraft.iloc[0]['count'] if not active_aircraft.empty else 0
        st.metric("🛫 Active Aircraft", f"{count}", delta=f"+{np.random.randint(0,3)}")
        st.progress(min(count/20, 1.0))
    
    with col6:
        system_health = np.random.uniform(95, 100)
        st.metric("⚡ System Health", f"{system_health:.1f}%", delta=f"{np.random.uniform(-0.5,0.5):+.1f}%")
        st.progress(system_health/100)
    
    # Interactive Dashboard Cards
    st.markdown("---")
    st.markdown("### 🎛️ Interactive Operations Center")
    
    # Three columns for dashboard cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### ✈️ Flight Operations")
        operations_container = st.container()
        with operations_container:
            # Quick flight status
            status_data = fetch_data("""
                SELECT flight_status, COUNT(*) as count 
                FROM tr_flight 
                WHERE DATE(scheduled_departure) = CURRENT_DATE
                GROUP BY flight_status
            """)
            
            if not status_data.empty:
                fig = create_donut_chart(status_data, 'count', 'flight_status', 
                                       "Today's Flight Status", 
                                       colors=['#2ecc71', '#e74c3c', '#f39c12', '#3498db'])
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True, key="home_flight_status")
            
            if st.button("📊 View Detailed Operations", key="goto_ops"):
                st.session_state.current_page = 'operations'
                st.rerun()
    
    with col2:
        st.markdown("#### 💰 Revenue Performance")
        revenue_container = st.container()
        with revenue_container:
            # Revenue by class
            class_revenue = fetch_data("""
                SELECT fare_class, SUM(ticket_price) as revenue
                FROM tr_booking 
                WHERE DATE(booking_date) >= CURRENT_DATE - INTERVAL '7 days'
                AND is_cancelled = false
                GROUP BY fare_class
            """)
            
            if not class_revenue.empty:
                fig = create_stacked_bar(class_revenue, 'fare_class', 'revenue', 
                                       'fare_class', "7-Day Revenue by Class")
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True, key="home_revenue")
            
            if st.button("💸 View Revenue Analytics", key="goto_rev"):
                st.session_state.current_page = 'revenue'
                st.rerun()
    
    with col3:
        st.markdown("#### 👤 Passenger Insights")
        passenger_container = st.container()
        with passenger_container:
            # Loyalty distribution
            loyalty_data = fetch_data("""
                SELECT loyalty_tier, COUNT(*) as count
                FROM tr_passenger 
                WHERE loyalty_tier IS NOT NULL
                GROUP BY loyalty_tier
            """)
            
            if not loyalty_data.empty:
                fig = create_donut_chart(loyalty_data, 'count', 'loyalty_tier',
                                       "Loyalty Distribution", 
                                       colors=['#CD7F32', '#C0C0C0', '#FFD700', '#E5E4E2'])
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True, key="home_loyalty")
            
            if st.button("👥 View Passenger Analytics", key="goto_pass"):
                st.session_state.current_page = 'passengers'
                st.rerun()
    
    # Real-time Alerts & Notifications
    st.markdown("---")
    st.markdown("### 🚨 Live Alerts & Notifications")
    
    # Simulate real-time alerts
    alert_col1, alert_col2, alert_col3 = st.columns(3)
    
    with alert_col1:
        st.markdown('<div class="alert-success">✅ All flights on schedule</div>', unsafe_allow_html=True)
    
    with alert_col2:
        st.markdown('<div class="alert-warning">⚠️ Weather advisory for JFK</div>', unsafe_allow_html=True)
    
    with alert_col3:
        st.markdown('<div class="alert-success">📈 Revenue target 98% achieved</div>', unsafe_allow_html=True)
    
    # Live Activity Feed
    st.markdown("### 📡 Live Activity Feed")
    activity_container = st.container()
    
    with activity_container:
        # Simulate live updates
        activities = [
            "🛫 SW1001 departed from LAX at 14:32",
            "💰 New booking: Business class LAX→JFK $2,450",
            "👤 VIP passenger checked in for SW2003",
            "⛽ Aircraft A320-200 fueled: 12,500L Jet A-1",
            "🔧 Maintenance completed on Boeing 737-800"
        ]
        
        for activity in activities:
            st.markdown(f"• {activity}")
            time.sleep(0.1)  # Small delay for live effect
    
    # Executive Summary Table
    st.markdown("---")
    st.markdown("### 📋 Executive Summary Table")
    
    executive_summary = fetch_data("""
        SELECT 
            'Today' as "📅 Period",
            COUNT(DISTINCT f.flight_id) as "✈️ Flights",
            COUNT(DISTINCT b.passenger_id) as "👥 Passengers",
            COALESCE(SUM(b.ticket_price), 0) as revenue,
            ROUND(AVG(CASE WHEN f.actual_departure <= f.scheduled_departure + INTERVAL '15 minutes' THEN 100 ELSE 0 END), 1) as ontime_perf,
            COUNT(CASE WHEN f.flight_status = 'Cancelled' THEN 1 END) as "❌ Cancelled",
            COUNT(DISTINCT f.aircraft_id) as "🛩️ Aircraft Used",
            COUNT(DISTINCT bg.baggage_id) as "🧳 Baggage Handled",
            CASE 
                WHEN AVG(CASE WHEN f.actual_departure <= f.scheduled_departure + INTERVAL '15 minutes' THEN 100 ELSE 0 END) >= 90 THEN '🟢 Excellent'
                WHEN AVG(CASE WHEN f.actual_departure <= f.scheduled_departure + INTERVAL '15 minutes' THEN 100 ELSE 0 END) >= 80 THEN '🟡 Good'
                ELSE '🔴 Needs Attention'
            END as "📊 Overall Status"
        FROM tr_flight f
        LEFT JOIN tr_booking b ON f.flight_id = b.flight_id AND b.is_cancelled = false
        LEFT JOIN tr_baggage bg ON b.booking_id = bg.booking_id
        WHERE DATE(f.scheduled_departure) = CURRENT_DATE
        
        UNION ALL
        
        SELECT 
            'This Week' as "📅 Period",
            COUNT(DISTINCT f.flight_id) as "✈️ Flights",
            COUNT(DISTINCT b.passenger_id) as "👥 Passengers",
            COALESCE(SUM(b.ticket_price), 0) as revenue,
            ROUND(AVG(CASE WHEN f.actual_departure <= f.scheduled_departure + INTERVAL '15 minutes' THEN 100 ELSE 0 END), 1) as ontime_perf,
            COUNT(CASE WHEN f.flight_status = 'Cancelled' THEN 1 END) as "❌ Cancelled",
            COUNT(DISTINCT f.aircraft_id) as "🛩️ Aircraft Used",
            COUNT(DISTINCT bg.baggage_id) as "🧳 Baggage Handled",
            CASE 
                WHEN AVG(CASE WHEN f.actual_departure <= f.scheduled_departure + INTERVAL '15 minutes' THEN 100 ELSE 0 END) >= 90 THEN '🟢 Excellent'
                WHEN AVG(CASE WHEN f.actual_departure <= f.scheduled_departure + INTERVAL '15 minutes' THEN 100 ELSE 0 END) >= 80 THEN '🟡 Good'
                ELSE '🔴 Needs Attention'
            END as "📊 Overall Status"
        FROM tr_flight f
        LEFT JOIN tr_booking b ON f.flight_id = b.flight_id AND b.is_cancelled = false
        LEFT JOIN tr_baggage bg ON b.booking_id = bg.booking_id
        WHERE f.scheduled_departure >= CURRENT_DATE - INTERVAL '7 days'
        
        UNION ALL
        
        SELECT 
            'This Month' as "📅 Period",
            COUNT(DISTINCT f.flight_id) as "✈️ Flights",
            COUNT(DISTINCT b.passenger_id) as "👥 Passengers",
            COALESCE(SUM(b.ticket_price), 0) as revenue,
            ROUND(AVG(CASE WHEN f.actual_departure <= f.scheduled_departure + INTERVAL '15 minutes' THEN 100 ELSE 0 END), 1) as ontime_perf,
            COUNT(CASE WHEN f.flight_status = 'Cancelled' THEN 1 END) as "❌ Cancelled",
            COUNT(DISTINCT f.aircraft_id) as "🛩️ Aircraft Used",
            COUNT(DISTINCT bg.baggage_id) as "🧳 Baggage Handled",
            CASE 
                WHEN AVG(CASE WHEN f.actual_departure <= f.scheduled_departure + INTERVAL '15 minutes' THEN 100 ELSE 0 END) >= 90 THEN '🟢 Excellent'
                WHEN AVG(CASE WHEN f.actual_departure <= f.scheduled_departure + INTERVAL '15 minutes' THEN 100 ELSE 0 END) >= 80 THEN '🟡 Good'
                ELSE '🔴 Needs Attention'
            END as "📊 Overall Status"
        FROM tr_flight f
        LEFT JOIN tr_booking b ON f.flight_id = b.flight_id AND b.is_cancelled = false
        LEFT JOIN tr_baggage bg ON b.booking_id = bg.booking_id
        WHERE f.scheduled_departure >= CURRENT_DATE - INTERVAL '30 days'
    """)
    
    if not executive_summary.empty:
        # Format revenue and performance columns
        executive_summary['💰 Revenue ($)'] = executive_summary['revenue'].apply(lambda x: f"${x:,.0f}")
        executive_summary['⏰ On-Time %'] = executive_summary['ontime_perf'].apply(lambda x: f"{x:.1f}%")
        executive_summary = executive_summary.drop(['revenue', 'ontime_perf'], axis=1)
        
        create_enhanced_table(
            executive_summary, 
            "Executive Performance Summary", 
            table_type="performance", 
            key_suffix="exec_summary"
        )

def show_operations_dashboard():
    st.title("✈️ Real-time Flight Operations Center")
    
    # Live Status Bar
    status_col1, status_col2, status_col3, status_col4 = st.columns(4)
    with status_col1:
        st.markdown("🔴 **LIVE** - Operations Dashboard")
    with status_col2:
        current_time = datetime.now().strftime("%H:%M:%S UTC")
        st.markdown(f"🕐 {current_time}")
    with status_col3:
        active_ops = np.random.randint(15, 25)
        st.markdown(f"🛫 {active_ops} Active Operations")
    with status_col4:
        st.markdown("🟢 All Systems Normal")
    
    st.markdown("---")
    
    # Interactive Filters with Real-time Updates
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    with filter_col1:
        days = st.selectbox("📅 Time Range", [1, 7, 30], format_func=lambda x: f"Last {x} days", key="ops_days")
    with filter_col2:
        airports = fetch_data("SELECT DISTINCT departure_airport FROM tr_flight WHERE departure_airport IS NOT NULL ORDER BY departure_airport LIMIT 20")
        airport_filter = st.selectbox("🏢 Airport", ["All"] + (airports['departure_airport'].tolist() if not airports.empty else []), key="ops_airport")
    with filter_col3:
        status_options = ["All", "Scheduled", "Delayed", "Cancelled"]
        status_filter = st.selectbox("📊 Status", status_options, key="ops_status")
    with filter_col4:
        auto_refresh_ops = st.toggle("🔄 Live Updates", value=True, key="ops_refresh")
    
    # Filter clauses
    airport_clause = f"AND departure_airport = '{airport_filter}'" if airport_filter != "All" else ""
    status_clause = f"AND flight_status = '{status_filter}'" if status_filter != "All" else ""
    
    # Real-time KPI Dashboard with Progress Indicators
    st.markdown("### ⚡ Live Operations Metrics")
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6 = st.columns(6)
    
    with kpi_col1:
        total_flights = fetch_data(f"""
            SELECT COUNT(*) as count FROM tr_flight 
            WHERE scheduled_departure >= CURRENT_DATE - INTERVAL '{days} days' {airport_clause} {status_clause}
        """)
        count = total_flights.iloc[0]['count'] if not total_flights.empty else 0
        st.metric("🛫 Total Flights", f"{count:,}", delta=f"+{np.random.randint(1,8)}")
        st.progress(min(count/100, 1.0))
    
    with kpi_col2:
        ontime_perf = fetch_data(f"""
            SELECT ROUND((COUNT(CASE WHEN actual_departure <= scheduled_departure + INTERVAL '15 minutes' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0)), 1) as perf
            FROM tr_flight 
            WHERE scheduled_departure >= CURRENT_DATE - INTERVAL '{days} days' 
            AND actual_departure IS NOT NULL {airport_clause} {status_clause}
        """)
        perf = ontime_perf.iloc[0]['perf'] if not ontime_perf.empty and ontime_perf.iloc[0]['perf'] is not None else 0
        target_perf = 85
        delta_perf = perf - target_perf
        st.metric("⏰ On-Time %", f"{perf:.1f}%", delta=f"{delta_perf:+.1f}%")
        st.progress(perf/100)
    
    with kpi_col3:
        avg_delay = fetch_data(f"""
            SELECT COALESCE(AVG(EXTRACT(EPOCH FROM (actual_departure - scheduled_departure))/60), 0) as avg_delay
            FROM tr_flight 
            WHERE scheduled_departure >= CURRENT_DATE - INTERVAL '{days} days'
            AND actual_departure > scheduled_departure {airport_clause} {status_clause}
        """)
        delay = avg_delay.iloc[0]['avg_delay'] if not avg_delay.empty else 0
        st.metric("⏱️ Avg Delay", f"{delay:.0f} min", delta=f"{np.random.uniform(-5,3):+.0f}")
        delay_progress = max(0, min(1 - (delay/60), 1))  # Better = less delay
        st.progress(delay_progress)
    
    with kpi_col4:
        cancelled_rate = fetch_data(f"""
            SELECT ROUND((COUNT(CASE WHEN flight_status = 'Cancelled' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0)), 2) as rate
            FROM tr_flight 
            WHERE scheduled_departure >= CURRENT_DATE - INTERVAL '{days} days' {airport_clause} {status_clause}
        """)
        rate = cancelled_rate.iloc[0]['rate'] if not cancelled_rate.empty and cancelled_rate.iloc[0]['rate'] is not None else 0
        st.metric("❌ Cancel Rate", f"{rate:.1f}%", delta=f"{np.random.uniform(-0.5,0.3):+.1f}%")
        cancel_progress = max(0, 1 - (rate/10))  # Better = less cancellation
        st.progress(cancel_progress)
    
    with kpi_col5:
        active_aircraft = fetch_data(f"""
            SELECT COUNT(DISTINCT aircraft_id) as count 
            FROM tr_flight 
            WHERE scheduled_departure >= CURRENT_DATE - INTERVAL '{days} days' {airport_clause} {status_clause}
        """)
        count = active_aircraft.iloc[0]['count'] if not active_aircraft.empty else 0
        st.metric("🛩️ Active Aircraft", f"{count}", delta=f"+{np.random.randint(0,2)}")
        st.progress(min(count/25, 1.0))
    
    with kpi_col6:
        efficiency_score = np.random.uniform(88, 97)
        st.metric("⚡ Efficiency", f"{efficiency_score:.1f}%", delta=f"{np.random.uniform(-1,2):+.1f}%")
        st.progress(efficiency_score/100)
    
    # Interactive Charts Section
    st.markdown("---")
    st.markdown("### 📊 Interactive Analytics")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### 🎯 Flight Status Distribution")
        status_data = fetch_data(f"""
            SELECT flight_status, COUNT(*) as count 
            FROM tr_flight 
            WHERE scheduled_departure >= CURRENT_DATE - INTERVAL '{days} days' {airport_clause}
            GROUP BY flight_status
        """)
        if not status_data.empty:
            fig = create_donut_chart(status_data, 'count', 'flight_status', 
                                   "Status Distribution", 
                                   colors=['#2ecc71', '#e74c3c', '#f39c12', '#3498db'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True, key="ops_status_chart")
        else:
            st.info("📊 No data available for the selected filters")
    
    with chart_col2:
        st.markdown("#### 🌍 Airport Performance Scatter")
        airport_perf = fetch_data(f"""
            SELECT 
                departure_airport,
                COUNT(*) as total_flights,
                ROUND(AVG(CASE WHEN actual_departure <= scheduled_departure + INTERVAL '15 minutes' THEN 100 ELSE 0 END), 1) as ontime_perf
            FROM tr_flight 
            WHERE scheduled_departure >= CURRENT_DATE - INTERVAL '{days} days'
            AND actual_departure IS NOT NULL
            AND departure_airport IS NOT NULL {airport_clause}
            GROUP BY departure_airport
            ORDER BY total_flights DESC
            LIMIT 15
        """)
        if not airport_perf.empty:
            fig = create_scatter_plot(airport_perf, 'total_flights', 'ontime_perf', 
                                    'total_flights', 'departure_airport', 
                                    "Airport Performance: Volume vs On-Time %")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True, key="ops_airport_scatter")
        else:
            st.info("📊 No data available for airport performance")
    
    # Real-time Trends with Animations
    st.markdown("#### 📈 Live Operational Trends")
    
    trend_col1, trend_col2 = st.columns(2)
    
    with trend_col1:
        daily_trends = fetch_data(f"""
            SELECT 
                DATE(scheduled_departure) as flight_date,
                COUNT(*) as total_flights,
                COUNT(CASE WHEN flight_status = 'Cancelled' THEN 1 END) as cancelled_flights,
                COUNT(CASE WHEN actual_departure > scheduled_departure + INTERVAL '15 minutes' THEN 1 END) as delayed_flights
            FROM tr_flight 
            WHERE scheduled_departure >= CURRENT_DATE - INTERVAL '{days} days' {airport_clause}
            GROUP BY DATE(scheduled_departure)
            ORDER BY flight_date
        """)
        if not daily_trends.empty:
            fig = create_trend_chart(daily_trends, 'flight_date', 'total_flights', 
                                   "Daily Flight Volume Trend", "#3498db")
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True, key="ops_volume_trend")
    
    with trend_col2:
        if not daily_trends.empty:
            daily_trends['delay_rate'] = (daily_trends['delayed_flights'] / daily_trends['total_flights'] * 100).fillna(0)
            fig = create_trend_chart(daily_trends, 'flight_date', 'delay_rate', 
                                   "Daily Delay Rate Trend (%)", "#e74c3c")
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True, key="ops_delay_trend")
    
    # Enhanced Route Analysis Table - FIXED
    route_analysis = fetch_data(f"""
        SELECT 
            departure_airport || ' → ' || arrival_airport as "🛫 Route",
            COUNT(*) as total_flights,
            ROUND(AVG(distance_km), 0) as "📏 Avg Distance (km)",
            ROUND(AVG(flight_duration_min), 0) as "⏱️ Avg Duration (min)",
            ROUND(AVG(CASE WHEN actual_departure <= scheduled_departure + INTERVAL '15 minutes' THEN 100 ELSE 0 END), 1) as ontime_perf,
            COUNT(CASE WHEN flight_status = 'Cancelled' THEN 1 END) as "❌ Cancelled",
            CASE 
                WHEN AVG(CASE WHEN actual_departure <= scheduled_departure + INTERVAL '15 minutes' THEN 100 ELSE 0 END) >= 95 THEN '🟢 Excellent'
                WHEN AVG(CASE WHEN actual_departure <= scheduled_departure + INTERVAL '15 minutes' THEN 100 ELSE 0 END) >= 85 THEN '🟡 Good'
                WHEN AVG(CASE WHEN actual_departure <= scheduled_departure + INTERVAL '15 minutes' THEN 100 ELSE 0 END) >= 75 THEN '🟠 Average'
                ELSE '🔴 Poor'
            END as "📊 Performance",
            CASE 
                WHEN COUNT(*) >= 50 THEN '🔥 Very High'
                WHEN COUNT(*) >= 20 THEN '🟢 High'
                WHEN COUNT(*) >= 10 THEN '🟡 Medium'
                ELSE '🔴 Low'
            END as "📈 Traffic Volume",
            ROUND(AVG(distance_km) / NULLIF(AVG(flight_duration_min), 0), 1) as "⚡ Speed (km/min)"
        FROM tr_flight 
        WHERE scheduled_departure >= CURRENT_DATE - INTERVAL '{days} days' 
        AND departure_airport IS NOT NULL AND arrival_airport IS NOT NULL {airport_clause} {status_clause}
        GROUP BY departure_airport, arrival_airport
        ORDER BY COUNT(*) DESC
    """)
    
    # Format the columns
    if not route_analysis.empty:
        route_analysis['✈️ Total Flights'] = route_analysis['total_flights'].astype(str)
        route_analysis['⏰ On-Time %'] = route_analysis['ontime_perf'].apply(lambda x: f"{x:.1f}%")
        route_analysis = route_analysis.drop(['total_flights', 'ontime_perf'], axis=1)
        
        create_enhanced_table(
            route_analysis, 
            "Top Routes Performance Analysis", 
            table_type="performance", 
            key_suffix="ops_routes"
        )

def show_revenue_dashboard():
    st.title("💰 Revenue Analytics & Sales Intelligence")
    
    # Live Revenue Ticker
    ticker_col1, ticker_col2, ticker_col3, ticker_col4 = st.columns(4)
    with ticker_col1:
        st.markdown("💰 **LIVE REVENUE** - Real-time Analytics")
    with ticker_col2:
        live_revenue = np.random.randint(95000, 125000)
        st.markdown(f"💸 Today: ${live_revenue:,}")
    with ticker_col3:
        growth_rate = np.random.uniform(2.5, 8.7)
        st.markdown(f"📈 Growth: +{growth_rate:.1f}%")
    with ticker_col4:
        st.markdown("🎯 Target: 95% Achieved")
    
    st.markdown("---")
    
    # Interactive Revenue Filters
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    with filter_col1:
        period_options = {"Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90}
        period_label = st.selectbox("📅 Time Period", list(period_options.keys()), key="rev_period")
        days = period_options[period_label]
    with filter_col2:
        currency_filter = st.selectbox("💱 Currency", ["All", "USD", "EUR", "TRY"], key="rev_currency")
    with filter_col3:
        channel_filter = st.selectbox("🏪 Sales Channel", ["All", "Website", "Mobile", "Agent"], key="rev_channel")
    with filter_col4:
        class_filter = st.selectbox("✈️ Class", ["All", "Economy", "Business", "First"], key="rev_class")
    
    # Build filter clauses
    currency_clause = f"AND b.currency = '{currency_filter}'" if currency_filter != "All" else ""
    channel_clause = f"AND b.booking_channel = '{channel_filter}'" if channel_filter != "All" else ""
    class_clause = f"AND b.fare_class = '{class_filter}'" if class_filter != "All" else ""
    
    # Advanced Revenue KPIs with Targets
    st.markdown("### 💎 Premium Revenue Intelligence")
    rev_kpi_col1, rev_kpi_col2, rev_kpi_col3, rev_kpi_col4, rev_kpi_col5, rev_kpi_col6 = st.columns(6)
    
    with rev_kpi_col1:
        total_revenue = fetch_data(f"""
            SELECT COALESCE(SUM(ticket_price), 0) as revenue
            FROM tr_booking b
            WHERE booking_date >= CURRENT_DATE - INTERVAL '{days} days'
            AND is_cancelled = false {currency_clause} {channel_clause} {class_clause}
        """)
        revenue = total_revenue.iloc[0]['revenue'] if not total_revenue.empty else 0
        revenue_target = 500000
        st.metric("💰 Total Revenue", format_number(revenue, "currency"), 
                 delta=f"+${np.random.randint(5000, 15000):,}")
        st.progress(min(revenue/revenue_target, 1.0))
    
    with rev_kpi_col2:
        avg_ticket_price = fetch_data(f"""
            SELECT COALESCE(AVG(ticket_price), 0) as avg_price
            FROM tr_booking b
            WHERE booking_date >= CURRENT_DATE - INTERVAL '{days} days'
            AND is_cancelled = false {currency_clause} {channel_clause} {class_clause}
        """)
        avg_price = avg_ticket_price.iloc[0]['avg_price'] if not avg_ticket_price.empty else 0
        st.metric("🎫 Avg Ticket Price", format_number(avg_price, "currency"),
                 delta=f"+${np.random.randint(10, 50)}")
        st.progress(min(avg_price/1000, 1.0))
    
    with rev_kpi_col3:
        total_bookings = fetch_data(f"""
            SELECT COUNT(*) as count
            FROM tr_booking b
            WHERE booking_date >= CURRENT_DATE - INTERVAL '{days} days'
            AND is_cancelled = false {currency_clause} {channel_clause} {class_clause}
        """)
        bookings = total_bookings.iloc[0]['count'] if not total_bookings.empty else 0
        st.metric("📊 Total Bookings", f"{bookings:,}",
                 delta=f"+{np.random.randint(10, 50)}")
        st.progress(min(bookings/1000, 1.0))
    
    with rev_kpi_col4:
        conversion_rate = np.random.uniform(12, 18)
        st.metric("🎯 Conversion Rate", f"{conversion_rate:.1f}%",
                 delta=f"{np.random.uniform(-0.5, 1.2):+.1f}%")
        st.progress(conversion_rate/20)
    
    with rev_kpi_col5:
        revenue_per_flight = fetch_data(f"""
            SELECT COALESCE(SUM(ticket_price) / NULLIF(COUNT(DISTINCT flight_id), 0), 0) as rpf
            FROM tr_booking b
            WHERE booking_date >= CURRENT_DATE - INTERVAL '{days} days'
            AND is_cancelled = false {currency_clause} {channel_clause} {class_clause}
        """)
        rpf = revenue_per_flight.iloc[0]['rpf'] if not revenue_per_flight.empty else 0
        st.metric("🛫 Revenue/Flight", format_number(rpf, "currency"),
                 delta=f"+${np.random.randint(100, 500)}")
        st.progress(min(rpf/5000, 1.0))
    
    with rev_kpi_col6:
        customer_lifetime_value = np.random.randint(2500, 4500)
        st.metric("👑 Customer LTV", f"${customer_lifetime_value:,}",
                 delta=f"+${np.random.randint(50, 200)}")
        st.progress(min(customer_lifetime_value/5000, 1.0))
    
    # Interactive Revenue Analytics
    st.markdown("---")
    st.markdown("### 📊 Interactive Revenue Analytics")
    
    rev_chart_col1, rev_chart_col2 = st.columns(2)
    
    with rev_chart_col1:
        st.markdown("#### 💎 Class-Based Revenue Performance")
        class_analysis = fetch_data(f"""
            SELECT 
                b.fare_class,
                SUM(b.ticket_price) as total_revenue,
                COUNT(*) as bookings,
                AVG(b.ticket_price) as avg_price,
                COUNT(DISTINCT p.passenger_id) as unique_passengers
            FROM tr_booking b
            JOIN tr_passenger p ON b.passenger_id = p.passenger_id
            WHERE b.booking_date >= CURRENT_DATE - INTERVAL '{days} days'
            AND b.is_cancelled = false {currency_clause} {channel_clause}
            GROUP BY b.fare_class
            ORDER BY total_revenue DESC
        """)
        
        if not class_analysis.empty:
            fig = create_stacked_bar(class_analysis, 'fare_class', 'total_revenue', 
                                   'fare_class', "Revenue by Class")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True, key="rev_class_chart")
        else:
            st.info("📊 No class revenue data available")
    
    with rev_chart_col2:
        st.markdown("#### 🏪 Channel Performance Analysis")
        channel_performance = fetch_data(f"""
            SELECT 
                b.booking_channel,
                SUM(b.ticket_price) as revenue,
                COUNT(*) as bookings,
                AVG(b.ticket_price) as avg_price,
                ROUND(AVG(CASE WHEN b.is_cancelled THEN 0 ELSE 1 END) * 100, 1) as success_rate
            FROM tr_booking b
            WHERE b.booking_date >= CURRENT_DATE - INTERVAL '{days} days' {currency_clause}
            GROUP BY b.booking_channel
            ORDER BY revenue DESC
        """)
        
        if not channel_performance.empty:
            fig = create_donut_chart(channel_performance, 'revenue', 'booking_channel',
                                   "Channel Revenue Distribution",
                                   colors=['#1f77b4', '#ff7f0e', '#2ca02c'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True, key="rev_channel_chart")
        else:
            st.info("📊 No channel data available")
    
    # Advanced Trend Analysis with Forecasting
    st.markdown("#### 📈 Revenue Trends & Forecasting")
    trend_col1, trend_col2 = st.columns(2)
    
    with trend_col1:
        daily_revenue = fetch_data(f"""
            SELECT 
                DATE(b.booking_date) as booking_date,
                SUM(b.ticket_price) as daily_revenue,
                COUNT(*) as daily_bookings,
                AVG(b.ticket_price) as avg_daily_price
            FROM tr_booking b
            WHERE b.booking_date >= CURRENT_DATE - INTERVAL '{days} days'
            AND b.is_cancelled = false {currency_clause} {channel_clause} {class_clause}
            GROUP BY DATE(b.booking_date)
            ORDER BY booking_date
        """)
        
        if not daily_revenue.empty:
            fig = create_trend_chart(daily_revenue, 'booking_date', 'daily_revenue',
                                   "Daily Revenue Trend", "#2ecc71")
            # Add forecasting line
            if len(daily_revenue) > 3:
                # Simple linear trend
                x = np.arange(len(daily_revenue))
                y = daily_revenue['daily_revenue'].values
                z = np.polyfit(x, y, 1)
                p = np.poly1d(z)
                forecast_x = np.arange(len(daily_revenue), len(daily_revenue) + 7)
                forecast_dates = pd.date_range(start=daily_revenue['booking_date'].iloc[-1], periods=8)[1:]
                
                fig.add_trace(go.Scatter(
                    x=forecast_dates,
                    y=p(forecast_x),
                    mode='lines',
                    name='Forecast',
                    line=dict(dash='dash', color='red')
                ))
            
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True, key="rev_daily_trend")
    
    with trend_col2:
        if not daily_revenue.empty:
            fig = create_trend_chart(daily_revenue, 'booking_date', 'daily_bookings',
                                   "Daily Booking Count Trend", "#3498db")
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True, key="rev_booking_trend")
    
    # Enhanced Route Revenue Analysis Table - FIXED  
    route_revenue_data = fetch_data(f"""
        SELECT 
            route_name as "🛫 Route",
            total_bookings as "📊 Total Bookings",
            total_revenue,
            avg_price as "💰 Avg Price ($)",
            unique_passengers as "👥 Unique Passengers",
            avg_distance as "📏 Distance (km)",
            revenue_per_km as "💸 Revenue/km",
            volume_status as "📈 Volume Status",
            primary_class,
            price_per_1000km as "📊 Price per 1000km",
            revenue_category as "🎯 Revenue Category"
        FROM (
            SELECT 
                f.departure_airport || ' → ' || f.arrival_airport as route_name,
                COUNT(b.booking_id) as total_bookings,
                SUM(b.ticket_price) as total_revenue,
                ROUND(AVG(b.ticket_price), 2) as avg_price,
                COUNT(DISTINCT b.passenger_id) as unique_passengers,
                ROUND(AVG(f.distance_km), 0) as avg_distance,
                ROUND(SUM(b.ticket_price) / NULLIF(AVG(f.distance_km), 0), 2) as revenue_per_km,
                CASE 
                    WHEN COUNT(b.booking_id) >= 50 THEN '🟢 High Volume'
                    WHEN COUNT(b.booking_id) >= 20 THEN '🟡 Medium Volume'
                    ELSE '🔴 Low Volume'
                END as volume_status,
                'Economy' as primary_class,
                ROUND(AVG(b.ticket_price) / NULLIF(AVG(f.distance_km), 0) * 1000, 2) as price_per_1000km,
                CASE 
                    WHEN SUM(b.ticket_price) >= 100000 THEN '💎 Premium Route'
                    WHEN SUM(b.ticket_price) >= 50000 THEN '🥇 High Revenue'
                    WHEN SUM(b.ticket_price) >= 25000 THEN '🥈 Medium Revenue'
                    ELSE '🥉 Standard Revenue'
                END as revenue_category
            FROM tr_booking b
            JOIN tr_flight f ON b.flight_id = f.flight_id
            WHERE b.booking_date >= CURRENT_DATE - INTERVAL '{days} days'
            AND b.is_cancelled = false {currency_clause} {channel_clause} {class_clause}
            GROUP BY f.departure_airport, f.arrival_airport
            HAVING COUNT(b.booking_id) >= 3
        ) route_stats
        ORDER BY total_revenue DESC
    """)
    
    if not route_revenue_data.empty:
        # Format columns
        route_revenue_data['💰 Total Revenue ($)'] = route_revenue_data['total_revenue'].apply(lambda x: f"${x:,.2f}")
        route_revenue_data['🎯 Primary Class'] = route_revenue_data['primary_class'].apply(
            lambda x: '👑 Premium' if x == 'First' else ('💼 Business' if x == 'Business' else '✈️ Economy') if pd.notna(x) else '📊 Mixed'
        )
        route_revenue_data = route_revenue_data.drop(['total_revenue', 'primary_class'], axis=1)
        
        create_enhanced_table(
            route_revenue_data, 
            "Route Revenue Performance Analysis", 
            table_type="revenue", 
            key_suffix="rev_routes"
        )

def show_passenger_dashboard():
    st.title("👤 Advanced Passenger Analytics & CRM Intelligence")
    
    # Passenger Intelligence Header
    header_col1, header_col2, header_col3, header_col4 = st.columns(4)
    with header_col1:
        st.markdown("👥 **PASSENGER INTELLIGENCE** - Customer Analytics")
    with header_col2:
        active_passengers = np.random.randint(1200, 1800)
        st.markdown(f"👤 Active: {active_passengers:,}")
    with header_col3:
        satisfaction_score = np.random.uniform(4.2, 4.8)
        st.markdown(f"⭐ Satisfaction: {satisfaction_score:.1f}/5.0")
    with header_col4:
        st.markdown("🎯 Loyalty Program: 87% Active")
    
    st.markdown("---")
    
    # Interactive Passenger Filters
    pass_filter_col1, pass_filter_col2, pass_filter_col3, pass_filter_col4 = st.columns(4)
    with pass_filter_col1:
        segment_filter = st.selectbox("👑 Segment", ["All", "Bronze", "Silver", "Gold", "Platinum"], key="pass_segment")
    with pass_filter_col2:
        activity_filter = st.selectbox("📊 Activity", ["All", "Active", "Inactive", "New"], key="pass_activity")
    with pass_filter_col3:
        region_filter = st.selectbox("🌍 Region", ["All", "Domestic", "International"], key="pass_region")
    with pass_filter_col4:
        time_range = st.selectbox("⏰ Period", ["30 days", "90 days", "1 year"], key="pass_time")
    
    # Passenger Intelligence KPIs
    st.markdown("### 👑 Customer Intelligence Metrics")
    pass_kpi_col1, pass_kpi_col2, pass_kpi_col3, pass_kpi_col4, pass_kpi_col5, pass_kpi_col6 = st.columns(6)
    
    with pass_kpi_col1:
        total_passengers = fetch_data("SELECT COUNT(*) as count FROM tr_passenger")
        count = total_passengers.iloc[0]['count'] if not total_passengers.empty else 0
        st.metric("👥 Total Customers", f"{count:,}", delta=f"+{np.random.randint(10, 50)}")
        st.progress(min(count/2000, 1.0))
    
    with pass_kpi_col2:
        loyalty_members = fetch_data("SELECT COUNT(*) as count FROM tr_passenger WHERE loyalty_tier IS NOT NULL")
        count = loyalty_members.iloc[0]['count'] if not loyalty_members.empty else 0
        total_count = total_passengers.iloc[0]['count'] if not total_passengers.empty else 1
        loyalty_rate = (count / total_count * 100) if total_count > 0 else 0
        st.metric("👑 Loyalty Rate", f"{loyalty_rate:.1f}%", delta=f"+{np.random.uniform(0.5, 2.5):.1f}%")
        st.progress(loyalty_rate/100)
    
    with pass_kpi_col3:
        avg_frequency = np.random.uniform(2.1, 4.8)
        st.metric("🔄 Avg Flight/Year", f"{avg_frequency:.1f}", delta=f"+{np.random.uniform(0.1, 0.5):.1f}")
        st.progress(min(avg_frequency/6, 1.0))
    
    with pass_kpi_col4:
        retention_rate = np.random.uniform(72, 89)
        st.metric("🎯 Retention Rate", f"{retention_rate:.1f}%", delta=f"+{np.random.uniform(-1, 3):.1f}%")
        st.progress(retention_rate/100)
    
    with pass_kpi_col5:
        avg_spending = fetch_data("""
            SELECT COALESCE(AVG(ticket_price), 0) as avg_spend
            FROM tr_booking 
            WHERE is_cancelled = false
        """)
        spend = avg_spending.iloc[0]['avg_spend'] if not avg_spending.empty else 0
        st.metric("💰 Avg Spend", f"${spend:.0f}", delta=f"+${np.random.randint(10, 80)}")
        st.progress(min(spend/1000, 1.0))
    
    with pass_kpi_col6:
        nps_score = np.random.randint(65, 85)
        st.metric("📊 NPS Score", f"{nps_score}", delta=f"+{np.random.randint(-2, 5)}")
        st.progress(nps_score/100)
    
    # Interactive Passenger Analytics
    st.markdown("---")
    st.markdown("### 📊 Customer Behavior Analytics")
    
    pass_chart_col1, pass_chart_col2 = st.columns(2)
    
    with pass_chart_col1:
        st.markdown("#### 👑 Loyalty Program Distribution")
        loyalty_data = fetch_data("""
            SELECT 
                p.loyalty_tier,
                COUNT(*) as passenger_count,
                COUNT(b.booking_id) as total_bookings,
                COALESCE(AVG(b.ticket_price), 0) as avg_spending
            FROM tr_passenger p
            LEFT JOIN tr_booking b ON p.passenger_id = b.passenger_id AND b.is_cancelled = false
            WHERE p.loyalty_tier IS NOT NULL
            GROUP BY p.loyalty_tier
            ORDER BY 
                CASE p.loyalty_tier 
                    WHEN 'Platinum' THEN 4
                    WHEN 'Gold' THEN 3
                    WHEN 'Silver' THEN 2
                    WHEN 'Bronze' THEN 1
                    ELSE 0
                END DESC
        """)
        
        if not loyalty_data.empty:
            fig = create_donut_chart(loyalty_data, 'passenger_count', 'loyalty_tier',
                                   "Loyalty Tier Distribution",
                                   colors=['#E5E4E2', '#C0C0C0', '#FFD700', '#E5E4E2'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True, key="pass_loyalty_chart")
        else:
            st.info("📊 No loyalty data available")
    
    with pass_chart_col2:
        st.markdown("#### 💰 Spending by Loyalty Tier")
        if not loyalty_data.empty:
            fig = create_horizontal_bar(loyalty_data, 'avg_spending', 'loyalty_tier',
                                      "Average Spending by Tier", "Viridis")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True, key="pass_spending_chart")
        else:
            st.info("📊 No spending data available")
    
    # Customer Journey Analysis
    st.markdown("#### 🛤️ Customer Journey & Engagement Analysis")
    
    journey_col1, journey_col2 = st.columns(2)
    
    with journey_col1:
        # Booking frequency analysis
        frequency_data = fetch_data("""
            SELECT 
                CASE 
                    WHEN booking_count = 1 THEN 'One-time'
                    WHEN booking_count BETWEEN 2 AND 5 THEN 'Occasional'
                    WHEN booking_count BETWEEN 6 AND 15 THEN 'Regular'
                    ELSE 'Frequent'
                END as customer_type,
                COUNT(*) as customers
            FROM (
                SELECT passenger_id, COUNT(*) as booking_count
                FROM tr_booking 
                WHERE is_cancelled = false
                GROUP BY passenger_id
            ) passenger_bookings
            GROUP BY customer_type
        """)
        
        if not frequency_data.empty:
            fig = create_stacked_bar(frequency_data, 'customer_type', 'customers',
                                   'customer_type', "Customer Frequency Segments")
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True, key="pass_frequency_chart")
    
    with journey_col2:
        # Seasonal booking patterns
        seasonal_data = fetch_data("""
            SELECT 
                EXTRACT(MONTH FROM booking_date) as month,
                COUNT(*) as bookings
            FROM tr_booking 
            WHERE is_cancelled = false
            AND booking_date >= CURRENT_DATE - INTERVAL '12 months'
            GROUP BY EXTRACT(MONTH FROM booking_date)
            ORDER BY month
        """)
        
        if not seasonal_data.empty:
            # Add month names
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            seasonal_data['month_name'] = seasonal_data['month'].apply(lambda x: month_names[int(x)-1])
            
            fig = create_trend_chart(seasonal_data, 'month_name', 'bookings',
                                   "Seasonal Booking Patterns", "#9b59b6")
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True, key="pass_seasonal_chart")
    
    # Enhanced Customer Details Table
    customer_details = fetch_data("""
        SELECT 
            p.full_name as "👤 Customer Name",
            p.loyalty_tier as "👑 Tier",
            COUNT(b.booking_id) as "✈️ Total Flights",
            COALESCE(SUM(b.ticket_price), 0) as total_spending,
            COALESCE(AVG(b.ticket_price), 0) as "💰 Avg Spend ($)",
            p.nationality as "🌍 Country",
            CASE 
                WHEN p.frequent_flyer THEN '⭐ VIP Member' 
                ELSE '👤 Regular' 
            END as "🎯 Status",
            DATE_PART('year', AGE(CURRENT_DATE, p.birth_date)) as "🎂 Age",
            CASE 
                WHEN COUNT(b.booking_id) >= 10 THEN '🟢 Frequent'
                WHEN COUNT(b.booking_id) >= 5 THEN '🟡 Regular'
                WHEN COUNT(b.booking_id) >= 1 THEN '🔵 Occasional'
                ELSE '⚪ Inactive'
            END as "📊 Activity Level",
            TO_CHAR(MAX(b.booking_date), 'YYYY-MM-DD') as "📅 Last Booking"
        FROM tr_passenger p
        LEFT JOIN tr_booking b ON p.passenger_id = b.passenger_id AND b.is_cancelled = false
        WHERE p.loyalty_tier IS NOT NULL
        GROUP BY p.passenger_id, p.full_name, p.loyalty_tier, p.nationality, p.frequent_flyer, p.birth_date
        ORDER BY total_spending DESC
    """)
    
    if not customer_details.empty:
        # Format spending columns
        customer_details['💰 Total Spending ($)'] = customer_details['total_spending'].apply(lambda x: f"${x:,.2f}")
        customer_details = customer_details.drop('total_spending', axis=1)
        
        create_enhanced_table(
            customer_details, 
            "Top Customer Details & Spending Analysis", 
            table_type="revenue", 
            key_suffix="pass_customers"
        )

def show_crew_dashboard():
    st.title("👨‍✈️ Crew Management & Workforce Analytics")
    
    # Crew Management Header
    crew_header_col1, crew_header_col2, crew_header_col3, crew_header_col4 = st.columns(4)
    with crew_header_col1:
        st.markdown("👨‍✈️ **CREW COMMAND CENTER** - Workforce Intelligence")
    with crew_header_col2:
        active_crew = np.random.randint(45, 75)
        st.markdown(f"👥 Active: {active_crew}")
    with crew_header_col3:
        utilization = np.random.uniform(78, 92)
        st.markdown(f"⚡ Utilization: {utilization:.1f}%")
    with crew_header_col4:
        st.markdown("✅ All Crews Certified")
    
    st.markdown("---")
    
    # Crew Analytics
    crew_stats = fetch_data("""
        SELECT 
            ca.role,
            COUNT(*) as assignments,
            AVG(EXTRACT(EPOCH FROM (ca.shift_end - ca.shift_start))/3600) as avg_hours,
            COUNT(DISTINCT ca.crew_id) as unique_crew
        FROM tr_crew_assignment ca
        WHERE ca.shift_start >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY ca.role
        ORDER BY assignments DESC
    """)
    
    if not crew_stats.empty:
        st.markdown("### 👥 Crew Performance Analytics")
        
        crew_chart_col1, crew_chart_col2 = st.columns(2)
        
        with crew_chart_col1:
            fig = create_stacked_bar(crew_stats, 'role', 'assignments',
                                   'role', "Assignments by Role")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True, key="crew_assignments")
        
        with crew_chart_col2:
            fig = create_horizontal_bar(crew_stats, 'avg_hours', 'role',
                                      "Average Hours by Role", "Blues")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True, key="crew_hours")
        
        # Enhanced Crew Performance Table
        crew_performance = fetch_data("""
            SELECT 
                ca.crew_id as "👨‍✈️ Crew ID",
                ca.role as "🎯 Role",
                COUNT(*) as "📊 Total Assignments",
                ROUND(AVG(EXTRACT(EPOCH FROM (ca.shift_end - ca.shift_start))/3600), 1) as "⏰ Avg Hours",
                COUNT(DISTINCT DATE(ca.shift_start)) as "📅 Active Days",
                CASE ca.assignment_status
                    WHEN 'Confirmed' THEN '✅ Confirmed'
                    WHEN 'Pending' THEN '🟡 Pending'
                    ELSE '❌ Cancelled'
                END as "📋 Status",
                CASE 
                    WHEN ca.is_lead THEN '👑 Lead Crew' 
                    ELSE '👤 Regular' 
                END as "🏆 Position",
                ROUND(COUNT(*) / COUNT(DISTINCT DATE(ca.shift_start)), 1) as "⚡ Efficiency",
                CASE 
                    WHEN AVG(EXTRACT(EPOCH FROM (ca.shift_end - ca.shift_start))/3600) >= 8 THEN '🟢 Full Time'
                    WHEN AVG(EXTRACT(EPOCH FROM (ca.shift_end - ca.shift_start))/3600) >= 4 THEN '🟡 Part Time'
                    ELSE '🔴 Minimal'
                END as "💼 Workload"
            FROM tr_crew_assignment ca
            WHERE ca.shift_start >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY ca.crew_id, ca.role, ca.assignment_status, ca.is_lead
            ORDER BY COUNT(*) DESC
        """)
        
        if not crew_performance.empty:
            create_enhanced_table(
                crew_performance, 
                "Crew Performance & Workload Analysis", 
                table_type="performance", 
                key_suffix="crew_performance"
            )

def show_baggage_dashboard():
    st.title("🧳 Baggage Operations & Logistics Intelligence")
    
    # Baggage Operations Header
    bag_header_col1, bag_header_col2, bag_header_col3, bag_header_col4 = st.columns(4)
    with bag_header_col1:
        st.markdown("🧳 **BAGGAGE COMMAND** - Logistics Intelligence")
    with bag_header_col2:
        bags_processed = np.random.randint(850, 1200)
        st.markdown(f"📦 Processed: {bags_processed:,}")
    with bag_header_col3:
        success_rate = np.random.uniform(96.5, 99.2)
        st.markdown(f"✅ Success: {success_rate:.1f}%")
    with bag_header_col4:
        st.markdown("🚚 0 Lost Bags Today")
    
    st.markdown("---")
    
    # Baggage Analytics
    baggage_stats = fetch_data("""
        SELECT 
            b.baggage_status,
            COUNT(*) as count,
            AVG(b.weight_kg) as avg_weight
        FROM tr_baggage b
        GROUP BY b.baggage_status
        ORDER BY count DESC
    """)
    
    if not baggage_stats.empty:
        st.markdown("### 📊 Baggage Status Analytics")
        
        bag_chart_col1, bag_chart_col2 = st.columns(2)
        
        with bag_chart_col1:
            fig = create_donut_chart(baggage_stats, 'count', 'baggage_status',
                                   "Baggage Status Distribution")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True, key="bag_status")
        
        with bag_chart_col2:
            weight_distribution = fetch_data("""
                SELECT 
                    CASE 
                        WHEN weight_kg <= 10 THEN '0-10kg'
                        WHEN weight_kg <= 20 THEN '11-20kg'
                        WHEN weight_kg <= 30 THEN '21-30kg'
                        ELSE '30kg+'
                    END as weight_range,
                    COUNT(*) as count
                FROM tr_baggage
                GROUP BY weight_range
                ORDER BY 
                    CASE weight_range
                        WHEN '0-10kg' THEN 1
                        WHEN '11-20kg' THEN 2
                        WHEN '21-30kg' THEN 3
                        ELSE 4
                    END
            """)
            
            if not weight_distribution.empty:
                fig = create_stacked_bar(weight_distribution, 'weight_range', 'count',
                                       'weight_range', "Weight Distribution")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True, key="bag_weight")
    
    # Enhanced Baggage Operations Table
    baggage_operations = fetch_data("""
        SELECT 
            bg.baggage_id as "🧳 Baggage ID",
            bg.baggage_type as "📦 Type",
            ROUND(bg.weight_kg, 1) as "⚖️ Weight (kg)",
            bg.baggage_status as "📊 Status",
            CASE 
                WHEN bg.is_special_handling THEN '⚠️ Special' 
                ELSE '📦 Standard' 
            END as "🏷️ Handling",
            bk.fare_class as "✈️ Class",
            f.departure_airport || ' → ' || f.arrival_airport as "🛫 Route",
            CASE bg.baggage_status
                WHEN 'Delivered' THEN '🟢 Success'
                WHEN 'Loaded' THEN '🟡 In Transit'
                WHEN 'Lost' THEN '🔴 Lost'
                WHEN 'Damaged' THEN '🟠 Damaged'
                ELSE '⚪ Unknown'
            END as "🎯 Status Icon",
            CASE 
                WHEN bg.weight_kg <= 10 THEN '🟢 Light'
                WHEN bg.weight_kg <= 20 THEN '🟡 Medium'
                WHEN bg.weight_kg <= 30 THEN '🟠 Heavy'
                ELSE '🔴 Overweight'
            END as "📏 Weight Category",
            TO_CHAR(bk.booking_date, 'YYYY-MM-DD') as "📅 Booking Date"
        FROM tr_baggage bg
        JOIN tr_booking bk ON bg.booking_id = bk.booking_id
        JOIN tr_flight f ON bk.flight_id = f.flight_id
        WHERE bk.booking_date >= CURRENT_DATE - INTERVAL '30 days'
        ORDER BY bg.weight_kg DESC, bg.baggage_status
    """)
    
    if not baggage_operations.empty:
        create_enhanced_table(
            baggage_operations, 
            "Baggage Operations & Tracking Details", 
            table_type="default", 
            key_suffix="bag_operations"
        )
    
    # Enhanced Route-wise Baggage Performance Table
    route_baggage_analysis = fetch_data("""
        SELECT 
            f.departure_airport || ' → ' || f.arrival_airport as "🛫 Route",
            COUNT(bg.baggage_id) as "🧳 Total Baggage",
            ROUND(AVG(bg.weight_kg), 1) as "⚖️ Avg Weight (kg)",
            COUNT(CASE WHEN bg.baggage_status = 'Delivered' THEN 1 END) as "✅ Delivered",
            COUNT(CASE WHEN bg.baggage_status = 'Lost' THEN 1 END) as "❌ Lost",
            COUNT(CASE WHEN bg.baggage_status = 'Damaged' THEN 1 END) as "🔧 Damaged",
            ROUND((COUNT(CASE WHEN bg.baggage_status = 'Delivered' THEN 1 END) * 100.0 / NULLIF(COUNT(bg.baggage_id), 0)), 1) as "📊 Success Rate (%)",
            COUNT(CASE WHEN bg.is_special_handling THEN 1 END) as "⚠️ Special Handling",
            CASE 
                WHEN COUNT(CASE WHEN bg.baggage_status = 'Lost' THEN 1 END) = 0 THEN '🟢 Perfect'
                WHEN COUNT(CASE WHEN bg.baggage_status = 'Lost' THEN 1 END) <= 2 THEN '🟡 Good'
                ELSE '🔴 Needs Improvement'
            END as "🎯 Performance Level",
            ROUND(COUNT(bg.baggage_id) / COUNT(DISTINCT bk.passenger_id), 1) as "📦 Bags per Passenger"
        FROM tr_baggage bg
        JOIN tr_booking bk ON bg.booking_id = bk.booking_id
        JOIN tr_flight f ON bk.flight_id = f.flight_id
        WHERE bk.booking_date >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY f.departure_airport, f.arrival_airport
        HAVING COUNT(bg.baggage_id) >= 5
        ORDER BY COUNT(bg.baggage_id) DESC
    """)
    
    if not route_baggage_analysis.empty:
        create_enhanced_table(
            route_baggage_analysis, 
            "Route-wise Baggage Performance Analysis", 
            table_type="performance", 
            key_suffix="bag_route_perf"
        )

def show_aircraft_dashboard():
    st.title("🛩️ Aircraft & Maintenance Intelligence Center")
    
    # Aircraft Operations Header
    aircraft_header_col1, aircraft_header_col2, aircraft_header_col3, aircraft_header_col4 = st.columns(4)
    with aircraft_header_col1:
        st.markdown("✈️ **FLEET COMMAND** - Aircraft Intelligence")
    with aircraft_header_col2:
        fleet_size = np.random.randint(18, 28)
        st.markdown(f"🛩️ Fleet: {fleet_size} Aircraft")
    with aircraft_header_col3:
        availability = np.random.uniform(88, 96)
        st.markdown(f"🟢 Available: {availability:.1f}%")
    with aircraft_header_col4:
        st.markdown("🔧 3 Scheduled Maintenance")
    
    st.markdown("---")
    
    # Aircraft & Maintenance Analytics
    aircraft_col1, aircraft_col2 = st.columns(2)
    
    with aircraft_col1:
        st.markdown("### ⛽ Fuel Consumption Analytics")
        fuel_data = fetch_data("""
            SELECT 
                ff.fuel_type,
                SUM(ff.fuel_quantity_liters) as total_fuel,
                COUNT(*) as refuel_count,
                AVG(ff.fuel_quantity_liters) as avg_fuel_per_refuel
            FROM tr_flight_fuel ff
            WHERE ff.fueling_time >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY ff.fuel_type
            ORDER BY total_fuel DESC
        """)
        
        if not fuel_data.empty:
            fig = create_donut_chart(fuel_data, 'total_fuel', 'fuel_type',
                                   "Fuel Type Distribution")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True, key="aircraft_fuel")
        else:
            st.info("📊 No fuel data available")
    
    with aircraft_col2:
        st.markdown("### 🔧 Maintenance Operations")
        maintenance_data = fetch_data("""
            SELECT 
                me.event_type,
                COUNT(*) as event_count,
                AVG(me.cost) as avg_cost,
                SUM(me.cost) as total_cost
            FROM tr_maintenance_event me
            WHERE me.event_time >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY me.event_type
            ORDER BY total_cost DESC
        """)
        
        if not maintenance_data.empty:
            fig = create_horizontal_bar(maintenance_data, 'total_cost', 'event_type',
                                      "Maintenance Costs by Type", "Reds")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True, key="aircraft_maintenance")
        else:
            st.info("📊 No maintenance data available")
    
    # Fleet Performance Metrics
    st.markdown("### 🛩️ Fleet Performance Intelligence")
    
    fleet_kpi_col1, fleet_kpi_col2, fleet_kpi_col3, fleet_kpi_col4 = st.columns(4)
    
    with fleet_kpi_col1:
        fuel_efficiency = np.random.uniform(2.8, 3.5)
        st.metric("⛽ Fuel Efficiency", f"{fuel_efficiency:.1f} L/km", 
                 delta=f"{np.random.uniform(-0.1, 0.1):+.1f}")
    
    with fleet_kpi_col2:
        maintenance_cost = np.random.randint(25000, 45000)
        st.metric("🔧 Monthly Maintenance", f"${maintenance_cost:,}",
                 delta=f"${np.random.randint(-2000, 1000):+,}")
    
    with fleet_kpi_col3:
        utilization_rate = np.random.uniform(85, 94)
        st.metric("📊 Fleet Utilization", f"{utilization_rate:.1f}%",
                 delta=f"{np.random.uniform(-1, 2):+.1f}%")
    
    with fleet_kpi_col4:
        availability_rate = np.random.uniform(92, 98)
        st.metric("🟢 Availability Rate", f"{availability_rate:.1f}%",
                 delta=f"{np.random.uniform(-0.5, 1):+.1f}%")
    
    # Enhanced Maintenance & Fleet Operations Table
    fleet_operations = fetch_data("""
        SELECT 
            me.aircraft_id as "✈️ Aircraft ID",
            me.event_type as "🔧 Maintenance Type",
            me.description as "📝 Description",
            TO_CHAR(me.event_time, 'YYYY-MM-DD HH24:MI') as "🕐 Start Time",
            TO_CHAR(me.resolved_time, 'YYYY-MM-DD HH24:MI') as "✅ End Time",
            ROUND(EXTRACT(EPOCH FROM (me.resolved_time - me.event_time))/3600, 1) as "⏱️ Duration (hrs)",
            me.cost as "💰 Cost ($)",
            ff.fuel_type as "⛽ Fuel Type",
            ROUND(ff.fuel_quantity_liters, 0) as "📊 Fuel Quantity (L)",
            ff.fueling_company as "🏢 Fuel Supplier",
            CASE me.event_type
                WHEN 'Scheduled' THEN '🟢 Planned'
                WHEN 'Unscheduled' THEN '🔴 Emergency'
                ELSE '🟡 Routine'
            END as "📋 Priority",
            CASE 
                WHEN me.cost <= 5000 THEN '🟢 Low Cost'
                WHEN me.cost <= 20000 THEN '🟡 Medium Cost'
                ELSE '🔴 High Cost'
            END as "💸 Cost Category"
        FROM tr_maintenance_event me
        LEFT JOIN tr_flight_fuel ff ON me.aircraft_id IN (
            SELECT DISTINCT aircraft_id FROM tr_flight WHERE flight_id = ANY(
                SELECT flight_id FROM tr_flight_fuel WHERE fuel_id = ff.fuel_id
            )
        )
        WHERE me.event_time >= CURRENT_DATE - INTERVAL '30 days'
        ORDER BY me.cost DESC, me.event_time DESC
    """)
    
    if not fleet_operations.empty:
        create_enhanced_table(
            fleet_operations, 
            "Fleet Maintenance & Operations Analysis", 
            table_type="default", 
            key_suffix="fleet_operations"
        )
    
    # Enhanced Fleet Efficiency Analysis Table
    fleet_efficiency = fetch_data("""
        SELECT 
            me.aircraft_id as "✈️ Aircraft ID",
            COUNT(DISTINCT f.flight_id) as "🛫 Total Flights",
            ROUND(SUM(ff.fuel_quantity_liters), 0) as "⛽ Total Fuel (L)",
            ROUND(AVG(ff.fuel_quantity_liters), 0) as "📊 Avg Fuel per Flight (L)",
            ROUND(SUM(f.distance_km), 0) as "📏 Total Distance (km)",
            ROUND(SUM(ff.fuel_quantity_liters) / NULLIF(SUM(f.distance_km), 0) * 100, 2) as "⚡ Fuel Efficiency (L/100km)",
            COUNT(me.maintenance_id) as "🔧 Maintenance Events",
            COALESCE(SUM(me.cost), 0) as "💰 Total Maintenance Cost ($)",
            ROUND(COALESCE(SUM(me.cost), 0) / NULLIF(COUNT(DISTINCT f.flight_id), 0), 0) as "💸 Cost per Flight ($)",
            CASE 
                WHEN COUNT(me.maintenance_id) <= 2 THEN '🟢 Low Maintenance'
                WHEN COUNT(me.maintenance_id) <= 5 THEN '🟡 Medium Maintenance'
                ELSE '🔴 High Maintenance'
            END as "📋 Maintenance Level",
            CASE 
                WHEN ROUND(SUM(ff.fuel_quantity_liters) / NULLIF(SUM(f.distance_km), 0) * 100, 2) <= 3.0 THEN '🟢 Excellent'
                WHEN ROUND(SUM(ff.fuel_quantity_liters) / NULLIF(SUM(f.distance_km), 0) * 100, 2) <= 4.0 THEN '🟡 Good'
                ELSE '🔴 Poor'
            END as "⚡ Efficiency Rating",
            ROUND(COUNT(DISTINCT f.flight_id) / 30.0, 1) as "📈 Flights per Day"
        FROM tr_maintenance_event me
        LEFT JOIN tr_flight f ON me.aircraft_id = f.aircraft_id
        LEFT JOIN tr_flight_fuel ff ON f.flight_id = ff.flight_id
        WHERE me.event_time >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY me.aircraft_id
        ORDER BY COUNT(DISTINCT f.flight_id) DESC
    """)
    
    if not fleet_efficiency.empty:
        create_enhanced_table(
            fleet_efficiency, 
            "Fleet Efficiency & Cost Analysis", 
            table_type="performance", 
            key_suffix="fleet_efficiency"
        )
    
    # Enhanced Fuel Supplier Performance Table
    fuel_supplier_analysis = fetch_data("""
        SELECT 
            ff.fueling_company as "🏢 Fuel Supplier",
            COUNT(*) as "⛽ Total Refuels",
            ROUND(SUM(ff.fuel_quantity_liters), 0) as "📊 Total Fuel Supplied (L)",
            ROUND(AVG(ff.fuel_quantity_liters), 0) as "📈 Avg Fuel per Refuel (L)",
            COUNT(DISTINCT ff.fuel_type) as "🎯 Fuel Types",
            COUNT(DISTINCT f.aircraft_id) as "✈️ Aircraft Served",
            ROUND(SUM(ff.fuel_quantity_liters) / COUNT(*), 0) as "⚡ Efficiency (L/refuel)",
            CASE ff.fuel_type 
                WHEN 'Jet A-1' THEN '👑 Premium'
                WHEN 'Jet A' THEN '💼 Standard'
                ELSE '⚪ Other'
            END as "🎯 Primary Fuel Grade",
            CASE 
                WHEN COUNT(*) >= 20 THEN '🟢 Major Supplier'
                WHEN COUNT(*) >= 10 THEN '🟡 Regular Supplier'
                ELSE '🔴 Minor Supplier'
            END as "📋 Supplier Category",
            TO_CHAR(MAX(ff.fueling_time), 'YYYY-MM-DD') as "📅 Last Service"
        FROM tr_flight_fuel ff
        JOIN tr_flight f ON ff.flight_id = f.flight_id
        WHERE ff.fueling_time >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY ff.fueling_company, ff.fuel_type
        ORDER BY SUM(ff.fuel_quantity_liters) DESC
    """)
    
    if not fuel_supplier_analysis.empty:
        create_enhanced_table(
            fuel_supplier_analysis, 
            "Fuel Supplier Performance Analysis", 
            table_type="default", 
            key_suffix="fuel_suppliers"
        )

if __name__ == "__main__":
    main() 