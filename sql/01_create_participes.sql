-- CRACION DE TABLA MAESTRA DE PARTICIPES
-- Objetivo: Centralizar datos estáticos de clientes (separado de inversiones)
-- Fecha: 2026-01-17

CREATE TABLE IF NOT EXISTS crm_participes (
    -- Identificación Principal
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    tipo_doc VARCHAR(20) NOT NULL, -- DNI, CEX, PASAPORTE
    documento_identidad VARCHAR(20) NOT NULL UNIQUE, -- NO_DOC_P1 (Llave de negocio)
    nombre_completo VARCHAR(200) NOT NULL, -- NOMBRE_COMPLETO_P1
    
    -- Datos Personales Adicionales (Fichas)
    fecha_nacimiento DATE, -- De Ficha Participe 02
    estado_civil VARCHAR(50), -- De Ficha Participe 02
    nacionalidad VARCHAR(100), -- De Ficha Participe 03
    residente_peru BOOLEAN DEFAULT TRUE, -- De Ficha Participe 03
    
    -- Contacto
    email VARCHAR(100), -- EMAIL_P1
    telefono VARCHAR(50), -- TELEF_CELULAR_P1
    direccion_fiscal TEXT, -- DOMICILIO_FISCAL
    codigo_postal VARCHAR(20), -- CODIGO_POSTAL
    
    -- Datos Laborales / Origen Fondos (Ficha 03)
    ocupacion VARCHAR(100), -- Profesión/Ocupación
    centro_labores VARCHAR(200), -- Empresa
    cargo_ocupado VARCHAR(100), -- Cargo
    antiguedad_laboral_anios INT, -- Antigüedad
    
    -- Perfil y Cumplimiento (Fichas 01 y 04)
    perfil_riesgo VARCHAR(50), -- Conservador/Moderado/Audaz (Ficha 01)
    es_pep BOOLEAN DEFAULT FALSE, -- Persona Políticamente Expuesta (Ficha 04)
    pep_detalle JSONB, -- Detalles si es PEP (Cargo, relación, etc.)
    
    -- Información Bancaria Principal (Para abonos por defecto)
    banco_nombre VARCHAR(100), -- BANCO
    numero_cuenta VARCHAR(100), -- NO_CUENTA
    cci VARCHAR(100), -- CCI
    moneda_cuenta VARCHAR(10), -- MONEDA (USD/PEN)
    
    -- Conyuge / Cotitular
    conyuge_nombre VARCHAR(200),
    conyuge_documento VARCHAR(20),
    cotitular_nombre VARCHAR(200), -- NOMBRE_COMPLETO_P2
    cotitular_documento VARCHAR(20), -- NO_DOC_P2
    
    -- Asesor Asignado
    asesor_nombre VARCHAR(100), -- ASESOR
    asesor_email VARCHAR(100), -- EMAIL_ASESOR
    
    -- Auditoría
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    origen_datos VARCHAR(50) DEFAULT 'MIGRACION_GSHEET'
);

-- Índices para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_participes_documento ON crm_participes(documento_identidad);
CREATE INDEX IF NOT EXISTS idx_participes_email ON crm_participes(email);
CREATE INDEX IF NOT EXISTS idx_participes_asesor ON crm_participes(asesor_email);
