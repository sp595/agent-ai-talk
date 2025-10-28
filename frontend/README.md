# Frontend - Assistente Vocale Comune di Codroipo

Demo frontend React per testare l'assistente vocale AI su una pagina web personalizzata.

## 🚀 Quick Start

### 1. Installazione Dipendenze

```bash
npm install
```

### 2. Configurazione

Copia il file `.env` e inserisci le tue credenziali Vapi:

```bash
# .env
VITE_VAPI_PUBLIC_KEY=your_public_key_here
VITE_ASSISTANT_ID=f25b74d7-dea8-4eb1-8e58-6225643b36b2
```

**IMPORTANTE**: Usa la **PUBLIC KEY** di Vapi, NON la chiave privata!
La public key è sicura da usare nel frontend perché è limitata solo a operazioni client-side.

### 3. Avvio Development Server

```bash
npm run dev
```

Apri [http://localhost:5173](http://localhost:5173) nel browser.

### 4. Build per Production

```bash
npm run build
```

I file verranno generati in `dist/`.

---

## 📦 Struttura Progetto

```
frontend/
├── public/                 # Asset statici
├── src/
│   ├── App.jsx            # Componente principale con logica Vapi
│   ├── App.css            # Stili applicazione
│   ├── index.css          # Stili globali
│   └── main.jsx           # Entry point React
├── .env                   # Variabili ambiente (da configurare!)
├── index.html             # HTML template
├── package.json           # Dipendenze npm
└── vite.config.js         # Configurazione Vite
```

---

## 🔑 Ottenere la Public Key Vapi

1. Vai su [Vapi Dashboard](https://dashboard.vapi.ai)
2. Naviga: **Settings** → **API Keys**
3. Copia la **Public Key** (inizia con `pk_...`)
4. Incollala in `.env` come `VITE_VAPI_PUBLIC_KEY`

**NON usare** la Private Key (inizia con `sk_...`) nel frontend!

---

## 🎨 Funzionalità

### Interfaccia Utente

- **Status Indicator**: Mostra lo stato della chiamata (idle, connecting, active)
- **Call Controls**: Pulsanti per iniziare/terminare chiamata
- **Transcript Display**: Visualizza la conversazione in tempo reale
- **Info Section**: Suggerimenti su cosa chiedere
- **Tech Info Card**: Dettagli tecnici dell'assistente

### Eventi Vapi

Il componente gestisce i seguenti eventi Vapi:

```javascript
vapi.on('call-start', () => { ... })      // Chiamata iniziata
vapi.on('call-end', () => { ... })        // Chiamata terminata
vapi.on('speech-start', () => { ... })    // Utente inizia a parlare
vapi.on('speech-end', () => { ... })      // Utente smette di parlare
vapi.on('message', (msg) => { ... })      // Messaggi e transcript
vapi.on('error', (error) => { ... })      // Errori
```

---

## 🛠️ Stack Tecnologico

- **React 18**: UI library
- **Vite**: Build tool veloce e moderno
- **@vapi-ai/web**: SDK Vapi per browser
- **CSS Modules**: Styling component-based
- **Google Fonts (Inter)**: Typography

---

## 🚀 Deployment

### Opzione 1: Vercel (Consigliato)

```bash
# Installa Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Opzione 2: Netlify

```bash
# Installa Netlify CLI
npm i -g netlify-cli

# Build
npm run build

# Deploy
netlify deploy --prod --dir=dist
```

### Opzione 3: GitHub Pages

1. Modifica `vite.config.js`:

```javascript
export default defineConfig({
  plugins: [react()],
  base: '/nome-repo/'  // Aggiungi questa linea
})
```

2. Build e deploy:

```bash
npm run build
gh-pages -d dist
```

### Opzione 4: Server Statico

Dopo `npm run build`, serve la cartella `dist/` con qualsiasi server statico:

```bash
# Esempio con Python
python3 -m http.server -d dist 8000

# Esempio con Node.js (serve)
npx serve dist
```

---

## 🔧 Configurazione Variabili Ambiente

### Development

Crea `.env`:

```bash
VITE_VAPI_PUBLIC_KEY=pk_xxxxx
VITE_ASSISTANT_ID=f25b74d7-dea8-4eb1-8e58-6225643b36b2
```

### Production

Configura le variabili sul tuo provider:

**Vercel**:
- Dashboard → Settings → Environment Variables

**Netlify**:
- Dashboard → Site settings → Environment → Environment variables

**GitHub Pages**:
- Le variabili devono essere hardcoded nel build (NON consigliato per chiavi sensibili)

---

## 🧪 Testing Locale

1. Assicurati che `.env` sia configurato
2. Avvia dev server: `npm run dev`
3. Apri http://localhost:5173
4. Clicca "Inizia Chiamata"
5. Parla con l'assistente
6. Verifica che la trascrizione appaia in tempo reale

### Troubleshooting

**Errore: "Configura VITE_VAPI_PUBLIC_KEY in .env"**
- Soluzione: Aggiungi la public key in `.env` e riavvia il dev server

**Errore: "VITE_ASSISTANT_ID non configurato"**
- Soluzione: Verifica che l'ID dell'assistente sia corretto in `.env`

**Chiamata non si avvia**
- Verifica che l'assistente sia attivo su Vapi Dashboard
- Controlla la console del browser per errori
- Verifica che il microfono sia autorizzato nel browser

**Nessun audio**
- Verifica i permessi del microfono nel browser
- Controlla le impostazioni audio del sistema
- Prova con auricolari/cuffie

---

## 📱 Browser Supportati

- ✅ Chrome/Edge (consigliato)
- ✅ Firefox
- ✅ Safari 14+
- ⚠️ Mobile browsers (funziona ma con limitazioni)

---

## 🎨 Personalizzazione

### Cambiare Colori

Modifica le variabili CSS in `App.css`:

```css
:root {
  --primary: #2563eb;      /* Colore primario */
  --danger: #dc2626;       /* Colore pulsante termina */
  --success: #16a34a;      /* Colore chiamata attiva */
  /* ... altri colori ... */
}
```

### Cambiare Font

Modifica il link in `index.html` e aggiorna `index.css`:

```html
<link href="https://fonts.googleapis.com/css2?family=TuoFont:wght@400;700&display=swap" rel="stylesheet">
```

### Modificare Layout

Il layout è responsive e si adatta automaticamente a mobile/desktop.
Modifica i breakpoint in `App.css`:

```css
@media (max-width: 640px) {
  /* Stili mobile */
}
```

---

## 📊 Metriche e Analytics

Per tracciare l'uso dell'assistente, puoi:

1. **Google Analytics**: Aggiungi lo script in `index.html`
2. **Eventi Custom**: Traccia chiamate in `App.jsx`:

```javascript
vapi.on('call-start', () => {
  // Invia evento a GA4
  gtag('event', 'call_start', {
    assistant_id: import.meta.env.VITE_ASSISTANT_ID
  })
})
```

---

## 🔐 Sicurezza

- ✅ Usa SEMPRE la Public Key nel frontend
- ✅ NON committare `.env` in git (è già in `.gitignore`)
- ✅ Configura CORS su Vapi se necessario
- ✅ Usa HTTPS in production

---

## 📚 Risorse

- [Vapi Documentation](https://docs.vapi.ai)
- [Vapi Web SDK](https://docs.vapi.ai/sdk/web)
- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)

---

## 🆘 Support

Per problemi o domande:

1. Controlla la [Vapi Documentation](https://docs.vapi.ai)
2. Verifica la console del browser per errori
3. Testa con il link pubblico Vapi per isolare il problema

---

**Ultimo aggiornamento**: 28 ottobre 2025
