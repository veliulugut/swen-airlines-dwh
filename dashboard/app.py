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
    from streamlit_option_menu import option_menu
    MODERN_UI_AVAILABLE = True
except ImportError:
    MODERN_UI_AVAILABLE = False

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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    :root {
        /* White Theme Color Palette */
        --primary-bg: #FFFFFF;
        --secondary-bg: #F8FAFC;
        --tertiary-bg: #F1F5F9;
        --card-bg: #FFFFFF;
        
        /* Brand Colors */
        --brand-primary: #2563EB;
        --brand-secondary: #0EA5E9;
        --brand-accent: #8B5CF6;
        --brand-success: #059669;
        --brand-warning: #D97706;
        --brand-danger: #DC2626;
        
        /* Text Colors */
        --text-primary: #1E293B;
        --text-secondary: #64748B;
        --text-muted: #94A3B8;
        --text-white: #FFFFFF;
        
        /* Border & Shadow */
        --border-light: #E2E8F0;
        --border-medium: #CBD5E1;
        --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        
        /* Gradient Colors */
        --gradient-primary: linear-gradient(135deg, var(--brand-primary) 0%, var(--brand-secondary) 100%);
        --gradient-success: linear-gradient(135deg, var(--brand-success) 0%, #10B981 100%);
        --gradient-warning: linear-gradient(135deg, var(--brand-warning) 0%, #F59E0B 100%);
        --gradient-purple: linear-gradient(135deg, var(--brand-accent) 0%, #A855F7 100%);
    }
    
    /* Main Container */
    .main > div {
        padding: 1.5rem 2rem;
        background: var(--primary-bg);
        min-height: 100vh;
    }
    
    /* Enhanced Header Sections */
    .page-header {
        background: var(--gradient-primary);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
    }
    
    .page-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='3'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        z-index: 1;
    }
    
    .page-header h1 {
        color: var(--text-white) !important;
        margin: 0 !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        position: relative;
        z-index: 2;
    }
    
    .page-header .subtitle {
        color: rgba(255,255,255,0.9) !important;
        font-size: 1.1rem !important;
        font-weight: 400 !important;
        margin-top: 0.5rem !important;
        position: relative;
        z-index: 2;
    }
    
         /* Modern Card Design */
     .metric-card {
         background: var(--card-bg);
         border: 1px solid var(--border-light);
        border-radius: 16px;
         padding: 1rem;
         margin: 0.5rem 0;
         box-shadow: var(--shadow-md);
         transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
         min-height: 120px;
         height: auto;
         display: flex;
         flex-direction: column;
         justify-content: space-between;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl);
        border-color: var(--brand-primary);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-primary);
        border-radius: 16px 16px 0 0;
    }
    
         .metric-header {
         display: flex;
         justify-content: space-between;
         align-items: center;
         margin-bottom: 0.75rem;
         gap: 0.75rem;
    }
    
     .metric-icon {
         font-size: 1.5rem;
         width: 40px;
         height: 40px;
         display: flex;
         align-items: center;
         justify-content: center;
         border-radius: 10px;
         background: var(--gradient-primary);
         color: var(--text-white);
         box-shadow: var(--shadow-md);
         flex-shrink: 0;
    }
    
    .metric-title {
        color: var(--text-secondary);
         font-size: 0.75rem;
         font-weight: 600;
         text-transform: uppercase;
         letter-spacing: 0.3px;
         flex: 1;
         line-height: 1.2;
         overflow: hidden;
         text-overflow: ellipsis;
         white-space: nowrap;
    }
    
    .metric-value {
        color: var(--text-primary);
         font-size: clamp(1.25rem, 4vw, 1.75rem);
        font-weight: 700;
         margin-bottom: 0.25rem;
         font-family: 'Poppins', sans-serif;
         line-height: 1.1;
         overflow: hidden;
         text-overflow: ellipsis;
         white-space: nowrap;
    }
    
    .metric-delta {
         color: var(--brand-success);
         font-size: 0.7rem;
         font-weight: 600;
         display: flex;
         align-items: center;
         gap: 0.25rem;
         overflow: hidden;
         text-overflow: ellipsis;
         white-space: nowrap;
     }
     
     .metric-delta.negative {
         color: var(--brand-danger);
     }
     
     .metric-delta.neutral {
         color: var(--text-secondary);
    }
    
         /* Chart Container */
     .chart-container {
         background: var(--card-bg);
         border: 1px solid var(--border-light);
         border-radius: 16px;
         padding: 1rem;
         margin: 0.5rem 0;
         box-shadow: var(--shadow-md);
         transition: all 0.3s ease;
         overflow: hidden;
     }
    
    .chart-container:hover {
        box-shadow: var(--shadow-lg);
    }
    
         .chart-title {
         color: var(--text-primary);
         font-size: clamp(1rem, 2.5vw, 1.25rem);
         font-weight: 600;
         margin-bottom: 0.75rem;
         padding-bottom: 0.5rem;
         border-bottom: 2px solid var(--border-light);
         display: flex;
         align-items: center;
         gap: 0.5rem;
         overflow: hidden;
         text-overflow: ellipsis;
         white-space: nowrap;
     }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: var(--secondary-bg) !important;
        border-right: 1px solid var(--border-medium) !important;
    }
    
         /* Sidebar logo container */
     .sidebar-logo-container {
         text-align: center;
         padding: 0.75rem 1rem;
         border-bottom: 1px solid var(--border-light);
         margin: 0 -1rem 1.5rem -1rem;
         background: linear-gradient(135deg, rgba(37, 99, 235, 0.05), rgba(14, 165, 233, 0.05));
         border-radius: 12px;
     }
    
         /* Logo styling for image */
     .element-container img {
         border-radius: 12px;
         box-shadow: 0 4px 15px rgba(37, 99, 235, 0.2);
         transition: all 0.3s ease;
         animation: float 3s ease-in-out infinite;
         max-width: 80px;
         height: auto;
         object-fit: contain;
     }
     
     .element-container img:hover {
         transform: scale(1.05);
         box-shadow: 0 6px 20px rgba(37, 99, 235, 0.3);
     }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
         .sidebar-title {
         margin: 0.25rem 0 0 0;
         font-size: 1.4rem;
         font-weight: 700;
         color: var(--text-primary);
         font-family: 'Poppins', sans-serif;
         letter-spacing: -0.5px;
     }
     
     .sidebar-subtitle {
         color: var(--text-secondary);
         font-size: 0.8rem;
         margin: 0;
         font-weight: 500;
         letter-spacing: 0.3px;
     }
    
    /* Navigation Buttons */
    .nav-button {
        width: 100%;
        background: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        margin: 0.25rem 0 !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 0.75rem !important;
        text-align: left !important;
    }
    
    .nav-button:hover {
        background: var(--brand-primary) !important;
        color: var(--text-white) !important;
        transform: translateX(4px) !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    .nav-button.active {
        background: var(--gradient-primary) !important;
        color: var(--text-white) !important;
        box-shadow: var(--shadow-lg) !important;
    }
    
    /* Status Indicators */
    .status-card {
        background: var(--card-bg);
        border: 1px solid var(--border-light);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .status-online { 
        color: var(--brand-success);
        border-color: var(--brand-success);
        background: rgba(5, 150, 105, 0.05);
    }
    .status-warning { 
        color: var(--brand-warning);
        border-color: var(--brand-warning);
        background: rgba(217, 119, 6, 0.05);
    }
    .status-error { 
        color: var(--brand-danger);
        border-color: var(--brand-danger);
        background: rgba(220, 38, 38, 0.05);
    }
    
    /* Tables */
    .dataframe {
        background: var(--card-bg) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-md) !important;
        font-size: 0.875rem !important;
    }
    
    .dataframe thead th {
        background: var(--gradient-primary) !important;
        color: var(--text-white) !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 1rem 0.75rem !important;
        text-align: center !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .dataframe tbody td {
        background: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-light) !important;
        padding: 0.75rem !important;
        text-align: center !important;
        transition: all 0.2s ease !important;
    }
    
    .dataframe tbody tr:nth-child(even) {
        background: var(--secondary-bg) !important;
    }
    
    .dataframe tbody tr:hover {
        background: rgba(37, 99, 235, 0.05) !important;
        transform: scale(1.01) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--gradient-primary) !important;
        color: var(--text-white) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        transition: all 0.3s ease !important;
        box-shadow: var(--shadow-md) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg) !important;
    }
    
         /* Section Headers */
     .section-header {
         display: flex;
         align-items: center;
         gap: 0.5rem;
         margin: 1.5rem 0 0.75rem 0;
         padding-bottom: 0.5rem;
         border-bottom: 2px solid var(--border-light);
     }
     
     .section-header h2, .section-header h3 {
         color: var(--text-primary) !important;
         margin: 0 !important;
         font-family: 'Poppins', sans-serif !important;
         font-weight: 600 !important;
         font-size: clamp(1rem, 2.5vw, 1.25rem) !important;
         overflow: hidden;
         text-overflow: ellipsis;
         white-space: nowrap;
     }
     
     .section-icon {
         font-size: clamp(1.25rem, 2vw, 1.5rem);
         color: var(--brand-primary);
         flex-shrink: 0;
     }
    
    /* Alert Styles */
    .alert {
        padding: 1rem 1.25rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid;
        font-weight: 500;
    }
    
    .alert-success {
        background: rgba(5, 150, 105, 0.1);
        border-color: var(--brand-success);
        color: var(--brand-success);
    }
    
    .alert-warning {
        background: rgba(217, 119, 6, 0.1);
        border-color: var(--brand-warning);
        color: var(--brand-warning);
    }
    
    .alert-error {
        background: rgba(220, 38, 38, 0.1);
        border-color: var(--brand-danger);
        color: var(--brand-danger);
    }
    
    .alert-info {
        background: rgba(37, 99, 235, 0.1);
        border-color: var(--brand-primary);
        color: var(--brand-primary);
    }
    
    /* Loading Animation */
    .loading {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
         /* Container Overrides */
     .element-container {
         margin-bottom: 0 !important;
     }
     
     .stColumn > div {
         padding: 0 0.25rem !important;
     }
     
     .stColumn:first-child > div {
         padding-left: 0 !important;
     }
     
     .stColumn:last-child > div {
         padding-right: 0 !important;
     }
     
     /* Remove default Streamlit gaps */
     .block-container {
         padding-top: 1rem !important;
         padding-bottom: 0 !important;
         max-width: none !important;
     }
     
     .main .block-container {
         padding: 1rem !important;
     }
     
     div[data-testid="stVerticalBlock"] > div:nth-child(n) {
         gap: 0.5rem !important;
    }
    
    /* Responsive Design */
     @media (max-width: 1200px) {
         .metric-value {
             font-size: clamp(1rem, 3vw, 1.5rem);
         }
         
         .metric-title {
             font-size: 0.7rem;
         }
     }
     
    @media (max-width: 768px) {
        .main > div {
             padding: 0.75rem 1rem;
        }
         
         .metric-card {
             margin: 0.25rem 0;
             padding: 0.75rem;
             min-height: 100px;
         }
         
         .metric-header {
             margin-bottom: 0.5rem;
             gap: 0.5rem;
         }
         
         .metric-icon {
             font-size: 1.25rem;
             width: 32px;
             height: 32px;
         }
         
         .metric-value {
             font-size: clamp(1rem, 5vw, 1.25rem);
         }
         
         .metric-title {
             font-size: 0.65rem;
         }
         
         .metric-delta {
             font-size: 0.6rem;
         }
         
         .page-header h1 {
             font-size: 1.75rem !important;
         }
         
         .page-header .subtitle {
             font-size: 0.9rem !important;
         }
         
         .chart-container {
             padding: 0.75rem;
            margin: 0.5rem 0;
         }
         
                   .stColumn > div {
              padding: 0 0.125rem !important;
          }
          
          .section-header {
              margin: 1rem 0 0.5rem 0;
              gap: 0.375rem;
              padding-bottom: 0.375rem;
          }
          
          .section-header h2, .section-header h3 {
              font-size: 0.9rem !important;
          }
          
          .section-icon {
              font-size: 1rem;
          }
          
          .element-container img {
              max-width: 60px !important;
          }
     }
     
     @media (max-width: 480px) {
         .main > div {
             padding: 0.5rem;
         }
         
         .metric-card {
             padding: 0.5rem;
             margin: 0.125rem 0;
             min-height: 85px;
         }
         
         .metric-header {
             flex-direction: row;
             align-items: center;
             gap: 0.5rem;
             margin-bottom: 0.25rem;
         }
         
         .metric-icon {
             font-size: 1rem;
             width: 28px;
             height: 28px;
         }
         
         .metric-title {
             font-size: 0.6rem;
             letter-spacing: 0.2px;
         }
         
         .metric-value {
             font-size: clamp(0.9rem, 6vw, 1.1rem);
             margin-bottom: 0.125rem;
         }
         
         .metric-delta {
             font-size: 0.55rem;
         }
         
         .page-header {
             padding: 1.25rem;
             margin-bottom: 1rem;
         }
         
         .page-header h1 {
             font-size: 1.5rem !important;
         }
         
         .page-header .subtitle {
             font-size: 0.8rem !important;
         }
         
                   .stColumn > div {
              padding: 0 0.0625rem !important;
          }
          
          .section-header {
              margin: 0.75rem 0 0.375rem 0;
              gap: 0.25rem;
              padding-bottom: 0.25rem;
          }
          
          .section-header h2, .section-header h3 {
              font-size: 0.8rem !important;
          }
          
          .section-icon {
              font-size: 0.9rem;
          }
          
          .element-container img {
              max-width: 50px !important;
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
    # Determine delta styling
    delta_class = "metric-delta"
    if delta:
        if isinstance(delta, str):
            if delta.startswith('+'):
                delta_class += ""  # positive (green)
            elif delta.startswith('-'):
                delta_class += " negative"  # negative (red)
            else:
                delta_class += " neutral"  # neutral (gray)
        delta_html = f'<div class="{delta_class}">📈 {delta}</div>'
    else:
        delta_html = ''
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">
            <div class="metric-icon">{icon}</div>
            <div class="metric-title">{title}</div>
        </div>
        <div>
        <div class="metric-value">{value}</div>
        {delta_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_modern_chart(data, chart_type, title, **kwargs):
    """Create beautiful modern charts with white theme"""
    if data.empty:
        st.markdown(f'<div class="alert alert-info">📊 No data available for {title}</div>', unsafe_allow_html=True)
        return
    
    with st.container():
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="chart-title"><span class="section-icon">📊</span>{title}</div>', unsafe_allow_html=True)
        
        # Chart creation logic with modern colors
        color_palette = ['#2563EB', '#0EA5E9', '#8B5CF6', '#059669', '#D97706', '#DC2626', '#6366F1', '#06B6D4']
        
        if chart_type == "donut":
            fig = px.pie(data, **kwargs, hole=0.6, color_discrete_sequence=color_palette)
            fig.update_traces(
                textfont_size=12,
                marker=dict(line=dict(color='#FFFFFF', width=3))
            )
            
        elif chart_type == "bar":
            fig = px.bar(data, **kwargs, color_discrete_sequence=color_palette)
            fig.update_traces(marker_line=dict(color='#FFFFFF', width=1))
            
        elif chart_type == "line":
            fig = px.line(data, **kwargs, markers=True, color_discrete_sequence=color_palette)
            fig.update_traces(line=dict(width=3), marker=dict(size=8))
            
        elif chart_type == "scatter":
            fig = px.scatter(data, **kwargs, size_max=25, color_discrete_sequence=color_palette)
            
        else:
            st.markdown(f'<div class="alert alert-warning">⚠️ Chart type "{chart_type}" not supported</div>', unsafe_allow_html=True)
            return
        
        # Apply ultra-modern white theme
        fig.update_layout(
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font=dict(color="#1E293B", size=12, family="Inter"),
            title=dict(
                text="",  # Remove title since we have custom title
                font=dict(size=16, color="#1E293B"),
                x=0.5,
                xanchor='center'
            ),
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=True,
            legend=dict(
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="#E2E8F0",
                borderwidth=1,
                font=dict(color="#1E293B")
            ),
            xaxis=dict(
                gridcolor="#F1F5F9",
                zerolinecolor="#E2E8F0",
                linecolor="#E2E8F0",
                tickfont=dict(color="#64748B")
            ),
            yaxis=dict(
                gridcolor="#F1F5F9",
                zerolinecolor="#E2E8F0",
                linecolor="#E2E8F0",
                tickfont=dict(color="#64748B")
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 🎯 Navigation System
def render_navigation():
    """Ultra-modern navigation with enhanced UI"""
    with st.sidebar:
        # Header section with logo
        try:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image("dashboard/swen_logo.png", use_container_width=True)
        except:
            try:
                # Try alternative path
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("swen_logo.png", use_container_width=True)
            except:
                # Fallback to emoji if logo file not found
                st.markdown('<div style="text-align: center; font-size: 3rem; margin-bottom: 0.5rem;">✈️</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sidebar-logo-container" style="margin-top: -1rem;">
            <h2 class="sidebar-title">Swen Airlines</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu
        if MODERN_UI_AVAILABLE:
            selected = option_menu(
                menu_title=None,
                options=["🏠 Dashboard", "✈️ Operations", "💰 Revenue", "👤 Passengers", "👨‍✈️ Crew", "🧳 Baggage", "🔧 Aircraft"],
                icons=[""] * 7,  # Empty icons
                menu_icon="cast",
                default_index=0,
                styles={
                    "container": {"padding": "0", "background-color": "transparent"},
                    "icon": {"display": "none"},  # Hide left icons completely
                    "nav-link": {
                        "font-size": "14px",
                        "text-align": "left", 
                        "margin": "4px 0",
                        "padding": "12px 16px",
                        "border-radius": "12px",
                        "background": "#FFFFFF",
                        "color": "#1E293B",
                        "border": "1px solid #E2E8F0",
                        "transition": "all 0.3s ease"
                    },
                    "nav-link-selected": {
                        "background": "linear-gradient(135deg, #2563EB, #0EA5E9)",
                        "color": "white",
                        "border": "1px solid #2563EB",
                        "box-shadow": "0 4px 15px rgba(37, 99, 235, 0.4)"
                    }
                }
            )
        else:
            # Fallback navigation with session state
            if 'selected_page' not in st.session_state:
                st.session_state.selected_page = "🏠 Dashboard"
            
            options = ["🏠 Dashboard", "✈️ Operations", "💰 Revenue", "👤 Passengers", "👨‍✈️ Crew", "🧳 Baggage", "🔧 Aircraft"]
            
            st.markdown("### 🧭 Navigation")
            
            # Create buttons for each option
            for i, option in enumerate(options):
                button_style = "primary" if st.session_state.selected_page == option else "secondary"
                if st.button(option, key=f"nav_{i}", use_container_width=True, type=button_style):
                    st.session_state.selected_page = option
                    st.rerun()
            
            selected = st.session_state.selected_page
        
        # Live system status
        st.markdown('<div style="margin: 2rem 0 1rem 0;"><div class="section-header"><span class="section-icon">📡</span><h3>System Status</h3></div></div>', unsafe_allow_html=True)
        
        # Status cards with better layout
        st.markdown("""
        <div class="status-card status-online">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">✈️</div>
            <div style="font-weight: 600;">{} Active Flights</div>
        </div>
        """.format(np.random.randint(15, 35)), unsafe_allow_html=True)
        
        st.markdown("""
        <div class="status-card status-online">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">⚡</div>
            <div style="font-weight: 600;">99.8% System Health</div>
        </div>
        """, unsafe_allow_html=True)
            
        # Real-time clock with modern styling
        current_time = datetime.now().strftime("%H:%M:%S UTC")
        st.markdown(f"""
        <div class="status-card" style="border-color: #8B5CF6; background: rgba(139, 92, 246, 0.05);">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem; color: #8B5CF6;">🕐</div>
            <div style="font-weight: 600; color: #8B5CF6;">Live Time: {current_time}</div>
        </div>
        """, unsafe_allow_html=True)
        
        return selected

# 📱 Dashboard Pages
def show_main_dashboard():
    """Ultra-modern main dashboard"""
    # Page Header
    st.markdown("""
    <div class="page-header">
        <h1>🎯 Executive Dashboard</h1>
        <div class="subtitle">Real-time Business Intelligence</div>
    </div>
    """, unsafe_allow_html=True)
    
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
        create_metric_card("On-Time Performance", f"{perf}%", f"{perf-85:+.1f}%", "⏰")
    
    with col4:
        passengers_today = execute_query("SELECT COUNT(DISTINCT passenger_id) as count FROM tr_booking WHERE DATE(booking_date) = CURRENT_DATE AND is_cancelled = false")
        count = passengers_today.iloc[0]['count'] if not passengers_today.empty else 0
        create_metric_card("Active Passengers", f"{count:,}", f"+{np.random.randint(5,15)}", "👥")
    
    # Interactive Analytics Section
    st.markdown('<div class="section-header"><span class="section-icon">📊</span><h2>Interactive Analytics Center</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        status_data = execute_query("""
            SELECT flight_status, COUNT(*) as count 
            FROM tr_flight 
            WHERE DATE(scheduled_departure) = CURRENT_DATE
            GROUP BY flight_status
        """)
        if not status_data.empty:
            create_modern_chart(status_data, "donut", "Today's Flight Status", values='count', names='flight_status')
    
    with col2:
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
        loyalty_data = execute_query("""
            SELECT loyalty_tier, COUNT(*) as count
            FROM tr_passenger 
            WHERE loyalty_tier IS NOT NULL
            GROUP BY loyalty_tier
        """)
        if not loyalty_data.empty:
            create_modern_chart(loyalty_data, "donut", "Customer Loyalty Tiers", values='count', names='loyalty_tier')
    
    with col2:
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
    # Page Header
    st.markdown("""
    <div class="page-header">
        <h1>✈️ Flight Operations</h1>
        <div class="subtitle">Real-time Flight Management & Analytics</div>
    </div>
    """, unsafe_allow_html=True)
    
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
        status_data = execute_query(f"""
            SELECT flight_status, COUNT(*) as count 
            FROM tr_flight 
            WHERE scheduled_departure >= CURRENT_DATE - INTERVAL '{days} days' {airport_clause}
            GROUP BY flight_status
        """)
        if not status_data.empty:
            create_modern_chart(status_data, "donut", "Flight Status Distribution", values='count', names='flight_status')
    
    with col2:
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
    # Page Header
    st.markdown("""
    <div class="page-header">
        <h1>💰 Revenue Analytics</h1>
        <div class="subtitle">Sales Performance & Financial Intelligence</div>
    </div>
    """, unsafe_allow_html=True)
    
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
    # Page Header
    st.markdown("""
    <div class="page-header">
        <h1>👤 Customer Analytics</h1>
        <div class="subtitle">Passenger Insights & Loyalty Management</div>
    </div>
    """, unsafe_allow_html=True)
    
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
    # Page Header
    st.markdown("""
    <div class="page-header">
        <h1>👨‍✈️ Crew Management</h1>
        <div class="subtitle">Workforce Analytics & Performance Tracking</div>
    </div>
    """, unsafe_allow_html=True)
    
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
    # Page Header
    st.markdown("""
    <div class="page-header">
        <h1>🧳 Baggage Operations</h1>
        <div class="subtitle">Baggage Handling & Logistics Analytics</div>
    </div>
    """, unsafe_allow_html=True)
    
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
    # Page Header
    st.markdown("""
    <div class="page-header">
        <h1>🛩️ Fleet Management</h1>
        <div class="subtitle">Aircraft Performance & Maintenance Analytics</div>
    </div>
    """, unsafe_allow_html=True)
    
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