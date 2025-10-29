#!/usr/bin/env python3
"""
Crea un nuovo assistente su Vapi.ai con configurazione completa.
Da usare solo per setup iniziale o per creare nuovi assistenti.
"""

import requests
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

VAPI_API_KEY = os.getenv('VAPI_API_KEY')
VAPI_BASE_URL = 'https://api.vapi.ai'

def load_template_config():
    """Carica la configurazione template da assistant-existing.json."""
    template_path = Path(__file__).parent.parent / 'config' / 'assistant-existing.json'

    if not template_path.exists():
        print("ATTENZIONE: Template assistant-existing.json non trovato!")
        print("  File atteso: {}".format(template_path))
        return None

    with open(template_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_system_prompt():
    """Carica il system prompt dal file."""
    prompt_path = Path(__file__).parent.parent / 'config' / 'vapi-system-prompt-with-tools.txt'

    if not prompt_path.exists():
        print("ATTENZIONE: System prompt non trovato!")
        print("  File atteso: {}".format(prompt_path))
        print("  Usando prompt di default...")
        return "Sei un assistente virtuale per il Comune di Codroipo. Aiuti i cittadini con informazioni sui servizi comunali."

    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def save_assistant_id(assistant_id):
    """Salva l'ID dell'assistente in .assistant-id."""
    id_file = Path(__file__).parent.parent / '.assistant-id'

    with open(id_file, 'w') as f:
        f.write(assistant_id)

    print("\nID assistente salvato in: {}".format(id_file))

def create_assistant(name=None, voice_provider=None):
    """
    Crea un nuovo assistente su Vapi.ai usando il template assistant-existing.json.

    Args:
        name: Nome dell'assistente (override del template)
        voice_provider: Provider voce ('11labs' o 'openai', override del template)

    Returns:
        dict: Informazioni assistente creato, o None se errore
    """

    if not VAPI_API_KEY:
        print("ERRORE: VAPI_API_KEY non trovata!")
        print("Crea un file .env con: VAPI_API_KEY=your_key")
        return None

    print("\nCreazione nuovo assistente...")

    # Carica configurazione dal template
    config = load_template_config()

    if not config:
        print("ERRORE: Impossibile caricare template!")
        return None

    print("✓ Template caricato da assistant-existing.json")

    # Override nome se specificato
    if name:
        config["name"] = name
        print("  Nome personalizzato: {}".format(name))
    else:
        print("  Nome: {}".format(config.get("name", "N/A")))

    # Override voice provider se specificato
    if voice_provider:
        if voice_provider == '11labs':
            config["voice"] = {
                "provider": "11labs",
                "voiceId": "Og6C5DgTHIScy85Fgh41",
                "model": "eleven_turbo_v2_5",
                "stability": 0.5,
                "similarityBoost": 0.75
            }
            print("  Voice: ElevenLabs (override)")
        elif voice_provider == 'openai':
            config["voice"] = {
                "provider": "openai",
                "voiceId": "alloy"
            }
            print("  Voice: OpenAI (override)")
    else:
        print("  Voice: {} (dal template)".format(config.get("voice", {}).get("provider", "N/A")))

    # Aggiorna system prompt dal file dedicato
    system_prompt = load_system_prompt()
    if "model" not in config:
        config["model"] = {}
    config["model"]["messages"] = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]
    print("✓ System prompt aggiornato da file")

    # Rimuovi knowledgeBase e toolIds dal template (saranno linkati dopo)
    if "model" in config and "knowledgeBase" in config["model"]:
        del config["model"]["knowledgeBase"]
        print("  (knowledgeBase rimossa - linkarla con update_assistant.py)")

    print()

    headers = {
        'Authorization': 'Bearer {}'.format(VAPI_API_KEY),
        'Content-Type': 'application/json'
    }

    print("Invio richiesta a Vapi.ai...")

    response = requests.post(
        '{}/assistant'.format(VAPI_BASE_URL),
        headers=headers,
        json=config
    )

    if response.status_code == 201:
        assistant = response.json()
        assistant_id = assistant.get('id')

        print("\n" + "="*60)
        print("ASSISTENTE CREATO CON SUCCESSO!")
        print("="*60)
        print("\nID:              {}".format(assistant_id))
        print("Nome:            {}".format(assistant.get('name')))
        print("Model:           {}".format(assistant.get('model', {}).get('model')))
        print("Voice Provider:  {}".format(assistant.get('voice', {}).get('provider')))
        print("Transcriber:     {}".format(assistant.get('transcriber', {}).get('provider')))
        print()
        print("Dashboard:       https://dashboard.vapi.ai")
        print("="*60)

        # Salva ID
        save_assistant_id(assistant_id)

        # Salva config completa
        save_config(assistant)

        return assistant

    else:
        print("\nERRORE nella creazione: {}".format(response.status_code))
        print(response.text)
        return None

