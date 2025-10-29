#!/usr/bin/env python3
"""
Script per gestire secrets e tool Mailtrap in VAPI
Combina creazione secret + creazione/aggiornamento tool
"""
import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
MAILTRAP_API_TOKEN = os.getenv("MAILTRAP_API_TOKEN")
VAPI_BASE_URL = "https://api.vapi.ai"


def save_secret_id(secret_id, name="mailtrap_token"):
    """Salva l'ID del secret in .secret-ids.json."""
    secrets_file = Path(__file__).parent.parent / ".secret-ids.json"

    secrets = {}
    if secrets_file.exists():
        with open(secrets_file, "r") as f:
            secrets = json.load(f)

    secrets[name] = secret_id

    with open(secrets_file, "w") as f:
        json.dump(secrets, f, indent=2)

    return secrets_file


def get_secret_id(name="mailtrap_token"):
    """Recupera l'ID del secret salvato."""
    secrets_file = Path(__file__).parent.parent / ".secret-ids.json"

    if not secrets_file.exists():
        return None

    with open(secrets_file, "r") as f:
        secrets = json.load(f)

    return secrets.get(name)


def create_secret(name="mailtrap_token", value=None):
    """Crea un secret su Vapi.ai per il Mailtrap API token."""
    if not value:
        value = MAILTRAP_API_TOKEN

    if not value:
        print("❌ MAILTRAP_API_TOKEN non trovato in .env")
        return None

    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }

    secret_config = {
        "provider": "custom-llm",
        "apiKey": value
    }

    print(f"📤 Creazione secret '{name}'...")

    response = requests.post(
        f"{VAPI_BASE_URL}/credential",
        headers=headers,
        json=secret_config
    )

    if response.status_code == 201:
        secret = response.json()
        secret_id = secret.get("id")

        print(f"✅ Secret creato: {secret_id}")

        # Salva ID
        secrets_file = save_secret_id(secret_id, name)
        print(f"   ID salvato in: {secrets_file}")

        return secret_id
    else:
        print(f"❌ Errore nella creazione secret: {response.status_code}")
        print(response.text)
        return None


def ensure_secret():
    """Assicura che il secret esista, altrimenti lo crea."""
    secret_id = get_secret_id("mailtrap_token")

    if secret_id:
        print(f"✓ Secret esistente trovato: {secret_id}")
        return secret_id

    print("✗ Secret non trovato, creazione in corso...")
    return create_secret("mailtrap_token")


def load_tool_config():
    """Carica la configurazione tool dal file JSON."""
    config_path = Path(__file__).parent.parent / "config" / "vapi-tools-config.json"

    if not config_path.exists():
        print("❌ ERRORE: config/vapi-tools-config.json non trovato")
        return None

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_existing_tools():
    """Ottiene la lista di tutti i tool esistenti in VAPI."""
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json",
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
        if tool.get("name") == name or tool.get("function", {}).get("name") == name:
            return tool.get("id")
    return None


