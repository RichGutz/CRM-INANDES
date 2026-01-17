
import graphviz
import os

def render_static():
    # Mismo DOT que en el script de Streamlit
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
            
            Deposit [label="💰 Depósito (Inversión)\n(Monto, Plazo, Tasa Congelada)", fillcolor="#FFE0B2"];
            Attr [label="Instrucción:\n¿Pagar o Capitalizar?", shape=diamond, fillcolor="#FFCC80"];
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
            
            Payout [label="📤 PAGAR\n(Transferencia)"];
            Compound [label="📈 CAPITALIZAR\n(Sumar al Principal)"];
            
            EndA [label="Fin Periodo\n(Capital Intacto)", shape=none];
            EndB [label="Fin Periodo\n(Capital Aumentado)", shape=none];
        }

        # --- RELACIONES ---
        Person -> Deposit [label="Invierte"];
        Fund -> Deposit [label="Define Reglas"];
        Deposit -> Attr;
        
        Deposit -> TimePass;
        TimePass -> EventGen;
        EventGen -> Calc -> Tax -> Net;
        
        # Switch Logic
        Net -> Payout [label="Si 'PAGAR'"];
        Net -> Compound [label="Si 'CAPITALIZAR'"];
        
        Payout -> EndA;
        Compound -> EndB;
        
        # Loop implícito
        EndA -> TimePass [style=dotted, label="Siguiente..."];
        EndB -> TimePass [style=dotted, label="Siguiente..."];
    }
    """
    
    # Renderizar a archivo
    output_path = os.path.join(os.path.dirname(__file__), 'flowchart_preview')
    try:
        graph = graphviz.Source(dot_code)
        output = graph.render(output_path, format='png', cleanup=True)
        print(f"✅ Diagrama generado exitosamente en: {output}")
    except Exception as e:
        print(f"❌ Error generando diagrama: {e}")
        print("Asegúrate de tener Graphviz instalado en el sistema (apt-get install graphviz).")

if __name__ == "__main__":
    render_static()
