# Web Scraper Comune Codroipo

Scraper automatico per estrarre servizi dal sito comunale e generare knowledge base.

## 🚀 Quick Start

```bash
# 1. Installa dipendenze
pip install -r requirements.txt
playwright install chromium

# 2. Setup automatico (tutto in un comando)
python scraper/setup_full_pipeline.py
```

Questo script:
1. ✅ Scraping servizi dal sito
2. ✅ Generazione file Markdown
3. ✅ Upload su VAPI
4. ✅ Collegamento all'assistente

## 📋 Script Disponibili

### `setup_full_pipeline.py` ⭐ - Setup Completo
Pipeline automatica completa.

```bash
python scraper/setup_full_pipeline.py
```

### `scrape_real.py` - Scraper
Estrae servizi dal sito reale.

```bash
python scraper/scrape_real.py
```
Output: `services_data_real.json`

### `generate_knowledge_base.py` - Generatore KB
Converte JSON in file Markdown.

```bash
python scraper/generate_knowledge_base.py
```
Output: `knowledge-base/*.md`

### `validate_data.py` - Validatore
Valida qualità dati estratti.

```bash
python scraper/validate_data.py
```

## 🔄 Workflow Manuale

```bash
# 1. Scraping
python scraper/scrape_real.py

# 2. Genera KB
python scraper/generate_knowledge_base.py

# 3. Upload
python scripts/upload_knowledge_base.py

# 4. Collega
python scripts/link_knowledge_base.py
```

## 📁 File Generati

```
scraper/
└── services_data_real.json      # Dati estratti

knowledge-base/
├── carta-identita.md
├── certificato-residenza.md
└── ...                          # Un file per servizio
```

## ⚙️ Configurazione

### Prerequisiti
```bash
# Dipendenze Python
pip install playwright beautifulsoup4 requests python-dotenv

# Browser Chromium
playwright install chromium

# File .env
echo "VAPI_API_KEY=your_key" > .env

# Assistant ID
echo "YOUR_ASSISTANT_ID" > .assistant-id
```

### Personalizzazione

**Modificare selettori scraping**
→ Edita `scraper/scrape_real.py` riga ~50

**Modificare template KB**
→ Edita `scraper/generate_knowledge_base.py` riga ~30

## 🆘 Troubleshooting

**"Playwright non installato"**
```bash
pip install playwright
playwright install chromium
```

**"Timeout durante scraping"**
→ Aumenta timeout in `scrape_real.py` (riga ~80)

**"Nessun servizio estratto"**
→ Selettori CSS potrebbero essere cambiati
→ Verifica struttura HTML del sito

**Scraping troppo lento**
→ Quando chiesto, rispondi 'N' a "estrarre dettagli"

## 🎯 Best Practices

1. Backup `services_data_real.json` prima di riscrapare
2. Esegui `validate_data.py` dopo scraping
3. Testa con pochi servizi prima di full scraping
4. Ri-esegui periodicamente per dati aggiornati
