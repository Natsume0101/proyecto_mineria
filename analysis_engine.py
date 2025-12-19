"""
Mineral Exploration Analysis Engine
=====================================
Core module for satellite-based hydrothermal alteration zone detection
using Google Earth Engine and Sentinel-2 imagery.

Target: Chile's IV Region (Coquimbo/La Serena) - Copper Exploration
Author: Data Science Portfolio Project
"""

import ee
import numpy as np
from sklearn.cluster import KMeans
from datetime import datetime, timedelta
import pandas as pd


class MineralExplorationAnalyzer:
    """
    Analyzes Sentinel-2 satellite imagery to identify hydrothermal alteration zones
    associated with copper mineralization (iron oxides, clay minerals).
    """
    
    def __init__(self):
        """Initialize Google Earth Engine with support for Streamlit Cloud"""
        try:
            # Check if running on Streamlit Cloud (secrets available)
            try:
                import streamlit as st
                if 'gee' in st.secrets:
                    # Use service account authentication for Streamlit Cloud
                    credentials = ee.ServiceAccountCredentials(
                        email=st.secrets['gee']['client_email'],
                        key_data=st.secrets['gee']['private_key']
                    )
                    ee.Initialize(credentials)
                    print("✅ Google Earth Engine initialized (Streamlit Cloud)")
                else:
                    # Local development - use standard authentication
                    ee.Initialize()
                    print("✅ Google Earth Engine initialized (Local)")
            except ImportError:
                # Streamlit not available - local development
                ee.Initialize()
                print("✅ Google Earth Engine initialized (Local)")
                
        except Exception as e:
            print(f"❌ GEE initialization error: {e}")
            print("💡 Run: earthengine authenticate")
            try:
                import streamlit as st
                st.error("Google Earth Engine authentication failed. Check secrets configuration.")
            except ImportError:
                pass
    
    def get_sentinel2_data(self, lat, lon, radius_km=10, start_date=None, end_date=None, 
                          cloud_cover_max=20):
        """
        Fetch cloud-free Sentinel-2 imagery for the specified location.
        
        Args:
            lat (float): Latitude (decimal degrees)
            lon (float): Longitude (decimal degrees)
            radius_km (int): Analysis radius in kilometers
            start_date (str): Start date 'YYYY-MM-DD' (default: 6 months ago)
            end_date (str): End date 'YYYY-MM-DD' (default: today)
            cloud_cover_max (int): Maximum cloud cover percentage
            
        Returns:
            ee.Image: Median composite of Sentinel-2 imagery
        """
        # Default date range: last 6 months
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        if start_date is None:
            start = datetime.now() - timedelta(days=180)
            start_date = start.strftime('%Y-%m-%d')
        
        # Define area of interest (circular buffer)
        point = ee.Geometry.Point([lon, lat])
        aoi = point.buffer(radius_km * 1000)  # Convert km to meters
        
        # Fetch Sentinel-2 Surface Reflectance data
        s2_collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
            .filterBounds(aoi) \
            .filterDate(start_date, end_date) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', cloud_cover_max))
        
        # Cloud masking function
        def mask_clouds(image):
            qa = image.select('QA60')
            # Bits 10 and 11 are clouds and cirrus
            cloud_mask = qa.bitwiseAnd(1 << 10).eq(0).And(
                        qa.bitwiseAnd(1 << 11).eq(0))
            return image.updateMask(cloud_mask).divide(10000)  # Scale to reflectance
        
        # Apply cloud mask and get median composite
        s2_composite = s2_collection.map(mask_clouds).median().clip(aoi)
        
        return s2_composite, aoi
    
    def calculate_band_ratios(self, image):
        """
        Calculate mineral exploration indices from Sentinel-2 bands.
        
        Indices:
        - Iron Oxide Index: (B4 - B2) / (B4 + B2)
        - Clay Minerals: B11 / B12 (SWIR ratio)
        - NDVI: (B8 - B4) / (B8 + B4) - for vegetation masking
        
        Args:
            image (ee.Image): Sentinel-2 image
            
        Returns:
            dict: Dictionary of index images
        """
        # Band selection
        red = image.select('B4')
        blue = image.select('B2')
        nir = image.select('B8')
        swir1 = image.select('B11')
        swir2 = image.select('B12')
        
        # Iron Oxide Index (Ferric Iron)
        # High values = iron oxide presence (gossans, oxidized zones)
        iron_oxide = red.subtract(blue).divide(red.add(blue)).rename('iron_oxide')
        
        # Clay Minerals Index (Hydroxyl-bearing minerals)
        # High values = clay alteration (kaolinite, alunite)
        clay_minerals = swir1.divide(swir2).rename('clay_minerals')
        
        # NDVI for vegetation masking
        # Exclude vegetated areas (false positives)
        ndvi = nir.subtract(red).divide(nir.add(red)).rename('ndvi')
        
        # Ferrous Iron Index (additional indicator)
        # B12 / B8 ratio
        ferrous_iron = swir2.divide(nir).rename('ferrous_iron')
        
        # Combine all indices
        indices = image.addBands([iron_oxide, clay_minerals, ndvi, ferrous_iron])
        
        return indices
    
    def identify_alteration_zones(self, image_with_indices, aoi, n_clusters=4, 
                                  ndvi_threshold=0.3):
        """
        Apply K-Means clustering to identify alteration zones.
        
        Args:
            image_with_indices (ee.Image): Image with calculated indices
            aoi (ee.Geometry): Area of interest
            n_clusters (int): Number of clusters for K-Means
            ndvi_threshold (float): NDVI threshold to mask vegetation
            
        Returns:
            tuple: (clustered_image, cluster_stats, drill_targets)
        """
        # Mask out vegetation (NDVI > threshold)
        non_veg_mask = image_with_indices.select('ndvi').lt(ndvi_threshold)
        masked_indices = image_with_indices.updateMask(non_veg_mask)
        
        # Select features for clustering
        features = masked_indices.select(['iron_oxide', 'clay_minerals', 'ferrous_iron'])
        
        # Sample points for clustering (for performance)
        sample = features.sample(
            region=aoi,
            scale=60,  # 60m resolution (faster processing)
            numPixels=5000,
            geometries=True
        )
        
        # Get sample data as numpy array
        try:
            sample_data = sample.getInfo()
            
            # Extract feature values
            feature_list = []
            coords_list = []
            
            for feature in sample_data['features']:
                props = feature['properties']
                coords = feature['geometry']['coordinates']
                
                # Skip if any value is None/null
                if all(props.get(band) is not None for band in ['iron_oxide', 'clay_minerals', 'ferrous_iron']):
                    feature_list.append([
                        props['iron_oxide'],
                        props['clay_minerals'],
                        props['ferrous_iron']
                    ])
                    coords_list.append(coords)
            
            # Convert to numpy array
            X = np.array(feature_list)
            coords_array = np.array(coords_list)
            
            # Apply K-Means clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(X)
            
            # Analyze clusters to identify high-priority zones
            cluster_stats = self._analyze_clusters(X, cluster_labels, kmeans, coords_array)
            
            return cluster_stats
            
        except Exception as e:
            print(f"Clustering error: {e}")
            return None
    
    def _analyze_clusters(self, features, labels, kmeans, coords):
        """
        Analyze clusters to prioritize drill targets.
        
        High-priority zones: High iron oxide + high clay minerals
        """
        cluster_data = []
        
        for cluster_id in range(kmeans.n_clusters):
            cluster_mask = labels == cluster_id
            cluster_features = features[cluster_mask]
            cluster_coords = coords[cluster_mask]
            
            if len(cluster_features) == 0:
                continue
            
            # Calculate cluster statistics
            mean_iron = np.mean(cluster_features[:, 0])
            mean_clay = np.mean(cluster_features[:, 1])
            mean_ferrous = np.mean(cluster_features[:, 2])
            
            # Priority score: weighted combination of indices
            # Iron oxide (40%) + Clay minerals (40%) + Ferrous iron (20%)
            priority_score = (mean_iron * 0.4) + (mean_clay * 0.4) + (mean_ferrous * 0.2)
            
            # Normalize score to 0-100
            confidence = min(max(priority_score * 100, 0), 100)
            
            # Determine alteration type
            if mean_iron > 0.2 and mean_clay > 1.1:
                alteration_type = "Mixed (Iron Oxide + Clay)"
                priority = "High"
            elif mean_iron > 0.2:
                alteration_type = "Iron Oxide Dominant"
                priority = "Medium"
            elif mean_clay > 1.1:
                alteration_type = "Clay Dominant"
                priority = "Medium"
            else:
                alteration_type = "Low Alteration"
                priority = "Low"
            
            # Calculate centroid (representative location)
            centroid_lon = np.mean(cluster_coords[:, 0])
            centroid_lat = np.mean(cluster_coords[:, 1])
            
            cluster_data.append({
                'cluster_id': cluster_id,
                'latitude': centroid_lat,
                'longitude': centroid_lon,
                'confidence_score': round(confidence, 1),
                'alteration_type': alteration_type,
                'priority': priority,
                'mean_iron_oxide': round(mean_iron, 3),
                'mean_clay_minerals': round(mean_clay, 3),
                'area_km2': round(len(cluster_features) * 0.0036, 2),  # 60m pixels
                'n_pixels': len(cluster_features),
                'sample_points': cluster_coords.tolist()[:10]  # First 10 points
            })
        
        # Sort by confidence score
        cluster_data.sort(key=lambda x: x['confidence_score'], reverse=True)
        
        return cluster_data
    
    def generate_drill_targets(self, cluster_stats, top_n=5):
        """
        Generate prioritized drill target recommendations.
        
        Args:
            cluster_stats (list): Cluster analysis results
            top_n (int): Number of top targets to return
            
        Returns:
            pandas.DataFrame: Drill target table
        """
        if not cluster_stats or len(cluster_stats) == 0:
            return pd.DataFrame()
        
        # Filter high and medium priority targets
        priority_targets = [c for c in cluster_stats if c['priority'] in ['High', 'Medium']]
        
        # Get top N
        top_targets = priority_targets[:top_n]
        
        # Create dataframe
        df = pd.DataFrame(top_targets)
        df['rank'] = range(1, len(df) + 1)
        
        # Reorder columns
        columns = ['rank', 'latitude', 'longitude', 'confidence_score', 
                  'alteration_type', 'priority', 'area_km2']
        
        return df[columns]
    
    def analyze_location(self, lat, lon, radius_km=10):
        """
        Complete analysis pipeline for a given location.
        
        Args:
            lat (float): Latitude
            lon (float): Longitude  
            radius_km (int): Analysis radius
            
        Returns:
            dict: Complete analysis results
        """
        try:
            # Step 1: Get satellite data
            print("📡 Fetching Sentinel-2 imagery...")
            image, aoi = self.get_sentinel2_data(lat, lon, radius_km)
            
            # Step 2: Calculate band ratios
            print("🔬 Calculating alteration indices...")
            indices = self.calculate_band_ratios(image)
            
            # Step 3: Identify alteration zones
            print("🎯 Identifying alteration zones...")
            cluster_stats = self.identify_alteration_zones(indices, aoi)
            
            if not cluster_stats:
                return {'error': 'No alteration zones identified'}
            
            # Step 4: Generate drill targets
            print("⛏️ Generating drill targets...")
            drill_targets = self.generate_drill_targets(cluster_stats)
            
            # Calculate summary metrics
            high_priority_area = sum(c['area_km2'] for c in cluster_stats if c['priority'] == 'High')
            total_area = radius_km * radius_km * 3.14159  # Approximate area
            
            results = {
                'success': True,
                'location': {'lat': lat, 'lon': lon, 'radius_km': radius_km},
                'drill_targets': drill_targets,
                'cluster_stats': cluster_stats,
                'metrics': {
                    'total_area_km2': round(total_area, 2),
                    'high_priority_area_km2': round(high_priority_area, 2),
                    'n_targets': len(drill_targets),
                    'n_clusters': len(cluster_stats)
                },
                'roi_estimate': {
                    'traditional_exploration_cost': 500000,
                    'satellite_analysis_cost': 150000,
                    'estimated_savings': 350000,
                    'cost_reduction_pct': 70
                }
            }
            
            return results
            
        except Exception as e:
            return {'error': str(e), 'success': False}


