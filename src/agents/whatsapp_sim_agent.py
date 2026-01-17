import random
import time
from datetime import datetime

class WhatsAppFinanceBot:
    """
    Simulates the logic of the WhatsApp Bot for Financial Inquiries.
    State Machine:
    0: INIT (Waiting for greeting/start)
    1: Q1_DNI (Select DNI from options)
    2: Q2_ADDRESS (Select Address from options)
    3: Q3_CURRENCY (Select Currency holding)
    4: AUTHENTICATED (Main Menu)
    """
    
    def __init__(self):
        # Mock database keyed by "Phone Number" (Simulated)
        self.mock_db = {
            "default": {
                "name": "Richard Gutierrez",
                "phone": "+51999999999",
                "real_dni": "70559385",
                "real_address": "Av. Javier Prado 123",
                "currency_type": "3", # 1: Soles, 2: Dólares, 3: Ambos
                "balance": 15430.50,
                "last_deposit": "15/01/2026",
                "last_deposit_amount": 2500.00
            }
        }
        
    def generate_options(self, correct_val, type_gen):
        """Generates 3 options with the correct one at a random index."""
        options = []
        if type_gen == 'dni':
            # Generate 2 dummy DNIs
            dummies = [str(random.randint(10000000, 99999999)) for _ in range(2)]
            options = dummies + [correct_val]
        elif type_gen == 'address':
            dummies = ["Calle Los Olivos 456", "Jr. San Martin 789", "Av. Arequipa 101", "Calle Las Begonias 222"]
            # Pick 2 random unique dummies
            selected_dummies = random.sample(dummies, 2)
            options = selected_dummies + [correct_val]
        
        random.shuffle(options)
        
        # Find correct index (1-based for user)
        correct_idx = options.index(correct_val) + 1
        return options, correct_idx
    
    def process_message(self, session_state, user_input):
        """
        Process incoming message based on current state.
        Returns: (response_text, new_state_dict)
        """
        current_step = session_state.get('step', 'INIT')
        user_data = session_state.get('user_data', {})
        
        # Helper for user_data lookup (Simulate "Recognizing Phone Number")
        if not user_data:
            user_data = self.mock_db["default"]
        
        # --- STATE 0: INIT ---
        if current_step == 'INIT':
            # 1. Greet by name
            greeting = f"👋 ¡Hola {user_data['name']}! Bienvenido al canal de Inandes.\n\n"
            
            # Prepare Q1 (DNI)
            options, correct_idx = self.generate_options(user_data['real_dni'], 'dni')
            
            msg = greeting + "Para continuar, por favor selecciona tu **DNI**:\n"
            msg += f"1. {options[0]}\n"
            msg += f"2. {options[1]}\n"
            msg += f"3. {options[2]}\n"
            msg += "\n(Escribe 1, 2 o 3)"
            
            # Store expected answer in session
            new_state = {
                'step': 'Q1_DNI', 
                'user_data': user_data,
                'expected_ans': str(correct_idx)
            }
            return msg, new_state

        # --- STATE 1: Q1_DNI ---
        elif current_step == 'Q1_DNI':
            # RELAXED LOGIC: Accept any valid option (1, 2, 3) for demo
            if user_input.strip() in ['1', '2', '3']:
                # Prepare Q2 (Address)
                options, correct_idx = self.generate_options(user_data['real_address'], 'address')
                
                # Show generic success message since we aren't checking correctness
                msg = "✅ Opción registrada.\n\nAhora, selecciona tu **dirección registrada**:\n"
                msg += f"1. {options[0]}\n"
                msg += f"2. {options[1]}\n"
                msg += f"3. {options[2]}\n"
                
                new_state = {
                    'step': 'Q2_ADDRESS',
                    'user_data': user_data,
                    'expected_ans': str(correct_idx)
                }
                return msg, new_state
            
            else:
                return "❌ Por favor responde 1, 2 o 3.", session_state

        # --- STATE 2: Q2_ADDRESS ---
        elif current_step == 'Q2_ADDRESS':
             # RELAXED LOGIC: Accept any valid option (1, 2, 3) for demo
             if user_input.strip() in ['1', '2', '3']:
                # Prepare Q3 (Currency)
                # Static options: 1. Soles, 2. Dolares, 3. Ambos
                msg = "✅ Opción registrada.\n\nÚltima pregunta: ¿Qué tipo de depósitos tienes en Inandes?\n"
                msg += "1. Soles\n"
                msg += "2. Dólares\n"
                msg += "3. AMBOS"
                
                new_state = {
                    'step': 'Q3_CURRENCY',
                    'user_data': user_data,
                    # We look up what is the correct one in DB. 
                    # For demo purposes, let's assume valid answer is what is in DB
                    'expected_ans': user_data['currency_type']
                }
                return msg, new_state
             else:
                return "❌ Por favor responde 1, 2 o 3.", session_state

        # --- STATE 3: Q3_CURRENCY ---
        elif current_step == 'Q3_CURRENCY':
            # RELAXED LOGIC: Accept any valid option (1, 2, 3) for demo
            if user_input.strip() in ['1', '2', '3']:
                msg = f"🔓 **VERIFICACIÓN EXITOSA (Modo Demo)**\n\n"
                msg += "¿En qué te puedo ayudar hoy?\n"
                msg += "1️⃣ Estado de Cuenta\n"
                msg += "2️⃣ Último Depósito\n"
                msg += "3️⃣ Certificado Retención Renta (2da cat)"
                
                new_state = {
                    'step': 'AUTHENTICATED',
                    'user_data': user_data
                }
                return msg, new_state
            else:
                 return "❌ Por favor responde 1, 2 o 3.", session_state

        # --- STATE 4: AUTHENTICATED (MENU) ---
        elif current_step == 'AUTHENTICATED':
            menu_opt = user_input.strip()
            
            if menu_opt == '1': # Estado de Cuenta
                return (
                    f"📊 **Estado de Cuenta**:\n"
                    f"Saldo Total: S/ {user_data['balance']:,.2f}\n"
                    f"(Información al {datetime.now().strftime('%d/%m/%Y')})\n\n"
                    "Elige otra opción o escribe 'Salir'.",
                    session_state
                )
            
            elif menu_opt == '2': # Ultimo Deposito
                 return (
                    f"📅 **Último Depósito**:\n"
                    f"Fecha: {user_data['last_deposit']}\n"
                    f"Monto: S/ {user_data['last_deposit_amount']:,.2f}\n\n"
                    "Elige otra opción o escribe 'Salir'.",
                    session_state
                )
            
            elif menu_opt == '3': # Certificado
                return (
                    f"📄 **Certificado de Retención**:\n"
                    "He generado tu certificado de Renta de 2da Categoría.\n"
                    "[ARCHIVO ADJUNTO: Certificado_Retencion_2026.pdf]\n\n"
                    "Elige otra opción o escribe 'Salir'.",
                    session_state
                )
            
            elif menu_opt.lower() == 'salir':
                return (
                    "👋 ¡Hasta luego! Gracias por contactar a Inandes.",
                    {'step': 'INIT', 'user_data': {}}
                )
            
            else:
                return (
                    "Por favor elige 1, 2 o 3.",
                    session_state
                )
        
        return "Error de estado. Escribe 'Hola' para reiniciar.", {'step': 'INIT', 'user_data': {}}
