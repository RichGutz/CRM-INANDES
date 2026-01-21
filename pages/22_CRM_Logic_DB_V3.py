import streamlit as st
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta
import graphviz

# --- LOGIC & SIMULATION ENGINE V3 ---

class TicketSimulatorV3:
    """
    Simulador de Ticket Individual bajo Reglas de Negocio V3.
    REGLA DE ORO: Un Ticket es una unidad atómica.
    - Los APORTES ADICIONALES crean NUEVOS Tickets (no modifican este).
    - Los RESCATES (Retiros) sí modifican el saldo de este ticket.
    """
    def __init__(self, monto, tasa_anual, fecha_inicio, plazo_meses, modalidad, pct_capitalizable=0, 
                 rescates_programados=None):
        """
        :param pct_capitalizable: Porcentaje del interés neto que se reinvierte.
                                  0 = Se paga todo (Pago Cupón).
                                  100 = Se capitaliza todo.
        :param rescates_programados: Lista de dicts [{'mes': 6, 'monto': 5000, 'penalidad_pct': 2}]
        """
        self.monto_inicial = monto
        self.saldo_actual = monto
        self.tasa_anual = tasa_anual
        self.fecha_inicio = fecha_inicio
        self.plazo_meses = plazo_meses
        self.fecha_fin = fecha_inicio + relativedelta(months=plazo_meses)
        self.modalidad = modalidad # Referencial, la lógica real usa pct_capitalizable
        self.pct_capitalizable = pct_capitalizable 
        
        # Rescates (Lista de eventos programados)
        self.rescates_programados = rescates_programados if rescates_programados else []
        self.rescates_programados.sort(key=lambda x: x['mes']) # Ordenar por mes
        
        self.eventos = []

    def generar_calendario(self):
        fecha_cursor = self.fecha_inicio
        
        # 1. EVENTO NACIMIENTO
        self.eventos.append({
            "Fecha": self.fecha_inicio,
            "Evento": "👶 NACIMIENTO",
            "Detalle": f"Origen Ticket | Tasa {self.tasa_anual}% | Plazo {self.plazo_meses}m",
            "Monto": self.monto_inicial,
            "Saldo": self.monto_inicial
        })
        
        # Loop Bimestral (o Mensual si se requiere, asumimos Bimestral por defecto en Inandes)
        # Ajuste: El loop avanza de corte en corte.
        while fecha_cursor < self.fecha_fin:
            if self.saldo_actual <= 0:
                break

            fecha_corte = fecha_cursor + relativedelta(months=2) # Default next cut
            if fecha_corte > self.fecha_fin:
                fecha_corte = self.fecha_fin
            
            # --- DETECCION DE RESCATES EN ESTE PERIODO ---
            # Verificamos si hay un rescate programado ANTES del corte
            rescate_in_period = None
            for r in self.rescates_programados:
                fecha_rescate_teorica = self.fecha_inicio + relativedelta(months=r['mes'])
                if fecha_cursor < fecha_rescate_teorica <= fecha_corte:
                    rescate_in_period = r
                    rescate_in_period['fecha_real'] = fecha_rescate_teorica
                    break # Solo procesamos un rescate mayor por periodo en esta simulacion simple
            
            # --- PROCESAMIENTO ---
            if rescate_in_period:
                # Hay un corte intermedio por Rescate
                fecha_evento = rescate_in_period['fecha_real']
                es_rescate = True
            else:
                fecha_evento = fecha_corte
                es_rescate = False
            
            # CALCULO DE INTERESES (Días reales / 360)
            dias = (fecha_evento - fecha_cursor).days
            if dias < 0: dias = 0
            
            interes_bruto = self.saldo_actual * (self.tasa_anual/100) * (dias/360)
            impuesto = interes_bruto * 0.05
            interes_neto = interes_bruto - impuesto
            
            # 2. EVENTO CORTE DE INTERES (Siempre ocurre al corte o rescate)
            if dias > 0:
                self.eventos.append({
                    "Fecha": fecha_evento,
                    "Evento": "⏱️ DEVENGUE INTERÉS" if es_rescate else "🗓️ CIERRE PERIODO",
                    "Detalle": f"Interés {dias} días sobre {self.saldo_actual:,.2f}",
                    "Monto": interes_neto,
                    "Saldo": self.saldo_actual # Aún no cambia
                })
            
            # DISTRIBUCION DE INTERESES (PAGO vs CAPITALIZACION)
            # Regla: Si es Rescate Total, el interés pendiente se suele pagar o capitalizar para liquidar.
            # Asumimos regla general: Se aplican preferencias de cliente.
            
            monto_capitalizar = interes_neto * (self.pct_capitalizable / 100)
            monto_pagar = interes_neto - monto_capitalizar
            
            if monto_pagar > 0.01:
                self.eventos.append({
                    "Fecha": fecha_evento,
                    "Evento": "💸 PAGO CUPÓN",
                    "Detalle": "Transferencia a Cliente",
                    "Monto": -monto_pagar,
                    "Saldo": self.saldo_actual
                })
            
            if monto_capitalizar > 0.01:
                self.saldo_actual += monto_capitalizar
                self.eventos.append({
                    "Fecha": fecha_evento,
                    "Evento": "📈 CAPITALIZACIÓN",
                    "Detalle": "Interés compuesto",
                    "Monto": monto_capitalizar,
                    "Saldo": self.saldo_actual
                })

            # 3. EJECUCION DEL RESCATE (Si aplica)
            if es_rescate:
                monto_solicitado = rescate_in_period['monto']
                penalidad_pct = rescate_in_period.get('penalidad_pct', 0)
                
                # Validar Topes
                tipo_rescate = "PARCIAL"
                if monto_solicitado >= self.saldo_actual:
                    monto_solicitado = self.saldo_actual
                    tipo_rescate = "TOTAL"
                
                penalidad_monto = monto_solicitado * (penalidad_pct / 100)
                neto_recibir = monto_solicitado - penalidad_monto
                
                self.saldo_actual -= monto_solicitado
                
                self.eventos.append({
                    "Fecha": fecha_evento,
                    "Evento": f"🚑 RESCATE {tipo_rescate}",
                    "Detalle": f"Solicitado: {monto_solicitado:,.2f} | Penalidad {penalidad_pct}%",
                    "Monto": -neto_recibir, # Salida de caja neta
                    "Saldo": self.saldo_actual
                })
                
                # Remover de pendientes
                self.rescates_programados.remove(rescate_in_period)
                
                if self.saldo_actual <= 0.01:
                    self.eventos.append({
                        "Fecha": fecha_evento,
                        "Evento": "🏁 LIQUIDACIÓN ANTICIPADA",
                        "Detalle": "Saldo agotado por rescate",
                        "Monto": 0,
                        "Saldo": 0
                    })
                    return pd.DataFrame(self.eventos)

            # Avanzar cursor
            fecha_cursor = fecha_evento
            
        # 4. EVENTO FINAL (Retorno Capital)
        if self.saldo_actual > 0.01:
             self.eventos.append({
                "Fecha": self.fecha_fin,
                "Evento": "🏁 RETORNO CAPITAL",
                "Detalle": "Vencimiento del Plazo",
                "Monto": -self.saldo_actual,
                "Saldo": 0
            })
             
        return pd.DataFrame(self.eventos)

