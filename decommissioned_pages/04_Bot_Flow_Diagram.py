import streamlit as st
import graphviz

def render_bot_flow():
    st.title("Diagrama de Flujo: Bot WhatsApp")
    
    st.markdown("### Lógica de Interacción")
    st.markdown("Este diagrama representa la máquina de estados del Bot simulado.")
    
    # Extracting the Mermaid / Graphviz logic from bot_flow.md manually since I have the content in memory/history (Step 26)
    # But I will prefer using the Graphviz version provided in the markdown file for better rendering in Streamlit.
    
    dot_code = """
    digraph WhatsAppBot {
        rankdir=TB;
        graph [bgcolor="#ffffff"];
        node [shape=box, style="filled,rounded", fontname="Arial", fontsize=10];
        edge [fontname="Arial", fontsize=9];

        Start [label="Inicio (WhatsApp)", shape=circle, fillcolor="#E1F5FE"];
        Verify [label="Verificación de Identidad", shape=diamond, fillcolor="#FFF9C4"];
        
        Q1 [label="Pregunta 1: DNI", fillcolor="#FFF59D"];
        Q2 [label="Pregunta 2: Dirección", fillcolor="#FFF59D"];
        Q3 [label="Pregunta 3: Seguridad", fillcolor="#FFF59D"];
        
        AccessGranted [label="✅ Acceso Concedido", shape=doublecircle, fillcolor="#C8E6C9"];
        AccessDenied [label="❌ Acceso Denegado", shape=octagon, fillcolor="#FFCDD2"];

        Menu [label="📌 Menú Principal", shape=note, fillcolor="#BBDEFB"];
        
        Start -> Verify -> Q1;
        Q1 -> Q2 [label="Correcto"];
        Q2 -> Q3 [label="Correcto"];
        Q3 -> AccessGranted [label="Correcto"];
        
        Q1 -> AccessDenied [label="Incorrecto"];
        Q2 -> AccessDenied;
        Q3 -> AccessDenied;
        
        AccessGranted -> Menu;
    }
    """
    
    st.graphviz_chart(dot_code, use_container_width=True)

if __name__ == "__main__":
    render_bot_flow()
