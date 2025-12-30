# Important Notes for Contributors

## Recent Fixes Applied

This project has been tested and the following fixes have been applied to ensure smooth setup:

### 1. **Dependency Versions**
- **PaddlePaddle**: Updated to `3.2.2` (version 2.6.0 no longer available)
- **PaddleOCR**: Updated to `>=2.7.3` for better compatibility
- **Groq SDK**: Updated to `>=0.9.0` (fixes httpx compatibility issues)
- **PyMuPDF**: Added `>=1.23.0` explicitly (has prebuilt Windows wheels)

### 2. **Code Fixes**
- **Import statements**: Changed from `from backend.X` to `from X` (relative imports)
- **PaddleOCR API**: Removed deprecated `show_log` and `cls` parameters
- **Groq models**: Updated to currently supported models:
  - Extractor: `llama-3.1-8b-instant`
  - Reasoning: `llama-3.3-70b-versatile` (was llama-3.1-70b-versatile)

### 3. **Configuration Fixes**
- **Vite proxy**: Uses `127.0.0.1` instead of `localhost` (forces IPv4)
- **.env setup**: Requires real Groq API key for functionality

## Setup Checklist

Before committing or deploying:

- [ ] Copy `.env.example` to `.env`
- [ ] Add your real Groq API key to `.env`
- [ ] Install Poppler (for PDF processing)
- [ ] Run `pip install -r requirements.txt` in backend
- [ ] Run `npm install` in frontend
- [ ] Test all three workflows (Pre-claim, Denial Explanation, Appeal Letter)

## Known Working Configuration

- **Python**: 3.12
- **Node.js**: 16+
- **OS Tested**: Windows 11
- **Groq SDK**: 0.37.1
- **PaddlePaddle**: 3.2.2
- **PaddleOCR**: 2.7.3+

## API Key Setup

⚠️ **CRITICAL**: The dummy API key in `.env.example` will NOT work. You must:

1. Get a free API key from https://console.groq.com
2. Create a `.env` file (copy from `.env.example`)
3. Replace the dummy key with your real key
4. Never commit your `.env` file to GitHub (it's in `.gitignore`)

## Common First-Time Setup Issues

1. **"No module named 'backend'"** → Already fixed with relative imports
2. **PyMuPDF build fails** → Already fixed with PyMuPDF>=1.23.0
3. **Groq proxies error** → Already fixed with groq>=0.9.0
4. **Model decommissioned** → Already fixed with llama-3.3-70b-versatile
5. **Frontend can't connect** → Already fixed with 127.0.0.1 in vite.config.js

All these issues have been resolved in the current codebase!

## Performance Notes

- First run downloads ~130MB of PaddleOCR models (cached afterward)
- OCR processing: ~2-5 seconds per page
- LLM analysis: ~10-30 seconds (depends on document complexity)
- Appeal letter generation: ~15-45 seconds

## Contributing

When contributing, please:

1. Test your changes locally before committing
2. Update SETUP.md if you discover new issues/fixes
3. Keep the `.env` file out of version control
4. Document any new dependencies in requirements.txt or package.json

Happy Hacking! 🚀
