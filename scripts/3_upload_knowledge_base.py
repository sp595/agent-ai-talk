#!/usr/bin/env python3
"""
Carica i file della knowledge base su Vapi.ai.
Se esiste .assistant-id, linka automaticamente i file all'assistente.
"""

import os
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VAPI_BASE_URL = "https://api.vapi.ai"


def get_assistant_id():
    """Legge l'ID dell'assistente se presente."""
    id_file = Path(__file__).parent.parent / ".assistant-id"
    if not id_file.exists():
        return None

    with open(id_file, "r") as f:
        return f.read().strip()


def get_current_config(assistant_id):
    """Fetch della configurazione corrente dell'assistente."""
    headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}

    response = requests.get(
        f"{VAPI_BASE_URL}/assistant/{assistant_id}",
        headers=headers
    )

    if response.status_code != 200:
        print(f"⚠️  Impossibile recuperare config assistente: {response.status_code}")
        return None

    return response.json()


def link_to_assistant(file_ids):
    """Linka i file KB all'assistente se presente .assistant-id."""
    assistant_id = get_assistant_id()

    if not assistant_id:
        print("\n⏭️  .assistant-id non trovato, skip auto-linking")
        print("   Usa: python scripts/update_assistant.py")
        return False

    print(f"\n📡 Auto-linking a assistente {assistant_id}...")

    # Fetch config corrente
    current_config = get_current_config(assistant_id)
    if not current_config:
        return False

    # Prepara update solo per model.knowledgeBase
    model_config = current_config.get("model", {})
    model_config["knowledgeBase"] = {
        "provider": "google",
        "fileIds": file_ids
    }

    # PATCH all'assistente
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.patch(
        f"{VAPI_BASE_URL}/assistant/{assistant_id}",
        headers=headers,
        json={"model": model_config}
    )

    if response.status_code == 200:
        print(f"✅ Knowledge Base linkata! ({len(file_ids)} file)")
        return True
    else:
        print(f"❌ Errore nel link: {response.status_code}")
        print(response.text)
        return False


def upload_file(filepath):
    """Carica un file nella knowledge base."""

    if not VAPI_API_KEY:
        print("ERRORE: VAPI_API_KEY non trovata!")
        return None

    headers = {"Authorization": "Bearer {}".format(VAPI_API_KEY)}

    filename = Path(filepath).name
    print("Caricamento {}...".format(filename))

    with open(filepath, "rb") as f:
        files = {"file": (filename, f, "text/markdown")}

        response = requests.post(
            "{}/file".format(VAPI_BASE_URL), headers=headers, files=files
        )

    if response.status_code == 201:
        file_data = response.json()
        print("  OK File ID: {}".format(file_data["id"]))
        return file_data["id"]
    else:
        print("  ERRORE: {}".format(response.status_code))
        print("  {}".format(response.text))
        return None


def upload_all():
    """Carica tutti i file della knowledge base."""

    kb_path = Path(__file__).parent.parent / "knowledge-base"
    md_files = sorted(kb_path.glob("*.md"))

    if not md_files:
        print("ERRORE: Nessun file .md trovato in knowledge-base/")
        return

    print("Trovati {} file da caricare\n".format(len(md_files)))

    file_ids = []
    for md_file in md_files:
        file_id = upload_file(md_file)
        if file_id:
            file_ids.append(file_id)

    if file_ids:
        print("\n✅ Caricati {}/{} file".format(len(file_ids), len(md_files)))

        # Salva gli ID
        ids_file = Path(__file__).parent.parent / ".knowledge-base-ids"
        with open(ids_file, "w") as f:
            f.write("\n".join(file_ids))

        print("✓ IDs salvati in .knowledge-base-ids")

        # Auto-link se esiste assistente
        linked = link_to_assistant(file_ids)

        if not linked:
            print("\n📋 Prossimo step:")
            print("   python scripts/update_assistant.py")
    else:
        print("\n❌ Nessun file caricato con successo")


if __name__ == "__main__":
    upload_all()
