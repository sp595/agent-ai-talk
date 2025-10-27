#!/usr/bin/env python3
"""
Aggiorna la configurazione dell'assistente esistente su Vapi.ai.
Utile quando modifichi il system prompt o altre impostazioni.
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

def load_system_prompt():
    """Carica il system prompt dal file."""
    prompt_path = Path(__file__).parent.parent / 'config' / 'vapi-system-prompt-with-tools.txt'
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_assistant_id():
    """Legge l'ID dell'assistente salvato."""
    id_file = Path(__file__).parent.parent / '.assistant-id'
    if not id_file.exists():
        print("ERRORE: File .assistant-id non trovato")
        print("Esegui prima: python scripts/create_assistant.py")
        return None

    with open(id_file, 'r') as f:
        return f.read().strip()

def update_assistant(update_type='all'):
    """
    Aggiorna l'assistente su Vapi.ai.

    Args:
        update_type: 'all', 'prompt', 'model', 'voice', 'settings'
    """

    if not VAPI_API_KEY:
        print("ERRORE: VAPI_API_KEY non trovata!")
        print("Crea un file .env con: VAPI_API_KEY=your_key")
        return False

    assistant_id = get_assistant_id()
    if not assistant_id:
        return False

    headers = {
        'Authorization': 'Bearer {}'.format(VAPI_API_KEY),
        'Content-Type': 'application/json'
    }

    # Costruisci config in base al tipo di update
    config = {}

    if update_type in ['all', 'prompt', 'model']:
        config['model'] = {
            "provider": "openai",
            "model": "gpt-4o",
            "temperature": 0.7,
            "messages": [{
                "role": "system",
                "content": load_system_prompt()
            }]
        }
        print("- Aggiornamento system prompt e model config")

    if update_type in ['all', 'voice']:
        # Carica voice config esistente se disponibile
        try:
            config_file = Path(__file__).parent.parent / 'config' / 'assistant-existing.json'
            with open(config_file, 'r') as f:
                current_config = json.load(f)
                config['voice'] = current_config.get('voice', {
                    "provider": "11labs",
                    "voiceId": "Og6C5DgTHIScy85Fgh41",
                    "model": "eleven_turbo_v2_5",
                    "stability": 0.5,
                    "similarityBoost": 0.75
                })
        except:
            config['voice'] = {
                "provider": "11labs",
                "voiceId": "Og6C5DgTHIScy85Fgh41",
                "model": "eleven_turbo_v2_5",
                "stability": 0.5,
                "similarityBoost": 0.75
            }
        print("- Aggiornamento voice config")

    if update_type in ['all', 'settings']:
        # Carica settings esistenti se disponibili
        try:
            config_file = Path(__file__).parent.parent / 'config' / 'assistant-existing.json'
            with open(config_file, 'r') as f:
                current_config = json.load(f)
                config.update({
                    "firstMessage": current_config.get('firstMessage', "Buongiorno! Sono l'assistente virtuale del Comune di Codroipo. Come posso aiutarti oggi?"),
                    "endCallMessage": current_config.get('endCallMessage', "Grazie per aver contattato il Comune di Codroipo. Buona giornata!"),
                    "silenceTimeoutSeconds": current_config.get('silenceTimeoutSeconds', 20),
                    "backgroundSound": current_config.get('backgroundSound', 'office')
                })
        except:
            config.update({
                "firstMessage": "Buongiorno! Sono l'assistente virtuale del Comune di Codroipo. Come posso aiutarti oggi?",
                "endCallMessage": "Grazie per aver contattato il Comune di Codroipo. Buona giornata!",
                "silenceTimeoutSeconds": 20,
                "backgroundSound": "office"
            })
        print("- Aggiornamento settings")

    if update_type == 'prompt':
        # Solo system prompt
        config = {
            "model": {
                "messages": [{
                    "role": "system",
                    "content": load_system_prompt()
                }]
            }
        }
        print("- Aggiornamento SOLO system prompt")

    print("\nAggiornamento assistente (ID: {})...".format(assistant_id[:8] + "..."))

    response = requests.patch(
        '{}/assistant/{}'.format(VAPI_BASE_URL, assistant_id),
        headers=headers,
        json=config
    )

    if response.status_code == 200:
        print("\nOK Assistente aggiornato con successo!")

        # Mostra cosa è stato aggiornato
        updated = response.json()
        print("\nConfigurazione attuale:")
        print("- Name: {}".format(updated.get('name', 'N/A')))
        print("- Model: {}".format(updated.get('model', {}).get('model', 'N/A')))
        print("- Voice Provider: {}".format(updated.get('voice', {}).get('provider', 'N/A')))

        print("\nL'assistente e' aggiornato!")
        print("Testalo su: https://dashboard.vapi.ai")

        return True
    else:
        print("\nERRORE: {}".format(response.status_code))
        print(response.text)
        return False

def main():
    """Main con supporto argomenti."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Aggiorna assistente Vapi.ai',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi d'uso:

  # Aggiorna tutto
  python scripts/update_assistant.py

  # Aggiorna solo il system prompt
  python scripts/update_assistant.py --type prompt

  # Aggiorna solo voice
  python scripts/update_assistant.py --type voice

  # Aggiorna solo settings
  python scripts/update_assistant.py --type settings
        """
    )

    parser.add_argument(
        '--type',
        choices=['all', 'prompt', 'model', 'voice', 'settings'],
        default='all',
        help='Tipo di aggiornamento (default: all)'
    )

    args = parser.parse_args()

    print("="*50)
    print("AGGIORNAMENTO ASSISTENTE VAPI.AI")
    print("="*50)
    print("Tipo: {}".format(args.type))
    print()

    success = update_assistant(args.type)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
