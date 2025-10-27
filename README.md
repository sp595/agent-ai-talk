# Assistente Virtuale Comune di Codroipo

Assistente vocale AI per gestire prenotazioni e fornire informazioni sui servizi comunali.

## 🚀 Quick Start

```bash
# 1. Setup ambiente
python3 -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate su Windows
pip install -r requirements.txt

# 2. Configura variabili
echo "VAPI_API_KEY=tua_key" > .env
echo "MAILTRAP_API_TOKEN=tua_key" >> .env

# 3. Setup knowledge base
python scraper/setup_full_pipeline.py

# 4. Aggiorna system prompt
python scripts/update_assistant.py
```

## 📁 Struttura Progetto

```
├── config/                          # Configurazioni
│   ├── vapi-system-prompt.txt      # System prompt assistente
│   └── vapi-tools-config.json      # Tool email Mailtrap
├── knowledge-base/                  # File servizi comunali
├── scripts/                         # Script gestione VAPI
└── scraper/                         # Scraper sito comunale
```

## 🔑 Features

- ✅ Prenotazione appuntamenti (Google Calendar)
- ✅ Informazioni servizi da knowledge base
- ✅ Conferma email automatica (Mailtrap)
- ✅ Pronuncia italiana corretta
- ✅ Scraping automatico servizi comunali

## 📚 Comandi Principali

### Knowledge Base
```bash
# Setup completo automatico
python scraper/setup_full_pipeline.py

# Aggiorna solo KB
python scripts/upload_knowledge_base.py
python scripts/link_knowledge_base.py
```

### System Prompt
```bash
# Aggiorna prompt
python scripts/update_assistant.py

# Verifica config
python scripts/get_assistant_info.py
```

### Tool Email
```bash
# Aggiorna tool Mailtrap
python scripts/upload_tool.py --update TOOL_ID

# Test API
python tools/test_mailtrap.py
```

## ⚙️ Configurazione

### File `.env`
```bash
VAPI_API_KEY=your_key          # Da https://dashboard.vapi.ai/settings
MAILTRAP_API_TOKEN=your_key    # Da https://mailtrap.io/api-tokens
```

### VAPI Dashboard

1. **Credenziale Mailtrap**: Dashboard → Credentials → New → API Key
2. **Tool Email**: Collega credenziale al tool `send_appointment_confirmation_email`
3. **System Prompt**: Aggiorna dalla dashboard o via script

## 📖 Documentazione

- `scripts/README.md` - Script Python disponibili
- `scraper/README.md` - Scraping e knowledge base
- `tools/MAILTRAP-SETUP.md` - Setup email Mailtrap

## 🧪 Test

```bash
# Test email
python tools/test_mailtrap.py

# Test chiamata
# Vai su dashboard.vapi.ai e fai una chiamata di test
```

## 🆘 Troubleshooting

**"VAPI_API_KEY non trovata"**
→ Crea file `.env` con key da dashboard VAPI

**"Assistente non consulta KB"**
→ Verifica files caricati su dashboard → Knowledge Base

**"Email in inglese"**
→ Dashboard → Assistant → Voice → Lingua: it-IT

**"Pronuncia inglese (2025 = two thousand)"**
→ Aggiorna system prompt con regole pronuncia

## 🔗 Links

- [VAPI Dashboard](https://dashboard.vapi.ai)
- [Mailtrap](https://mailtrap.io)
- [Comune Codroipo](https://www.comune.codroipo.ud.it)

## 📝 License

MIT
