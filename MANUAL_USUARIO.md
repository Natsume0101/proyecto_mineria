# 📘 Manual de Usuario: Dashboard de Exploración Mineral

## Maximizando el Rendimiento con Google Earth Engine

**Versión:** 1.0  
**Última actualización:** Diciembre 2024  
**Autor:** Julie Gaete | Data Science Specialist

---

## 🎯 Objetivo del Manual

Este manual te enseñará a **maximizar el uso de tu cuota gratuita de Google Earth Engine**, permitiéndote analizar la **mayor cantidad de kilómetros cuadrados posible** por análisis mientras mantienes la calidad de los resultados.

### Límites de GEE (Plan Gratuito No-Comercial)

| Recurso | Límite | Impacto en tu Dashboard |
|---------|--------|-------------------------|
| **Solicitudes por segundo** | 100 req/sec | ✅ No limitante (1 análisis = ~3-5 requests) |
| **Solicitudes concurrentes** | 40 simultáneas | ✅ Suficiente para uso individual |
| **Tiempo de cómputo (EECU)** | Ilimitado por día | ✅ **Sin límite diario** |
| **Píxeles por solicitud** | 16MB descomprimidos | ⚠️ **Limitante principal** |
| **Almacenamiento de assets** | 250 GB | ✅ No aplica (no guardamos assets) |
| **Tareas batch** | 2 concurrentes promedio | ✅ No aplica (procesamiento en tiempo real) |

> [!IMPORTANT]
> El **único límite real** para maximizar km² es el **tamaño de datos por solicitud (16MB)**. Todo lo demás es prácticamente ilimitado para tu uso.

---

## 🚀 Estrategias para Maximizar Cobertura

### 1. Optimización del Radio de Análisis

El parámetro más importante para controlar km² vs. velocidad.

#### Tabla de Cobertura por Radio

| Radio (km) | Área Aprox. (km²) | Píxeles (60m) | Tiempo Estimado | Recomendación |
|------------|-------------------|---------------|-----------------|---------------|
| **5 km** | 78.5 km² | ~21,800 | ⚡ 15-25 seg | Pruebas rápidas |
| **10 km** | 314 km² | ~87,200 | ⚡ 30-45 seg | **ÓPTIMO: Uso general** |
| **15 km** | 707 km² | ~196,000 | ⏱️ 60-90 seg | Exploración regional |
| **20 km** | 1,257 km² | ~349,000 | ⏱️ 90-120 seg | Máxima cobertura |
| **25 km** | 1,964 km² | ~545,000 | 🐢 120-180 seg | Riesgo de timeout |

> [!TIP]
> **Configuración recomendada para máximo rendimiento:**  
> Radio: **10-15 km** | Nube: **10-20%** | Targets: **5**

#### ¿Por qué 10-15 km es óptimo?

- ✅ Cubre 300-700 km² en un solo análisis
- ✅ Tiempo de procesamiento razonable (30-90 seg)
- ✅ Suficientes píxeles para clustering preciso
- ✅ **Bajo riesgo de exceder límite de 16MB**

### 2. Gestión de Cobertura de Nubes

La **tolerancia de nubes** afecta directamente cuántas imágenes Sentinel-2 se procesan.

```python
# Configuración interna del dashboard
cloud_cover_max = 20  # Parámetro ajustable en sidebar
```

| Cloud Cover (%) | Imágenes Disponibles | Calidad | Velocidad | Uso Recomendado |
|-----------------|----------------------|---------|-----------|-----------------|
| **5%** | Muy pocas | 🌟🌟🌟 Excelente | ⚡ Rápido | Zonas áridas (IV Región Chile) |
| **10%** | Pocas | 🌟🌟🌟 Excelente | ⚡ Rápido | **RECOMENDADO: Chile Norte** |
| **20%** | Moderadas | 🌟🌟 Buena | ⚡ Moderado | **Balance óptimo** |
| **30%** | Muchas | 🌟 Aceptable | 🐢 Lento | Zonas nubladas |
| **50%** | Máximas | ⚠️ Riesgo de artefactos | 🐢 Muy lento | Solo si no hay alternativa |

> [!WARNING]
> **Cloud Cover > 30%** puede incluir imágenes con nubes residuales que afectan los resultados. Para IV Región Chile, **10-20% es ideal**.

#### Estrategia por Región

**Chile IV Región (Andacollo, Coquimbo):**
```
✅ Cloud Cover: 10%
✅ Razón: Clima árido, cielos despejados
✅ Resultado: Imágenes de alta calidad todo el año
```

