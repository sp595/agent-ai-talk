#!/usr/bin/env python3
"""
Scraper REALE per estrarre servizi dal sito del Comune di Codroipo.
Usa Playwright per gestire JavaScript rendering (Angular SPA).
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Prova a importare playwright
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright non installato!")
    print("\nPer installare:")
    print("  pip install playwright")
    print("  playwright install chromium")
    print()

def scrape_services_with_playwright():
    """Scrape servizi usando Playwright."""

    if not PLAYWRIGHT_AVAILABLE:
        print("ERRORE: Playwright richiesto ma non installato")
        return None

    print("="*60)
    print("SCRAPING SERVIZI REALI - Comune di Codroipo")
    print("="*60)
    print()

    url = "https://www.comune.codroipo.ud.it/it/servizi-224003"

    print(f"URL: {url}")
    print("Avvio browser headless...")
    print()

    services = []

    with sync_playwright() as p:
        # Avvia browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Caricamento pagina...")
        page.goto(url, wait_until='networkidle')

        # Attendi che Angular carichi il contenuto
        print("Attendo rendering Angular...")
        page.wait_for_selector('.service-card, .servizio, article, .card', timeout=10000)

        # Estrai servizi
        print("Estrazione servizi...")

        # Strategia: cerca vari selettori comuni per servizi
        service_elements = page.query_selector_all('article, .service-card, .servizio, .card')

        print(f"Trovati {len(service_elements)} elementi potenziali")
        print()

        for idx, element in enumerate(service_elements[:10], 1):  # Max 10 servizi
            try:
                # Estrai titolo
                title_elem = element.query_selector('h1, h2, h3, .title, .titolo')
                title = title_elem.inner_text().strip() if title_elem else f"Servizio {idx}"

                # Estrai descrizione
                desc_elem = element.query_selector('p, .description, .descrizione')
                description = desc_elem.inner_text().strip() if desc_elem else ""

                # Estrai link
                link_elem = element.query_selector('a')
                service_url = link_elem.get_attribute('href') if link_elem else ""
                if service_url and not service_url.startswith('http'):
                    service_url = f"https://www.comune.codroipo.ud.it{service_url}"

                # Se abbiamo dati validi, aggiungi
                if title and len(title) > 3:
                    service = {
                        'service_name': title,
                        'description': description[:500] if description else f"Servizio {title} del Comune di Codroipo",
                        'url': service_url,
                        'office_hours': 'Lunedì-Venerdì: 8:30-12:30',  # Default generico
                        'requirements': [],  # Da completare manualmente
                        'qa_pairs': []  # Generati dopo
                    }

                    services.append(service)
                    print(f"✓ {idx}. {title[:50]}...")

            except Exception as e:
                print(f"✗ Errore elemento {idx}: {e}")
                continue

        browser.close()

    print()
    print(f"OK Estratti {len(services)} servizi")
    return services

def scrape_service_detail(url):
    """Scrape dettagli di un singolo servizio."""

    if not PLAYWRIGHT_AVAILABLE:
        return None

    print(f"\nEstrazione dettagli da: {url[:60]}...")

    details = {
        'requirements': [],
        'office_hours': '',
        'cost': '',
        'how_to': ''
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(url, wait_until='networkidle', timeout=15000)
            page.wait_for_timeout(2000)  # Attendi caricamento completo

            # Estrai tutto il testo della pagina
            content = page.inner_text('body')

            # Cerca sezioni comuni
            if 'documenti necessari' in content.lower() or 'requisiti' in content.lower():
                # Trova paragrafi dopo "documenti" o "requisiti"
                paragraphs = page.query_selector_all('p, li')
                for p in paragraphs[:20]:
                    text = p.inner_text().strip()
                    if len(text) > 10 and len(text) < 200:
                        if any(keyword in text.lower() for keyword in ['documento', 'carta', 'codice', 'certificato', 'identità']):
                            details['requirements'].append(text)

            # Cerca orari
            if 'orari' in content.lower() or 'apertura' in content.lower():
                for p in page.query_selector_all('p, li, .orari, .hours'):
                    text = p.inner_text().strip()
                    if any(day in text.lower() for day in ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì']):
                        details['office_hours'] = text
                        break

            # Cerca costo
            if '€' in content or 'euro' in content.lower() or 'costo' in content.lower():
                for p in page.query_selector_all('p, li'):
                    text = p.inner_text().strip()
                    if '€' in text or 'euro' in text.lower():
                        details['cost'] = text
                        break

        except Exception as e:
            print(f"  ⚠️  Errore: {e}")

        browser.close()

    return details

def generate_qa_pairs(service):
    """Genera Q&A pairs basate sul servizio."""

    service_name = service['service_name']

    # Q&A generiche ma realistiche
    qa_pairs = [
        {
            'question': f"Come posso richiedere {service_name}?",
            'answer': f"Per richiedere {service_name} devi prenotare un appuntamento presso l'ufficio comunale competente. Puoi farlo telefonando al numero 0432 905511 o tramite questo assistente virtuale."
        },
        {
            'question': f"Quali documenti servono per {service_name}?",
            'answer': f"Per {service_name} generalmente servono: documento di identità valido, codice fiscale e eventuale documentazione specifica. Ti consiglio di verificare i requisiti esatti al momento della prenotazione."
        },
        {
            'question': f"Quanto costa {service_name}?",
            'answer': service.get('cost', f"Il costo di {service_name} varia in base al tipo di richiesta. Per informazioni precise contatta l'ufficio al 0432 905511.")
        },
        {
            'question': f"Quali sono gli orari per {service_name}?",
            'answer': service.get('office_hours', "L'ufficio è aperto generalmente dal lunedì al venerdì in orario mattutino. Per orari precisi contatta il numero 0432 905511.")
        },
        {
            'question': f"Quanto tempo serve per ottenere {service_name}?",
            'answer': f"I tempi di rilascio di {service_name} variano. Generalmente il servizio viene erogato entro pochi giorni dalla richiesta. Per informazioni precise contatta l'ufficio competente."
        }
    ]

    return qa_pairs

def save_to_json(services, output_file):
    """Salva servizi estratti in JSON."""

    output_path = Path(__file__).parent / output_file

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(services, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Dati salvati in: {output_path}")

def main():
    """Main."""

    if not PLAYWRIGHT_AVAILABLE:
        print("\n❌ Impossibile continuare senza Playwright")
        print("\nAlternativa:")
        print("  1. Installa Playwright: pip install playwright")
        print("  2. Installa browser: playwright install chromium")
        print("  3. Riesegui: python scraper/scrape_real.py")
        return False

    # Scrape servizi principali
    services = scrape_services_with_playwright()

    if not services:
        print("\n❌ Nessun servizio estratto")
        return False

    # Arricchisci con dettagli (opzionale - può essere lento)
    enrich = input("\nVuoi estrarre dettagli da ogni servizio? (lento, 1-2min) [s/N]: ").lower()

    if enrich == 's':
        print("\nEstrazione dettagli...")
        for service in services[:5]:  # Max 5 per non essere troppo lento
            if service.get('url'):
                details = scrape_service_detail(service['url'])
                if details:
                    service['requirements'] = details.get('requirements', [])[:5]
                    if details.get('office_hours'):
                        service['office_hours'] = details['office_hours']
                    if details.get('cost'):
                        service['cost'] = details['cost']

    # Genera Q&A pairs
    print("\nGenerazione Q&A pairs...")
    for service in services:
        service['qa_pairs'] = generate_qa_pairs(service)
        print(f"✓ {len(service['qa_pairs'])} Q&A per: {service['service_name'][:40]}...")

    # Salva JSON
    save_to_json(services, 'services_data_real.json')

    print("\n" + "="*60)
    print("SCRAPING COMPLETATO!")
    print("="*60)
    print(f"\n✓ {len(services)} servizi estratti")
    print("✓ Q&A pairs generate")
    print("\nProssimo step:")
    print("  python scraper/generate_knowledge_base.py")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
