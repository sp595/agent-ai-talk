#!/usr/bin/env python3
"""
Aggiorna l'assistente Vapi.ai con:
- System prompt
- Configurazioni (voice, settings)
- Knowledge Base (se .knowledge-base-ids esiste)
- Tools (se .tool-ids esiste)

Preserva automaticamente tutte le altre configurazioni.
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
        print("⚠️  Template assistant-existing.json non trovato")
        print("   Verrà aggiornato solo il system prompt")
        return None

    with open(template_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_system_prompt():
    """Carica il system prompt dal file."""
    prompt_path = Path(__file__).parent.parent / 'config' / 'vapi-system-prompt-with-tools.txt'
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_assistant_id():
    """Legge l'ID dell'assistente salvato."""
    id_file = Path(__file__).parent.parent / '.assistant-id'
    if not id_file.exists():
        print("❌ File .assistant-id non trovato")
        print("Esegui prima: python scripts/create_assistant.py")
        return None

    with open(id_file, 'r') as f:
        return f.read().strip()


def get_knowledge_base_ids():
    """Legge gli ID dei file knowledge base se esistono."""
    kb_file = Path(__file__).parent.parent / '.knowledge-base-ids'

    if not kb_file.exists():
        return None

    with open(kb_file, 'r') as f:
        file_ids = [line.strip() for line in f.readlines() if line.strip()]

    return file_ids if file_ids else None


def get_tool_ids():
    """Legge gli ID dei tool se esistono."""
    tool_file = Path(__file__).parent.parent / '.tool-ids'

    if not tool_file.exists():
        return None

    with open(tool_file, 'r') as f:
        tool_ids = [line.strip() for line in f.readlines() if line.strip()]

    return tool_ids if tool_ids else None


def get_current_config(assistant_id, headers):
    """Fetch della configurazione corrente dell'assistente."""
    response = requests.get(
        f'{VAPI_BASE_URL}/assistant/{assistant_id}',
        headers=headers
    )

    if response.status_code != 200:
        print(f"❌ Impossibile recuperare configurazione assistente: {response.status_code}")
        print(response.text)
        return None

    return response.json()

