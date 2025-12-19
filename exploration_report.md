# MINERAL EXPLORATION REPORT
## Satellite-Based Alteration Mapping for Drill Target Generation

<div align="center">

### Andacollo Copper District, IV Region Chile
**Executive Summary for Junior Mining Companies**

---

**Project:** Hydrothermal Alteration Zone Identification  
**Location:** 29.5°S to 30.5°S, 70.5°W to 71.5°W (Coquimbo Region)  
**Data Source:** Sentinel-2 Multispectral Satellite Imagery  
**Analysis Date:** December 2025  
**Prepared by:** Julie Gaete, Data Science Specialist

</div>

---

## 1. EXECUTIVE SUMMARY

### Key Findings

✅ **5 high-confidence drill targets** identified within 10 km radius of Andacollo district  
✅ **4.2 km²** of high-priority hydrothermal alteration zones mapped  
✅ **70% cost reduction** compared to traditional surface sampling programs  
✅ **$350,000 estimated savings** in Phase 1 exploration

### Recommended Action

Proceed with **focused field verification** of Top 3 drill targets before committing to full surface sampling program. Estimated field work: 2-3 weeks, $50,000 budget.

---

## 2. PROJECT OVERVIEW

### 2.1 Objective

Identify hydrothermal alteration zones associated with **porphyry copper mineralization** using free satellite imagery and machine learning, prioritizing drill targets to reduce exploration risk and costs.

### 2.2 Study Area

**Location:** Andacollo Copper District, IV Region Chile
- **Latitude:** -30.226°
- **Longitude:** -71.078°
- **Area Analyzed:** 314 km² (10 km radius)
- **Geological Setting:** Coastal Cordillera, Andean Copper Belt
- **Known Mineralization:** Porphyry copper, historic production from Andacollo mine

### 2.3 Methodology

**Data Source:**
- Sentinel-2 Surface Reflectance (10-60m resolution)
- 6-month cloud-free composite (June-December 2025)
- Bands used: B2 (Blue), B4 (Red), B8 (NIR), B11 (SWIR1), B12 (SWIR2)

**Analysis Workflow:**
1. **Satellite Data Retrieval** - Google Earth Engine cloud processing
2. **Band Ratio Calculation** - Iron oxide index, clay minerals, NDVI
3. **Vegetation Masking** - Exclude false positives from vegetation
4. **K-Means Clustering** - Unsupervised classification (4 clusters)
5. **Target Prioritization** - Confidence scoring based on alteration intensity

---

## 3. TECHNICAL RESULTS

### 3.1 Alteration Indices

**Iron Oxide Index Formula:**
```
(B4 - B2) / (B4 + B2)
```
**Interpretation:** High values indicate ferric iron oxides (gossans, limonite) associated with oxidized sulfide zones.

**Clay Mineral Index Formula:**
```
B11 / B12
```
**Interpretation:** High values indicate hydroxyl-bearing clay minerals (kaolinite, alunite) from argillic alteration.

**NDVI (Vegetation Mask):**
```
(B8 - B4) / (B8 + B4)
```
**Interpretation:** Areas with NDVI > 0.3 excluded (vegetation causes false alteration signals).

### 3.2 Clustering Results

**4 Distinct Clusters Identified:**

1. **High Priority (Cluster 1)**
   - Mean Iron Oxide: 0.28
   - Mean Clay Minerals: 1.15
   - Area: 4.2 km²
   - Interpretation: **Mixed alteration - Prime drill targets**

2. **Medium Priority (Cluster 2)**
   - Mean Iron Oxide: 0.22
   - Mean Clay Minerals: 1.08
   - Area: 6.8 km²
   - Interpretation: **Iron oxide dominant - Secondary targets**

3. **Low Priority (Cluster 3)**
   - Mean Iron Oxide: 0.15
   - Mean Clay Minerals: 0.98
   - Area: 12.3 km²
   - Interpretation: **Weak alteration - Low priority**

4. **Background (Cluster 4)**
   - Mean Iron Oxide: 0.08
   - Mean Clay Minerals: 0.92
   - Area: 290.7 km²
   - Interpretation: **No significant alteration**

---

## 4. DRILL TARGET RECOMMENDATIONS

### Top 5 Prioritized Drill Targets

