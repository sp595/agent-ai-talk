# Assistente Virtuale Comune di Codroipo

Assistente vocale AI per il Comune di Codroipo (UD) che gestisce prenotazioni appuntamenti e fornisce informazioni sui servizi comunali.

## 🚀 Quick Start

```bash
# 1. Setup ambiente
python3 -m venv .venv
source .venv/bin/activate  # su Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. Configura .env
echo "VAPI_API_KEY=your_key" > .env
echo "MAILTRAP_API_TOKEN=your_key" >> .env

# 3. Crea assistente
python scripts/create_assistant.py

# 4. Carica knowledge base (auto-link)
python scripts/upload_knowledge_base.py

# 5. Crea tools (auto-crea credential + auto-link)
python scripts/create_tool.py
```

## 📁 Struttura

```
├── config/
│   ├── assistant-existing.json           # Template assistente (pulito)
│   ├── vapi-system-prompt-with-tools.txt # System prompt
│   ├── vapi-tools-config.json            # Tool email
│   ├── vapi-check_calendar-tools-config.json
│   └── vapi-send_calendar-tools-config.json
├── knowledge-base/                       # Servizi comunali (Markdown)
└── scripts/                              # Script gestione VAPI
```

## ✨ Funzionalità

- 🗓️ Prenotazione appuntamenti su Google Calendar
- 📚 Consulta knowledge base per info servizi
- 📧 Email conferma automatica (Mailtrap)
- 🇮🇹 Pronuncia italiana corretta (date, email, numeri)
- 🔧 Gestione template-based per configurazione

## 📚 Comandi Principali

### Gestione Assistente
```bash
# Crea nuovo assistente (usa template)
python scripts/create_assistant.py

# Aggiorna assistente (auto-linka KB e tools)
python scripts/update_assistant.py

# Info assistente
python scripts/get_assistant_info.py
```

### Knowledge Base
```bash
# Carica file KB su VAPI (auto-link se esiste .assistant-id)
python scripts/upload_knowledge_base.py
```

### Tools
```bash
# Crea tutti i tools (auto-crea credential + auto-link)
python scripts/create_tool.py
```

## ⚙️ Configurazione

### Variabili ambiente (.env)
```bash
VAPI_API_KEY=your_key          # https://dashboard.vapi.ai/settings
MAILTRAP_API_TOKEN=your_key    # https://mailtrap.io/api-tokens
```

### Template Assistente
Il file `config/assistant-existing.json` è il template master:
- Modifica qui voice, transcriber, settings
- Usa `update_assistant.py` per applicare modifiche
- KB e tools vengono linkati automaticamente

## 📖 Documentazione

Vedi `scripts/README.md` per dettagli su tutti gli script disponibili.

## 🔗 Workflow Template-Based

1. **Template**: Modifica `config/assistant-existing.json`
2. **Apply**: Lancia `update_assistant.py`
3. **Auto-link**: KB e tools linkati automaticamente se presenti `.knowledge-base-ids` e `.tool-ids`

## 🔗 Links

- [VAPI Dashboard](https://dashboard.vapi.ai) - Gestione assistente
- [Mailtrap](https://mailtrap.io) - Email testing
- [Comune di Codroipo](https://www.comune.codroipo.ud.it)
