# File Path: backend/intent_parser.py
# Description: Translates Natural Language / Hinglish to System Actions
# Rule Applied: "Understand Intent over Syntax"

import re

class IntentEngine:
    def __init__(self, active_modules):
        """
        Ye engine initialize hote hi saare active modules (Web, Dev, Storage) 
        ka access le leta hai, taaki unhe commands bhej sake.
        """
        self.modules = active_modules

    def process_intent(self, user_input):
        """
        Terminal input ko parse karke correct backend function trigger karta hai.
        """
        command = user_input.lower().strip()
        response = ""

        print(f"🧠 [Intent Engine]: Analyzing Command -> '{command}'")

        # ==========================================
        # 1. WEB & WORDPRESS INTENTS (Connects to File 06)
        # ==========================================
        # Example command: "ek wordpress website banao" ya "install wp"
        if any(word in command for word in ["wordpress", "wp", "website", "site"]):
            if any(word in command for word in ["install", "banao", "create", "dalo", "setup"]):
                
                # Basic Entity Extraction (Finding domain name if mentioned)
                domain = "new-ai-site.com" # Default fallback
                if "domain" in command:
                    parts = command.split("domain")
                    if len(parts) > 1:
                        # Extracting the word right after 'domain'
                        extracted = parts[1].strip().split()[0]
                        # Clean up punctuation
                        domain = re.sub(r'[^\w\.\-]', '', extracted)
                        
                if 'web' in self.modules and self.modules['web']:
                    response = self.modules['web'].install_wordpress(domain, f"db_{domain.split('.')[0]}")
                    return f"🤖 Intent Understood: WordPress Installation.\n{response}"
                else:
                    return "❌ Error: Web Injector (File 06) is offline."

            # Example: "website mein ai inject karo" ya "ai jodo"
            if any(word in command for word in ["inject", "jodo", "connect ai", "daal do"]):
                if 'web' in self.modules and self.modules['web']:
                    response = self.modules['web'].inject_ai_into_website("new-ai-site.com")
                    return f"🤖 Intent Understood: AI Injection.\n{response}"

        # ==========================================
        # 2. DEV CONTROLS & LOGIC BUILDER INTENTS (Connects to File 07)
        # ==========================================
        # Example: "python script chalao" ya "run python"
        if "python" in command and any(word in command for word in ["run", "chalao", "execute"]):
            if 'dev' in self.modules and self.modules['dev']:
                # Abhi test code bhej rahe hain, UI editor se live code aayega
                test_code = "print('Hello Master, Python Sandbox is Active!')\nprint('Calculation: 5 * 5 =', 5*5)"
                response = self.modules['dev'].execute_python(test_code)
                return f"🤖 Intent Understood: Python Execution.\n{response}"
            else:
                return "❌ Error: Dev Sandbox (File 07) is offline."

        # Example: "logic link karo" ya "nodes jodo"
        if "logic" in command or "node" in command:
            if any(word in command for word in ["link", "jodo", "connect"]):
                if 'dev' in self.modules and self.modules['dev']:
                    response = self.modules['dev'].connect_nodes("UI_Terminal", "Intent_Parser", "send_data")
                    return f"🤖 Intent Understood: Logic Builder Link.\n{response}"

        # ==========================================
        # 3. DIRECTORY / SYSTEM INTENTS (Hinglish Translation)
        # ==========================================
        # Example: "ek naya folder banao test_folder"
        if "folder banao" in command or "make folder" in command:
            folder_name = "new_folder"
            words = command.split()
            if len(words) > 2:
                folder_name = words[-1] # Usually the last word is the name
            import os
            try:
                os.makedirs(folder_name, exist_ok=True)
                return f"🤖 Intent Understood: Directory Creation.\n✅ Success: Folder '{folder_name}' bana diya gaya hai."
            except Exception as e:
                return f"❌ Error creating folder: {str(e)}"

        # ==========================================
        # UNKNOWN INTENT FALLBACK
        # ==========================================
        # Agar engine Hinglish/English intent nahi samajh paya, toh ye server ko signal dega 
        # ki isko normal bash/cmd ki tarah chalane ki koshish kare.
        return "UNKNOWN_INTENT"

# Test Code (Ignored during actual run)
if __name__ == "__main__":
    dummy_modules = {}
    engine = IntentEngine(dummy_modules)
    print(engine.process_intent("ek wordpress website banao domain a1-master.com"))
    print(engine.process_intent("ek naya folder banao secret_data"))
              