def update_assistant(update_type='all'):
    """
    Aggiorna l'assistente su Vapi.ai usando il template assistant-existing.json.
    Linka automaticamente KB e tools se presenti.

    Args:
        update_type: 'all', 'prompt', 'config'
    """

    if not VAPI_API_KEY:
        print("❌ VAPI_API_KEY non trovata in .env")
        return False

    assistant_id = get_assistant_id()
    if not assistant_id:
        return False

    headers = {
        'Authorization': f'Bearer {VAPI_API_KEY}',
        'Content-Type': 'application/json'
    }

    print(f"\n📡 Fetch configurazione corrente...")
    current_config = get_current_config(assistant_id, headers)
    if not current_config:
        return False

    print("✓ Configurazione recuperata")
    print()

    # Carica template
    template_config = load_template_config()

    # Prepara config per PATCH
    patch_config = {}

    # Aggiorna campi dal template se richiesto
    if update_type in ['all', 'config'] and template_config:
        print("📋 Aggiornamento configurazione da template...")

        # Copia campi dal template (esclusi model, che gestiamo separatamente)
        fields_to_update = [
            'name', 'voice', 'transcriber', 'firstMessage', 'voicemailMessage',
            'endCallMessage', 'endCallFunctionEnabled', 'silenceTimeoutSeconds',
            'clientMessages', 'serverMessages', 'responseDelaySeconds',
            'llmRequestDelaySeconds', 'maxDurationSeconds', 'numWordsToInterruptAssistant',
            'backgroundSound', 'analysisPlan', 'messagePlan', 'startSpeakingPlan',
            'compliancePlan'
        ]

        for field in fields_to_update:
            if field in template_config:
                patch_config[field] = template_config[field]

        print(f"✓ Aggiornati {len([f for f in fields_to_update if f in template_config])} campi dal template")

    # Gestisci model config separatamente
    if template_config and 'model' in template_config:
        model_config = template_config['model'].copy()
    else:
        model_config = current_config.get('model', {})

    # Aggiorna system prompt se richiesto
    if update_type in ['all', 'prompt']:
        print("\n📝 Aggiornamento system prompt...")
        model_config['messages'] = [{
            "role": "system",
            "content": load_system_prompt()
        }]
        print("✓ System prompt aggiornato")

    # Linka Knowledge Base se esiste .knowledge-base-ids
    kb_ids = get_knowledge_base_ids()
    if kb_ids:
        print(f"\n📚 Link Knowledge Base ({len(kb_ids)} file)...")
        model_config['knowledgeBase'] = {
            "provider": "google",
            "fileIds": kb_ids
        }
        print("✓ Knowledge Base linkata")
    else:
        print("\n⏭️  Nessun file Knowledge Base da linkare")
        # Rimuovi KB dal model se non ci sono file
        if 'knowledgeBase' in model_config:
            del model_config['knowledgeBase']

    # Linka Tools se esiste .tool-ids
    tool_ids = get_tool_ids()
    if tool_ids:
        print(f"\n🛠️  Link Tools ({len(tool_ids)} tool)...")
        model_config['toolIds'] = tool_ids
        print("✓ Tools linkati")
    else:
        print("\n⏭️  Nessun tool da linkare")
        # Rimuovi toolIds dal model se non ci sono tool
        if 'toolIds' in model_config:
            del model_config['toolIds']

    # Aggiungi model config al patch
    patch_config["model"] = model_config

    print(f"\n📤 Invio aggiornamenti a Vapi.ai...")
    response = requests.patch(
        f'{VAPI_BASE_URL}/assistant/{assistant_id}',
        headers=headers,
        json=patch_config
    )

    if response.status_code == 200:
        print("\n" + "=" * 60)
        print("✅ ASSISTENTE AGGIORNATO CON SUCCESSO!")
        print("=" * 60)

        updated = response.json()
        print(f"\nAssistente: {updated.get('name', 'N/A')}")
        print(f"Model: {updated.get('model', {}).get('model', 'N/A')}")

        # Mostra KB e tools
        kb = updated.get('model', {}).get('knowledgeBase', {})
        if kb:
            kb_count = len(kb.get('fileIds', []))
            print(f"Knowledge Base: {kb_count} file")

        tools = updated.get('model', {}).get('toolIds', [])
        if tools:
            print(f"Tools: {len(tools)} tool")

        print("\n🎉 L'assistente è pronto!")
        print("Testalo su: https://dashboard.vapi.ai")

        return True
    else:
        print(f"\n❌ ERRORE: {response.status_code}")
        print(response.text)
        return False

def main():
    """Main - Aggiorna assistente."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Aggiorna assistente Vapi.ai e linka automaticamente KB e tools',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi d'uso:

  # Aggiorna tutto: config da template + prompt + KB + tools
  python scripts/update_assistant.py

  # Aggiorna solo il system prompt (preserva resto)
  python scripts/update_assistant.py --type prompt

  # Aggiorna solo config da template (preserva prompt, KB, tools)
  python scripts/update_assistant.py --type config

Note:
  - Usa il template assistant-existing.json per aggiornare i campi
  - Se esiste .knowledge-base-ids, linka automaticamente KB
  - Se esiste .tool-ids, linka automaticamente tutti i tool
  - Preserva sempre le configurazioni non specificate
        """
    )

    parser.add_argument(
        '--type',
        choices=['all', 'prompt', 'config'],
        default='all',
        help='Tipo di aggiornamento: all (tutto), prompt (solo prompt), config (solo config da template)'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("🔧 AGGIORNAMENTO ASSISTENTE VAPI.AI")
    print("=" * 60)
    print()

    success = update_assistant(args.type)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
