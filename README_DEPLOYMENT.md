# Nunno AI - Finance Assistant Deployment Guide

## 🚀 Quick Deploy to Replit

This Streamlit application is ready for immediate deployment on Replit's hosting platform.

### Prerequisites
- Replit account
- OpenRouter AI API key (for AI chat functionality)
- NewsAPI key (optional - for market news)

### Deployment Steps

1. **Fork/Import this Replit**
   - Click "Fork" or import this project to your Replit account

2. **Set Environment Variables**
   - Go to the "Secrets" tab in your Replit
   - Add the following secrets:
     - `AI_API_KEY`: Your OpenRouter API key
     - `NEWS_API_KEY`: Your NewsAPI key (optional)

3. **Deploy**
   - Click the "Deploy" button in the workspace header
   - Select "Autoscale Deployment"
   - Configure your deployment name and domain
   - Set run command: `streamlit run app.py --server.port 5000`

### Features
- 🤖 AI-powered financial education chat
- 📊 Advanced technical analysis with interactive charts
- 💰 Cryptocurrency tokenomics evaluation
- 📰 Real-time market news aggregation
- 🌙 Dark/Light mode toggle
- 📱 Full mobile responsiveness

### API Keys Setup
The application will prompt users to enter their API keys on first launch for secure session-based storage.

### Technical Stack
- **Frontend**: Streamlit with custom CSS theming
- **Charts**: Plotly for interactive financial visualizations
- **APIs**: Binance/CoinGecko for market data, OpenRouter for AI
- **Analysis**: Technical Analysis library for trading indicators

### File Structure
```
├── app.py                 # Main application entry point
├── pages/                 # Multi-page application structure
│   ├── 1_🔮_AI_Chat.py   # AI chat interface
│   ├── 2_📊_Trading_Analysis.py # Technical analysis
│   ├── 3_💰_Tokenomics.py # Token analysis
│   ├── 4_📰_Market_News.py # News aggregation
│   └── 5_⚙️_Settings.py  # User settings
├── betterpredictormodule.py # Technical analysis engine
├── .streamlit/config.toml # Streamlit configuration
└── requirements.txt       # Dependencies
```

### Security Features
- Environment variable-based API key storage
- Session-based user authentication
- Input validation and error handling
- No hardcoded credentials

### Performance Optimizations
- Cached API responses
- Fallback data sources (Binance → CoinGecko)
- Optimized chart rendering
- Mobile-first responsive design

---
Built by Mujtaba Kazmi | Nunno AI - Numinous Nexus AI