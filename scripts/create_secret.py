#!/usr/bin/env python3
"""
Crea un secret su Vapi.ai per autenticazione sicura.
I secrets sono credenziali criptate che possono essere usate dai custom tools.
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

    print(f"\n✓ Secret ID salvato in: {secrets_file}")


def get_secret_id(name):
    """Recupera l'ID di un secret salvato."""
    secrets_file = Path(__file__).parent.parent / ".secret-ids.json"

    if not secrets_file.exists():
        return None

    with open(secrets_file, "r") as f:
        secrets = json.load(f)

    return secrets.get(name)


def create_secret(name, value):
    """
    Crea un secret su Vapi.ai.

    Args:
        name: Nome del secret (es. "mailtrap_token")
        value: Valore del secret (es. il token)

    Returns:
        dict: Informazioni sul secret creato, o None se errore
    """

    if not VAPI_API_KEY:
        print("❌ VAPI_API_KEY non trovata in .env")
        return None

    if not value:
        print(f"❌ Valore per '{name}' non trovato!")
        return None

    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }

    # Configurazione secret (Vapi richiede provider specifico)
    secret_config = {
        "provider": "custom-llm",
        "apiKey": value
    }

    print(f"\n📤 Creazione secret '{name}'...")

    response = requests.post(
        f"{VAPI_BASE_URL}/credential",
        headers=headers,
        json=secret_config
    )

    if response.status_code == 201:
        secret = response.json()
        secret_id = secret.get("id")

        print("\n" + "=" * 60)
        print("✅ SECRET CREATO CON SUCCESSO!")
        print("=" * 60)
        print(f"\nID:              {secret_id}")
        print(f"Nome:            {name}")
        print(f"Provider:        {secret.get('provider', 'custom-llm')}")
        print("=" * 60)

        # Salva ID
        save_secret_id(secret_id, name)

        return secret
    else:
        print(f"\n❌ Errore nella creazione: {response.status_code}")
        print(response.text)
        return None


def check_existing_secret(name):
    """Controlla se esiste già un secret con questo nome."""
    secret_id = get_secret_id(name)

    if secret_id:
        print("\n" + "=" * 60)
        print("⚠️  Secret già configurato!")
        print("=" * 60)
        print(f"Nome: {name}")
        print(f"ID esistente: {secret_id}")
        print()
        print("Se procedi, verrà creato un NUOVO secret.")
        print("Il vecchio ID rimarrà valido ma sarà sostituito nel file.")
        print()

        response = input("Vuoi continuare? (s/N): ").strip().lower()
        return response == "s"

    return True


def main():
    """Main."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Crea secret su Vapi.ai",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi d'uso:

  # Crea secret per Mailtrap (usa MAILTRAP_API_TOKEN da .env)
  python scripts/create_secret.py

  # Crea secret con nome custom
  python scripts/create_secret.py --name my_token --value "abc123"

  # Forza creazione senza conferma
  python scripts/create_secret.py --force

NOTA:
I secrets su Vapi.ai sono criptati e possono essere usati
nei custom tools per autenticazione sicura (es. Bearer token).
        """
    )

    parser.add_argument(
        "--name",
        type=str,
        default="mailtrap_token",
        help='Nome del secret (default: "mailtrap_token")'
    )

    parser.add_argument(
        "--value",
        type=str,
        help="Valore del secret (default: usa MAILTRAP_API_TOKEN da .env)"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Salta conferma se esiste già un secret"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("🔐 CREAZIONE SECRET VAPI.AI")
    print("=" * 60)

    # Determina valore
    value = args.value
    if not value:
        if args.name == "mailtrap_token":
            value = MAILTRAP_API_TOKEN
            if not value:
                print("\n❌ MAILTRAP_API_TOKEN non trovato in .env")
                print("Aggiungi: MAILTRAP_API_TOKEN=your_token")
                sys.exit(1)
            print(f"\n✓ Usando MAILTRAP_API_TOKEN da .env")
        else:
            print("\n❌ Devi specificare --value per secret custom")
            sys.exit(1)

    # Controlla se esiste già
    if not args.force:
        if not check_existing_secret(args.name):
            print("\nCreazione annullata.")
            sys.exit(0)

    # Crea secret
    secret = create_secret(args.name, value)

    if secret:
        print("\n📋 PROSSIMI STEP:")
        print()
        print("1. Il secret è ora disponibile per i tuoi custom tools")
        print()
        print("2. Usa questo secret nel tool:")
        print("   python scripts/upload_tool.py")
        print("   oppure")
        print("   python scripts/create_tool.py")
        print()

        sys.exit(0)
    else:
        print("\n❌ Creazione fallita!")
        sys.exit(1)


if __name__ == "__main__":
    main()
