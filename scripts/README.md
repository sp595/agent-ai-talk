# Scripts VAPI

Script Python per gestire l'assistente vocale su VAPI.

## 📋 Script Disponibili

### `update_assistant.py` - Aggiorna Assistente
Aggiorna system prompt e configurazioni.

```bash
# Aggiorna tutto
python scripts/update_assistant.py

# Solo prompt
python scripts/update_assistant.py --type prompt
```

### `get_assistant_info.py` - Info Assistente
Mostra config e salva backup.

```bash
# Info formattate
python scripts/get_assistant_info.py

# Salva backup
python scripts/get_assistant_info.py --save
```

### `upload_knowledge_base.py` - Carica KB
Carica file Markdown su VAPI.

```bash
python scripts/upload_knowledge_base.py
```

### `link_knowledge_base.py` - Collega KB
Collega KB all'assistente.

```bash
python scripts/link_knowledge_base.py
```

### `upload_tool.py` - Gestisci Tool
Crea o aggiorna tool Mailtrap.

```bash
# Auto-detect (crea o aggiorna)
python scripts/upload_tool.py

# Aggiorna specifico
python scripts/upload_tool.py --update TOOL_ID
```

## 🔄 Workflow Tipici

### Setup Iniziale
```bash
python scripts/upload_knowledge_base.py
python scripts/link_knowledge_base.py
python scripts/upload_tool.py
python scripts/update_assistant.py
```

### Aggiorna Prompt
```bash
# 1. Modifica config/vapi-system-prompt.txt
# 2. Aggiorna
python scripts/update_assistant.py --type prompt
```

### Aggiorna KB
```bash
# 1. Modifica file in knowledge-base/
# 2. Ricarica
python scripts/upload_knowledge_base.py
python scripts/link_knowledge_base.py
```

## ⚙️ Configurazione

### File `.env`
```bash
VAPI_API_KEY=your_key
```

### File Usati
- `config/vapi-system-prompt.txt` - System prompt
- `config/vapi-tools-config.json` - Tool email
- `.assistant-id` - ID assistente
- `.knowledge-base-ids.txt` - IDs KB files
- `.tool-ids.txt` - IDs tools

## 🆘 Troubleshooting

**"File .assistant-id non trovato"**
```bash
echo "YOUR_ASSISTANT_ID" > .assistant-id
```

**"VAPI_API_KEY non trovata"**
```bash
echo "VAPI_API_KEY=your_key" > .env
```

**Errore 404/400**
→ Verifica ID in `.assistant-id` e key in `.env`
