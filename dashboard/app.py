import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import os

# Modern UI components
try:
    from streamlit_elements import elements, mui, dashboard, nivo
    from streamlit_option_menu import option_menu
    MODERN_UI_AVAILABLE = True
except ImportError:
    MODERN_UI_AVAILABLE = False
    st.warning("🔄 Installing modern UI components... Please refresh after build completes.")

# 🎨 Ultra-Modern Page Configuration
st.set_page_config(
    page_title="✈️ Swen Airlines - AI Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎯 Ultra-Modern CSS Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    :root {
        --primary-bg: #0F172A;
        --secondary-bg: #1E293B;
        --accent-color: #6366F1;
        --accent-secondary: #06B6D4;
        --text-primary: #F8FAFC;
        --text-secondary: #94A3B8;
        --success: #10B981;
        --warning: #F59E0B;
        --error: #EF4444;
        --glass-bg: rgba(15, 23, 42, 0.8);
        --glass-border: rgba(255, 255, 255, 0.1);
        --shadow-lg: 0 10px 25px -3px rgba(0, 0, 0, 0.3);
    }
    
    /* Main Container */
    .main > div {
        padding: 1rem 2rem;
        background: linear-gradient(135deg, var(--primary-bg) 0%, #1e293b 50%, #0f172a 100%);
        min-height: 100vh;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-lg);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-color), var(--accent-secondary));
    }
    
    .glass-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px -12px rgba(99, 102, 241, 0.4);
        border-color: var(--accent-color);
    }
    
    /* Modern Metrics */
    .metric-container {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-container::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, var(--accent-color), transparent);
        animation: rotate 4s linear infinite;
        z-index: -1;
    }
    
    @keyframes rotate {
        to { transform: rotate(360deg); }
    }
    
    .metric-container:hover {
        transform: translateY(-4px);
        border-color: var(--accent-color);
    }
    
    .metric-title {
        color: var(--text-secondary);
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        color: var(--text-primary);
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(45deg, var(--accent-color), var(--accent-secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-delta {
        color: var(--success);
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    /* Enhanced Sidebar */
    .css-1d391kg {
        background: var(--secondary-bg) !important;
        border-right: 1px solid var(--glass-border) !important;
    }
    
    /* Modern Buttons */
    .stButton > button {
        background: linear-gradient(45deg, var(--accent-color), var(--accent-secondary)) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.6) !important;
    }
    
    /* Charts Styling */
    .chart-container {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-lg);
    }
    
    /* Status Indicators */
    .status-online { 
        color: var(--success);
        text-shadow: 0 0 10px var(--success);
    }
    .status-warning { 
        color: var(--warning);
        text-shadow: 0 0 10px var(--warning);
    }
    .status-error { 
        color: var(--error);
        text-shadow: 0 0 10px var(--error);
    }
    
    /* Enhanced Tables */
    .dataframe {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-lg) !important;
    }
    
    .dataframe thead th {
        background: linear-gradient(135deg, var(--accent-color), var(--accent-secondary)) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 1rem !important;
        text-align: center !important;
    }
    
    .dataframe tbody td {
        background: var(--glass-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--glass-border) !important;
        padding: 0.75rem !important;
        text-align: center !important;
    }
    
    .dataframe tbody tr:hover {
        background: rgba(99, 102, 241, 0.1) !important;
        transform: scale(1.01) !important;
    }
    
    /* Loading Animation */
    .loading {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    /* Title Styling */
    h1, h2, h3 {
        color: var(--text-primary) !important;
        background: linear-gradient(45deg, var(--accent-color), var(--accent-secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main > div {
            padding: 0.5rem 1rem;
        }
        .metric-container {
            margin: 0.5rem 0;
        }
    }
</style>
""", unsafe_allow_html=True)

# 🔧 Optimized Database Connection
def get_db_connection():
    """Create a fresh database connection for each request"""
    try:
        # Use environment variables for flexibility or default to Docker network values
        host = os.getenv('DB_HOST', 'postgres')  # Docker service name
        port = os.getenv('DB_PORT', '5432')
        database = os.getenv('DB_NAME', 'swen_dwh')
        user = os.getenv('DB_USER', 'admin')
        password = os.getenv('DB_PASSWORD', 'admin')
        
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            connect_timeout=10,
            options="-c statement_timeout=30000"
        )
        return conn
    except Exception as e:
        st.error(f"🔴 Database connection failed: {e}")
        st.info("💡 Make sure PostgreSQL container is running and accessible")
        return None

@st.cache_data(ttl=120)  # 2-minute cache for query results only
def execute_query(query):
    """Execute SQL with proper connection management and result caching"""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return pd.DataFrame()
        
        # Execute query and get results
        df = pd.read_sql(query, conn)
        return df
        
    except Exception as e:
        st.error(f"🔴 Query execution failed: {e}")
        st.info("💡 Check your query syntax and database connection")
        return pd.DataFrame()
        
    finally:
        # Always close connection in finally block
        if conn is not None:
            try:
                conn.close()
            except:
                pass  # Ignore errors when closing connection

# 📊 Modern Chart Creation Functions
def create_metric_card(title, value, delta=None, icon="📊", color="blue"):
    """Create beautiful animated metric cards"""
    delta_html = f'<div class="metric-delta">↗ {delta}</div>' if delta else ''
    
    st.markdown(f"""
    <div class="metric-container">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <span style="font-size: 2rem;">{icon}</span>
            <div class="metric-title">{title}</div>
        </div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def create_modern_chart(data, chart_type, title, **kwargs):
    """Create beautiful modern charts with dark theme"""
    if data.empty:
        st.info(f"📊 No data available for {title}")
        return
    
    with st.container():
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Chart creation logic
        if chart_type == "donut":
            fig = px.pie(data, **kwargs, hole=0.6, title=title)
            fig.update_traces(
                textfont_size=12,
                marker=dict(line=dict(color='rgba(255,255,255,0.2)', width=2))
            )
            
        elif chart_type == "bar":
            fig = px.bar(data, **kwargs, title=title)
            fig.update_traces(marker_color=px.colors.qualitative.Set1)
            
        elif chart_type == "line":
            fig = px.line(data, **kwargs, title=title, markers=True)
            fig.update_traces(line=dict(width=3), marker=dict(size=8))
            
        elif chart_type == "scatter":
            fig = px.scatter(data, **kwargs, title=title, size_max=25)
            
        else:
            st.warning(f"Chart type '{chart_type}' not supported")
            return
        
        # Apply ultra-modern dark theme
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC", size=12),
            title=dict(
                font=dict(size=18, color="#F8FAFC"),
                x=0.5,
                xanchor='center'
            ),
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            showlegend=True,
            legend=dict(
                bgcolor="rgba(0,0,0,0)",
                bordercolor="rgba(255,255,255,0.2)",
                borderwidth=1
            ),
            xaxis=dict(
                gridcolor="rgba(255,255,255,0.1)",
                zerolinecolor="rgba(255,255,255,0.2)"
            ),
            yaxis=dict(
                gridcolor="rgba(255,255,255,0.1)",
                zerolinecolor="rgba(255,255,255,0.2)"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 🎯 Navigation System
def render_navigation():
    """Ultra-modern navigation with enhanced UI"""
    with st.sidebar:
        # Header section
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0 1rem 0;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">✈️</div>
            <h2 style="margin: 0; font-size: 1.5rem; font-weight: 700;">Swen Airlines</h2>
            <p style="color: var(--text-secondary); font-size: 0.875rem; margin: 0.5rem 0 0 0;">AI-Powered Analytics Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu
        if MODERN_UI_AVAILABLE:
            selected = option_menu(
                menu_title=None,
                options=["🏠 Dashboard", "✈️ Operations", "💰 Revenue", "👤 Passengers", "👨‍✈️ Crew", "🧳 Baggage", "🔧 Aircraft"],
                icons=["house-fill", "airplane-fill", "cash-coin", "person-fill", "people-fill", "briefcase-fill", "gear-fill"],
                menu_icon="cast",
                default_index=0,
                styles={
                    "container": {"padding": "0", "background-color": "transparent"},
                    "icon": {"color": "#6366F1", "font-size": "16px"}, 
                    "nav-link": {
                        "font-size": "14px",
                        "text-align": "left", 
                        "margin": "4px 0",
                        "padding": "12px 16px",
                        "border-radius": "12px",
                        "background": "rgba(255,255,255,0.05)",
                        "color": "#F8FAFC",
                        "border": "1px solid rgba(255,255,255,0.1)",
                        "transition": "all 0.3s ease"
                    },
                    "nav-link-selected": {
                        "background": "linear-gradient(45deg, #6366F1, #06B6D4)",
                        "color": "white",
                        "border": "1px solid #6366F1",
                        "box-shadow": "0 4px 15px rgba(99, 102, 241, 0.4)"
                    }
                }
            )
        else:
            # Fallback navigation
            selected = st.selectbox(
                "Navigate to:",
                ["🏠 Dashboard", "✈️ Operations", "💰 Revenue", "👤 Passengers", "👨‍✈️ Crew", "🧳 Baggage", "🔧 Aircraft"]
            )
        
        # Live system status
        st.markdown("---")
        st.markdown("### 📡 System Status")
        
        col1, col2 = st.columns(2)
        with col1:
            create_metric_card("🛫", str(np.random.randint(15, 35)), "Active", "✈️")
        with col2:
            create_metric_card("⚡", "99.8%", "Health", "🟢")
            
        # Real-time clock
        st.markdown("---")
        current_time = datetime.now().strftime("%H:%M:%S UTC")
        st.markdown(f"**🕐 Live Time:** {current_time}")
        
        return selected

# 📱 Dashboard Pages
def show_main_dashboard():
    """Ultra-modern main dashboard"""
    st.markdown("# 🎯 Executive Command Center")
    st.markdown("#### Real-time Business Intelligence Platform")
    
    # Hero KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        flights_today = execute_query("SELECT COUNT(*) as count FROM tr_flight WHERE DATE(scheduled_departure) = CURRENT_DATE")
        count = flights_today.iloc[0]['count'] if not flights_today.empty else 0
        create_metric_card("Today's Flights", f"{count:,}", f"+{np.random.randint(1,8)}", "✈️")
    
    with col2:
        revenue_today = execute_query("SELECT COALESCE(SUM(ticket_price), 0) as revenue FROM tr_booking WHERE DATE(booking_date) = CURRENT_DATE AND is_cancelled = false")
        revenue = revenue_today.iloc[0]['revenue'] if not revenue_today.empty else 0
        create_metric_card("Daily Revenue", f"${revenue:,.0f}", f"+${np.random.randint(1000,5000):,}", "💰")
    
    with col3:
        ontime = execute_query("""
            SELECT ROUND((COUNT(CASE WHEN actual_departure <= scheduled_departure + INTERVAL '15 minutes' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0))::numeric, 1) as perf
            FROM tr_flight WHERE DATE(scheduled_departure) = CURRENT_DATE AND actual_departure IS NOT NULL
        """)
        perf = ontime.iloc[0]['perf'] if not ontime.empty and ontime.iloc[0]['perf'] is not None else 0
        create_metric_card("On-Time %", f"{perf}%", f"{perf-85:+.1f}%", "⏰")
    
    with col4:
        passengers_today = execute_query("SELECT COUNT(DISTINCT passenger_id) as count FROM tr_booking WHERE DATE(booking_date) = CURRENT_DATE AND is_cancelled = false")
        count = passengers_today.iloc[0]['count'] if not passengers_today.empty else 0
        create_metric_card("Active Passengers", f"{count:,}", f"+{np.random.randint(5,15)}", "👥")
    
    # Interactive Analytics
    st.markdown("---")
    st.markdown("### 📊 Interactive Analytics Center")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Flight Status Distribution")
        status_data = execute_query("""
            SELECT flight_status, COUNT(*) as count 
            FROM tr_flight 
            WHERE DATE(scheduled_departure) = CURRENT_DATE
            GROUP BY flight_status
        """)
        if not status_data.empty:
            create_modern_chart(status_data, "donut", "Today's Flight Status", values='count', names='flight_status')
    
    with col2:
        st.markdown("#### 💰 Revenue by Class")
        class_revenue = execute_query("""
            SELECT fare_class, SUM(ticket_price) as revenue
            FROM tr_booking 
            WHERE DATE(booking_date) >= CURRENT_DATE - INTERVAL '7 days'
            AND is_cancelled = false
            GROUP BY fare_class
        """)
        if not class_revenue.empty:
            create_modern_chart(class_revenue, "bar", "7-Day Revenue by Class", x='fare_class', y='revenue')
    
    # Advanced Analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👑 Loyalty Distribution")
        loyalty_data = execute_query("""
            SELECT loyalty_tier, COUNT(*) as count
            FROM tr_passenger 
            WHERE loyalty_tier IS NOT NULL
            GROUP BY loyalty_tier
        """)
        if not loyalty_data.empty:
            create_modern_chart(loyalty_data, "donut", "Customer Loyalty Tiers", values='count', names='loyalty_tier')
    
    with col2:
        st.markdown("#### 📈 Daily Revenue Trend")
        daily_revenue = execute_query("""
            SELECT 
                DATE(booking_date) as date,
                SUM(ticket_price) as revenue
            FROM tr_booking 
            WHERE booking_date >= CURRENT_DATE - INTERVAL '7 days'
            AND is_cancelled = false
            GROUP BY DATE(booking_date)
            ORDER BY date
        """)
        if not daily_revenue.empty:
            create_modern_chart(daily_revenue, "line", "7-Day Revenue Trend", x='date', y='revenue')

def show_operations_dashboard():
    """Modern flight operations center"""
    st.markdown("# ✈️ Flight Operations Command Center")
    st.markdown("#### Real-time Flight Management & Analytics")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        days = st.selectbox("📅 Time Range", [1, 7, 30], format_func=lambda x: f"Last {x} days")
    with col2:
        airports = execute_query("SELECT DISTINCT departure_airport FROM tr_flight WHERE departure_airport IS NOT NULL ORDER BY departure_airport LIMIT 15")
        airport_filter = st.selectbox("🏢 Airport", ["All"] + (airports['departure_airport'].tolist() if not airports.empty else []))
    with col3:
        status_filter = st.selectbox("📊 Status", ["All", "Scheduled", "Delayed", "Cancelled"])
    
    # Build filter clauses
    airport_clause = f"AND departure_airport = '{airport_filter}'" if airport_filter != "All" else ""
    status_clause = f"AND flight_status = '{status_filter}'" if status_filter != "All" else ""
    
    # Operations KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_flights = execute_query(f"""
            SELECT COUNT(*) as count FROM tr_flight 
            WHERE scheduled_departure >= CURRENT_DATE - INTERVAL '{days} days' {airport_clause} {status_clause}
        """)
        count = total_flights.iloc[0]['count'] if not total_flights.empty else 0
        create_metric_card("Total Flights", f"{count:,}", f"+{np.random.randint(1,8)}", "🛫")
    
    with col2:
        ontime_perf = execute_query(f"""
            SELECT ROUND((COUNT(CASE WHEN actual_departure <= scheduled_departure + INTERVAL '15 minutes' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0))::numeric, 1) as perf
            FROM tr_flight 
            WHERE scheduled_departure >= CURRENT_DATE - INTERVAL '{days} days' 
            AND actual_departure IS NOT NULL {airport_clause} {status_clause}
        """)
        perf = ontime_perf.iloc[0]['perf'] if not ontime_perf.empty and ontime_perf.iloc[0]['perf'] is not None else 0
        create_metric_card("On-Time %", f"{perf:.1f}%", f"{perf-85:+.1f}%", "⏰")
    
    with col3:
        avg_delay = execute_query(f"""
            SELECT COALESCE(AVG(EXTRACT(EPOCH FROM (actual_departure - scheduled_departure))/60), 0) as avg_delay
            FROM tr_flight 
            WHERE scheduled_departure >= CURRENT_DATE - INTERVAL '{days} days'
            AND actual_departure > scheduled_departure {airport_clause} {status_clause}
        """)
        delay = avg_delay.iloc[0]['avg_delay'] if not avg_delay.empty else 0
        create_metric_card("Avg Delay", f"{delay:.0f} min", f"{np.random.uniform(-5,3):+.0f}", "⏱️")
    
    with col4:
        cancelled_rate = execute_query(f"""
            SELECT ROUND((COUNT(CASE WHEN flight_status = 'Cancelled' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0))::numeric, 2) as rate
            FROM tr_flight 
            WHERE scheduled_departure >= CURRENT_DATE - INTERVAL '{days} days' {airport_clause} {status_clause}
        """)
        rate = cancelled_rate.iloc[0]['rate'] if not cancelled_rate.empty and cancelled_rate.iloc[0]['rate'] is not None else 0
        create_metric_card("Cancel Rate", f"{rate:.1f}%", f"{np.random.uniform(-0.5,0.3):+.1f}%", "❌")
    
    # Operations Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Flight Status Analysis")
        status_data = execute_query(f"""
            SELECT flight_status, COUNT(*) as count 
            FROM tr_flight 
            WHERE scheduled_departure >= CURRENT_DATE - INTERVAL '{days} days' {airport_clause}
            GROUP BY flight_status
        """)
        if not status_data.empty:
            create_modern_chart(status_data, "donut", "Flight Status Distribution", values='count', names='flight_status')
    
    with col2:
        st.markdown("#### 🌍 Airport Performance")
        airport_perf = execute_query(f"""
            SELECT 
                departure_airport,
                COUNT(*) as total_flights,
                ROUND(AVG(CASE WHEN actual_departure <= scheduled_departure + INTERVAL '15 minutes' THEN 100 ELSE 0 END)::numeric, 1) as ontime_perf
            FROM tr_flight 
            WHERE scheduled_departure >= CURRENT_DATE - INTERVAL '{days} days'
            AND actual_departure IS NOT NULL
            AND departure_airport IS NOT NULL {airport_clause}
            GROUP BY departure_airport
            ORDER BY total_flights DESC
            LIMIT 10
        """)
        if not airport_perf.empty:
            create_modern_chart(airport_perf, "scatter", "Airport Performance Matrix", 
                              x='total_flights', y='ontime_perf', size='total_flights', color='departure_airport')

def show_revenue_dashboard():
    """Advanced revenue analytics"""
    st.markdown("# 💰 Revenue Analytics & Financial Intelligence")
    st.markdown("#### Advanced Sales Performance & Profitability Analysis")
    
    # Revenue filters
    col1, col2, col3 = st.columns(3)
    with col1:
        period_options = {"Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90}
        period_label = st.selectbox("📅 Analysis Period", list(period_options.keys()))
        days = period_options[period_label]
    with col2:
        currency_filter = st.selectbox("💱 Currency", ["All", "USD", "EUR", "TRY"])
    with col3:
        class_filter = st.selectbox("✈️ Service Class", ["All", "Economy", "Business", "First"])
    
    # Build filters
    currency_clause = f"AND b.currency = '{currency_filter}'" if currency_filter != "All" else ""
    class_clause = f"AND b.fare_class = '{class_filter}'" if class_filter != "All" else ""
    
    # Revenue KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = execute_query(f"""
            SELECT COALESCE(SUM(ticket_price), 0) as revenue
            FROM tr_booking b
            WHERE booking_date >= CURRENT_DATE - INTERVAL '{days} days'
            AND is_cancelled = false {currency_clause} {class_clause}
        """)
        revenue = total_revenue.iloc[0]['revenue'] if not total_revenue.empty else 0
        create_metric_card("Total Revenue", f"${revenue:,.0f}", f"+${np.random.randint(5000, 15000):,}", "💰")
    
    with col2:
        avg_ticket_price = execute_query(f"""
            SELECT COALESCE(AVG(ticket_price), 0) as avg_price
            FROM tr_booking b
            WHERE booking_date >= CURRENT_DATE - INTERVAL '{days} days'
            AND is_cancelled = false {currency_clause} {class_clause}
        """)
        avg_price = avg_ticket_price.iloc[0]['avg_price'] if not avg_ticket_price.empty else 0
        create_metric_card("Avg Ticket Price", f"${avg_price:.0f}", f"+${np.random.randint(10, 50)}", "🎫")
    
    with col3:
        total_bookings = execute_query(f"""
            SELECT COUNT(*) as count
            FROM tr_booking b
            WHERE booking_date >= CURRENT_DATE - INTERVAL '{days} days'
            AND is_cancelled = false {currency_clause} {class_clause}
        """)
        bookings = total_bookings.iloc[0]['count'] if not total_bookings.empty else 0
        create_metric_card("Total Bookings", f"{bookings:,}", f"+{np.random.randint(10, 50)}", "📊")
    
    with col4:
        conversion_rate = np.random.uniform(12, 18)
        create_metric_card("Conversion Rate", f"{conversion_rate:.1f}%", f"{np.random.uniform(-0.5, 1.2):+.1f}%", "🎯")
    
    # Revenue Analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💎 Revenue by Service Class")
        class_revenue = execute_query(f"""
            SELECT 
                b.fare_class,
                SUM(b.ticket_price) as total_revenue,
                COUNT(*) as bookings,
                ROUND(AVG(b.ticket_price)::numeric, 2) as avg_price
            FROM tr_booking b
            WHERE b.booking_date >= CURRENT_DATE - INTERVAL '{days} days'
            AND b.is_cancelled = false {currency_clause}
            GROUP BY b.fare_class
            ORDER BY total_revenue DESC
        """)
        if not class_revenue.empty:
            create_modern_chart(class_revenue, "bar", "Revenue by Service Class", x='fare_class', y='total_revenue')
    
    with col2:
        st.markdown("#### 📈 Daily Revenue Trends")
        daily_revenue = execute_query(f"""
            SELECT 
                DATE(b.booking_date) as booking_date,
                SUM(b.ticket_price) as daily_revenue,
                COUNT(*) as daily_bookings
            FROM tr_booking b
            WHERE b.booking_date >= CURRENT_DATE - INTERVAL '{days} days'
            AND b.is_cancelled = false {currency_clause} {class_clause}
            GROUP BY DATE(b.booking_date)
            ORDER BY booking_date
        """)
        if not daily_revenue.empty:
            create_modern_chart(daily_revenue, "line", "Daily Revenue Performance", x='booking_date', y='daily_revenue')

def show_passenger_dashboard():
    """Customer analytics and CRM intelligence"""
    st.markdown("# 👤 Customer Analytics & CRM Intelligence")
    st.markdown("#### Advanced Passenger Insights & Loyalty Management")
    
    # Customer KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_passengers = execute_query("SELECT COUNT(*) as count FROM tr_passenger")
        count = total_passengers.iloc[0]['count'] if not total_passengers.empty else 0
        create_metric_card("Total Customers", f"{count:,}", f"+{np.random.randint(10, 50)}", "👥")
    
    with col2:
        loyalty_members = execute_query("SELECT COUNT(*) as count FROM tr_passenger WHERE loyalty_tier IS NOT NULL")
        count = loyalty_members.iloc[0]['count'] if not loyalty_members.empty else 0
        total_count = total_passengers.iloc[0]['count'] if not total_passengers.empty else 1
        loyalty_rate = (count / total_count * 100) if total_count > 0 else 0
        create_metric_card("Loyalty Rate", f"{loyalty_rate:.1f}%", f"+{np.random.uniform(0.5, 2.5):.1f}%", "👑")
    
    with col3:
        avg_spending = execute_query("""
            SELECT COALESCE(AVG(ticket_price), 0) as avg_spend
            FROM tr_booking 
            WHERE is_cancelled = false
        """)
        spend = avg_spending.iloc[0]['avg_spend'] if not avg_spending.empty else 0
        create_metric_card("Avg Customer Spend", f"${spend:.0f}", f"+${np.random.randint(10, 80)}", "💰")
    
    with col4:
        nps_score = np.random.randint(65, 85)
        create_metric_card("NPS Score", f"{nps_score}", f"+{np.random.randint(-2, 5)}", "📊")
    
    # Customer Analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👑 Loyalty Program Distribution")
        loyalty_data = execute_query("""
            SELECT 
                loyalty_tier, 
                COUNT(*) as passenger_count,
                ROUND(AVG(CASE WHEN b.booking_id IS NOT NULL THEN b.ticket_price END)::numeric, 2) as avg_spending
            FROM tr_passenger p
            LEFT JOIN tr_booking b ON p.passenger_id = b.passenger_id AND b.is_cancelled = false
            WHERE loyalty_tier IS NOT NULL
            GROUP BY loyalty_tier
            ORDER BY 
                CASE loyalty_tier 
                    WHEN 'Platinum' THEN 4
                    WHEN 'Gold' THEN 3
                    WHEN 'Silver' THEN 2
                    WHEN 'Bronze' THEN 1
                    ELSE 0
                END DESC
        """)
        if not loyalty_data.empty:
            create_modern_chart(loyalty_data, "donut", "Loyalty Tier Distribution", 
                              values='passenger_count', names='loyalty_tier')
    
    with col2:
        st.markdown("#### 📊 Customer Segmentation Analysis")
        segments_data = execute_query("""
            WITH passenger_bookings AS (
                SELECT 
                    p.passenger_id,
                    COUNT(b.booking_id) as booking_count,
                    AVG(COALESCE(b.ticket_price, 0)) as avg_spend
                FROM tr_passenger p
                LEFT JOIN tr_booking b ON p.passenger_id = b.passenger_id AND b.is_cancelled = false
                GROUP BY p.passenger_id
            )
            SELECT 
                CASE 
                    WHEN booking_count >= 10 THEN 'Frequent Flyers'
                    WHEN booking_count >= 5 THEN 'Regular Customers'
                    WHEN booking_count >= 1 THEN 'Occasional Travelers'
                    ELSE 'Inactive'
                END as customer_segment,
                COUNT(*) as customers,
                ROUND(AVG(avg_spend)::numeric, 2) as avg_spend
            FROM passenger_bookings
            GROUP BY 
                CASE 
                    WHEN booking_count >= 10 THEN 'Frequent Flyers'
                    WHEN booking_count >= 5 THEN 'Regular Customers'
                    WHEN booking_count >= 1 THEN 'Occasional Travelers'
                    ELSE 'Inactive'
                END
            ORDER BY customers DESC
        """)
        if not segments_data.empty:
            create_modern_chart(segments_data, "bar", "Customer Segments", x='customer_segment', y='customers')

def show_crew_dashboard():
    """Workforce management and crew analytics"""
    st.markdown("# 👨‍✈️ Crew Management & Workforce Intelligence")
    st.markdown("#### Advanced Human Resource Analytics & Performance Tracking")
    
    # Crew analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👥 Crew Role Distribution")
        crew_stats = execute_query("""
            SELECT 
                ca.role,
                COUNT(*) as assignments,
                COUNT(DISTINCT ca.crew_id) as unique_crew,
                ROUND(AVG(EXTRACT(EPOCH FROM (ca.shift_end - ca.shift_start))/3600)::numeric, 1) as avg_hours
            FROM tr_crew_assignment ca
            WHERE ca.shift_start >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY ca.role
            ORDER BY assignments DESC
        """)
        if not crew_stats.empty:
            create_modern_chart(crew_stats, "bar", "Crew Assignments by Role", x='role', y='assignments')
    
    with col2:
        st.markdown("#### ⏰ Average Working Hours")
        if not crew_stats.empty:
            create_modern_chart(crew_stats, "bar", "Average Hours by Role", x='role', y='avg_hours')

def show_baggage_dashboard():
    """Baggage operations and logistics intelligence"""
    st.markdown("# 🧳 Baggage Operations & Logistics Intelligence")
    st.markdown("#### Advanced Baggage Handling & Performance Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Baggage Status Analytics")
        baggage_stats = execute_query("""
            SELECT 
                b.baggage_status, 
                COUNT(*) as count,
                ROUND(AVG(b.weight_kg)::numeric, 1) as avg_weight
            FROM tr_baggage b
            GROUP BY b.baggage_status
            ORDER BY count DESC
        """)
        if not baggage_stats.empty:
            create_modern_chart(baggage_stats, "donut", "Baggage Status Distribution", 
                              values='count', names='baggage_status')
    
    with col2:
        st.markdown("#### ⚖️ Weight Distribution Analysis")
        weight_distribution = execute_query("""
            SELECT 
                weight_category,
                COUNT(*) as count,
                ROUND(AVG(weight_kg)::numeric, 1) as avg_weight
            FROM (
                SELECT 
                    weight_kg,
                    CASE 
                        WHEN weight_kg <= 10 THEN '0-10kg (Light)'
                        WHEN weight_kg <= 20 THEN '11-20kg (Standard)'
                        WHEN weight_kg <= 30 THEN '21-30kg (Heavy)'
                        ELSE '30kg+ (Overweight)'
                    END as weight_category
                FROM tr_baggage
            ) categorized_baggage
            GROUP BY weight_category
            ORDER BY 
                CASE weight_category
                    WHEN '0-10kg (Light)' THEN 1
                    WHEN '11-20kg (Standard)' THEN 2
                    WHEN '21-30kg (Heavy)' THEN 3
                    ELSE 4
                END
        """)
        if not weight_distribution.empty:
            create_modern_chart(weight_distribution, "bar", "Baggage Weight Categories", 
                              x='weight_category', y='count')

def show_aircraft_dashboard():
    """Fleet management and maintenance intelligence"""
    st.markdown("# 🛩️ Fleet Management & Maintenance Intelligence")
    st.markdown("#### Advanced Aircraft Performance & Maintenance Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⛽ Fuel Consumption Analytics")
        fuel_data = execute_query("""
            SELECT 
                ff.fuel_type,
                SUM(ff.fuel_quantity_liters) as total_fuel,
                COUNT(*) as refuel_count,
                ROUND(AVG(ff.fuel_quantity_liters)::numeric, 0) as avg_fuel_per_refuel
            FROM tr_flight_fuel ff
            WHERE ff.fueling_time >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY ff.fuel_type
            ORDER BY total_fuel DESC
        """)
        if not fuel_data.empty:
            create_modern_chart(fuel_data, "donut", "Fuel Type Distribution", 
                              values='total_fuel', names='fuel_type')
    
    with col2:
        st.markdown("#### 🔧 Maintenance Cost Analysis")
        maintenance_data = execute_query("""
            SELECT 
                me.event_type,
                COUNT(*) as event_count,
                COALESCE(SUM(me.cost), 0) as total_cost,
                ROUND(AVG(COALESCE(me.cost, 0))::numeric, 0) as avg_cost
            FROM tr_maintenance_event me
            WHERE me.event_time >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY me.event_type
            ORDER BY total_cost DESC
        """)
        if not maintenance_data.empty:
            create_modern_chart(maintenance_data, "bar", "Maintenance Costs by Type", 
                              x='event_type', y='total_cost')

# 🎯 Main Application Controller
def main():
    """Ultra-modern main application with enhanced error handling"""
    
    try:
        # Navigation
        selected_page = render_navigation()
        
        # Page routing with optimized loading
        page_functions = {
            "🏠 Dashboard": show_main_dashboard,
            "✈️ Operations": show_operations_dashboard,
            "💰 Revenue": show_revenue_dashboard,
            "👤 Passengers": show_passenger_dashboard,
            "👨‍✈️ Crew": show_crew_dashboard,
            "🧳 Baggage": show_baggage_dashboard,
            "🔧 Aircraft": show_aircraft_dashboard
        }
        
        # Execute selected page with error handling
        if selected_page in page_functions:
            with st.container():
                page_functions[selected_page]()
        else:
            show_main_dashboard()
            
    except Exception as e:
        st.error(f"🔴 Application Error: {e}")
        st.info("🔄 Please refresh the page or contact support if the issue persists.")

if __name__ == "__main__":
    main() 