def save_config(assistant):
    """Salva la configurazione dell'assistente in un file."""
    config_file = Path(__file__).parent.parent / 'config' / 'assistant-existing.json'

    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(assistant, f, indent=2, ensure_ascii=False)

    print("\nConfigurazione salvata in: {}".format(config_file))

def check_existing_assistant():
    """Controlla se esiste già un assistente configurato."""
    id_file = Path(__file__).parent.parent / '.assistant-id'

    if id_file.exists():
        assistant_id = id_file.read_text().strip()
        print("\n" + "="*60)
        print("ATTENZIONE: Assistente già configurato!")
        print("="*60)
        print("ID esistente: {}".format(assistant_id))
        print()
        print("Se procedi, verrà creato un NUOVO assistente.")
        print("L'ID esistente verrà sovrascritto in .assistant-id")
        print()

        response = input("Vuoi continuare? (s/N): ").strip().lower()
        return response == 's'

    return True

def main():
    """Main con supporto argomenti."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Crea nuovo assistente Vapi.ai',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi d'uso:

  # Crea assistente usando template assistant-existing.json
  python scripts/create_assistant.py

  # Crea assistente con nome personalizzato
  python scripts/create_assistant.py --name "Il Mio Assistente"

  # Crea assistente con voce OpenAI (override template)
  python scripts/create_assistant.py --voice openai

  # Forza creazione senza conferma
  python scripts/create_assistant.py --force

IMPORTANTE:
Questo script crea un NUOVO assistente su Vapi.ai usando il template.
Se hai già un assistente configurato, usa update_assistant.py
        """
    )

    parser.add_argument(
        '--name',
        type=str,
        help='Nome dell\'assistente (default: "Assistente Comune Codroipo")'
    )

    parser.add_argument(
        '--voice',
        choices=['11labs', 'openai'],
        help='Provider voce (default: usa template)'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Salta conferma se esiste già un assistente'
    )

    args = parser.parse_args()

    print("="*60)
    print("CREAZIONE NUOVO ASSISTENTE VAPI.AI")
    print("="*60)

    # Controlla se esiste già un assistente
    if not args.force:
        if not check_existing_assistant():
            print("\nCreazione annullata.")
            sys.exit(0)

    # Crea assistente
    assistant = create_assistant(
        name=args.name,
        voice_provider=args.voice
    )

    if assistant:
        print("\nPROSSIMI STEP:")
        print()
        print("1. Configura Knowledge Base:")
        print("   python scripts/upload_knowledge_base.py")
        print("   python scripts/link_knowledge_base.py")
        print()
        print("2. Configura Google Calendar (sul dashboard Vapi)")
        print()
        print("3. Configura Email Tool:")
        print("   python scripts/create_tool.py --url YOUR_SERVER_URL")
        print("   python scripts/link_tool_to_assistant.py")
        print()
        print("4. Testa l'assistente:")
        print("   https://dashboard.vapi.ai")
        print()

        sys.exit(0)
    else:
        print("\nCreazione fallita!")
        sys.exit(1)

if __name__ == "__main__":
    main()
