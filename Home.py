
import streamlit as st
import sys
import os

# Ajuste de path para imports si fuera necesario
sys.path.insert(0, os.path.abspath('.'))

st.set_page_config(page_title="Flujo CRM Inandes", layout="wide")

# render_header("CRM Inandes - Flujo de Procesos")
st.title("CRM Inandes - Sistema de Gestión")
st.caption("Última actualización: 2026-01-17")
st.info("🚀 RAILWAY_TEST_VERSION_17ENE2026_1347 🚀")

st.markdown("---")

st.markdown("""
### 📋 Módulos Disponibles

Utiliza el menú lateral para navegar entre los diferentes módulos del sistema:

#### 🤖 Chat WhatsApp
Simulador del bot de WhatsApp para atención al inversionista.

#### 📊 Logic DB Complete
Diagrama de flujo completo del CRM incluyendo:
- Mantenimiento / Configuración
- Maestro de Partícipes
- Gestión de Inversiones
- Procesos (Cierre Bimestral)
- Tesorería & Reportes
- Agente IA / Bot WhatsApp

---

**Desarrollado para Inandes** | Última actualización: 2026-01-17
""")
