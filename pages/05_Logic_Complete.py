import streamlit as st
import graphviz

def render_complete_logic():
    st.title("Lógica de Negocio CRM: Versión Completa con Detalles")
    
    st.markdown("""
    Este diagrama modela el ciclo de vida completo de una inversión, desde el depósito inicial 
    hasta la generación y tratamiento de los cupones bimestrales, incluyendo todos los documentos y procesos.
    """)
    
    dot_code = """
    digraph CRMLogicComplete {
        rankdir=TB;
        graph [bgcolor="#ffffff"];
        node [shape=box, style="filled,rounded", fontname="Arial", fontsize=10];
        edge [fontname="Arial", fontsize=9];

        # --- ENTITIES ---
        subgraph cluster_master {
            label = "1. Configuración Inicial";
            style = filled;
            color = "#E1F5FE";
            Person [label="👤 Partícipe", shape=ellipse, fillcolor="#FFFFFF"];
            Fund [label="🏦 Fondo (Reglas de Tasa)", shape=cylinder, fillcolor="#FFFFFF"];
        }

        # --- INCEPTION ---
        subgraph cluster_inception {
            label = "2. Nacimiento del Depósito";
            style = filled;
            color = "#FFF3E0";
            
            Deposit [label="💰 Depósito Nuevo", fillcolor="#FFE0B2"];
            Rules [label="📜 Fijar Reglas", fillcolor="#FFE0B2"];
            Attr [label="Instrucción:\\n¿Pagar o Capitalizar?", shape=diamond, fillcolor="#FFCC80"];
        }

        # --- TIMELINE ---
        subgraph cluster_lifecycle {
            label = "3. Ciclo Bimestral";
            style = filled;
            color = "#F3E5F5";
            
            TimePass [label="⏳ Pasan 2 Meses", shape=plain];
            EventGen [label="⚡ Generar Evento/Cupón", shape=component, fillcolor="#E1BEE7"];
            Calc [label="🧮 Calcular Interés Bruto", fillcolor="#E1BEE7"];
            Tax [label="💸 Restar 5% Retención", fillcolor="#E1BEE7"];
            Net [label="💰 Obtener Neto", fillcolor="#BA68C8", fontcolor="white"];
        }

        # --- DECISION ---
        subgraph cluster_decision {
            label = "4. Bifurcación de Destino";
            style = filled;
            color = "#E8F5E9";
            
            Switch [label="¿Instrucción?", shape=diamond, fillcolor="#FFF59D"];
            
            # CAMINO A: PAGO
            PayoutNode [label="📤 Generar Orden de Pago", fillcolor="#C8E6C9"];
            Voucher [label="📄 PDF Voucher Interés", fillcolor="#C8E6C9"];
            Transfer [label="🏦 Transferencia Bancaria", fillcolor="#C8E6C9"];
            EndPeriodA [label="🏁 Fin Periodo\\n(Capital Intacto)", shape=none];
            
            # CAMINO B: CAPITALIZACION
            CompoundNode [label="📈 Sumar al Principal", fillcolor="#C8E6C9"];
            UpdateCert [label="🔄 Actualizar Certificado", fillcolor="#C8E6C9"];
            EndPeriodB [label="🏁 Fin Periodo\\n(Capital Aumentado)", shape=none];
        }

        # --- RELACIONES ---
        Person -> Deposit [label="Invierte"];
        Fund -> Rules [label="Define"];
        Rules -> Deposit [label="Aplica Tasa %"];
        Deposit -> Attr;
        
        Deposit -> TimePass;
        TimePass -> EventGen;
        EventGen -> Calc;
        Calc -> Tax;
        Tax -> Net;
        
        # Switch Logic
        Net -> Switch;
        Switch -> PayoutNode [label="Pagar"];
        Switch -> CompoundNode [label="Capitalizar"];
        
        # CAMINO PAGO
        PayoutNode -> Voucher;
        Voucher -> Transfer;
        Transfer -> EndPeriodA;
        
        # CAMINO CAPITALIZACION
        CompoundNode -> UpdateCert;
        UpdateCert -> EndPeriodB;
        
        # Loop implícito
        EndPeriodA -> TimePass [style=dotted, label="Esperar sgte bimestre"];
        EndPeriodB -> TimePass [style=dotted, label="Esperar sgte bimestre"];
    }
    """
    
    st.graphviz_chart(dot_code, use_container_width=True)

if __name__ == "__main__":
    render_complete_logic()
