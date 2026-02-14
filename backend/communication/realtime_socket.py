# File: backend/communication/realtime_socket.py
# Purpose: Instant, bidirectional communication (Chat & Commands).
# Strategy: "Musk Rule" - Zero lag, minimum CPU usage.

from flask_socketio import SocketIO, emit

# SocketIO initialize karna (Flask ke saath)
socketio = SocketIO(cors_allowed_origins="*")

@socketio.on('user_message')
def handle_message(data):
    """
    Jab user Indore se msg bhejega, ye Bhopal server par turant trigger hoga.
    """
    user_input = data.get('msg')
    print(f"📡 [Socket]: New command received: {user_input}")

    # Step 1: Brain (Groq/Gemini) ko msg bhejo
    # Step 2: Response milte hi 'emit' kar do
    
    emit('ai_response', {
        'data': f"A1 OS processing: {user_input}...",
        'status': 'thinking'
    })

    # Final result bhejna
    emit('ai_response', {
        'data': "Bhai, naya folder 'Bansal_Project' bana diya gaya hai.",
        'status': 'complete'
    })

# --- Deployment Note ---
# Bhopal server (Oracle Cloud) par ise 'gunicorn' ke saath 
# '--worker-class eventlet' use karke run karenge.
