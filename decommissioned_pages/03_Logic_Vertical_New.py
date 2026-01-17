import streamlit as st
import graphviz
import os

def render_logic_page():
    st.title("Lógica de Negocio CRM: Flujo Verticalizado (Nuevo)")
    
    dot_code = """
    digraph CRMLogic {
        rankdir=TB;
        graph [bgcolor="#ffffff"];
        node [shape=box, style="filled,rounded", fontname="Arial", fontsize=10];
        edge [fontname="Arial", fontsize=9];

        # --- ENTIDADES ---
        subgraph cluster_master {
            label = "1. Configuración Inicial";
            style = filled;
            color = "#E1F5FE";
            Person [label="👤 Partícipe", shape=ellipse, fillcolor="#FFFFFF"];
            Fund [label="🏦 Fondo (Reglas Tasa)", shape=cylinder, fillcolor="#FFFFFF"];
        }

        # --- INCEPTION ---
        subgraph cluster_inception {
            label = "2. Nacimiento del Depósito";
            style = filled;
            color = "#FFF3E0";
            
            Deposit [label="💰 Depósito (Inversión)\\n(Monto, Plazo, Tasa Congelada)", fillcolor="#FFE0B2"];
            Attr [label="Instrucción:\\n¿Pagar o Capitalizar?", shape=diamond, fillcolor="#FFCC80"];
        }

        # --- TIMELINE ---
        subgraph cluster_lifecycle {
            label = "3. Ciclo Bimestral (Eventos)";
            style = filled;
            color = "#F3E5F5";
            
            TimePass [label="⏳ Pasan 2 Meses", shape=plain];
            EventGen [label="⚡ Generar Evento (Cupón)", shape=component, fillcolor="#E1BEE7"];
            Calc [label="🧮 Calcular: Cap * Tasa * Días", fillcolor="#E1BEE7"];
            Tax [label="💸 Restar 5% Retención", fillcolor="#E1BEE7"];
            Net [label="💰 Neto a Distribuir", shape=box, fillcolor="#BA68C8", fontcolor="white"];
        }

        # --- DECISION ---
        subgraph cluster_decision {
            label = "4. Switch de Destino";
            style = filled;
            color = "#E8F5E9";
            
            node [fillcolor="#C8E6C9"];
            
            Payout [label="📤 PAGAR\\n(Transferencia)"];
            Compound [label="📈 CAPITALIZAR\\n(Sumar al Principal)"];
            
            EndA [label="Fin Periodo\\n(Capital Intacto)", shape=none];
            EndB [label="Fin Periodo\\n(Capital Aumentado)", shape=none];
        }

        # --- RELACIONES ---
        Person -> Deposit [label="Invierte"];
        Fund -> Deposit [label="Define Reglas"];
        Deposit -> Attr;
        
        Deposit -> TimePass;
        TimePass -> EventGen;
        EventGen -> Calc -> Tax -> Net;
        
        # Switch Logic
        Net -> Payout [label="Si Pagar"];
        Net -> Compound [label="Si Capitalizar"];
        
        Payout -> EndA;
        Compound -> EndB;
        
        # Loop implícito
        EndA -> TimePass [style=dotted, label="Siguiente..."];
        EndB -> TimePass [style=dotted, label="Siguiente..."];
    }
    """
    
    st.graphviz_chart(dot_code, use_container_width=True)

if __name__ == "__main__":
    render_logic_page()
