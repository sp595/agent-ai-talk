#!/usr/bin/env python3
"""
Crea TUTTI i tool custom su Vapi.ai in una volta:
- Email tool (con autenticazione Bearer)
- Calendar check tool
- Calendar create tool

Automazioni:
- Crea credential Mailtrap se non esiste
- Linka credential al tool email
- Se esiste .assistant-id, linka automaticamente i tool all'assistente
"""

import json
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
MAILTRAP_API_TOKEN = os.getenv("MAILTRAP_API_TOKEN")
VAPI_BASE_URL = "https://api.vapi.ai"

# Configurazione dei 3 tool
TOOLS_CONFIG = {
    "email": {
        "file": "vapi-tools-config.json",
        "name": "Email Confirmation Tool",
        "use_secret": True
    },
    "calendar-check": {
        "file": "vapi-check_calendar-tools-config.json",
        "name": "Calendar Availability Check Tool",
        "use_secret": False
    },
    "calendar-create": {
        "file": "vapi-send_calendar-tools-config.json",
        "name": "Calendar Event Creation Tool",
        "use_secret": False
    }
}


def load_tool_config(config_file):
    """Carica la configurazione tool dal file JSON."""
    config_path = Path(__file__).parent.parent / "config" / config_file

    if not config_path.exists():
        print(f"❌ File {config_file} non trovato")
        return None

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Rimuovi campi che non devono essere inviati nella creazione
    config.pop("id", None)
    config.pop("orgId", None)
    config.pop("createdAt", None)
    config.pop("updatedAt", None)

    return config


def save_secret_id(secret_id, name):
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


def create_secret(name="mailtrap_token"):
    """Crea una Bearer Token credential su Vapi.ai."""

    if not MAILTRAP_API_TOKEN:
        print("\n      ❌ MAILTRAP_API_TOKEN non trovato in .env")
        print("         Aggiungi: MAILTRAP_API_TOKEN=your_token")
        return None

    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }

    # Configurazione Bearer Token credential
    secret_config = {
        "provider": "webhook",
        "authenticationPlan": {
            "type": "bearer",
            "token": MAILTRAP_API_TOKEN,
            "headerName": "Authorization",
            "bearerPrefixEnabled": True
        },
        "name": name
    }

    print(f"\n      🔄 Chiamata API Vapi per credential '{name}'...")

    try:
        response = requests.post(
            f"{VAPI_BASE_URL}/credential",
            headers=headers,
            json=secret_config,
            timeout=10
        )

        if response.status_code == 201:
            secret = response.json()
            secret_id = secret.get("id")

            print(f"      ✅ Credential creata con successo!")
            print(f"         ID: {secret_id}")

            # Salva ID
            save_secret_id(secret_id, name)
            print(f"         Salvata in .secret-ids.json")

            return secret_id
        else:
            print(f"\n      ❌ Errore API: {response.status_code}")
            print(f"         Response: {response.text}")
            return None

    except Exception as e:
        print(f"\n      ❌ Errore durante la chiamata: {str(e)}")
        return None


def ensure_secret():
    """Assicura che il secret esista, altrimenti lo crea."""
    print("\n🔐 Verifica credential Mailtrap...")

    secret_id = get_secret_id("mailtrap_token")

    if secret_id:
        print(f"   ✓ Credential esistente: {secret_id}")
        return secret_id

    print("   ⚠️  Credential non trovata")
    print("   📤 Creazione automatica...")

    new_secret_id = create_secret("mailtrap_token")

    if new_secret_id:
        print(f"   ✅ Credential creata: {new_secret_id}")
    else:
        print("   ❌ Creazione fallita!")

    return new_secret_id


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


def get_tool_ids():
    """Legge gli ID dei tool da .tool-ids."""
    tool_file = Path(__file__).parent.parent / ".tool-ids"

    if not tool_file.exists():
        return []

    with open(tool_file, "r") as f:
        tool_ids = [line.strip() for line in f.readlines() if line.strip()]

    return tool_ids


def link_to_assistant():
    """Linka i tool all'assistente se presente .assistant-id."""
    assistant_id = get_assistant_id()

    if not assistant_id:
        print("\n⏭️  .assistant-id non trovato, skip auto-linking")
        print("   Usa: python scripts/update_assistant.py")
        return False

    tool_ids = get_tool_ids()
    if not tool_ids:
        print("\n⏭️  Nessun tool da linkare")
        return False

    print(f"\n📡 Auto-linking a assistente {assistant_id}...")

    # Fetch config corrente
    current_config = get_current_config(assistant_id)
    if not current_config:
        return False

    # Prepara update solo per model.toolIds
    model_config = current_config.get("model", {})
    model_config["toolIds"] = tool_ids

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
        print(f"✅ Tools linkati! ({len(tool_ids)} tool)")
        return True
    else:
        print(f"❌ Errore nel link: {response.status_code}")
        print(response.text)
        return False


