import streamlit as st
import graphviz

def render_complete_db_logic():
    st.title("Lógica de Negocio CRM: Versión Completa con Tablas de Base de Datos")
    
    st.markdown("""
    Este diagrama muestra el flujo completo del CRM incluyendo las **tablas de base de datos** 
    que almacenan la información de cada módulo.
    """)
    
    dot_code = """
    digraph CRMLogicDB {
        rankdir=TB;
        splines=ortho;
        nodesep=0.6;
        ranksep=0.8;
        
        node [shape=box, style="filled,rounded", fontname="Arial", fontsize=10];
        edge [fontname="Arial", fontsize=9];

        # --- 1. MANTENIMIENTO ---
        subgraph cluster_maintenance {
            label = "1. MANTENIMIENTO / CONFIG\\n(Tabla: crm_fondos)";
            style = "filled,dashed";
            fillcolor = "#ECEFF1";
            color = "#455A64";
            
            Fund [label="🏦 Catálogo de Fondos", shape=cylinder, fillcolor="#FFFFFF"];
            
            DataManto [label="{Datos Clave:|• Nombre Fondo\\n• Moneda (PEN/USD)\\n• Plazo Mínimo\\n• Tasa % Anual}", shape=record, fontsize=9, fillcolor="#CFD8DC"];
            Fund -> DataManto [style=dotted, arrowhead=none];
        }

        # --- 2. PARTICIPES ---
        subgraph cluster_participes {
            label = "2. MAESTRO DE PARTÍCIPES\\n(Tabla: crm_participes)";
            style = "filled,dashed";
            fillcolor = "#E3F2FD";
            color = "#1E88E5";
            
            Person [label="👤 Partícipe", shape=ellipse, fillcolor="#FFFFFF"];
            
            DataParticipe [label="{Datos Clave:|• Datos Personales\\n• Contacto (Email/Cel)\\n• Cuenta Bancaria (CCI)}", shape=record, fontsize=9, fillcolor="#BBDEFB"];
            Person -> DataParticipe [style=dotted, arrowhead=none];
        }

        # --- 3. INVERSIONES ---
        subgraph cluster_inversiones {
            label = "3. GESTIÓN DE INVERSIONES\\n(Tabla: crm_inversiones)";
            style = "filled,dashed";
            fillcolor = "#FFF3E0";
            color = "#FB8C00";
            
            Deposit [label="💰 Depósito / Inversión", fillcolor="#FFE0B2"];
            Attr [label="Instrucción:\\n¿Pagar o Capitalizar?", shape=diamond, fillcolor="#FFCC80"];
            
            DataInv [label="{Datos Clave:|• Monto Invertido\\n• Plazo & Tasa (Snapshot)\\n• Fecha Inicio\\n• Estado}", shape=record, fontsize=9, fillcolor="#FFE0B2"];
            Deposit -> DataInv [style=dotted, arrowhead=none];
        }

        # --- 4. PROCESOS ---
        subgraph cluster_procesos {
            label = "4. PROCESOS (CIERRE BIMESTRAL)\\n(Motor de Cálculo)";
            style = "filled,dashed";
            fillcolor = "#F3E5F5";
            color = "#8E24AA";
            
            CheckFirst [label="¿Es Ingreso Reciente?\\n(Stub Period)", shape=diamond, fillcolor="#E1BEE7"];
            Calc [label="🧮 Calcular Interés\\n(-5% Retención)", fillcolor="#E1BEE7"];
            Net [label="💰 Neto Disponible", shape=box, fillcolor="#BA68C8", fontcolor="white"];
        }

        # --- 5. TESORERIA ---
        subgraph cluster_tesoreria {
            label = "5. TESORERÍA & REPORTES\\n(Ejecución)";
            style = "filled,dashed";
            fillcolor = "#E8F5E9";
            color = "#43A047";
            
            Payout [label="📤 PAGAR\\n(Transferencia)", fillcolor="#C8E6C9"];
            Compound [label="📈 CAPITALIZAR\\n(Re-invertir)", fillcolor="#C8E6C9"];
            
            Reports [label="📧 ENVIAR EMAILS\\n(Adjuntos)", shape=note, fillcolor="#A5D6A7"];
            DataDocs [label="{Adjuntos:|• Estado de Cuenta\\n• Cert. Retención}", shape=record, fontsize=9, fillcolor="#E8F5E9"];
            
            Reports -> DataDocs [style=dotted];
        }

        # --- 6. BOT (AL FINAL) ---
        subgraph cluster_bot {
            label = "6. AGENTE IA / BOT\\n(Lectura Transversal)";
            style = "filled,dashed";
            fillcolor = "#FFFDE7";
            color = "#FBC02D";
            
            Bot [label="🤖 Bot WhatsApp\\n(Lee todos los módulos)", shape=hexagon, fillcolor="#FFF59D"];
        }

        # --- CONEXIONES POR ORDEN VERTICAL FORZADO ---
        
        # 1. Manto -> Participes (Invisible para orden)
        DataManto -> Person [style=invis];
        
        # 2. Participes -> Inversiones
        Person -> Deposit [label="Crea Inversión"];
        DataParticipe -> Deposit [style=invis];
        
        # 3. Conexión Lógica (Manto -> Inversiones)
        Fund -> Deposit [label="Aplica Reglas", constraint=false, color="#455A64", style=dashed];

        # 4. Inversiones -> Procesos
        Deposit -> Attr;
        Attr -> CheckFirst [label="Ciclo Bimestral"];
        
        # 5. Procesos -> Tesoreria
        CheckFirst -> Calc -> Net;
        
        Net -> Payout [label="Si Pagar"];
        Net -> Compound [label="Si Capitalizar"];
        
        Payout -> Reports;
        Compound -> Reports;
        
        # 6. Tesoreria -> Bot (Visualmente abajo)
        Reports -> Bot [style=invis];
        
        # Conexiones Lógicas del Bot (Lectura)
        edge [style=dashed, color="#FBC02D", constraint=false, fontsize=8];
        Bot -> DataParticipe [label="Lee DNI"];
        Bot -> DataInv [label="Lee Saldos"];
        Bot -> Net [label="Consulta"];
    }
    """
    
    st.graphviz_chart(dot_code, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📊 Estructura de Base de Datos")
    st.markdown("""
    - **crm_fondos**: Catálogo de fondos con tasas y plazos
    - **crm_participes**: Datos personales y bancarios de inversionistas
    - **crm_inversiones**: Depósitos vinculados a partícipes y fondos
    """)

if __name__ == "__main__":
    render_complete_db_logic()