def create_tool(tool_config, secret_id=None):
    """Crea un nuovo tool in VAPI."""
    # Aggiungi credentialId se fornito
    if secret_id:
        tool_config["credentialId"] = secret_id
        print(f"✓ Credenziale Mailtrap collegata: {secret_id}")

    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json",
    }

    print("📤 Creazione nuovo tool...")
    print("\n" + "=" * 60)
    print("CONFIGURAZIONE:")
    print(json.dumps(tool_config, indent=2, ensure_ascii=False))
    print("=" * 60 + "\n")

    try:
        response = requests.post(
            f"{VAPI_BASE_URL}/tool", json=tool_config, headers=headers
        )

        print(f"Status Code: {response.status_code}")

        if response.status_code == 201:
            result = response.json()
            print("\n✅ Tool creato con successo!")
            print(f"Tool ID: {result.get('id')}")

            # Salva ID in un file
            ids_file = Path(__file__).parent.parent / ".tool-ids"

            # Leggi IDs esistenti
            existing_ids = []
            if ids_file.exists():
                with open(ids_file, "r") as f:
                    existing_ids = [line.strip() for line in f.readlines() if line.strip()]

            # Aggiungi nuovo ID se non già presente
            tool_id = result.get("id")
            if tool_id not in existing_ids:
                existing_ids.append(tool_id)

            # Scrivi tutti gli IDs
            with open(ids_file, "w") as f:
                f.write("\n".join(existing_ids))

            print("ID salvato in .tool-ids")

            if secret_id:
                print("\n✅ Tool configurato con autenticazione Bearer!")
            else:
                print("\n⚠️  Tool creato senza autenticazione")

            return tool_id
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
        "Content-Type": "application/json",
    }

    # Rimuovi il campo "type" per l'update (non è modificabile)
    update_config = {k: v for k, v in tool_config.items() if k != "type"}

    print(f"🔄 Aggiornamento tool (ID: {tool_id})...")
    print("\n" + "=" * 60)
    print("CONFIGURAZIONE:")
    print(json.dumps(update_config, indent=2, ensure_ascii=False))
    print("=" * 60 + "\n")

    try:
        response = requests.patch(
            f"{VAPI_BASE_URL}/tool/{tool_id}", json=update_config, headers=headers
        )

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
        description="Gestisce secrets e tool Mailtrap in VAPI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi d'uso:

  # Crea secret + tool automaticamente (raccomandato)
  python scripts/upload_tool.py

  # Forza creazione nuovo tool
  python scripts/upload_tool.py --create

  # Aggiorna tool specifico
  python scripts/upload_tool.py --update TOOL_ID

Note:
  - Crea automaticamente il secret Mailtrap se non esiste
  - Collega il secret al tool per autenticazione Bearer
  - La configurazione viene letta da config/vapi-tools-config.json
        """,
    )

    parser.add_argument(
        "--create", action="store_true", help="Forza la creazione di un nuovo tool"
    )

    parser.add_argument(
        "--update",
        type=str,
        metavar="TOOL_ID",
        help="Aggiorna un tool esistente specificando il suo ID",
    )

    args = parser.parse_args()

    if not VAPI_API_KEY:
        print("❌ ERRORE: VAPI_API_KEY non trovato nel file .env")
        sys.exit(1)

    print("🛠️  GESTIONE TOOL MAILTRAP IN VAPI")
    print("=" * 60)
    print()

    # Step 1: Assicura che il secret esista
    print("STEP 1: Verifica Secret Mailtrap")
    print("-" * 60)
    secret_id = ensure_secret()
    if not secret_id:
        print("❌ Impossibile creare/trovare il secret")
        sys.exit(1)
    print()

    # Step 2: Carica configurazione tool
    print("STEP 2: Caricamento Configurazione Tool")
    print("-" * 60)
    tool_config = load_tool_config()
    if not tool_config:
        sys.exit(1)

    tool_name = tool_config.get("function", {}).get("name", tool_config.get("name"))
    print(f"✓ Tool: {tool_name}")
    print()

    # Step 3: Crea o aggiorna tool
    print("STEP 3: Creazione/Aggiornamento Tool")
    print("-" * 60)

    if args.create:
        # Forza creazione
        tool_id = create_tool(tool_config, secret_id)
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
            if response.lower() in ["", "s", "y", "si", "yes"]:
                success = update_tool(existing_tool_id, tool_config)
                sys.exit(0 if success else 1)
            else:
                print("Operazione annullata.")
                sys.exit(0)
        else:
            print("✗ Nessun tool esistente trovato.")
            response = input("Vuoi creare un nuovo tool? [S/n] ")
            if response.lower() in ["", "s", "y", "si", "yes"]:
                tool_id = create_tool(tool_config, secret_id)
                sys.exit(0 if tool_id else 1)
            else:
                print("Operazione annullata.")
                sys.exit(0)


if __name__ == "__main__":
    main()
