
import sys
import os
import pandas as pd

# Add project root to path to allow importing src
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.utils.gsheets_integration import get_gsheets_client

def inspect_participes_columns():
    # ID del Sheet proporcionado por el usuario
    SHEET_ID = '1D8tl6nmQlr8MnxbwSAPhQ0WvEhagusgtNds1sJeNJDY'
    GID = '45831439'
    
    print(f"📊 Conectando a Sheet ID: {SHEET_ID}")
    
    try:
        client = get_gsheets_client()
        sheet = client.open_by_key(SHEET_ID)
        
        # Buscar la hoja por GID
        ws = None
        for w in sheet.worksheets():
            if str(w.id) == GID:
                ws = w
                break
        
        if not ws:
            print("❌ No se encontró la hoja con el GID especificado.")
            print("   Listando hojas disponibles:")
            for w in sheet.worksheets():
                print(f"   - {w.title} (GID: {w.id})")
            return

        print(f"✅ Hoja encontrada: {ws.title}")
        
        # Leer valores
        all_values = ws.get_all_values()
        
        if not all_values:
            print("❌ La hoja está vacía.")
            return

        print("\n--- MUESTRA DE PRIMERAS 5 FILAS (Para detectar headers) ---")
        for i, row in enumerate(all_values[:5]):
            print(f"Row {i+1}: {row}")
            
        # Intentar detectar headers automáticamente o usar fila 3
        headers_row_idx = 2 # Default to row 3 (0-indexed)
        if len(all_values) > headers_row_idx:
            headers = all_values[headers_row_idx]
            
            print("\n--- COLUMNAS DETECTADAS (Fila 3) ---")
            with open('participes_columns_dump.txt', 'w', encoding='utf-8') as f:
                for i, col in enumerate(headers):
                    if col.strip():
                        print(f"{i}: {col}")
                        f.write(f"{col}\n")
            print(f"\n💾 Columnas guardadas en participes_columns_dump.txt")
        else:
            print("⚠️ No hay suficientes filas para leer headers en la fila 3.")

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"❌ Error: {repr(e)}")

if __name__ == "__main__":
    inspect_participes_columns()
