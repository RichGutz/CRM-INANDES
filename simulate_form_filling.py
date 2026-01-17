
import json

def simulate_filling():
    # 1. Array con los campos propuestos (Schema CRM_PARTICIPES)
    # Estos son las columnas que tendremos en la Base de Datos
    crm_participes_schema = [
        "tipo_doc", "documento_identidad", "nombre_completo", 
        "fecha_nacimiento", "estado_civil", "nacionalidad", "residente_peru",
        "email", "telefono", "direccion_fiscal", "codigo_postal",
        "ocupacion", "centro_labores", "cargo_ocupado", "antiguedad_laboral_anios",
        "perfil_riesgo", "es_pep", "pep_detalle",
        "banco_nombre", "numero_cuenta", "cci", "moneda_cuenta",
        "conyuge_nombre", "conyuge_documento",
        "cotitular_nombre", "cotitular_documento",
        "asesor_nombre", "asesor_email"
    ]

    # 2. Simulación de Datos (Mock Data)
    mock_participe = {
        "tipo_doc": "DNI",
        "documento_identidad": "45892134",
        "nombre_completo": "Juan Perez del Solar",
        "fecha_nacimiento": "1985-04-12",
        "estado_civil": "Casado",
        "nacionalidad": "Peruana",
        "residente_peru": True,
        "email": "juan.perez@email.com",
        "telefono": "999888777",
        "direccion_fiscal": "Av. Javier Prado 123, San Isidro, Lima",
        "codigo_postal": "15036",
        "ocupacion": "Gerente Comercial",
        "centro_labores": "Inversiones SAC",
        "cargo_ocupado": "Gerente",
        "antiguedad_laboral_anios": 5,
        "perfil_riesgo": "Moderado", 
        "es_pep": False,
        "pep_detalle": None,
        "banco_nombre": "BCP",
        "numero_cuenta": "193-12345678-0-01",
        "cci": "002-193-12345678001-12",
        "moneda_cuenta": "USD",
        "conyuge_nombre": "Maria Gonzalez",
        "conyuge_documento": "41234567",
        "cotitular_nombre": None,
        "cotitular_documento": None,
        "asesor_nombre": "Ricardo Gutierrez",
        "asesor_email": "rgallo@inandes.com"
    }

    print("✅ DATOS DE SIMULACIÓN CARGADOS (Tabla crm_participes)")
    print(json.dumps(mock_participe, indent=2))
    print("\n" + "="*60 + "\n")

    # 3. Validación vs Formatos
    # Definimos qué campos pide cada documento (basado en análisis previo)
    
    forms = {
        "PDF 01: Perfil de Riesgo": {
            "required": ["nombre_completo", "asesor_nombre"],
            "dynamic": ["fecha_firma", "respuestas_test"], # No están en Tabla Participe
            "status": "PARCIAL" 
        },
        "PDF 02: Ficha de Datos": {
            "required": ["nombre_completo", "tipo_doc", "documento_identidad", "direccion_fiscal", "fecha_nacimiento", "email", "telefono", "estado_civil", "conyuge_nombre", "conyuge_documento"],
            "dynamic": ["fecha_firma"],
            "status": "COMPLETO (Salvo fecha firma)"
        },
        "PDF 03: Origen de Fondos": {
            "required": ["nombre_completo", "tipo_doc", "documento_identidad", "nacionalidad", "residente_peru", "estado_civil", "ocupacion", "centro_labores", "cargo_ocupado", "antiguedad_laboral_anios"],
            "dynamic": ["monto_operacion", "moneda_operacion", "origen_fondos_detalle"], # Específico de la inversión
            "status": "PARCIAL (Faltan datos de la operación)"
        },
        "PDF 04: PEP": {
            "required": ["nombre_completo", "es_pep", "pep_detalle"],
            "dynamic": ["fecha_firma"],
            "status": "COMPLETO (Salvo fecha firma)"
        },
        "Word: Certificado/Estado Cuenta": {
            "required": ["nombre_completo", "direccion_fiscal", "documento_identidad"],
            "dynamic": ["monto_invertido", "ganancia", "impuestos", "valor_cuota"], # Datos de Inversión
            "status": "PARCIAL (Falta data financiera)"
        }
    }

    # 4. Reporte de Cobertura
    print("📊 REPORTE DE COBERTURA DE FORMATOS")
    for form_name, specs in forms.items():
        print(f"\n📄 {form_name}")
        
        # Verificar campos estáticos presentes
        present = [f for f in specs['required'] if f in mock_participe]
        missing = [f for f in specs['required'] if f not in mock_participe]
        
        if missing:
            print(f"   ❌ FALTAN CAMPOS ESTÁTICOS: {missing}")
        else:
            print(f"   ✅ Campos estáticos cubiertos: 100%")
            
        if specs['dynamic']:
            print(f"   ⚠️  Requiere campos dinámicos (Tabla Inversiones): {specs['dynamic']}")
            
        print(f"   RESULTADO: {specs['status']}")

if __name__ == "__main__":
    simulate_filling()
