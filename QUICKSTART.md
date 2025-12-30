# Quick Start Guide

## For New Contributors

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Hackios
   ```

2. **Get a Groq API Key** (Required!)
   - Go to https://console.groq.com
   - Sign up (free)
   - Create an API key
   - Save it for step 4

3. **Setup Backend**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cd ..
   copy .env.example .env  # Windows
   # OR
   cp .env.example .env    # Mac/Linux
   ```
   
   **Edit `.env` and add your Groq API key!**

5. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   ```

6. **Run the Application**
   
   Terminal 1 (Backend):
   ```bash
   cd backend
   python -m uvicorn main:app --reload
   ```
   
   Terminal 2 (Frontend):
   ```bash
   cd frontend
   npm run dev
   ```

7. **Access the App**
   - Open http://localhost:5173
   - Upload medical documents
   - Test the three workflows!

## Need Help?

- See [SETUP.md](SETUP.md) for detailed instructions
- See [CONTRIBUTING.md](CONTRIBUTING.md) for known issues and fixes
- Check [README.md](README.md) for architecture details

**⚠️ Don't forget to add your Groq API key in `.env`!**
