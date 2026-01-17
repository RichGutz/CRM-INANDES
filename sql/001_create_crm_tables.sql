-- Crear esquema si no existe
-- CREATE SCHEMA IF NOT EXISTS crm;

-- 1. Tabla de Partícipes (Inversionistas)
CREATE TABLE IF NOT EXISTS crm_participes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    
    -- Identificación
    nombre_completo TEXT NOT NULL,
    tipo_doc TEXT, -- DNI, CE, PASAPORTE, RUC
    num_doc TEXT,
    
    -- Contacto
    email TEXT,
    telefono TEXT,
    direccion TEXT,
    ubigeo TEXT,
    
    -- Datos Bancarios (Principalmente para abonar intereses)
    banco TEXT,
    cuenta_bancaria TEXT,
    cci TEXT,
    
    -- Metada
    origen_datos TEXT DEFAULT 'GSHEET_MIGRATION',
    
    -- Restricción de Unicidad
    CONSTRAINT uq_participes_doc UNIQUE (tipo_doc, num_doc)
);

-- 2. Tabla de Fondos (Entidad que agrupa inversiones)
CREATE TABLE IF NOT EXISTS crm_fondos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    
    alias TEXT NOT NULL UNIQUE, -- Ejemplo: 'PEN01', 'USD01'
    nombre_oficial TEXT,         -- Ejemplo: 'Fondo Privado Inandes Soles I'
    
    moneda TEXT CHECK (moneda IN ('PEN', 'USD')),
    
    fecha_inicio DATE,
    fecha_fin DATE,
    
    tasa_anual_referencial NUMERIC(5, 4), -- 0.1200
    estado TEXT DEFAULT 'ACTIVO' -- ACTIVO, CERRADO, LIQUIDADO
);

-- 3. Tabla de Inversiones (Depositos vinculados a un Participes y un Fondo)
CREATE TABLE IF NOT EXISTS crm_inversiones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    
    -- Relación con Partícipes (Titular y Suplente)
    participe_titular_id UUID REFERENCES crm_participes(id) ON DELETE CASCADE NOT NULL,
    participe_suplente_id UUID REFERENCES crm_participes(id) ON DELETE SET NULL,
    
    -- Relación con el Fondo
    fondo_id UUID REFERENCES crm_fondos(id) ON DELETE RESTRICT NOT NULL,
    
    -- Detalles específicos de esta inversión
    moneda TEXT NOT NULL CHECK (moneda IN ('PEN', 'USD')), -- Redundante con fondo pero útil
    monto_invertido NUMERIC(18, 2) NOT NULL DEFAULT 0,
    monto_actual NUMERIC(18, 2), -- Puede crecer si capitaliza
    
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    
    num_certificado TEXT, -- Identificador único del certificado físico
    asesor_email TEXT,
    
    estado TEXT DEFAULT 'ACTIVO',
    
    -- Constraint: La moneda de la inversión debe coincidir con la del fondo (Logic check)
    CONSTRAINT uq_certificado_fondo UNIQUE (fondo_id, num_certificado) -- Evitar dupes en el mismo fondo
);

-- Indices
CREATE INDEX IF NOT EXISTS idx_participes_nombre ON crm_participes(nombre_completo);
CREATE INDEX IF NOT EXISTS idx_participes_doc ON crm_participes(num_doc);
CREATE INDEX IF NOT EXISTS idx_inversiones_fondo ON crm_inversiones(fondo_id);
