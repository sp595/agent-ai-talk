# Scripts VAPI

Script Python per gestire l'assistente vocale su VAPI.

## 📋 Script Disponibili

### `create_assistant.py` - Crea Nuovo Assistente
Crea un nuovo assistente da zero con configurazione completa.
**Usare solo per setup iniziale** o per creare nuovi assistenti.

```bash
# Crea assistente con configurazione di default
python scripts/create_assistant.py

# Crea con nome personalizzato
python scripts/create_assistant.py --name "Il Mio Assistente"

# Crea con voce OpenAI invece di ElevenLabs
python scripts/create_assistant.py --voice openai

# Forza creazione senza conferma
python scripts/create_assistant.py --force
```

**ATTENZIONE**: Se hai già un assistente configurato, usa `update_assistant.py` invece!

### `update_assistant.py` - Aggiorna Assistente
Aggiorna system prompt e configurazioni di un assistente esistente.

```bash
# Aggiorna tutto
python scripts/update_assistant.py

# Solo prompt
python scripts/update_assistant.py --type prompt

# Solo voice
python scripts/update_assistant.py --type voice

# Solo settings
python scripts/update_assistant.py --type settings
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

### Setup Completo da Zero
```bash
# 1. Crea assistente
python scripts/create_assistant.py

# 2. Carica e collega knowledge base
python scripts/upload_knowledge_base.py
python scripts/link_knowledge_base.py

# 3. Crea e collega email tool
python scripts/create_tool.py
# 3.1 oppure fai upload di un tool
python scripts/upload_tool.py
python scripts/link_tool_to_assistant.py

# 4. Verifica configurazione
python scripts/get_assistant_info.py --save
```

### Setup se Assistente Già Esiste
```bash
python scripts/upload_knowledge_base.py
python scripts/link_knowledge_base.py
python scripts/create_tool.py --url YOUR_SERVER_URL
python scripts/link_tool_to_assistant.py
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
# Opzione 1: Crea nuovo assistente
python scripts/create_assistant.py

# Opzione 2: Se hai già un assistente, crea il file manualmente
echo "YOUR_ASSISTANT_ID" > .assistant-id
```

**"VAPI_API_KEY non trovata"**
```bash
echo "VAPI_API_KEY=your_key" > .env
```

**Errore 404/400**
→ Verifica ID in `.assistant-id` e key in `.env`
