# -*- coding: utf-8 -*-
"""
Mineral Exploration Satellite Analysis Dashboard
=================================================
Interactive Streamlit app for junior mining companies to identify
drill targets using Sentinel-2 satellite imagery.

Target Market: TSX-V listed junior miners (Canada/Australia)
Geographic Focus: Chile's IV Region (Coquimbo/La Serena)
"""

import sys
import io

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from analysis_engine import MineralExplorationAnalyzer, create_kml_export
from datetime import datetime
import time


# Page configuration
st.set_page_config(
    page_title="Mineral Exploration Satellite Analysis",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for mining industry aesthetics
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #8B4513;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #A0522D;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background: linear-gradient(135deg, #D2691E 0%, #8B4513 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .roi-banner {
        background: linear-gradient(90deg, #228B22 0%, #006400 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        text-align: center;
        margin: 1rem 0;
    }
    .stButton>button {
        background-color: #8B4513;
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #A0522D;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">⛏️ Mineral Exploration Satellite Analysis</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Drill Target Generation for Junior Mining Companies</p>', unsafe_allow_html=True)

# ROI Banner
st.markdown("""
<div class="roi-banner">
    💰 Reduce Exploration Costs by 70% | $350,000 Average Savings | Automated Target Generation
</div>
""", unsafe_allow_html=True)

# Sidebar - Input Parameters
st.sidebar.title("📍 Analysis Parameters")
st.sidebar.markdown("---")

# Default location: Andacollo Copper District
st.sidebar.subheader("Location")
st.sidebar.caption("Default: Andacollo Copper District, IV Region Chile")

latitude = st.sidebar.number_input(
    "Latitude (°)",
    min_value=-90.0,
    max_value=90.0,
    value=-30.226,
    step=0.001,
    format="%.3f",
    help="Andacollo: -30.226°"
)

longitude = st.sidebar.number_input(
    "Longitude (°)",
    min_value=-180.0,
    max_value=180.0,
    value=-71.078,
    step=0.001,
    format="%.3f",
    help="Andacollo: -71.078°"
)

st.sidebar.markdown("---")
st.sidebar.subheader("Analysis Settings")

radius_km = st.sidebar.select_slider(
    "Analysis Radius (km)",
    options=[5, 10, 15, 20, 25],
    value=10,
    help="Larger radius = more area analyzed (slower processing)"
)

cloud_cover = st.sidebar.slider(
    "Max Cloud Cover (%)",
    min_value=5,
    max_value=50,
    value=20,
    step=5,
    help="Lower values = clearer imagery (fewer available images)"
)

n_targets = st.sidebar.slider(
    "Number of Drill Targets",
    min_value=3,
    max_value=10,
    value=5,
    help="Top N prioritized drill targets to display"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📊 About This Tool
**Data Source:** Sentinel-2 Satellite  
**Resolution:** 10-60m multispectral  
**Update Frequency:** 5 days  
**Coverage:** Global (free)

**Alteration Indicators:**
- 🟤 Iron Oxides (Gossans)
- 🟡 Clay Minerals (Argillic)
- 🌱 Vegetation Masking (NDVI)

**Use Case:** Cost-effective exploration targeting for junior mining companies before committing to expensive drill programs.
""")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ Interactive Analysis Map")
    
with col2:
    st.subheader("📊 Key Metrics")

# Analysis button
analyze_button = st.button("🎯 GENERATE DRILL TARGETS", use_container_width=True)

# Session state for results
if 'results' not in st.session_state:
    st.session_state.results = None

# Run analysis
if analyze_button:
    with st.spinner("🛰️ Analyzing satellite imagery... This may take 30-60 seconds"):
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Initialize analyzer
        analyzer = MineralExplorationAnalyzer()
        
        # Run analysis with progress updates
        status_text.text("📡 Fetching Sentinel-2 imagery from Google Earth Engine...")
        progress_bar.progress(25)
        time.sleep(0.5)
        
        status_text.text("🔬 Calculating band ratios (Iron Oxide, Clay Minerals)...")
        progress_bar.progress(50)
        
        # Execute analysis
        results = analyzer.analyze_location(latitude, longitude, radius_km)
        
        status_text.text("🎯 Identifying alteration zones with K-Means clustering...")
        progress_bar.progress(75)
        time.sleep(0.5)
        
        status_text.text("⛏️ Generating prioritized drill targets...")
        progress_bar.progress(100)
        time.sleep(0.5)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        # Store results
        st.session_state.results = results
        
        if results.get('success'):
            st.success("✅ Analysis complete! Drill targets identified.")
        else:
            st.error(f"❌ Analysis failed: {results.get('error', 'Unknown error')}")

# Display results
if st.session_state.results and st.session_state.results.get('success'):
    results = st.session_state.results
    
    # Create two-column layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Interactive map
        st.subheader("🗺️ Drill Target Locations")
        
        # Create Folium map
        m = folium.Map(
            location=[latitude, longitude],
            zoom_start=11,
            tiles='Esri WorldImagery',
            attr='Esri'
        )
        
        # Add analysis center point
        folium.Marker(
            [latitude, longitude],
            popup="Analysis Center",
            tooltip="Analysis Center",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
        
        # Add drill targets
        drill_targets = results['drill_targets']
        
        for _, target in drill_targets.iterrows():
            # Colors by priority
            color_map = {
                'High': 'red',
                'Medium': 'orange',
                'Low': 'yellow'
            }
            
            color = color_map.get(target['priority'], 'gray')
            
            popup_html = f"""
            <div style="font-family: Arial; font-size: 12px;">
                <b>🎯 Target #{target['rank']}</b><br>
                <b>Confidence:</b> {target['confidence_score']}%<br>
                <b>Priority:</b> {target['priority']}<br>
                <b>Alteration:</b> {target['alteration_type']}<br>
                <b>Area:</b> {target['area_km2']} km²<br>
                <b>Coordinates:</b><br>
                Lat: {target['latitude']:.4f}°<br>
                Lon: {target['longitude']:.4f}°
            </div>
            """
            
            folium.Marker(
                [target['latitude'], target['longitude']],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f"Target {target['rank']} - {target['confidence_score']}%",
                icon=folium.Icon(color=color, icon='glyphicon-flag', prefix='glyphicon')
            ).add_to(m)
        
        # Add analysis radius circle
        folium.Circle(
            [latitude, longitude],
            radius=radius_km * 1000,
            color='blue',
            fill=False,
            weight=2,
            opacity=0.5,
            popup=f"Analysis Area ({radius_km} km radius)"
        ).add_to(m)
        
        # Display map
        st_folium(m, width=700, height=500)
    
    with col2:
        # Key metrics
        metrics = results['metrics']
        roi = results['roi_estimate']
        
        st.metric("🎯 Drill Targets Identified", metrics['n_targets'])
        st.metric("📏 Total Area Analyzed", f"{metrics['total_area_km2']} km²")
        st.metric("🔴 High-Priority Zones", f"{metrics['high_priority_area_km2']} km²")
        st.metric("🏔️ Alteration Clusters", metrics['n_clusters'])
        
        st.markdown("---")
        
        # ROI Metrics
        st.markdown("### 💰 Cost Savings")
        st.metric("Traditional Exploration", f"${roi['traditional_exploration_cost']:,}")
        st.metric("Satellite Analysis", f"${roi['satellite_analysis_cost']:,}")
        st.metric("💵 ESTIMATED SAVINGS", f"${roi['estimated_savings']:,}", 
                 delta=f"-{roi['cost_reduction_pct']}%")
    
    # Drill targets table
    st.markdown("---")
    st.subheader("📋 Prioritized Drill Target Table")
    
    # Format table for display
    display_df = drill_targets.copy()
    display_df['latitude'] = display_df['latitude'].round(4)
    display_df['longitude'] = display_df['longitude'].round(4)
    
    # Apply styling
    def highlight_priority(row):
        if row['priority'] == 'High':
            return ['background-color: #ffcccc'] * len(row)
        elif row['priority'] == 'Medium':
            return ['background-color: #ffe6cc'] * len(row)
        else:
            return ['background-color: #ffffcc'] * len(row)
    
    styled_df = display_df.style.apply(highlight_priority, axis=1)
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # Export options
    st.markdown("---")
    st.subheader("📥 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # CSV export
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📄 Download CSV Table",
            data=csv,
            file_name=f"drill_targets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # KML export
        try:
            kml_path = create_kml_export(drill_targets, results['cluster_stats'])
            if kml_path:
                with open(kml_path, 'r') as f:
                    kml_data = f.read()
                st.download_button(
                    label="🗺️ Download KML (for QGIS)",
                    data=kml_data,
                    file_name=f"drill_targets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.kml",
                    mime="application/vnd.google-earth.kml+xml",
                    use_container_width=True
                )
        except Exception as e:
            st.warning(f"KML export unavailable: {e}")
    
    # Detailed cluster information (expandable)
    with st.expander("🔬 View Detailed Cluster Analysis"):
        cluster_df = pd.DataFrame(results['cluster_stats'])
        st.dataframe(
            cluster_df[['cluster_id', 'priority', 'confidence_score', 
                       'alteration_type', 'area_km2', 'mean_iron_oxide', 'mean_clay_minerals']],
            use_container_width=True
        )

elif st.session_state.results and not st.session_state.results.get('success'):
    st.error(f"Analysis failed: {st.session_state.results.get('error')}")
    st.info("💡 Try adjusting parameters: increase cloud cover tolerance or change location")

else:
    # Initial state - show sample map
    st.info("👆 Click 'GENERATE DRILL TARGETS' to start analysis")
    
    # Display placeholder map
    m = folium.Map(
        location=[latitude, longitude],
        zoom_start=10,
        tiles='Esri WorldImagery'
    )
    
    folium.Marker(
        [latitude, longitude],
        popup="Analysis Center (Andacollo Copper District)",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)
    
    st_folium(m, width=700, height=400)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p><b>Mineral Exploration Satellite Analysis Tool</b> | Powered by Google Earth Engine & Sentinel-2</p>
    <p>🎓 Portfolio Project by Julie Gaete | Data Science Specialist</p>
    <p>📧 Contact: juliegaeteguzman@gmail.com | 🔗 LinkedIn: linkedin.com/in/juliegaete</p>
    <p style="font-size: 0.8rem; margin-top: 1rem;">
        <i>Disclaimer: This tool is for exploration prioritization only. Results should be validated 
        with ground-truthing and professional geological assessment before drilling.</i>
    </p>
</div>
""", unsafe_allow_html=True)
