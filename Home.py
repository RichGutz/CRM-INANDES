
import streamlit as st
import sys
import os

# Ajuste de path para imports si fuera necesario
sys.path.insert(0, os.path.abspath('.'))

st.set_page_config(page_title="Flujo CRM Inandes", layout="wide")

# render_header("CRM Inandes - Flujo de Procesos")
st.title("CRM Inandes - V2 (Updated)")

st.markdown("### Diagrama de Flujo CRM Inandes")
st.markdown("Basado en el análisis de requerimientos (Audios de WhatsApp).")

st.graphviz_chart("""
digraph CRM_Inandes {
    rankdir=TB;
    node [shape=box, style="filled,rounded", fontname="Arial", fontsize=10];
    edge [fontname="Arial", fontsize=9];

    # --- ACTORES ---
    User [label="Partícipe (Inversionista)", shape=person, fillcolor="#E1F5FE"];
    Admin [label="Administrador Inandes", shape=person, fillcolor="#E1F5FE"];

    # --- FLUJO PRINCIPAL (Columna Vertebral) ---
    
    subgraph cluster_mod1 {
        label = "PASO 1: Maestro de Partícipes\n(Alta de Cliente)";
        style = filled;
        color = "#E3F2FD";
        
        AltaParticipe [label="Alta de Partícipe", shape=diamond, fillcolor="#BBDEFB"];
        MasterDB [label="BASE DE DATOS MAESTRA", shape=cylinder, style="filled,dashed", fillcolor="#90CAF9"];
        
        AltaParticipe -> MasterDB;
    }

    subgraph cluster_mod2 {
        label = "PASO 2: Gestión de Fondos\n(Operativa Diaria)";
        style = filled;
        color = "#FFF3E0";
        
        InputCapital [label="Registro Ingreso Capital", fillcolor="#FFE0B2"];
        CierreBimestre [label="Cierre Bimestre", shape=doublecircle, fillcolor="#FFAB91"];
        
        InputCapital -> CierreBimestre [label="Procesa Periodo"];
    }

    subgraph cluster_mod3 {
        label = "PASO 3: Cuenta Corriente & Reportes\n(Saldos y Documentos)";
        style = filled;
        color = "#E8F5E9";
        
        Posicion [label="Cálculo Rentabilidad", fillcolor="#C8E6C9"];
        GenerarDocs [label="Generación PDF:\nEstado Cuenta y Certificados", shape=note, fillcolor="#A5D6A7"];

        Posicion -> GenerarDocs;
    }

    subgraph cluster_bot {
        label = "PASO FINAL: Bot WhatsApp\n(Atención al Inversionista)";
        style = filled;
        color = "#F3E5F5";
        penwidth = 2;
        
        Inicio [label="📱 Chat WhatsApp", shape=circle, fillcolor="#E1BEE7"];
        Verif [label="Verificación Identidad", shape=diamond, fillcolor="#CE93D8"];
        Respuestabot [label="🤖 RESPUESTA AUTOMÁTICA:\n- Saldo Actual\n- Último Pago\n- PDF Adjunto", shape=box, fillcolor="#BA68C8", fontcolor="white"];
        
        Inicio -> Verif -> Respuestabot;
    }

    # --- CONEXIONES ENTRE MÓDULOS (Flujo Lógico) ---
    Admin -> AltaParticipe [label="Alta"];
    Admin -> InputCapital [label="Inversión"];
    
    MasterDB -> InputCapital [style="dashed", label="Vincula"];
    CierreBimestre -> Posicion [label="Alimenta"];
    
    # --- CONEXIONES AL BOT ---
    User -> Inicio [label="Consulta"];
    
    MasterDB -> Verif [style="dotted", label="Valida Datos"];
    Posicion -> Respuestabot [style="dotted", label="Lee Saldo"];
    GenerarDocs -> Respuestabot [style="dotted", label="Obtiene PDF"];

    # --- FORZAR ORDEN VERTICAL ESCRITO ---
    edge [style=invis];
    MasterDB -> InputCapital -> Posicion -> Inicio;
}
""", use_container_width=True)