**Zonas Húmedas (Ej: Sur de Chile):**
```
⚠️ Cloud Cover: 30%
⚠️ Razón: Clima lluvioso, más nubes
⚠️ Resultado: Menos imágenes, posibles artefactos
```

### 3. Estrategia de Análisis Multi-Zona

Para analizar áreas **muy grandes (>2,000 km²)**, divide en múltiples análisis solapados.

#### Ejemplo: Prospección de Distrito Minero (50 km x 50 km = 2,500 km²)

**Opción A: Un solo análisis (NO RECOMENDADO)**
```
Radio: 28 km
Área: ~2,500 km²
Tiempo: 3-5 minutos ⏱️
Riesgo: Alto (puede fallar por timeout)
```

**Opción B: Grid de 4 análisis (RECOMENDADO)**
```
4 análisis de Radio: 15 km cada uno
Área total: ~2,800 km² (con solape)
Tiempo: 4 x 60 seg = 4 minutos ⚡
Riesgo: Bajo (análisis paralelos independientes)
Ventaja: Solape de 20% reduce gaps
```

#### Cómo calcular coordenadas para grid

Para crear un grid 2x2 con solape del 20%:

```python
# Centro del área de interés
lat_centro = -30.226
lon_centro = -71.078

# Radio efectivo por zona (15 km con solape 20%)
offset = 0.12  # ~13 km en grados (aprox)

# Coordenadas para 4 análisis
zonas = [
    (lat_centro + offset, lon_centro - offset),  # NE
    (lat_centro + offset, lon_centro + offset),  # NW
    (lat_centro - offset, lon_centro - offset),  # SE
    (lat_centro - offset, lon_centro + offset),  # SW
]

# Ejecutar análisis para cada zona
for i, (lat, lon) in enumerate(zonas):
    print(f"Zona {i+1}: Lat={lat:.3f}, Lon={lon:.3f}")
    # (Analizar en dashboard con Radio 15km)
```

> [!TIP]
> **Para áreas gigantes (>10,000 km²):** Usa grids de 3x3 o 4x4 con Radio 10-15 km cada uno.

---

## ⚙️ Configuración Óptima por Escenario

### Escenario 1: Exploración Inicial Rápida
**Objetivo:** Primera inspección rápida de un área nueva

```yaml
Radio: 10 km
Cloud Cover: 10%
Targets: 5
Tiempo: ~30 segundos
Cobertura: ~314 km²
```

**Cuándo usar:**
- Primera vez analizando un área
- Necesitas resultados rápidos para decisión GO/NO-GO
- Prueba de concepto para stakeholders

### Escenario 2: Análisis de Producción
**Objetivo:** Máxima cobertura con calidad confiable

```yaml
Radio: 15 km
Cloud Cover: 20%
Targets: 5
Tiempo: ~60-90 segundos
Cobertura: ~707 km²
```

**Cuándo usar:**
- Análisis final pre-campo
- Generación de drill targets para presentación
- **Recomendado para reportes ejecutivos**

### Escenario 3: Cobertura Máxima
**Objetivo:** Analizar el área más grande posible

```yaml
Radio: 20 km
Cloud Cover: 20%
Targets: 7
Tiempo: ~90-120 segundos
Cobertura: ~1,257 km²
```

**Cuándo usar:**
- Exploración regional
- Comparación de múltiples distritos
- Cuando dispones de 2-3 minutos por análisis

### Escenario 4: Análisis de Alta Precisión
**Objetivo:** Máxima calidad sobre cobertura

```yaml
Radio: 5 km
Cloud Cover: 5%
Targets: 3
Tiempo: ~15-20 segundos
Cobertura: ~78 km²
```

**Cuándo usar:**
- Zona conocida con mineralización confirmada
- Refinamiento de targets existentes
- Validación de anomalías geoquímicas

---

## 📊 Workflow Recomendado: De Regional a Local

### Fase 1: Reconocimiento Regional (Día 1)
```
1. Análisis inicial: Radio 15 km → ~700 km²
2. Identificar 3-5 zonas de interés
3. Tiempo total: 2-3 minutos
```

### Fase 2: Análisis Detallado (Día 2)
```
1. Para cada zona interesante:
   - Radio 10 km → ~300 km² por zona
   - Total: 3 zonas × 10 km = ~900 km²
2. Tiempo total: 3 × 45 seg = ~2.5 minutos
```

