#!/usr/bin/env python3
"""
Collega il tool email custom all'assistente.
Aggiunge il tool alla lista toolIds del modello.
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

def get_assistant_id():
    """Legge l'ID dell'assistente salvato."""
    id_file = Path(__file__).parent.parent / '.assistant-id'
    if not id_file.exists():
        print("ERRORE: File .assistant-id non trovato")
        return None

    with open(id_file, 'r') as f:
        return f.read().strip()

def get_tool_ids():
    """Legge gli ID dei tool salvati."""
    ids_file = Path(__file__).parent.parent / '.tool-ids.txt'
    if not ids_file.exists():
        print("ERRORE: File .tool-ids.txt non trovato")
        print("Esegui prima: python scripts/create_tool.py --url YOUR_URL")
        return None

    with open(ids_file, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def link_tool_to_assistant():
    """Collega il tool all'assistente."""

    if not VAPI_API_KEY:
        print("ERRORE: VAPI_API_KEY non trovata!")
        return False

    assistant_id = get_assistant_id()
    if not assistant_id:
        return False

    tool_ids = get_tool_ids()
    if not tool_ids:
        return False

    print("="*50)
    print("COLLEGAMENTO TOOL ALL'ASSISTENTE")
    print("="*50)
    print()
    print("Assistant ID: {}".format(assistant_id[:8] + "..."))
    print("Tool IDs: {}".format(len(tool_ids)))
    for tid in tool_ids:
        print("  - {}".format(tid[:8] + "..."))
    print()

    headers = {
        'Authorization': 'Bearer {}'.format(VAPI_API_KEY),
        'Content-Type': 'application/json'
    }

    # Carica config esistente
    try:
        config_file = Path(__file__).parent.parent / 'config' / 'assistant-existing.json'
        with open(config_file, 'r') as f:
            current_config = json.load(f)
            existing_tool_ids = current_config.get('model', {}).get('toolIds', [])
    except:
        existing_tool_ids = []

    # Unisci tool IDs (evita duplicati)
    all_tool_ids = list(set(existing_tool_ids + tool_ids))

    print("Tool esistenti: {}".format(len(existing_tool_ids)))
    print("Tool totali dopo aggiunta: {}".format(len(all_tool_ids)))
    print()

    config = {
        "model": {
            "toolIds": all_tool_ids
        }
    }

    response = requests.patch(
        '{}/assistant/{}'.format(VAPI_BASE_URL, assistant_id),
        headers=headers,
        json=config
    )

    if response.status_code == 200:
        print("OK Tool collegato con successo!")
        print()
        print("L'assistente ora ha accesso a:")
        for tid in all_tool_ids:
            print("  - {}".format(tid[:8] + "..."))
        print()
        print("Vai su https://dashboard.vapi.ai per testare")
        return True
    else:
        print("ERRORE: {}".format(response.status_code))
        print(response.text)
        return False

def main():
    """Main."""
    success = link_tool_to_assistant()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
