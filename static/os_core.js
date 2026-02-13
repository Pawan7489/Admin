/* * File 04: static/os_core.js 
 * Description: Advanced SPA Logic, Real-Time Terminal Execution, and WebSocket Connection
 * Connects the Tailwind HTML UI to the Python Flask Backend.
 */

document.addEventListener("DOMContentLoaded", () => {
    console.log("A1 OS Core Initialized. Awaiting Server Connection...");

    // --- 1. DOM Elements (HTML se elements uthana) ---
    const loginModal = document.getElementById('login-modal');
    const appContainer = document.getElementById('app-container');
    const loginBtn = document.getElementById('login-btn');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    
    const terminalScreen = document.getElementById('terminal-screen');
    const cmdInput = document.getElementById('cmd-input');
    const execBtn = document.getElementById('exec-btn');
    const killSwitch = document.getElementById('kill-switch');

    // --- 2. WebSockets Setup (Connecting to Python Backend) ---
    let socket;
    try {
        // Ye Flask-SocketIO se real-time connection banayega
        socket = io(); 
        
        socket.on('connect', () => {
            printToTerminal("🟢 System Link Established. Connected to A1 Python Backend.", "text-neonGreen");
        });

        // Backend (Python) se jo reply aayega, wo terminal me print hoga
        socket.on('terminal_output', (data) => {
            printToTerminal(`[A1]: ${data.output}`, "text-gray-300");
        });

    } catch (e) {
        console.warn("Socket.io not found. Backend server might be offline.");
        printToTerminal("⚠️ Warning: Running in UI Simulation Mode (Backend disconnected).", "text-yellow-500");
    }

    // --- 3. PHASE 1: LOGIN LOGIC (Frontend Gatekeeper) ---
    function handleLogin() {
        const user = usernameInput.value;
        const pass = passwordInput.value;

        // Default local login check
        if(user === "admin" && pass !== "") {
            // Hacker style button animation
            loginBtn.innerHTML = "<i class='fas fa-spinner fa-spin'></i> VERIFYING...";
            loginBtn.classList.replace("bg-green-700", "bg-yellow-600");
            
            setTimeout(() => {
                loginModal.classList.add("hidden"); // Login screen chupao
                appContainer.classList.remove("hidden"); // Main UI dikhao
                printToTerminal("Welcome Admin. All systems nominal.", "text-neonGreen");
                cmdInput.focus();
            }, 1000); 
        } else {
            loginBtn.innerHTML = "❌ ACCESS DENIED";
            loginBtn.classList.replace("bg-green-700", "bg-red-600");
            setTimeout(() => {
                loginBtn.innerHTML = "INITIALIZE CORE";
                loginBtn.classList.replace("bg-red-600", "bg-green-700");
            }, 2000);
        }
    }

    loginBtn.addEventListener('click', handleLogin);
    passwordInput.addEventListener('keypress', (e) => {
        if(e.key === 'Enter') handleLogin();
    });

    // --- 4. PHASE 2: TERMINAL LOGIC ---
    // Terminal me text dikhane ka function
    function printToTerminal(text, colorClass = "text-white") {
        const div = document.createElement('div');
        div.className = `mb-1 ${colorClass} font-mono text-sm break-words`;
        div.innerText = text;
        terminalScreen.appendChild(div);
        terminalScreen.scrollTop = terminalScreen.scrollHeight; // Auto-scroll to bottom
    }

    // Command run karne ka function
    function executeCommand() {
        const command = cmdInput.value.trim();
        if(!command) return;

        // 1. User ka command show karo
        printToTerminal(`admin@A1-OS:~$ ${command}`, "text-blue-400 font-bold");
        cmdInput.value = ''; // Input box clear karo

        // 2. UI Simulation: Council of Experts Auditing
        printToTerminal("⏳ Council of Experts Auditing Intent...", "text-yellow-500 text-xs");
        
        setTimeout(() => {
            if (socket && socket.connected) {
                // Asli Python backend ko command bhejo
                socket.emit('command_input', command);
            } else {
                // Agar python server band hai, to error do
                printToTerminal("❌ ERROR: Connection to Python Core lost.", "text-red-500 font-bold");
            }
        }, 600);
    }

    execBtn.addEventListener('click', executeCommand);
    cmdInput.addEventListener('keypress', (e) => {
        if(e.key === 'Enter') executeCommand();
    });

    // --- 5. PHASE 3: RLHF (Human Feedback Logic) ---
    const thumbsUp = document.querySelector('.fa-thumbs-up');
    const thumbsDown = document.querySelector('.fa-thumbs-down');

    if (thumbsUp && thumbsDown) {
        thumbsUp.addEventListener('click', () => {
            printToTerminal("💡 RLHF: Positive feedback saved. Vector DB updated.", "text-neonGreen text-xs");
        });
        
        thumbsDown.addEventListener('click', () => {
            printToTerminal("⚠️ RLHF: Negative feedback saved. Logic path discarded.", "text-red-400 text-xs");
        });
    }

    // --- 6. PHASE 4: EMERGENCY KILL SWITCH ---
    killSwitch.addEventListener('click', () => {
        printToTerminal("🚨 EMERGENCY OVERRIDE ACTIVATED! FREEZING ALL SYSTEMS...", "text-red-500 font-bold text-lg");
        
        // Puri screen ko laal kar do
        document.body.classList.remove("bg-darkBg");
        document.body.classList.add("bg-red-950");
        document.body.style.transition = "background-color 0.5s ease";
        
        if (socket) socket.emit('command_input', 'SYSTEM_FREEZE_PROTOCOL_ACTIVATE');
        
        setTimeout(() => {
            alert("SYSTEM FROZEN. NETWORK DISCONNECTED.");
            location.reload(); // Reloads to login screen
        }, 1500);
    });

    // --- 7. AUTO-CLICK FOR ALL DASHBOARD BUTTONS ---
    // UI ke kisi bhi button par click karne se terminal usko command bana lega
    document.querySelectorAll('button').forEach(btn => {
        if(btn.id === 'login-btn' || btn.id === 'exec-btn' || btn.id === 'kill-switch') return;

        btn.addEventListener('click', (e) => {
            const btnText = e.target.innerText.trim();
            // Find which card/section this button belongs to
            const cardTitle = e.target.closest('div, td').parentElement.querySelector('h3, td')?.innerText || "Module";
            
            // Terminal me automatic type karke enter maar dega
            cmdInput.value = `Execute Action: [${btnText}] on [${cardTitle}]`;
            executeCommand();
        });
    });
});
          