| **Rank** | **Latitude** | **Longitude** | **Confidence** | **Alteration Type** | **Priority** | **Area (km²)** | **Rationale** |
|----------|--------------|---------------|----------------|---------------------|--------------|----------------|---------------|
| **1** | -30.2234 | -71.0812 | 87.3% | Mixed (Fe+Clay) | High | 2.4 | Strongest combined alteration signal, proximal to known Andacollo structure |
| **2** | -30.2189 | -71.0745 | 82.1% | Iron Oxide | High | 1.8 | Large gossan zone, coincident with structural lineament |
| **3** | -30.2301 | -71.0891 | 76.5% | Clay Dominant | Medium | 1.2 | Argillic alteration, potential epithermal component |
| **4** | -30.2156 | -71.0823 | 71.2% | Mixed (Fe+Clay) | Medium | 0.9 | Moderate alteration, parallel to district trend |
| **5** | -30.2278 | -71.0764 | 68.9% | Iron Oxide | Medium | 0.7 | Small high-grade gossan, exploration upside |

### Recommended Drilling Sequence

**Phase 1 (Immediate):**
- **Target 1** - 3 drill holes, 200m depth, RC drilling
- **Target 2** - 2 drill holes, 150m depth, RC drilling
- **Budget:** $150,000 (5 holes × $30k/hole)

**Phase 2 (Contingent on Phase 1 results):**
- Targets 3-5 if Phase 1 encounters mineralization
- Diamond drilling for resource definition if Phase 1 successful

---

## 5. GEOLOGICAL CONTEXT

### 5.1 Regional Setting

The Andacollo District is located in Chile's **Coastal Cordillera**, part of the broader **Andean Copper Province**. The area hosts:
- **Porphyry copper deposits** (Cenozoic intrusion-related)
- **Hydrothermal alteration zones** (quartz-sericite-pyrite, argillic, propylitic)
- **Historic production** from Andacollo mine (1850s-present)

### 5.2 Validation Against Known Deposits

**Andacollo Mine Location:** -30.241°, -71.082°
- ✅ **Target 1 is located 1.8 km north** of the known mine
- ✅ Alteration signature matches documented argillic-potassic zones
- ✅ Structural trend aligns with district-scale faults (NNE-SSW)

**Confidence Validation:**  
The proximity of high-confidence targets to the **known producing mine** validates the methodology and increases exploration success probability.

---

## 6. COST-BENEFIT ANALYSIS

### 6.1 Traditional Exploration Approach

| **Activity** | **Duration** | **Cost** | **Coverage** |
|--------------|--------------|----------|--------------|
| Reconnaissance mapping | 2 months | $80,000 | 50 km² |
| Surface geochemistry (rock/soil) | 3 months | $150,000 | 25 km² |
| Geophysical surveys (IP/Mag) | 2 months | $200,000 | 20 km² |
| Target selection | 1 month | $20,000 | - |
| **TOTAL** | **8 months** | **$450,000** | **Limited** |

### 6.2 Satellite-First Approach

| **Activity** | **Duration** | **Cost** | **Coverage** |
|--------------|--------------|----------|--------------|
| Satellite analysis (this study) | 3 days | $15,000 | 314 km² |
| Focused field verification (Top 3) | 3 weeks | $50,000 | 5 km² |
| Targeted geochemistry | 2 weeks | $35,000 | Target zones |
| Drill planning | 1 week | $10,000 | - |
| **TOTAL** | **2 months** | **$110,000** | **Comprehensive** |

### 6.3 ROI Analysis

**Direct Savings:** $450,000 - $110,000 = **$340,000 (76% reduction)**  
**Time Savings:** 8 months - 2 months = **6 months faster to drilling**  
**Risk Reduction:** Data-driven targeting vs. blind exploration  
**Additional Value:** 10x larger area analyzed for future prospects

---

## 7. COMPETITIVE ADVANTAGES

### Why Satellite Analysis First?

✅ **Cost-Effective:** 1/4 the cost of traditional exploration  
✅ **Comprehensive:** Analyze 10x more area in 1/10 the time  
✅ **Objective:** Data-driven, removes bias from target selection  
✅ **Repeatable:** Monitor changes over time (re-analysis costs <$5k)  
✅ **Complementary:** Integrates with traditional methods, doesn't replace them

### Positioning for Junior Miners

For **TSX-V/ASX junior mining companies** with limited budgets ($1-5M market cap):
- Extends runway by **reducing burn rate** on early exploration
- **Data-driven pitch** to investors (satellite targets > geologist hunches)
- Enables **portfolio approach** (analyze 5 prospects for cost of 1 field program)
- **Exit strategy:** Sell targets to larger companies with satellite validation

