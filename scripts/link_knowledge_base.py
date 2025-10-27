#!/usr/bin/env python3
"""
Collega i file della knowledge base all'assistente.
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

def link_knowledge_base():
    """Collega la knowledge base all'assistente."""

    if not VAPI_API_KEY:
        print("ERRORE: VAPI_API_KEY non trovata!")
        return

    # Leggi assistant ID
    id_file = Path(__file__).parent.parent / '.assistant-id'
    if not id_file.exists():
        print("ERRORE: File .assistant-id non trovato")
        print("Esegui prima: python scripts/create_assistant.py")
        return

    with open(id_file, 'r') as f:
        assistant_id = f.read().strip()

    # Leggi knowledge base IDs
    kb_ids_file = Path(__file__).parent.parent / '.knowledge-base-ids.txt'
    if not kb_ids_file.exists():
        print("ERRORE: File .knowledge-base-ids.txt non trovato")
        print("Esegui prima: python scripts/upload_knowledge_base.py")
        return

    with open(kb_ids_file, 'r') as f:
        file_ids = [line.strip() for line in f.readlines() if line.strip()]

    print("Collegamento knowledge base...")
    print("Assistant ID: {}".format(assistant_id))
    print("File IDs: {}".format(len(file_ids)))

    headers = {
        'Authorization': 'Bearer {}'.format(VAPI_API_KEY),
        'Content-Type': 'application/json'
    }

    # Carica config attuale
    try:
        config_file = Path(__file__).parent.parent / 'config' / 'assistant-existing.json'
        with open(config_file, 'r') as f:
            current_config = json.load(f)
            model_config = current_config.get('model', {})
    except:
        model_config = {}

    config = {
        "model": {
            "provider": model_config.get('provider', 'openai'),
            "model": model_config.get('model', 'gpt-4o'),
            "temperature": model_config.get('temperature', 0.65),
            "maxTokens": model_config.get('maxTokens', 400),
            "knowledgeBase": {
                "provider": "google",
                "fileIds": file_ids
            }
        }
    }

    response = requests.patch(
        '{}/assistant/{}'.format(VAPI_BASE_URL, assistant_id),
        headers=headers,
        json=config
    )

    if response.status_code == 200:
        print("\nOK Knowledge base collegata con successo!")
        print("\nL'assistente e' pronto!")
        print("Vai su https://dashboard.vapi.ai per testarlo")
    else:
        print("\nERRORE: {}".format(response.status_code))
        print(response.text)

if __name__ == "__main__":
    link_knowledge_base()