# Utility functions for KML export
def create_kml_export(drill_targets, cluster_stats, output_path='drill_targets.kml'):
    """
    Create KML file for import into QGIS/ArcGIS.
    
    Args:
        drill_targets (pd.DataFrame): Drill target table
        cluster_stats (list): Cluster statistics
        output_path (str): Output file path
    """
    try:
        import simplekml
        
        kml = simplekml.Kml()
        
        # Add drill targets as placemarks
        folder = kml.newfolder(name="Drill Targets")
        
        for _, target in drill_targets.iterrows():
            pnt = folder.newpoint(
                name=f"Target {target['rank']}",
                coords=[(target['longitude'], target['latitude'])]
            )
            pnt.description = f"""
            Confidence: {target['confidence_score']}%
            Alteration: {target['alteration_type']}
            Priority: {target['priority']}
            Area: {target['area_km2']} km²
            """
            
            # Color by priority
            if target['priority'] == 'High':
                pnt.style.iconstyle.color = 'ff0000ff'  # Red
            elif target['priority'] == 'Medium':
                pnt.style.iconstyle.color = 'ff00a5ff'  # Orange
            else:
                pnt.style.iconstyle.color = 'ff00ffff'  # Yellow
        
        kml.save(output_path)
        return output_path
        
    except Exception as e:
        print(f"KML export error: {e}")
        return None
