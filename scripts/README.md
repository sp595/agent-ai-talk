# Scripts VAPI

Script Python per gestire l'assistente vocale su VAPI.

## 🚀 Workflow Semplificato

Il workflow è stato ottimizzato per essere più lineare e automatico:

1. **`create_assistant.py`** - Crea l'assistente base
2. **`create_secret.py`** - Crea secret
3. **`upload_tool.py`** - Gestisce secrets + crea tool email
4. **`create_tool.py`** - Crea TUTTI i tool (email, calendar) in una volta
5. **`upload_knowledge_base.py`** - Carica file knowledge base
6. **`update_assistant.py`** - Aggiorna assistente e linka automaticamente KB + tools

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

Carica file Markdown su VAPI (genera `.knowledge-base-ids`).

```bash
python scripts/upload_knowledge_base.py
```

### `create_secret.py` - Crea Secret

Crea un secret criptato su Vapi.ai per autenticazione sicura.

```bash
# Crea secret Mailtrap (da .env)
python scripts/create_secret.py

# Crea secret custom
python scripts/create_secret.py --name my_secret --value "abc123"

# Forza creazione senza conferma
python scripts/create_secret.py --force
```

**Usa questo se**:

- Vuoi gestire secrets separatamente dai tool
- Hai bisogno di creare secrets per altri tool (non solo email)

### `upload_tool.py` - Gestisce Secret + Tool Email (All-in-One)

Crea automaticamente il secret Mailtrap (se non esiste) E il tool email con autenticazione Bearer.

```bash
# Auto: crea secret + tool email
python scripts/upload_tool.py

# Forza creazione nuovo tool
python scripts/upload_tool.py --create

# Aggiorna tool esistente
python scripts/upload_tool.py --update TOOL_ID
```

**Usa questo se**:

- Vuoi fare tutto in un comando
- Setup rapido del tool email
- Non hai bisogno di gestire secrets custom

### `create_tool.py` - Crea TUTTI i Tool

Crea tutti e 3 i tool in una volta:

- Email tool (con secret se disponibile)
- Calendar check tool
- Calendar create tool

```bash
python scripts/create_tool.py
```

Conferma e crea automaticamente tutti i tool. Salva IDs in `.tool-ids`.

## 🔄 Workflow Completi

### Setup Completo da Zero

**Opzione A - All-in-One (Consigliato)**:

```bash
# 1. Crea assistente base
python scripts/create_assistant.py

# 2. Carica knowledge base
python scripts/upload_knowledge_base.py

# 3. Crea secret + tool email (tutto insieme)
python scripts/upload_tool.py

# 4. Crea tutti i tool (calendar check & create)
python scripts/create_tool.py

# 5. Aggiorna e linka automaticamente KB + tools
python scripts/update_assistant.py

# 6. Verifica
python scripts/get_assistant_info.py
```

**Opzione B - Modulare**:

```bash
# 1. Crea assistente base
python scripts/create_assistant.py

# 2. Carica knowledge base
python scripts/upload_knowledge_base.py

# 3. Crea secret Mailtrap
python scripts/create_secret.py

# 4. Crea TUTTI i tool (email con secret, calendar)
python scripts/create_tool.py

# 5. Aggiorna e linka automaticamente KB + tools
python scripts/update_assistant.py

# 6. Verifica
python scripts/get_assistant_info.py
```

**Vantaggi**:

- ✅ Nessuno script di "link" manuale
- ✅ KB e tools linkati automaticamente
- ✅ Due approcci disponibili (all-in-one o modulare)

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
| `.secret-ids.json` | `upload_tool.py` | Mapping secret names → IDs |
| `.tool-ids` | `upload_tool.py` + `create_tool.py` | IDs tools |

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