# --- UI COMPONENTS V3 ---

def render_diagram_v3():
    st.markdown("### 🧬 Arquitectura V3: Flujo Estricto de Eventos")
    st.info("Reglas V3: Aportes crean nuevos Tickets (Hijos). Rescates reducen Saldo.")
    
    dot = """
    digraph CRMLogicV3 {
        rankdir=LR;
        node [shape=box, style="filled,rounded", fontname="Arial"];
        
        # ACTORES
        Cliente [shape=ellipse, fillcolor="#BBDEFB", label="👤 Cliente"];
        
        # TICKETS (Entidades Independientes)
        subgraph cluster_tickets {
            label = "Portafolio de Inversiones";
            style = "dashed"; color = "#607D8B";
            
            Ticket1 [shape=folder, fillcolor="#C8E6C9", label="📄 Ticket #1\n(Saldo A)"];
            Ticket2 [shape=folder, fillcolor="#C8E6C9", label="📄 Ticket #2\n(Saldo B)"];
            
            Ticket1 -> Ticket2 [style=invis]; # Layout force
        }
        
        # EVENTOS DE ENTRADA
        Origen [label="👶 NACIMIENTO\n(Depósito Inicial)", fillcolor="#FFCC80"];
        Aporte [label="💰 APORTE ADICIONAL\n(Crea Nuevo Ticket)", fillcolor="#FFCC80"];
        
        Cliente -> Origen;
        Cliente -> Aporte;
        
        Origen -> Ticket1 [label="Crea"];
        Aporte -> Ticket2 [label="Crea Indep."];
        
        # EVENTOS DE SALIDA (Rescates)
        Rescate [label="🚑 RESCATE\n(Parcial/Total)", shape=note, fillcolor="#FFCDD2"];
        
        Cliente -> Rescate [label="Solicita"];
        Rescate -> Ticket1 [label="Reduce Saldo", color="red"];
        
        # MOTOR BIMESTRAL
        Motor [shape=diamond, label="⚙️ Motor\nCálculo", fillcolor="#E1BEE7"];
        
        Ticket1 -> Motor;
        Ticket2 -> Motor;
        
        Pago [label="💸 PAGO CUPÓN", fillcolor="#B2DFDB"];
        Cap [label="📈 CAPITALIZACIÓN", fillcolor="#B2DFDB"];
        
        Motor -> Pago [label="Si Cap=0%"];
        Motor -> Cap [label="Si Cap>0%"];
        
        Cap -> Ticket1 [label="Aumenta Saldo", style=dashed, color="blue"];
        
    }
    """
    st.graphviz_chart(dot, use_container_width=True)

