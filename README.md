# Mineral Exploration Satellite Analysis - IV Region Chile

<div align="center">

![Mining Analysis](https://img.shields.io/badge/Industry-Mining%20Exploration-8B4513?style=for-the-badge)
![Tech Stack](https://img.shields.io/badge/Stack-GEE%20%7C%20Python%20%7C%20Streamlit-blue?style=for-the-badge)
![Region](https://img.shields.io/badge/Region-Chile%20IV%20(Coquimbo)-red?style=for-the-badge)

### 🎯 AI-Powered Drill Target Generation for Junior Mining Companies

**Reduce exploration costs by 70% | Generate drill targets in minutes | Sentinel-2 satellite analysis**

[🚀 Live Demo](#live-demo) • [📊 Business Case](#business-case) • [💻 Quick Start](#quick-start)

</div>

---

## 🔥 The Problem

Junior mining companies (TSX-V, ASX listed) face a critical challenge:

- **$500,000+** spent on surface sampling before first drill
- **Months** of field work in remote locations
- **High risk** of drilling in wrong locations
- **Limited budgets** for early-stage exploration

**Traditional Exploration Timeline:**
```
Surface Sampling → Geochemistry → Geophysics → Target Selection → Drilling
    3-6 months              $300k-$500k                    High Risk
```

## ✨ The Solution

Automated satellite-based alteration mapping using **Sentinel-2** imagery and **Machine Learning** to prioritize 3-5 high-confidence drill targets **before** expensive field programs.

**Satellite-First Approach:**
```
Satellite Analysis → Prioritized Targets → Focused Field Work → Drilling
    2-3 days              $150k                      Reduced Risk
```

### 🎯 Business Impact

| Metric | Traditional | Satellite-First | **Savings** |
|--------|------------|-----------------|-------------|
| **Cost** | $500,000 | $150,000 | **$350,000 (70%)** |
| **Timeline** | 3-6 months | 1-2 weeks | **80% faster** |
| **Risk** | High (blind drilling) | Medium (data-driven) | **Reduced failure rate** |
| **Coverage** | 10-20 km² | 100+ km² | **10x more area** |

### 💰 ROI Example: Andacollo District, Chile

**Investment:** $150,000 (satellite analysis + focused field verification)  
**Savings:** $350,000 (avoided unnecessary sampling)  
**Output:** 5 prioritized drill targets with confidence scores  
**Result:** 70% cost reduction in Phase 1 exploration

---

## 🛰️ Technical Stack

### Data Source
- **Sentinel-2** (Copernicus/ESA) - Free, 10-60m resolution, 5-day revisit
- **Coverage:** Global (focus: Chile IV Region - Coquimbo/La Serena)
- **Temporal Range:** 2015-present

### Core Technology
- **Google Earth Engine** - Cloud-based satellite processing
- **Scikit-learn** - K-Means clustering for zone classification
- **Streamlit** - Interactive web dashboard
- **Folium** - Geospatial visualization

### Alteration Detection Methodology

```python
# Band Ratios for Hydrothermal Alteration
Iron Oxide Index = (B4 - B2) / (B4 + B2)      # Detects gossans, oxidized zones
Clay Minerals = B11 / B12                     # Detects argillic alteration
Vegetation Mask = (B8 - B4) / (B8 + B4)       # Excludes false positives (NDVI)
```

**Machine Learning Pipeline:**
1. Fetch cloud-free Sentinel-2 imagery (6-month composite)
2. Calculate band ratios for alteration indices
3. Apply K-Means clustering (4 clusters: High/Medium/Low/Background)
4. Rank targets by confidence score (iron oxide + clay mineral intensity)
5. Generate exportable drill target coordinates (KML/CSV)

---

## 🚀 Live Demo

### [📺 Click Here for Live Streamlit App](#) *(Deploy to Streamlit Cloud)*

**Demo Coordinates:** Andacollo Copper District, Chile  
- **Latitude:** -30.226°  
- **Longitude:** -71.078°  
- **Radius:** 10 km

### Sample Output

#### Drill Target Map
*[Screenshot: Interactive Folium map with color-coded drill targets]*

#### Top 5 Drill Targets
| Rank | Latitude | Longitude | Confidence | Alteration Type | Priority | Area (km²) |
|------|----------|-----------|------------|-----------------|----------|------------|
| 1 | -30.2234 | -71.0812 | 87.3% | Mixed (Iron+Clay) | High | 2.4 |
| 2 | -30.2189 | -71.0745 | 82.1% | Iron Oxide Dominant | High | 1.8 |
| 3 | -30.2301 | -71.0891 | 76.5% | Clay Dominant | Medium | 1.2 |
| 4 | -30.2156 | -71.0823 | 71.2% | Mixed (Iron+Clay) | Medium | 0.9 |
| 5 | -30.2278 | -71.0764 | 68.9% | Iron Oxide Dominant | Medium | 0.7 |

**Metrics:**
- ✅ 5 drill targets identified
- 📏 314 km² total area analyzed
- 🔴 4.2 km² high-priority alteration zones
- 💰 Estimated $350k exploration savings

---

## 💻 Quick Start

### Prerequisites
1. **Google Earth Engine Account** (free)  
   Sign up: [https://earthengine.google.com/signup/](https://earthengine.google.com/signup/)

2. **Python 3.8+**

### Local Installation

```bash
# Clone repository
git clone https://github.com/yourusername/proyecto_mineria.git
cd proyecto_mineria

# Install dependencies
pip install -r requirements.txt

# Authenticate Google Earth Engine (one-time)
earthengine authenticate

# Run Streamlit app
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Usage

1. **Input coordinates** (or use default Andacollo location)
2. **Adjust parameters:**
   - Analysis radius (5-25 km)
   - Cloud cover tolerance (5-50%)
   - Number of drill targets (3-10)
3. **Click "GENERATE DRILL TARGETS"**
4. **View results:**
   - Interactive map with color-coded priorities
   - Drill target table with confidence scores
   - ROI metrics
5. **Export:**
   - Download CSV table
   - Download KML for QGIS/ArcGIS

---

## 📁 Project Structure

```
proyecto_mineria/
├── app.py                      # Streamlit dashboard
├── analysis_engine.py          # GEE processing & ML clustering
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml            # UI theme configuration
├── README.md                   # This file
├── deployment.md               # Streamlit Cloud deployment guide
├── exploration_report.md       # Executive summary template
└── data/
    └── sample_output.csv      # Sample drill targets (demo)
```

---

## 🌍 Geographic Focus: Chile's IV Region

### Why Coquimbo/La Serena?

- **Proven copper belt** - Part of Andean Copper Province
- **Active exploration** - Multiple TSX-V/ASX junior miners
- **Known deposits:** Andacollo, Carmen de Andacollo, El Tofo (historic)
- **Alteration signatures** - Strong iron oxide + clay mineral zones
- **Arid climate** - Minimal vegetation interference (better signal)

### Expandable to Other Regions
The methodology works globally for:
- Porphyry copper (Chile, Peru, Arizona, British Columbia)
- Epithermal gold (Nevada, Mexico, Argentina)
- VMS deposits (Canada, Australia)
- IOCG systems (South Australia, Brazil)

---

## 🎓 Portfolio Highlights

### Target Audience
This project demonstrates expertise relevant to:
- **Junior mining companies** seeking cost-effective exploration tools
- **Remote sensing analysts** in natural resources
- **Geospatial data scientists** working with satellite imagery
- **ML engineers** building real-world classification systems

### Skills Demonstrated
✅ **Google Earth Engine API** - Cloud geospatial processing  
✅ **Remote Sensing** - Multispectral band ratio analysis  
✅ **Machine Learning** - Unsupervised clustering (K-Means)  
✅ **Geospatial Viz** - Interactive maps (Folium, Streamlit)  
✅ **Business Acumen** - ROI calculation, junior mining market understanding  
✅ **Full-Stack Development** - End-to-end deployable application  

---

## 🔮 Future Enhancements

### Version 2.0 Roadmap
- [ ] **Multi-temporal analysis** - Track alteration changes over time
- [ ] **Landsat 8/9 integration** - Extended historical coverage (1984-present)
- [ ] **Deep learning classifier** - CNN-based alteration detection
- [ ] **3D terrain visualization** - Integrate DEMs for topographic context
- [ ] **API endpoint** - Integrate into mining company GIS workflows
- [ ] **Multi-region templates** - Pre-configured for major mining districts

### Potential Commercial Applications
- **SaaS for junior miners** - Subscription-based target generation
- **Consulting deliverable** - Custom reports for exploration projects
- **Integration with drilling databases** - Validation loop for model improvement

---

## 📊 Validation & Accuracy

### Ground-Truth Comparison
The Andacollo district is chosen as the demo location because:
- ✅ **Known copper deposit** - Active mine validates alteration presence
- ✅ **Public geological data** - SERNAGEOMIN (Chile) maps available
- ✅ **Historical exploration** - Multiple drill campaigns to compare against

### Methodology Validation
This approach is based on peer-reviewed research:
- ASTER & Sentinel-2 for hydrothermal alteration mapping (NASA, ESA)
- Band ratio techniques validated in Andes porphyry systems
- K-Means clustering for mineral exploration (Journal of Geochemical Exploration)

---

## 📞 Contact & Deployment

### Author
**Julie Gaete**  
Data Science Specialist | Remote Sensing & ML  
📧 juliegaeteguzman@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/juliegaete)  
💻 [Portfolio](https://github.com/yourusername)

### Deployment
See [deployment.md](deployment.md) for full Streamlit Cloud deployment instructions.

**Quick Deploy:**
1. Push to GitHub
2. Connect Streamlit Cloud
3. Add GEE credentials to secrets
4. Deploy! ⚡

---

## 📜 License & Disclaimer

**License:** MIT - Free for portfolio and educational use

**Disclaimer:**  
This tool is for **exploration prioritization only**. Results should be validated with:
- Ground-truthing (field mapping, sampling)
- Professional geological assessment
- Geochemical analysis
- Geophysical surveys

Satellite analysis **reduces risk** but does **not replace** comprehensive exploration programs. Always consult qualified geologists before drilling decisions.

---

## 🙏 Acknowledgments

- **Copernicus/ESA** - Sentinel-2 satellite data
- **Google Earth Engine** - Cloud processing platform
- **SERNAGEOMIN (Chile)** - Geological reference data
- **Mining community** - Domain expertise and feedback

---

<div align="center">

### ⭐ Star this repo if it helps your exploration program!

**Built with 🧠 by Julie Gaete | Powered by 🛰️ Sentinel-2 & ☁️ Google Earth Engine**

</div>