### Fase 3: Refinamiento (Día 3)
```
1. Top 2 targets más prometedores:
   - Radio 5 km → ~75 km² por target
   - Cloud cover: 5% (máxima calidad)
2. Tiempo total: 2 × 20 seg = 40 segundos
```

**Total analizado:** ~1,650 km² en 3 sesiones (~6 min total)

---

## 🔧 Trucos para Maximizar Rendimiento

### 1. Usa la Cache de Resultados

El dashboard guarda resultados en `st.session_state`. Aprovéchalo:

```
✅ Analiza una vez → Descarga CSV
✅ Cambia parámetros de visualización sin re-analizar
✅ Exporta múltiples formatos (CSV + KML) sin procesar de nuevo
```

### 2. Análisis Batch (Múltiples Ubicaciones)

Para analizar **múltiples concesiones mineras** en un día:

```python
# Lista de ubicaciones
concesiones = [
    {"nombre": "Andacollo", "lat": -30.226, "lon": -71.078},
    {"nombre": "Carmen", "lat": -30.250, "lon": -71.100},
    {"nombre": "Talcuna", "lat": -30.180, "lon": -71.050},
]

# Plan de análisis
for i, con in enumerate(concesiones):
    print(f"Análisis {i+1}/{len(concesiones)}: {con['nombre']}")
    print(f"   Lat: {con['lat']}, Lon: {con['lon']}")
    print(f"   Radio: 10 km → ~314 km²")
    print(f"   Tiempo estimado: 30-45 seg")
    print(f"   ---")

# Total: 3 concesiones × 314 km² = 942 km² en ~3 minutos
```

> [!TIP]
> Con la cuota gratuita, puedes analizar fácilmente **20+ ubicaciones por día** (>6,000 km²) sin problemas.

### 3. Horarios de Menor Carga (Opcional)

Aunque GEE tiene cuota generosa, para **análisis muy grandes (>20 km radio)**:

```
🌍 Mejor rendimiento: 00:00-06:00 UTC (21:00-03:00 Chile)
⚡ Rendimiento normal: Resto del día
```

Probablemente no notarás diferencia, pero si experimentas lentitud, prueba en horarios nocturnos.

### 4. Prioriza 60m de Resolución (Ya Implementado)

El dashboard usa 60m para sampling (ya optimizado):

```python
# En analysis_engine.py (línea 169)
sample = features.sample(
    region=aoi,
    scale=60,  # ✅ 60m = balance óptimo
    numPixels=5000,
    geometries=True
)
```

**¿Por qué 60m?**
- ✅ 6x más rápido que 10m
- ✅ Suficiente para detectar alteración (zonas >100m)
- ✅ Reduce uso de cuota de píxeles

---

## 📈 Casos de Uso Reales: Chile IV Región

### Caso 1: Junior Minera con Presupuesto Limitado

**Contexto:**
- 5 concesiones mineras (área total: ~80 km²)
- Presupuesto: $5,000 USD para exploración inicial
- Objetivo: Identificar 2-3 drill targets

**Estrategia con Dashboard:**

```yaml
Configuración:
  - Radio: 10 km por concesión
  - Cloud Cover: 10%
  - Targets: 3 por análisis

Ejecución:
  - 5 análisis × 45 seg = 3.75 minutos
  - Cobertura total: 5 × 314 km² = 1,570 km²
  - Drill targets generados: 15 (filtrar top 5)

Resultado:
  ✅ Cobertura: 1,570 km² (vs 80 km² de concesiones)
  ✅ Tiempo: 4 minutos (vs 3 meses de campo)
  ✅ Costo: $0 (vs $50k+ en muestreo)
  ✅ Decisión: 2 concesiones prioritarias identificadas
```

### Caso 2: Consultoría Regional

**Contexto:**
- Cliente solicita análisis de distrito minero completo
- Área: 50 km × 40 km = 2,000 km²
- Plazo: 2 días

**Estrategia con Dashboard:**

```yaml
Día 1 - Reconocimiento (2 horas):
  - Grid 3×3 de análisis (Radio 12 km cada uno)
  - 9 análisis × 50 seg = 7.5 minutos de procesamiento
  - Cobertura: ~4,000 km² (con solapes)
  
Día 2 - Refinamiento (1 hora):
  - Top 5 zonas → Re-analizar con Radio 8 km
  - 5 análisis × 35 seg = 3 minutos
  - Targets finales: 15 (priorizados por confidence)

Entrega:
  ✅ Mapa interactivo con 15 drill targets
  ✅ Archivos KML para QGIS
  ✅ Tabla CSV con coordenadas y confianza
  ✅ Total tiempo GEE: <15 minutos
```

