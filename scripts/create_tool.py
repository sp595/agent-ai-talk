#!/usr/bin/env python3
"""
Crea il tool email custom su Vapi.ai.
Usa config/vapi-tools-config.json come template.
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

def load_tool_config():
    """Carica la configurazione tool dal file JSON."""
    config_path = Path(__file__).parent.parent / 'config' / 'vapi-tools-config.json'

    if not config_path.exists():
        print("ERRORE: config/vapi-tools-config.json non trovato")
        return None

    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_tool(server_url):
    """
    Crea il tool custom su Vapi.ai.

    Args:
        server_url: URL pubblico dove è deployato tools/email_reminder.py
    """

    if not VAPI_API_KEY:
        print("ERRORE: VAPI_API_KEY non trovata!")
        print("Crea un file .env con: VAPI_API_KEY=your_key")
        return None

    if not server_url:
        print("ERRORE: Devi specificare l'URL del server!")
        return None

    # Carica template
    tool_config = load_tool_config()
    if not tool_config:
        return None

    # Aggiorna URL server
    tool_config['server']['url'] = server_url

    print("="*50)
    print("CREAZIONE TOOL EMAIL SU VAPI.AI")
    print("="*50)
    print()
    print("Tool: send_appointment_confirmation")
    print("Server URL: {}".format(server_url))
    print()

    headers = {
        'Authorization': 'Bearer {}'.format(VAPI_API_KEY),
        'Content-Type': 'application/json'
    }

    response = requests.post(
        '{}/tool'.format(VAPI_BASE_URL),
        headers=headers,
        json=tool_config
    )

    if response.status_code == 201:
        tool_data = response.json()
        tool_id = tool_data.get('id')

        print("OK Tool creato con successo!")
        print()
        print("Tool ID: {}".format(tool_id))
        print()

        # Salva ID
        ids_file = Path(__file__).parent.parent / '.tool-ids.txt'
        with open(ids_file, 'w') as f:
            f.write(tool_id)

        print("ID salvato in .tool-ids.txt")
        print()
        print("Prossimo step:")
        print("  python scripts/link_tool_to_assistant.py")

        return tool_id
    else:
        print("ERRORE: {}".format(response.status_code))
        print(response.text)
        return None

def main():
    """Main."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Crea tool email custom su Vapi.ai',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi d'uso:

  # Con URL ngrok (test)
  python scripts/create_tool.py --url https://abc123.ngrok.io/send-appointment-confirmation

  # Con URL Railway (production)
  python scripts/create_tool.py --url https://codroipo-email.up.railway.app/send-appointment-confirmation

Note:
  - Il server deve essere raggiungibile pubblicamente
  - Testa prima con: curl https://YOUR_URL/health
  - Vedi tools/TOOLS-SETUP.md per deployment
        """
    )

    parser.add_argument(
        '--url',
        required=True,
        help='URL pubblico del server Flask (es: https://abc123.ngrok.io/send-appointment-confirmation)'
    )

    args = parser.parse_args()

    tool_id = create_tool(args.url)
    sys.exit(0 if tool_id else 1)

if __name__ == "__main__":
    main()
