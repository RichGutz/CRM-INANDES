import streamlit as st
import sys
import os
import datetime as dt
import pandas as pd
import io

# Path setup
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.data.supabase_client import get_supabase_client
from src.ui.header import render_header

# Constants
TABLE_NAME = "crm_participes"

# Page config
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_title="Gestión de Partícipes",
    page_icon="👥"
)

# Session state
if 'vista_participes' not in st.session_state:
    st.session_state.vista_participes = 'busqueda'
if 'participe_seleccionado' not in st.session_state:
    st.session_state.participe_seleccionado = None

# CSS
st.markdown('''<style>
[data-testid="stHorizontalBlock"] { align-items: center; }
.stButton>button.red-button { background-color: #FF4B4B; color: white; border-color: #FF4B4B; }
.stButton>button.red-button:hover { background-color: #FF6F6F; border-color: #FF6F6F; }
</style>''', unsafe_allow_html=True)

render_header("Gestión de Partícipes")

# --- Database Functions ---
def buscar_participes_db(query=""):
    """Busca en crm_participes por nombre o documento"""
    supabase = get_supabase_client()
    try:
        if query and len(query.strip()) > 0:
            response = supabase.table(TABLE_NAME).select('*').or_(
                f"nombre_completo.ilike.%{query}%,documento_identidad.ilike.%{query}%"
            ).order('nombre_completo', desc=False).execute()
            return response.data if response.data else []
        else:
            return []
    except Exception as e:
        st.error(f"Error buscando en {TABLE_NAME}: {e}")
        return []

def guardar_registro_db(data, update_id=None):
    supabase = get_supabase_client()
    try:
        clean_data = {k: (v if v != "" else None) for k, v in data.items()}
        
        if update_id:
            response = supabase.table(TABLE_NAME).update(clean_data).eq('id', update_id).execute()
            return True, "Registro actualizado correctamente."
        else:
            existing = supabase.table(TABLE_NAME).select('id').eq('documento_identidad', clean_data['documento_identidad']).execute()
            if existing.data:
                return False, f"Ya existe un partícipe con el documento {clean_data['documento_identidad']}."
            
            response = supabase.table(TABLE_NAME).insert(clean_data).execute()
            return True, "Registro creado correctamente."
    except Exception as e:
        return False, f"Error en BD: {e}"

def exportar_excel_db():
    supabase = get_supabase_client()
    try:
        response = supabase.table(TABLE_NAME).select('*').execute()
        if not response.data: return None
        df = pd.DataFrame(response.data)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Participes')
        return buffer.getvalue()
    except Exception as e:
        st.error(f"Error generando Excel: {e}")
        return None

# --- VIEWS ---

