import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def create_kpi_card(title, value, subtitle="", delta=None, delta_color="normal"):
    """Modern KPI kartı oluşturur"""
    fig = go.Figure()
    
    fig.add_trace(go.Indicator(
        mode = "number+delta" if delta else "number",
        value = value,
        title = {"text": title, "font": {"size": 20}},
        number = {"font": {"size": 40, "color": "#1f4e79"}},
        delta = {"reference": delta, "valueformat": ".1f"} if delta else None,
        domain = {'x': [0, 1], 'y': [0, 1]}
    ))
    
    fig.update_layout(
        height=150,
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def create_donut_chart(data, values_col, names_col, title, colors=None):
    """Modern donut chart oluşturur"""
    if data.empty:
        fig = go.Figure()
        fig.add_annotation(text="Veri bulunamadı", 
                         xref="paper", yref="paper", 
                         x=0.5, y=0.5, 
                         showarrow=False)
        fig.update_layout(title=title)
        return fig
        
    fig = px.pie(data, values=values_col, names=names_col, 
                 hole=0.6, title=title)
    
    if colors:
        fig.update_traces(marker_colors=colors)
    
    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5),
        font=dict(size=12),
        title_font_size=16
    )
    
    return fig

def create_trend_chart(data, x_col, y_col, title, color="#3498db"):
    """Trend çizgi grafiği oluşturur"""
    if data.empty:
        fig = go.Figure()
        fig.add_annotation(text="Veri bulunamadı", 
                         xref="paper", yref="paper", 
                         x=0.5, y=0.5, 
                         showarrow=False)
        fig.update_layout(title=title)
        return fig
        
    fig = px.line(data, x=x_col, y=y_col, title=title,
                  markers=True, line_shape="spline")
    
    fig.update_traces(line_color=color, line_width=3, 
                      marker_size=8, marker_color=color)
    
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        hovermode='x unified',
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def create_horizontal_bar(data, x_col, y_col, title, color_scale="Blues"):
    """Yatay bar chart oluşturur"""
    fig = px.bar(data, x=x_col, y=y_col, orientation='h',
                 title=title, color=x_col, color_continuous_scale=color_scale)
    
    fig.update_layout(
        showlegend=False,
        yaxis={'categoryorder':'total ascending'},
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def create_stacked_bar(data, x_col, y_col, color_col, title):
    """Stacked bar chart oluşturur"""
    if data.empty:
        fig = go.Figure()
        fig.add_annotation(text="Veri bulunamadı", 
                         xref="paper", yref="paper", 
                         x=0.5, y=0.5, 
                         showarrow=False)
        fig.update_layout(title=title)
        return fig
        
    fig = px.bar(data, x=x_col, y=y_col, color=color_col,
                 title=title, barmode='stack')
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    
    return fig

def create_scatter_plot(data, x_col, y_col, size_col, color_col, title):
    """Scatter plot oluşturur"""
    if data.empty:
        fig = go.Figure()
        fig.add_annotation(text="Veri bulunamadı", 
                         xref="paper", yref="paper", 
                         x=0.5, y=0.5, 
                         showarrow=False)
        fig.update_layout(title=title)
        return fig
        
    fig = px.scatter(data, x=x_col, y=y_col, size=size_col, 
                     color=color_col, title=title, 
                     hover_data=[size_col])
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def create_gauge_chart(value, title, max_value=100, threshold1=70, threshold2=90):
    """Gauge chart oluşturur"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 16}},
        gauge = {
            'axis': {'range': [None, max_value], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, threshold1], 'color': 'lightgray'},
                {'range': [threshold1, threshold2], 'color': 'yellow'},
                {'range': [threshold2, max_value], 'color': 'green'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def create_heatmap(data, x_col, y_col, z_col, title):
    """Heatmap oluşturur"""
    pivot_data = data.pivot(index=y_col, columns=x_col, values=z_col)
    
    fig = px.imshow(pivot_data, 
                    title=title,
                    color_continuous_scale='RdYlBu_r',
                    aspect="auto")
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def create_waterfall_chart(categories, values, title):
    """Waterfall chart oluşturur"""
    fig = go.Figure(go.Waterfall(
        name = title,
        orientation = "v",
        measure = ["relative"] * (len(categories) - 1) + ["total"],
        x = categories,
        textposition = "outside",
        text = [f"+{v}" if v > 0 else str(v) for v in values],
        y = values,
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))
    
    fig.update_layout(
        title=title,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def calculate_performance_metrics(data):
    """Performance metrikleri hesaplar"""
    if data.empty:
        return {}
    
    metrics = {}
    
    # Temel istatistikler
    metrics['total_records'] = len(data)
    
    # Numerik kolonlar için
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        metrics[f'{col}_avg'] = data[col].mean()
        metrics[f'{col}_sum'] = data[col].sum()
        metrics[f'{col}_max'] = data[col].max()
        metrics[f'{col}_min'] = data[col].min()
    
    return metrics

def format_number(num, format_type="standard"):
    """Sayıları formatlı hale getirir"""
    if pd.isna(num):
        return "N/A"
    
    if format_type == "currency":
        return f"${num:,.2f}"
    elif format_type == "percentage":
        return f"{num:.1f}%"
    elif format_type == "integer":
        return f"{int(num):,}"
    else:
        return f"{num:,.2f}" 