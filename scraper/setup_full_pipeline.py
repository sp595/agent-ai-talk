#!/usr/bin/env python3
"""
Script MASTER per setup completo knowledge base.

Workflow completo:
1. Scraping servizi reali dal sito Comune
2. Generazione file Markdown knowledge base
3. Upload file su Vapi.ai
4. Collegamento knowledge base all'assistente

Tutto automatico in un unico comando!
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Esegue comando e mostra output."""
    print("\n" + "="*60)
    print(f"⚙️  {description}")
    print("="*60)
    print()

    result = subprocess.run(cmd, shell=True)

    if result.returncode != 0:
        print(f"\n❌ Errore durante: {description}")
        return False

    print(f"\n✅ Completato: {description}")
    return True

def check_prerequisites():
    """Verifica prerequisiti."""
    print("="*60)
    print("CONTROLLO PREREQUISITI")
    print("="*60)
    print()

    # Check playwright
    try:
        import playwright
        print("✓ Playwright installato")
    except ImportError:
        print("✗ Playwright NON installato")
        print("\nInstalla con:")
        print("  pip install playwright")
        print("  playwright install chromium")
        return False

    # Check .env
    env_file = Path(__file__).parent.parent / '.env'
    if env_file.exists():
        print("✓ File .env trovato")
    else:
        print("✗ File .env NON trovato")
        print("\nCrea .env con:")
        print("  VAPI_API_KEY=your_key_here")
        return False

    # Check .assistant-id
    id_file = Path(__file__).parent.parent / '.assistant-id'
    if id_file.exists():
        print("✓ File .assistant-id trovato")
    else:
        print("⚠️  File .assistant-id NON trovato")
        print("   (Sarà creato durante il setup)")

    print()
    return True

def main():
    """Main pipeline."""

    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   SETUP COMPLETO KNOWLEDGE BASE - Comune di Codroipo    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")

    # 1. Check prerequisiti
    if not check_prerequisites():
        print("\n❌ Prerequisiti mancanti. Impossibile continuare.")
        return False

    print("\nPrerequisiti OK! Avvio pipeline completa...\n")
    input("Premi INVIO per continuare...")

    # 2. Scraping
    if not run_command(
        "python scraper/scrape_real.py",
        "Step 1/4: Scraping servizi dal sito web"
    ):
        return False

    # 3. Generazione KB
    if not run_command(
        "python scraper/generate_knowledge_base.py",
        "Step 2/4: Generazione file Markdown knowledge base"
    ):
        return False

    # 4. Upload KB
    if not run_command(
        "python scripts/upload_knowledge_base.py",
        "Step 3/4: Upload knowledge base su Vapi.ai"
    ):
        return False

    # 5. Link KB
    if not run_command(
        "python scripts/link_knowledge_base.py",
        "Step 4/4: Collegamento knowledge base all'assistente"
    ):
        return False

    # Success!
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETATO CON SUCCESSO!")
    print("="*60)
    print("""
✅ Servizi scraped dal sito reale
✅ Knowledge base generata
✅ File caricati su Vapi.ai
✅ Knowledge base collegata all'assistente

Prossimi step opzionali:
  1. Aggiorna system prompt:
     python scripts/update_assistant.py --type prompt

  2. Verifica configurazione:
     python scripts/get_assistant_info.py

  3. Testa assistente:
     https://dashboard.vapi.ai
""")

    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrotta dall'utente")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Errore imprevisto: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