---

## ⚠️ Errores Comunes y Soluciones

### Error 1: "Computation timed out"

**Causa:** Radio muy grande (>25 km) o cloud cover muy alto (>40%)

**Solución:**
```yaml
❌ Radio: 30 km, Cloud: 50%
✅ Radio: 15 km, Cloud: 20%
```

### Error 2: "No alteration zones identified"

**Causas posibles:**
1. Área sin alteración real (zona sedimentaria)
2. Cloud cover muy bajo (sin imágenes disponibles)
3. Área 100% vegetada (NDVI mask muy restrictivo)

**Solución:**
```yaml
# Prueba 1: Aumentar cloud cover
Cloud Cover: 5% → 20%

# Prueba 2: Cambiar ubicación (prueba zona conocida)
Lat: -30.226, Lon: -71.078 (Andacollo - zona validada)

# Prueba 3: Revisar NDVI threshold
Si área boscosa → considerar ajustar threshold en código
```

### Error 3: "Google Earth Engine authentication failed"

**Solución local:**
```bash
# Re-autenticar GEE (una vez)
earthengine authenticate

# Reiniciar app
streamlit run app.py
```

**Solución Streamlit Cloud:**
- Verificar secrets en `.streamlit/secrets.toml`
- Confirmar service account activa

### Error 4: Análisis muy lento (>5 minutos)

**Diagnóstico:**
```yaml
1. Chequear radio: ¿>20 km? → Reducir a 15 km
2. Chequear cloud cover: ¿>30%? → Bajar a 20%
3. Chequear conexión a internet
4. Intentar en horario nocturno (opcional)
```

---

## 📋 Checklist Pre-Análisis

Antes de cada análisis, verifica:

- [ ] **Coordenadas correctas** (usar Google Maps para validar)
- [ ] **Radio apropiado** (10-15 km para uso general)
- [ ] **Cloud cover optimizado** (10-20% para Chile Norte)
- [ ] **Targets suficientes** (5 es óptimo)
- [ ] **Área de interés conocida** (primera vez: probar con Andacollo)

---

## 🎓 Mejores Prácticas: Resumen

### ✅ DO (Hacer)

1. **Usa Radio 10-15 km** para balance óptimo
2. **Cloud Cover 10-20%** en zonas áridas
3. **Divide áreas grandes** en grids solapados
4. **Exporta resultados** (CSV + KML) inmediatamente
5. **Analiza múltiples ubicaciones** en sesión
6. **Valida con zona conocida** (Ej: Andacollo) primero

### ❌ DON'T (Evitar)

1. **No uses Radio >25 km** (riesgo timeout)
2. **No uses Cloud >40%** (calidad baja)
3. **No re-analices** sin necesidad (usa cache)
4. **No ignores warnings** del dashboard
5. **No confíes 100%** sin validación de campo
6. **No uses múltiples cuentas** (viola ToS de GEE)

---

## 📞 Soporte y Recursos

### Documentación Oficial
- [Google Earth Engine Quotas](https://developers.google.com/earth-engine/guides/usage)
- [Sentinel-2 Data Guide](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED)

### Contacto
**Julie Gaete**  
📧 juliegaeteguzman@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/juliegaete)

### Archivos del Proyecto
- `README.md` - Documentación técnica
- `deployment.md` - Guía de deploy en Streamlit Cloud
- `exploration_report.md` - Template de reporte ejecutivo

---

## 🚀 Conclusión

Con la configuración óptima del dashboard, puedes:

✅ **Analizar 1,000-2,000 km²** en un solo análisis (Radio 15-20 km)  
✅ **Procesar 20+ ubicaciones por día** (>6,000 km² totales)  
✅ **Tiempo ilimitado de cómputo** (plan gratuito GEE)  
✅ **Costo $0** (vs $500k+ exploración tradicional)

**Configuración recomendada universal:**
```yaml
Radio: 15 km
Cloud Cover: 20%
Targets: 5
Tiempo: ~60 segundos
Cobertura: ~707 km² por análisis
```

> [!TIP]
> **Maximiza tu ROI:** Con solo 10 análisis por día, cubres **7,070 km²** - equivalente a **meses de trabajo de campo tradicional**.

---

**¡Buena exploración! ⛏️🛰️**