---

## 8. RISK FACTORS & LIMITATIONS

### 8.1 Limitations of Satellite Analysis

⚠️ **Does NOT replace field geology** - Requires ground-truthing  
⚠️ **Vegetation cover** - Dense forests mask alteration (not an issue in arid Chile)  
⚠️ **Depth limitation** - Only detects surface/near-surface alteration  
⚠️ **False positives** - Natural iron staining, lithology can mimic alteration  
⚠️ **Cloud cover** - Requires extended analysis periods in cloudy regions

### 8.2 Recommended Mitigation

1. **Field verification mandatory** before drilling
2. **Geochemical sampling** of top 3 targets (rock chips, soils)
3. **Structural mapping** to confirm lineaments
4. **Integration with historic data** (SERNAGEOMIN, company reports)
5. **Staged drilling** (RC → Diamond) to control costs

---

## 9. NEXT STEPS FOR JUNIOR MINERS

### Immediate Actions (Week 1-2)

1. ✅ **Review this report** with technical team
2. ✅ **Secure land position** (concession applications for targets)
3. ✅ **Budget approval** for $50k field verification
4. ✅ **Hire local geologist** (La Serena-based)

### Short-Term (Month 1-2)

1. 🗺️ **Field reconnaissance** of Top 3 targets
2. 🧪 **Surface sampling** (30 rock chips, 50 soil samples)
3. 📊 **Geochemical analysis** (Cu, Au, Mo, As, Fe)
4. 📐 **Structural mapping** (faults, veins, alteration zones)

### Medium-Term (Month 3-4)

1. ⛏️ **Drill planning** if field results positive
2. 💰 **Raise capital** ($500k-$1M for drill program)
3. 📰 **News release** - "Satellite analysis identifies high-priority targets"
4. 🤝 **Partner discussions** (joint ventures with larger miners)

---

## 10. CONCLUSION

Satellite-based alteration mapping has successfully identified **5 high-confidence drill targets** in the Andacollo District, offering a **$340,000 cost savings** and **6-month timeline reduction** compared to traditional exploration.

The proximity of **Target 1 to the known Andacollo mine**, combined with strong mixed alteration signatures, provides high confidence for exploration success.

**Recommendation:** Proceed immediately with **focused field verification** of Targets 1-3 to de-risk before committing to full drill program.

---

## APPENDIX A: Coordinates Reference Table

### Complete Drill Target Coordinates (WGS84)

| Target | Latitude (Decimal °) | Longitude (Decimal °) | UTM East (m) | UTM North (m) | Zone |
|--------|----------------------|-----------------------|--------------|---------------|------|
| 1 | -30.2234 | -71.0812 | 332,456 | 6,656,234 | 19H |
| 2 | -30.2189 | -71.0745 | 333,123 | 6,656,789 | 19H |
| 3 | -30.2301 | -71.0891 | 331,789 | 6,655,456 | 19H |
| 4 | -30.2156 | -71.0823 | 332,345 | 6,657,123 | 19H |
| 5 | -30.2278 | -71.0764 | 332,890 | 6,655,890 | 19H |

**Download KML:** Available in app export for direct import to QGIS, ArcGIS, Google Earth.

---

## APPENDIX B: References

1. **Sentinel-2 Data:** Copernicus/ESA - [https://scihub.copernicus.eu/](https://scihub.copernicus.eu/)
2. **Google Earth Engine:** [https://earthengine.google.com/](https://earthengine.google.com/)
3. **SERNAGEOMIN (Chile):** Geological maps and mineral deposits database
4. **Methodology:** Based on ASTER alteration mapping techniques (Abrams & Hook, 1995)
5. **Andacollo Mine:** Historic production data (Chilean Mining Chamber)

---

## APPENDIX C: Contact & Licensing

**Report Prepared by:**  
Julie Gaete  
Data Science Specialist - Remote Sensing & ML  
📧 juliegaeteguzman@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/juliegaete)

**Licensing:**  
This report template is provided for **portfolio demonstration purposes**. For commercial exploration projects, contact for custom analysis and confidential reporting.

**Satellite Data License:**  
Sentinel-2 data is freely available under Copernicus license (full, free, and open access).

---

<div align="center">

**Prepared December 2025**  
*For demonstration purposes - Not a replacement for professional geological assessment*

</div>
