
import sys
import os

# Asegurar que podemos importar desde src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.gsheets_integration import read_sheet_data

def inspect_sheet():
    # ID del Sheet proporcionado (NUEVO LINK NATIVO)
    SHEET_ID = '1NIgBsPHeEhyQR4ypD-Cpgvvnky-HxJ2lTJemawkVh2E'
    # GID extraído de la URL (#gid=45831439)
    GID = '45831439'
    
    print(f"Conectando a Sheet ID: {SHEET_ID}")
    print(f"Conectando a Sheet ID: {SHEET_ID}")
    
    try:
        from src.utils.gsheets_integration import list_worksheets, read_sheet_data
        
        # 1. Listar Worksheets para ver si el archivo es accesible y qué pestañas tiene
        sheets = list_worksheets(SHEET_ID)
        print(f"\n--- PESTAÑAS DISPONIBLES ({len(sheets)}) ---")
        for s in sheets:
            print(f"ID: {s['id']} | Título: {s['title']} | Filas: {s['row_count']}")
            
        if not sheets:
            print("ERROR: No se encontraron pestañas.")
            return

        if not sheets:
            print("ERROR: No se encontraron pestañas.")
            return

        # 3. Iterar sobre TODAS las pestañas para validar consistencia
        print(f"\n--- ANALIZANDO {len(sheets)} PESTAÑAS ---")
        
        from src.utils.gsheets_integration import get_gsheets_client
        client = get_gsheets_client()
        sheet = client.open_by_key(SHEET_ID)
        
        for s_info in sheets:
            gid = s_info['id']
            title = s_info['title']
            print(f"\n>>> PROCESANDO PESTAÑA: {title} (GID: {gid})")
            
            # Buscar worksheet object
            ws = None
            for w in sheet.worksheets():
                if str(w.id) == str(gid):
                    ws = w
                    break
            
            if not ws:
                print(f"   [WARN] No se pudo abrir objeto worksheet para {title}")
                continue
                
            all_values = ws.get_all_values()
            
            # Headers en fila 3 (index 2)
            headers_row_idx = 2
            if len(all_values) <= headers_row_idx:
                print("   [SKIP] Archivo muy corto/vacío.")
                continue

            headers = all_values[headers_row_idx]
            
            # --- NUEVO: Extraer Metadata del Fondo (Fila 1) ---
            metadata_fondo = {}
            if len(all_values) > 0:
                row1 = all_values[0]
                # Búsqueda heurística básica en la fila 1
                # Ejemplo real: ['', '', 'Fecha de inicio :', 'Fecha de término:', 'sábado, noviembre 01, 2025', 'miércoles, diciembre 31, 2025']
                # Parece que la estructura es Key -> Value en celdas adyacentes o cercanas
                print(f"   [INFO] Fila 1 (Metadata): {row1}")
                metadata_fondo['raw_row1'] = row1

            # Identificar columnas clave presentes
            cols_found = [c for c in headers if c.strip()]
            print(f"   Columnas detectadas: {len(cols_found)}")
            # Imprimir las primeras 5 para validar visualmente
            print(f"   Primeras 5 columnas: {cols_found[:5]}")
            
            # Validar si tiene las columnas críticas
            critical = ['NOMBRE_COMPLETO_P1', 'MONTO INVERTIDO']
            missing = [c for c in critical if c not in cols_found]
            if missing:
                print(f"   [ALERTA] Faltan columnas críticas: {missing}")
            else:
                print("   [OK] Esquema parece compatible.")

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\nERROR AL ACCEDER: {e}")
        print("\nPosibles causas:")
        print("1. El archivo sigue siendo un EXCEL (.xlsx) y no un Google Sheet nativo.")
        print("2. Permisos insuficientes (Verificar email del Service Account).")

if __name__ == "__main__":
    inspect_sheet()
