# Reglas de Negocio y Eventos CRM V3

## 1. Principios Fundamentales
Este documento define las reglas estrictas para la lógica de negocio de inversiones (Tickets) en el módulo CRM V3. Estas definiciones alimentan el diseño del pseudocódigo y la implementación en Python.

## 2. Definición de Eventos

### A. Nacimiento / Origen
- **Evento**: `NACIMIENTO`
- **Descripción**: Creación inicial de un Ticket de Inversión.
- **Regla**: Todo ticket nace con un saldo inicial, una tasa pactada, una fecha de inicio y una configuración de pago/capitalización.

### B. Aportes Adicionales (Top-ups)
- **Evento**: `APORTE_ADICIONAL`
- **Regla Crítica**: ❌ **NO** se suma al saldo del ticket existente.
- **Acción**: ✅ **CREA UN NUEVO TICKET**.
    - El nuevo aporte se trata como una inversión independiente (Hijo) con sus propias condiciones (que pueden o no heredar las del padre, pero es una entidad distinta).
    - **Razón**: Permite manejar tasas/plazos distintos para el dinero nuevo y facilita la trazabilidad.

### C. Rescates (Retiros)
- **Evento**: `RESCATE_PARCIAL`
    - **Descripción**: El cliente rescata una parte del capital antes del vencimiento.
    - **Acción**: Reduce el `Saldo Actual` del ticket.
    - **Consecuencia**: Los intereses futuros se calculan sobre el nuevo saldo reducido. Puede aplicar penalidad.
- **Evento**: `RESCATE_TOTAL` (Liquidación Anticipada)
    - **Descripción**: El cliente rescata todo el dinero.
    - **Acción**: El saldo llega a 0. El ticket cambia de estado a `TERMINADO` o `LIQUIDADO`.

### D. Capitalización vs. Pago (Intereses)
- **Evento**: `CORTE_INTERES` (Cierre de periodo, usualmente mensual o bimestral).
- **Reglas**:
    1.  **Por Defecto (0% Capitalización)**:
        - Se asume que el cliente quiere **cobrar** sus intereses.
        - Se genera un evento `PAGO_CUPON`.
    2.  **Capitalización Parcial**:
        - Un % se paga (`PAGO_CUPON`) y el resto se suma al capital (`CAPITALIZACION`).
        - *Ejemplo*: 30% se paga, 70% se reinvierte.
    3.  **Capitalización Total (100%)**:
        - No hay salida de caja. Todo el interés neto se suma al `Saldo Actual`.
        - Genera evento `CAPITALIZACION`.

### E. Cambios Administrativos
- **Evento**: `CESION_DERECHOS` (Cambio de Titular)
    - **Descripción**: El ticket cambia de dueño.
    - **Regla**: Se mantiene la antigüedad y condiciones del ticket original, pero se actualiza el `Participante` asociado.
    - **Auditoría**: Debe quedar registro de quién era el dueño anterior.

## 3. Resumen de Flujo
1.  **Inicio**: Cliente deposita 10k -> Crea Ticket #1.
2.  **Mes 2**: Cliente deposita 5k más -> Crea Ticket #2 (Independiente).
3.  **Cierre**: Ticket #1 genera interés. Si Cap=0%, se paga. Ticket #2 genera su propio interés.
4.  **Rescate**: Cliente pide 2k del Ticket #1. Ticket #1 baja a 8k. Ticket #2 sigue en 5k.