def create_single_tool(tool_key, config_file, tool_name, use_secret=False):
    """
    Crea un singolo tool su Vapi.ai.

    Args:
        tool_key: Chiave identificativa (email, calendar-check, calendar-create)
        config_file: Nome file configurazione
        tool_name: Nome descrittivo del tool
        use_secret: Se True, usa il secret per autenticazione Bearer

    Returns:
        str: Tool ID se successo, None altrimenti
    """
    print(f"\n📤 Creazione {tool_name}...")
    print("-" * 60)

    # Carica configurazione
    tool_config = load_tool_config(config_file)
    if not tool_config:
        return None

    # Se usa secret, assicurati che esista e linkalo
    if use_secret:
        secret_id = ensure_secret()
        if secret_id:
            tool_config["credentialId"] = secret_id
            print(f"✓ Credential collegata: {secret_id}")
        else:
            print("❌ Impossibile creare/trovare credential")
            print("   Tool creato SENZA autenticazione!")
            print("   Aggiungi MAILTRAP_API_TOKEN in .env e ricrea il tool")

    # Dettagli tool
    func_name = tool_config.get('function', {}).get('name', 'N/A')
    print(f"Nome funzione: {func_name}")

    if tool_key == "email":
        print(f"URL: {tool_config.get('url', 'N/A')}")
    else:
        cal_id = tool_config.get('metadata', {}).get('calendarId', 'N/A')
        print(f"Calendar ID: {cal_id[:20]}..." if len(cal_id) > 20 else cal_id)

    # Crea tool
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        f"{VAPI_BASE_URL}/tool",
        headers=headers,
        json=tool_config
    )

    if response.status_code == 201:
        tool_data = response.json()
        tool_id = tool_data.get("id")

        print(f"✅ Tool creato: {tool_id}")

        # Salva ID (append)
        ids_file = Path(__file__).parent.parent / ".tool-ids"

        existing_ids = []
        if ids_file.exists():
            with open(ids_file, "r") as f:
                existing_ids = [line.strip() for line in f.readlines() if line.strip()]

        if tool_id not in existing_ids:
            existing_ids.append(tool_id)

        with open(ids_file, "w") as f:
            f.write("\n".join(existing_ids))

        return tool_id
    else:
        print(f"❌ Errore: {response.status_code}")
        print(response.text)
        return None


def create_all_tools():
    """Crea tutti e 3 i tool in una volta."""
    if not VAPI_API_KEY:
        print("❌ VAPI_API_KEY non trovata in .env")
        return False

    print("=" * 60)
    print("CREAZIONE TOOLS SU VAPI.AI")
    print("=" * 60)
    print()

    # Verifica variabili ambiente
    print("📋 Verifica configurazione:")
    print(f"   VAPI_API_KEY: {'✓ presente' if VAPI_API_KEY else '❌ mancante'}")
    print(f"   MAILTRAP_API_TOKEN: {'✓ presente' if MAILTRAP_API_TOKEN else '❌ mancante'}")
    print()

    results = {}

    # Crea tutti i tool
    for tool_key, config in TOOLS_CONFIG.items():
        tool_id = create_single_tool(
            tool_key,
            config["file"],
            config["name"],
            config["use_secret"]
        )
        results[tool_key] = tool_id

    # Riepilogo
    print("\n" + "=" * 60)
    print("RIEPILOGO")
    print("=" * 60)

    success_count = 0
    for tool_key, tool_id in results.items():
        status = "✅" if tool_id else "❌"
        tool_name = TOOLS_CONFIG[tool_key]["name"]
        print(f"{status} {tool_name}")
        if tool_id:
            print(f"   ID: {tool_id}")
            success_count += 1

    print(f"\n{success_count}/{len(TOOLS_CONFIG)} tool creati con successo")

    if success_count > 0:
        # Auto-link se esiste assistente
        linked = link_to_assistant()

        if success_count == len(TOOLS_CONFIG):
            print("\n✅ Tutti i tool sono stati creati!")
        else:
            print("\n⚠️  Alcuni tool sono stati creati")

        if not linked:
            print("\n📋 Prossimo step:")
            print("   python scripts/update_assistant.py")

        return True
    else:
        print("\n❌ Nessun tool creato")
        return False


def main():
    """Main - Crea tutti e 3 i tool."""
    print("🛠️  CREATE TOOLS")
    print()
    print("Questo script crea TUTTI e 3 i tool:")
    print("  1. Email tool (crea credential Mailtrap se necessario)")
    print("  2. Calendar check tool")
    print("  3. Calendar create tool")
    print()
    print("⚙️  Verifica automatica credential Mailtrap...")
    print()

    response = input("Vuoi procedere? [S/n] ")
    if response.lower() not in ["", "s", "y", "si", "yes"]:
        print("Operazione annullata.")
        sys.exit(0)

    success = create_all_tools()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
