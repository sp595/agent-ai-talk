# Scripts VAPI

Script Python per gestire l'assistente vocale su VAPI.

## 🚀 Workflow Completamente Automatico

Il workflow è completamente automatizzato:

1. **`create_assistant.py`** - Crea l'assistente base (da template)
2. **`upload_knowledge_base.py`** - Carica KB + auto-link all'assistente
3. **`create_tool.py`** - Crea TUTTI i tool (auto-crea credential + auto-link)
4. **`update_assistant.py`** - Aggiorna prompt/config (opzionale)

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

Aggiorna system prompt e LINKA AUTOMATICAMENTE KB e tools se presenti.

```bash
# Aggiorna prompt + linka KB e tools automaticamente
python scripts/update_assistant.py

# Solo prompt (preserva KB e tools)
python scripts/update_assistant.py --type prompt
```

**Funzionalità automatiche**:

- ✅ Linka KB se esiste `.knowledge-base-ids`
- ✅ Linka tools se esiste `.tool-ids`
- ✅ Preserva tutte le altre configurazioni

### `get_assistant_info.py` - Info Assistente

Mostra config e salva backup.

```bash
# Info formattate
python scripts/get_assistant_info.py

# Salva backup
python scripts/get_assistant_info.py --save
```

### `upload_knowledge_base.py` - Carica KB

Carica file Markdown su VAPI e linka automaticamente all'assistente.

```bash
python scripts/upload_knowledge_base.py
```

**Funzionalità automatiche**:

- ✅ Carica tutti i file `.md` da `knowledge-base/`
- ✅ Salva IDs in `.knowledge-base-ids`
- ✅ Se esiste `.assistant-id`, linka automaticamente KB all'assistente

### `create_tool.py` - Crea TUTTI i Tool

Crea tutti e 3 i tool in una volta con auto-setup credential:

- Email tool (crea e linka credential Mailtrap automaticamente)
- Calendar check tool
- Calendar create tool

```bash
python scripts/create_tool.py
```

**Funzionalità automatiche**:

- ✅ Verifica se esiste credential Mailtrap
- ✅ Se non esiste, la crea automaticamente da `MAILTRAP_API_TOKEN` (.env)
- ✅ Linka credential al tool email
- ✅ Salva IDs in `.tool-ids`
- ✅ Se esiste `.assistant-id`, linka automaticamente tools all'assistente

## 🔄 Workflow Completi

### Setup Completo da Zero

**Workflow Consigliato (Completamente Automatico)**:

```bash
# 1. Crea assistente base
python scripts/create_assistant.py

# 2. Carica knowledge base (auto-link)
python scripts/upload_knowledge_base.py

# 3. Crea TUTTI i tool (auto-crea credential + auto-link)
python scripts/create_tool.py

# 4. Verifica (opzionale)
python scripts/get_assistant_info.py
```

**Vantaggi**:

- ✅ Auto-creazione credential Mailtrap
- ✅ Auto-linking KB (upload_knowledge_base.py)
- ✅ Auto-linking tools (create_tool.py)
- ✅ Workflow ridotto a 3 comandi principali!

### Aggiorna Prompt

```bash
# 1. Modifica config/vapi-system-prompt-with-tools.txt

# 2. Aggiorna (preserva KB e tools)
python scripts/update_assistant.py --type prompt
```

### Aggiorna KB

```bash
# 1. Modifica file in knowledge-base/

# 2. Ricarica
python scripts/upload_knowledge_base.py

# 3. Linka automaticamente
python scripts/update_assistant.py
```

## ⚙️ Configurazione

### File `.env`

```bash
VAPI_API_KEY=your_key
MAILTRAP_API_TOKEN=your_mailtrap_token
```

### File Generati Automaticamente

| File | Generato da | Descrizione |
|------|-------------|-------------|
| `.assistant-id` | `create_assistant.py` | ID assistente |
| `.knowledge-base-ids` | `upload_knowledge_base.py` | IDs file KB |
| `.secret-ids.json` | `create_tool.py` | Mapping credential names → IDs |
| `.tool-ids` | `create_tool.py` | IDs tools |

**IMPORTANTE**: Tutti in `.gitignore` per sicurezza!

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