def mostrar_busqueda():
    st.header("Búsqueda de Partícipes")
    
    # Top row: Search + New + Export
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        # IMPORTANTE: Deshabilitar autocomplete del navegador
        search_query = st.text_input(
            "🔍 Buscar por Nombre o DNI",
            placeholder="Escribe para buscar...",
            key="participes_search_v2",
            help="Busca solo en la tabla de Partícipes"
        )
    
    with col2:
        st.write("")
        st.write("")
        if st.button("➕ Nuevo Registro", type="primary", use_container_width=True):
            st.session_state.vista_participes = 'crear'
            st.session_state.participe_seleccionado = None
            st.rerun()
    
    with col3:
        st.write("")
        st.write("")
        excel_data = exportar_excel_db()
        if excel_data:
            st.download_button(
                label="📥 Exportar Todo (Excel)",
                data=excel_data,
                file_name=f"participes_{dt.date.today()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    # Search results
    if search_query:
        resultados = buscar_participes_db(search_query)
        
        if resultados:
            # Auto-redirect si solo hay 1 resultado
            if len(resultados) == 1:
                st.session_state.participe_seleccionado = resultados[0]
                st.session_state.vista_participes = 'editar'
                st.rerun()
            
            st.caption(f"✅ Se encontraron {len(resultados)} partícipes")
            
            # Headers
            c1, c2, c3, c4 = st.columns([1, 4, 3, 1])
            c1.markdown("**DNI**")
            c2.markdown("**Nombre Completo**")
            c3.markdown("**Email**")
            c4.markdown("**Acción**")
            st.divider()
            
            # Results
            for idx, row in enumerate(resultados):
                c1, c2, c3, c4 = st.columns([1, 4, 3, 1])
                c1.write(f"`{row.get('documento_identidad', '')}`")
                c2.write(row.get('nombre_completo', ''))
                c3.write(row.get('email', ''))
                if c4.button("✏️", key=f"edit_{row['id']}", use_container_width=True):
                    st.session_state.participe_seleccionado = row
                    st.session_state.vista_participes = 'editar'
                    st.rerun()
                st.divider()
        else:
            st.warning(f"❌ No se encontraron partícipes con: '{search_query}'")
    else:
        st.info("👆 Ingresa un Nombre o DNI para buscar")
    
    # Tools
    st.write("---")
    st.subheader("🛠️ Herramientas")
    if st.button("🚀 Ejecutar Migración desde GSheets"):
        st.session_state.vista_participes = 'migracion'
        st.rerun()

def render_form(modo='crear'):
    reg = st.session_state.participe_seleccionado or {}
    is_edit = (modo == 'editar')
    
    if st.button("⬅️ Volver a Búsqueda"):
        st.session_state.vista_participes = 'busqueda'
        st.session_state.participe_seleccionado = None
        st.rerun()

    st.title(f"{'Editar' if is_edit else 'Crear'} Partícipe")

    with st.form("form_participes_main"):
        tab_id, tab_contact, tab_fin, tab_bank, tab_guar, tab_extra = st.tabs([
            "🏢 Identidad", "📞 Contacto", "💼 Laboral", "🏦 Bancario", "⚖️ Cumplimiento", "👥 Cotitular"
        ])
        
        # TAB 1: IDENTIDAD
        with tab_id:
            col1, col2 = st.columns(2)
            with col1:
                doc_num = st.text_input("N° Documento/DNI *", value=reg.get('documento_identidad', ''), max_chars=20, disabled=is_edit)
            with col2:
                curr_tipo = reg.get('tipo_doc', 'DNI')
                if not curr_tipo: curr_tipo = 'DNI'
                tipo_opts = ["DNI", "CEX", "PASAPORTE", "RUC"]
                idx = tipo_opts.index(curr_tipo) if curr_tipo in tipo_opts else 0
                tipo_doc = st.selectbox("Tipo Documento *", tipo_opts, index=idx)
            
            nombre = st.text_input("Nombre Completo / Razón Social *", value=reg.get('nombre_completo', ''))
            
            c3, c4, c5 = st.columns(3)
            with c3:
                f_nac_val = reg.get('fecha_nacimiento')
                f_nac = st.date_input("Fecha Nacimiento", value=dt.datetime.strptime(f_nac_val, '%Y-%m-%d').date() if f_nac_val else None)
            with c4:
                nacionalidad = st.text_input("Nacionalidad", value=reg.get('nacionalidad', 'Peruana'))
            with c5:
                ec_opts = ["Soltero", "Casado", "Divorciado", "Viudo", "Conviviente"]
                curr_ec = reg.get('estado_civil', 'Soltero')
                idx_ec = ec_opts.index(curr_ec) if curr_ec in ec_opts else 0
                est_civil = st.selectbox("Estado Civil", ec_opts, index=idx_ec)
        
        # TAB 2: CONTACTO
        with tab_contact:
            k1, k2 = st.columns(2)
            email = k1.text_input("Correo Electrónico", value=reg.get('email', ''))
            telf = k2.text_input("Teléfono / Celular", value=reg.get('telefono', ''))
            
            st.markdown("#### Dirección")
            dir_fiscal = st.text_area("Domicilio Fiscal / Dirección", value=reg.get('direccion_fiscal', ''))
            
            k3, k4 = st.columns(2)
            cod_postal = k3.text_input("Código Postal", value=reg.get('codigo_postal', ''))
            residente = k4.checkbox("Residente en Perú", value=reg.get('residente_peru', True))

        # TAB 3: LABORAL
        with tab_fin:
            st.caption("Información Laboral y Origen de Fondos")
            
            l1, l2 = st.columns(2)
            ocupacion = l1.text_input("Ocupación / Profesión", value=reg.get('ocupacion', ''))
            centro_lab = l2.text_input("Centro de Labores / Empresa", value=reg.get('centro_labores', ''))
            
            l3, l4 = st.columns(2)
            cargo = l3.text_input("Cargo que Ocupa", value=reg.get('cargo_ocupado', ''))
            antiguedad = l4.number_input("Antigüedad (años)", value=int(reg.get('antiguedad_laboral_anios') or 0), min_value=0)

        # TAB 4: BANCARIO
        with tab_bank:
            st.caption("Cuenta Principal para Abonos")
            b1, b2 = st.columns(2)
            banco = b1.text_input("Banco", value=reg.get('banco_nombre', ''))
            mon_opts = ["PEN", "USD"]
            curr_mon = reg.get('moneda_cuenta', 'PEN')
            idx_mon = mon_opts.index(curr_mon) if curr_mon in mon_opts else 0
            moneda = b2.selectbox("Moneda", mon_opts, index=idx_mon)
            
            b3, b4 = st.columns(2)
            cuenta = b3.text_input("N° Cuenta", value=reg.get('numero_cuenta', ''))
            cci = b4.text_input("CCI", value=reg.get('cci', ''))

        # TAB 5: CUMPLIMIENTO
        with tab_guar:
            es_pep = st.checkbox("¿Es PEP (Persona Políticamente Expuesta)?", value=reg.get('es_pep', False))
            pep_det = st.text_area("Detalle PEP (Cargo/Relación)", value=str(reg.get('pep_detalle') or ''), 
                                   disabled=not es_pep, help="Detallar cargo o relación si es PEP")
            
            st.divider()
            pr_opts = ["Conservador", "Moderado", "Audaz"]
            curr_pr = reg.get('perfil_riesgo', 'Conservador')
            idx_pr = pr_opts.index(curr_pr) if curr_pr in pr_opts else 0
            perfil = st.selectbox("Perfil de Riesgo", pr_opts, index=idx_pr)

        # TAB 6: COTITULAR
        with tab_extra:
            st.subheader("Cónyuge")
            c_nm = st.text_input("Nombre Cónyuge", value=reg.get('conyuge_nombre', ''))
            c_dc = st.text_input("DNI Cónyuge", value=reg.get('conyuge_documento', ''))
            
            st.divider()
            st.subheader("Cotitular")
            ct_nm = st.text_input("Nombre Cotitular", value=reg.get('cotitular_nombre', ''))
            ct_dc = st.text_input("DNI Cotitular", value=reg.get('cotitular_documento', ''))
            
            st.divider()
            st.subheader("Asesor Asignado")
            as_nm = st.text_input("Nombre Asesor", value=reg.get('asesor_nombre', ''))
            as_em = st.text_input("Email Asesor", value=reg.get('asesor_email', ''))

        st.markdown("---")
        submitted = st.form_submit_button("💾 Guardar Cambios", type="primary")
        
        if submitted:
            if not doc_num or not nombre:
                st.error("⚠️ Documento y Nombre son obligatorios.")
            else:
                form_data = {
                    'tipo_doc': tipo_doc,
                    'documento_identidad': doc_num,
                    'nombre_completo': nombre,
                    'fecha_nacimiento': str(f_nac) if f_nac else None,
                    'nacionalidad': nacionalidad,
                    'estado_civil': est_civil,
                    'residente_peru': residente,
                    'email': email,
                    'telefono': telf,
                    'direccion_fiscal': dir_fiscal,
                    'codigo_postal': cod_postal,
                    'ocupacion': ocupacion,
                    'centro_labores': centro_lab,
                    'cargo_ocupado': cargo,
                    'antiguedad_laboral_anios': antiguedad,
                    'banco_nombre': banco,
                    'numero_cuenta': cuenta,
                    'cci': cci,
                    'moneda_cuenta': moneda,
                    'es_pep': es_pep,
                    'pep_detalle': pep_det if es_pep else None,
                    'perfil_riesgo': perfil,
                    'conyuge_nombre': c_nm,
                    'conyuge_documento': c_dc,
                    'cotitular_nombre': ct_nm,
                    'cotitular_documento': ct_dc,
                    'asesor_nombre': as_nm,
                    'asesor_email': as_em
                }
                
                success, msg = guardar_registro_db(form_data, update_id=reg.get('id') if is_edit else None)
                if success:
                    st.success(msg)
                    st.session_state.vista_participes = 'busqueda'
                    st.rerun()
                else:
                    st.error(msg)

def vista_migracion():
    st.button("⬅️ Volver", on_click=lambda: st.session_state.update(vista_participes='busqueda'))
    st.title("🚀 Migración Masiva")
    
    st.info("Sincroniza los datos maestro desde Google Sheets.")
    
    if st.button("Iniciar Sincronización"):
        with st.status("Migrando...", expanded=True) as status:
            try:
                from src.utils.migration_participes import migrate_participes_from_gsheet
                success, msg, count = migrate_participes_from_gsheet()
                if success:
                    st.write(f"✅ {msg}")
                    st.write(f"Partícipes Actualizados: {count}")
                    status.update(label="Completado", state="complete", expanded=False)
                    st.success("Migración Finalizada.")
                else:
                    status.update(label="Fallo", state="error", expanded=False)
                    st.error(msg)
            except Exception as e:
                st.error(f"Error: {e}")

# Router
if st.session_state.vista_participes == 'migracion':
    vista_migracion()
elif st.session_state.vista_participes in ['crear', 'editar']:
    render_form(st.session_state.vista_participes)
else:
    mostrar_busqueda()