def render_simulator_v3():
    st.markdown("### 🧮 Simulador V3 (Reglas Estrictas)")
    
    with st.form("sim_v3"):
        c1, c2, c3 = st.columns(3)
        monto = c1.number_input("Monto Ticket", value=10000.0, step=1000.0)
        tasa = c2.number_input("Tasa Anual (%)", value=12.0)
        plazo = c3.selectbox("Plazo (Meses)", [12, 18, 24, 36])
        
        c4, c5 = st.columns(2)
        inicio = c4.date_input("Fecha Inicio", value=dt.date.today())
        pct_cap = c5.slider("% Capitalización (Reinvest)", 0, 100, 0, help="0% = Pagar Todo. 100% = Interés Compuesto.")
        
        st.divider()
        st.markdown("#### Programación de Rescates")
        has_rescate = st.checkbox("Incluir Rescate Parcial")
        r_mes = st.number_input("Mes del Rescate", 1, plazo-1, 6, disabled=not has_rescate)
        r_monto = st.number_input("Monto Rescate", 0.0, monto, 2000.0, disabled=not has_rescate)
        
        if st.form_submit_button("🚀 Simular Ticket Individual"):
            rescates = []
            if has_rescate:
                rescates.append({'mes': r_mes, 'monto': r_monto, 'penalidad_pct': 0})
                
            sim = TicketSimulatorV3(monto, tasa, inicio, plazo, "CUSTOM", pct_cap, rescates)
            df = sim.generar_calendario()
            
            c_res1, c_res2 = st.columns(2)
            c_res1.success(f"Saldo Final: {sim.saldo_actual:,.2f}")
            c_res2.info(f"Total Eventos: {len(df)}")
            
            st.dataframe(df.style.format({
                'Monto': "{:,.2f}", 
                'Saldo': "{:,.2f}"
            }))

def render_v3_logic():
    st.title("🧠 Lógica DB V3: Reglas de Negocio Oficiales")
    st.warning("Versión Refinada: Manejo estricto de Aportes (Hijos) y Rescates.")
    
    tab1, tab2 = st.tabs(["Diagrama V3", "Simulador V3"])
    with tab1:
        render_diagram_v3()
    with tab2:
        render_simulator_v3()

if __name__ == "__main__":
    render_v3_logic()
