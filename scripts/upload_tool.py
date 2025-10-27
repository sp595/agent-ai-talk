#!/usr/bin/env python3
"""
Script per creare o aggiornare il tool Mailtrap in VAPI
Legge la configurazione da config/vapi-tools-config.json
"""
import os
import sys
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VAPI_BASE_URL = "https://api.vapi.ai"

def load_tool_config():
    """Carica la configurazione tool dal file JSON."""
    config_path = Path(__file__).parent.parent / 'config' / 'vapi-tools-config.json'

    if not config_path.exists():
        print("❌ ERRORE: config/vapi-tools-config.json non trovato")
        return None

    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_existing_tools():
    """Ottiene la lista di tutti i tool esistenti in VAPI."""
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(f"{VAPI_BASE_URL}/tool", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️  Impossibile ottenere la lista dei tool: {response.status_code}")
            return []
    except Exception as e:
        print(f"⚠️  Errore nel recupero dei tool: {str(e)}")
        return []

def find_tool_by_name(name):
    """Cerca un tool esistente per nome."""
    tools = get_existing_tools()
    for tool in tools:
        if tool.get('name') == name or tool.get('function', {}).get('name') == name:
            return tool.get('id')
    return None

def create_tool(tool_config):
    """Crea un nuovo tool in VAPI."""
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }

    print("📤 Creazione nuovo tool...")
    print("\n" + "="*60)
    print("CONFIGURAZIONE:")
    print(json.dumps(tool_config, indent=2, ensure_ascii=False))
    print("="*60 + "\n")

    try:
        response = requests.post(f"{VAPI_BASE_URL}/tool", json=tool_config, headers=headers)

        print(f"Status Code: {response.status_code}")

        if response.status_code == 201:
            result = response.json()
            print("\n✅ Tool creato con successo!")
            print(f"Tool ID: {result.get('id')}")

            # Salva ID in un file
            ids_file = Path(__file__).parent.parent / '.tool-ids.txt'
            with open(ids_file, 'a') as f:
                f.write(f"{result.get('id')}\n")

            print(f"ID salvato in .tool-ids.txt")

            print("\n⚠️  IMPORTANTE: Configura manualmente:")
            print("1. Vai su https://dashboard.vapi.ai/credentials")
            print("2. Crea una credenziale 'API Key' con il tuo MAILTRAP_API_TOKEN")
            print("3. Vai su https://dashboard.vapi.ai/tools")
            print("4. Apri il tool 'send_appointment_confirmation_email'")
            print("5. Nella sezione 'Credential', seleziona la credenziale Mailtrap")
            print("6. Salva")
            print("\nPoi collega il tool all'assistente:")
            print("  python scripts/link_tool_to_assistant.py send_appointment_confirmation_email")

            return result.get('id')
        else:
            print(f"\n❌ Errore nella creazione: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print(f"\n❌ Eccezione durante la creazione: {str(e)}")
        return None

def update_tool(tool_id, tool_config):
    """Aggiorna un tool esistente in VAPI."""
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }

    # Rimuovi il campo "type" per l'update (non è modificabile)
    update_config = {k: v for k, v in tool_config.items() if k != 'type'}

    print(f"🔄 Aggiornamento tool (ID: {tool_id})...")
    print("\n" + "="*60)
    print("CONFIGURAZIONE:")
    print(json.dumps(update_config, indent=2, ensure_ascii=False))
    print("="*60 + "\n")

    try:
        response = requests.patch(f"{VAPI_BASE_URL}/tool/{tool_id}", json=update_config, headers=headers)

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("\n✅ Tool aggiornato con successo!")

            print("\n⚠️  IMPORTANTE: Verifica la configurazione:")
            print("1. Vai su https://dashboard.vapi.ai/tools")
            print("2. Apri il tool 'send_appointment_confirmation_email'")
            print("3. Verifica che la credenziale Mailtrap sia configurata")
            print("4. Salva se necessario")

            return True
        else:
            print(f"\n❌ Errore nell'aggiornamento: {response.status_code}")
            print(response.text)
            return False

    except Exception as e:
        print(f"\n❌ Eccezione durante l'aggiornamento: {str(e)}")
        return False

def main():
    """Main."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Crea o aggiorna il tool Mailtrap in VAPI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi d'uso:

  # Crea un nuovo tool o aggiorna quello esistente (auto-detect)
  python scripts/upload_tool.py

  # Forza la creazione di un nuovo tool
  python scripts/upload_tool.py --create

  # Aggiorna un tool specifico per ID
  python scripts/upload_tool.py --update 7fc0553d-be04-487e-a0a1-2c50454bdf83

Note:
  - La configurazione viene letta da config/vapi-tools-config.json
  - Il tool chiama direttamente l'API Mailtrap (no server esterno necessario)
  - Devi configurare la credenziale Mailtrap nella dashboard VAPI
        """
    )

    parser.add_argument(
        '--create',
        action='store_true',
        help='Forza la creazione di un nuovo tool'
    )

    parser.add_argument(
        '--update',
        type=str,
        metavar='TOOL_ID',
        help='Aggiorna un tool esistente specificando il suo ID'
    )

    args = parser.parse_args()

    if not VAPI_API_KEY:
        print("❌ ERRORE: VAPI_API_KEY non trovato nel file .env")
        sys.exit(1)

    # Carica configurazione
    tool_config = load_tool_config()
    if not tool_config:
        sys.exit(1)

    tool_name = tool_config.get('function', {}).get('name', tool_config.get('name'))

    print("🛠️  UPLOAD TOOL MAILTRAP IN VAPI")
    print("="*60)
    print(f"Tool name: {tool_name}")
    print()

    # Modalità: create, update, o auto-detect
    if args.create:
        # Forza creazione
        tool_id = create_tool(tool_config)
        sys.exit(0 if tool_id else 1)
    elif args.update:
        # Aggiorna tool specifico
        success = update_tool(args.update, tool_config)
        sys.exit(0 if success else 1)
    else:
        # Auto-detect: cerca se esiste già
        print("🔍 Ricerca tool esistente...")
        existing_tool_id = find_tool_by_name(tool_name)

        if existing_tool_id:
            print(f"✓ Tool esistente trovato (ID: {existing_tool_id})")
            response = input("Vuoi aggiornarlo? [S/n] ")
            if response.lower() in ['', 's', 'y', 'si', 'yes']:
                success = update_tool(existing_tool_id, tool_config)
                sys.exit(0 if success else 1)
            else:
                print("Operazione annullata.")
                sys.exit(0)
        else:
            print("✗ Nessun tool esistente trovato.")
            response = input("Vuoi creare un nuovo tool? [S/n] ")
            if response.lower() in ['', 's', 'y', 'si', 'yes']:
                tool_id = create_tool(tool_config)
                sys.exit(0 if tool_id else 1)
            else:
                print("Operazione annullata.")
                sys.exit(0)

if __name__ == "__main__":
    main()
