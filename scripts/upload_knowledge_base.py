#!/usr/bin/env python3
"""
Carica i file della knowledge base su Vapi.ai.
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
        print("\nOK Caricati {}/{} file".format(len(file_ids), len(md_files)))

        # Salva gli ID
        ids_file = Path(__file__).parent.parent / ".knowledge-base-ids"
        with open(ids_file, "w") as f:
            f.write("\n".join(file_ids))

        print("IDs salvati in .knowledge-base-ids")
        print("\nProssimo step:")
        print("  python scripts/link_knowledge_base.py")
    else:
        print("\nERRORE: Nessun file caricato con successo")


if __name__ == "__main__":
    upload_all()
