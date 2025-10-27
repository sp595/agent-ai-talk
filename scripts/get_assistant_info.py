#!/usr/bin/env python3
"""
Mostra informazioni sull'assistente configurato.
Utile per verificare lo stato corrente.
"""

import requests
import os
import sys
import json
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
        return None

    with open(id_file, 'r') as f:
        return f.read().strip()

def get_assistant_info():
    """Recupera info sull'assistente da Vapi.ai."""

    if not VAPI_API_KEY:
        print("ERRORE: VAPI_API_KEY non trovata!")
        return None

    assistant_id = get_assistant_id()
    if not assistant_id:
        print("ERRORE: File .assistant-id non trovato")
        print("Esegui prima: python scripts/create_assistant.py")
        return None

    headers = {
        'Authorization': 'Bearer {}'.format(VAPI_API_KEY)
    }

    print("Recupero informazioni assistente...")
    print("ID: {}".format(assistant_id))
    print()

    response = requests.get(
        '{}/assistant/{}'.format(VAPI_BASE_URL, assistant_id),
        headers=headers
    )

    if response.status_code == 200:
        return response.json()
    else:
        print("ERRORE: {}".format(response.status_code))
        print(response.text)
        return None

def display_info(assistant):
    """Mostra le informazioni in modo leggibile."""

    print("="*60)
    print("INFORMAZIONI ASSISTENTE")
    print("="*60)

    print("\nGENERALE")
    print("-" * 60)
    print("Nome:            {}".format(assistant.get('name', 'N/A')))
    print("ID:              {}".format(assistant.get('id', 'N/A')))
    print("Creato:          {}".format(assistant.get('createdAt', 'N/A')))
    print("Aggiornato:      {}".format(assistant.get('updatedAt', 'N/A')))

    print("\nMODELLO")
    print("-" * 60)
    model = assistant.get('model', {})
    print("Provider:        {}".format(model.get('provider', 'N/A')))
    print("Model:           {}".format(model.get('model', 'N/A')))
    print("Temperature:     {}".format(model.get('temperature', 'N/A')))
    print("Max Tokens:      {}".format(model.get('maxTokens', 'N/A')))

    messages = model.get('messages', [])
    if messages:
        system_msg = next((m for m in messages if m.get('role') == 'system'), None)
        if system_msg:
            content = system_msg.get('content', '')
            preview = content[:100] + "..." if len(content) > 100 else content
            print("System Prompt:   {}".format(preview))

    print("\nVOICE")
    print("-" * 60)
    voice = assistant.get('voice', {})
    print("Provider:        {}".format(voice.get('provider', 'N/A')))
    print("Voice ID:        {}".format(voice.get('voiceId', 'N/A')))

    print("\nTRANSCRIBER")
    print("-" * 60)
    transcriber = assistant.get('transcriber', {})
    print("Provider:        {}".format(transcriber.get('provider', 'N/A')))
    print("Model:           {}".format(transcriber.get('model', 'N/A')))
    print("Language:        {}".format(transcriber.get('language', 'N/A')))

    print("\nKNOWLEDGE BASE")
    print("-" * 60)
    # KB può essere sia top-level che dentro model
    kb = assistant.get('knowledgeBase') or assistant.get('model', {}).get('knowledgeBase', {})
    if kb:
        print("Provider:        {}".format(kb.get('provider', 'N/A')))
        file_ids = kb.get('fileIds', [])
        print("Files:           {} file(s)".format(len(file_ids)))
        for i, fid in enumerate(file_ids, 1):
            print("  {}. {}".format(i, fid))
    else:
        print("Nessuna knowledge base configurata")

    print("\nSETTINGS")
    print("-" * 60)
    print("First Message:   {}".format(assistant.get('firstMessage', 'N/A')[:60] + "..."))
    print("End Call Msg:    {}".format(assistant.get('endCallMessage', 'N/A')[:60] + "..."))
    print("Silence Timeout: {}s".format(assistant.get('silenceTimeoutSeconds', 'N/A')))
    print("Response Delay:  {}s".format(assistant.get('responseDelaySeconds', 'N/A')))
    print("Max Duration:    {}s".format(assistant.get('maxDurationSeconds', 'N/A')))

    print("\n" + "="*60)

def save_full_config(assistant):
    """Salva la configurazione completa in un file JSON."""
    output_file = Path(__file__).parent.parent / 'config' / 'assistant-current.json'

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(assistant, f, indent=2, ensure_ascii=False)

    print("\nConfigurazione completa salvata in:")
    print("  {}".format(output_file))
    print("\nUsa questo file come riferimento per update_assistant.py")

def main():
    """Main."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Mostra info assistente Vapi.ai'
    )

    parser.add_argument(
        '--save',
        action='store_true',
        help='Salva configurazione completa in JSON'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in formato JSON'
    )

    args = parser.parse_args()

    assistant = get_assistant_info()

    if not assistant:
        sys.exit(1)

    if args.json:
        # Output JSON
        print(json.dumps(assistant, indent=2, ensure_ascii=False))
    else:
        # Output formattato
        display_info(assistant)

    if args.save:
        save_full_config(assistant)

if __name__ == "__main__":
    main()
