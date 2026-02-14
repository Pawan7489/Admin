from terminal_backend import app

# Vercel aur baaki serverless platforms is 'app' variable ko dhoondte hain
# Humne terminal_backend se 'app' ko import karke yahan expose kar diya.
if __name__ == "__main__":
    app.run()
  
