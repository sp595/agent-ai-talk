# Frontend React - Demo Assistente Vocale

Applicazione React per demo dell'assistente vocale Comune di Codroipo.

## 🎯 Caratteristiche

- ✅ Interfaccia moderna e responsive
- ✅ Integrazione completa Vapi Web SDK
- ✅ Visualizzazione real-time trascrizione
- ✅ Controlli chiamata intuitivi
- ✅ Indicatori di stato animati
- ✅ Pronto per il deployment

---

## 🚀 Setup Rapido

```bash
# 1. Vai nella directory frontend
cd frontend

# 2. Installa dipendenze
npm install

# 3. Configura variabili ambiente
cp .env .env.local
# Poi edita .env e aggiungi la tua VAPI_PUBLIC_KEY

# 4. Avvia development server
npm run dev

# Apri http://localhost:5173
```

---

## 🔑 Configurazione Vapi

### Ottenere la Public Key

1. Vai su https://dashboard.vapi.ai
2. Settings → API Keys
3. Copia la **Public Key** (inizia con `pk_...`)
4. Inseriscila in `.env`:

```bash
VITE_VAPI_PUBLIC_KEY=pk_your_key_here
VITE_ASSISTANT_ID=f25b74d7-dea8-4eb1-8e58-6225643b36b2
```

**IMPORTANTE**: Usa SOLO la Public Key nel frontend, mai la Private Key!

---

## 📁 Struttura

```
frontend/
├── src/
│   ├── App.jsx           # Componente principale + logica Vapi
│   ├── App.css           # Stili applicazione
│   ├── index.css         # Stili globali
│   └── main.jsx          # Entry point
├── .env                  # Config (da personalizzare)
├── index.html            # HTML template
├── package.json          # Dipendenze
└── README.md             # Documentazione dettagliata
```

---

## 🎨 Componenti

### App.jsx

Componente principale che gestisce:
- Inizializzazione Vapi SDK
- Gestione stato chiamata (idle/connecting/active)
- Event listeners Vapi
- UI e controlli

**Eventi gestiti:**
```javascript
call-start     → Chiamata iniziata
call-end       → Chiamata terminata
speech-start   → Utente parla
speech-end     → Utente smette di parlare
message        → Trascrizione e messaggi
error          → Errori
```

---

## 🎨 Stili e Personalizzazione

### Temi Colori

Modifica variabili CSS in `App.css`:

```css
:root {
  --primary: #2563eb;      /* Blu primario */
  --danger: #dc2626;       /* Rosso termina */
  --success: #16a34a;      /* Verde attivo */
  --gray-*: ...            /* Scale grigi */
}
```

### Layout Responsive

Breakpoint mobile: `640px`

```css
@media (max-width: 640px) {
  /* Adattamenti mobile */
}
```

---

## 🚀 Deployment

### Vercel (Consigliato)

```bash
npm i -g vercel
cd frontend
vercel
```

Configura variabili ambiente su dashboard Vercel.

### Netlify

```bash
npm i -g netlify-cli
cd frontend
npm run build
netlify deploy --prod --dir=dist
```

### Build Manuale

```bash
npm run build
# Files in dist/ pronti per deployment
```

Server statico:
```bash
python3 -m http.server -d dist 8000
# Oppure
npx serve dist
```

---

## 🧪 Testing

### Test Locale

1. Configura `.env` con Public Key
2. `npm run dev`
3. Apri http://localhost:5173
4. Clicca "Inizia Chiamata"
5. Autorizza microfono
6. Parla con l'assistente

### Troubleshooting

**"Configura VITE_VAPI_PUBLIC_KEY"**
→ Aggiungi Public Key in `.env` e riavvia server

**Chiamata non si avvia**
→ Verifica assistente attivo su Vapi Dashboard
→ Controlla console browser per errori
→ Verifica permessi microfono

**Nessun audio**
→ Controlla permessi microfono browser
→ Verifica volume sistema
→ Prova con cuffie

---

## 📱 Browser Supportati

| Browser | Supporto | Note |
|---------|----------|------|
| Chrome/Edge | ✅ | Consigliato |
| Firefox | ✅ | Ottimo |
| Safari | ✅ | 14+ |
| Mobile | ⚠️ | Limitazioni possibili |

---

## 🔐 Sicurezza

✅ Usa SEMPRE Public Key
✅ `.env` in `.gitignore`
✅ HTTPS obbligatorio in production
✅ Configura CORS su Vapi se necessario

---

## 📚 Documentazione Completa

Vedi `frontend/README.md` per:
- Guide deployment dettagliate
- Personalizzazione avanzata
- Metriche e analytics
- Troubleshooting esteso

---

## 🛠️ Stack Tecnologico

- **React 18** - UI Framework
- **Vite** - Build tool ultravel oce
- **@vapi-ai/web** - SDK Vapi ufficiale
- **CSS3** - Styling moderno
- **Google Fonts (Inter)** - Typography

---

## 🎯 Prossimi Step

1. ✅ Setup completato
2. ✅ App funzionante in locale
3. 🔄 Deploy su Vercel/Netlify
4. 🔄 Personalizza colori/brand
5. 🔄 Aggiungi analytics (opzionale)

---

## 📞 Link Utili

- [Vapi Dashboard](https://dashboard.vapi.ai)
- [Vapi Docs](https://docs.vapi.ai)
- [Vapi Web SDK](https://docs.vapi.ai/sdk/web)
- [React Docs](https://react.dev)
- [Vite Docs](https://vitejs.dev)

---

**Progetto**: Test Tecnico Fullstack Developer AI & Automation
**Cliente**: Comune di Codroipo
**Data**: Ottobre 2025
