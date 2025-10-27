#!/usr/bin/env python3
"""
Validatore dati per knowledge base.
Verifica che i dati estratti da scraping siano completi e validi.

Uso:
  python scraper/validate_data.py                    # Valida services_data_real.json
  python scraper/validate_data.py services_data.json # Valida file specifico
"""

import json
import sys
from pathlib import Path


def validate_service_data(service):
    """Valida un singolo servizio."""
    errors = []
    warnings = []

    # Campi obbligatori
    required_fields = ['service_name', 'description', 'qa_pairs']

    for field in required_fields:
        if field not in service:
            errors.append("Campo mancante: {}".format(field))
        elif service[field] is None or (
            isinstance(service[field], (str, list, dict)) and not service[field]):
            errors.append("Campo vuoto: {}".format(field))

    # Campi raccomandati
    recommended_fields = ['url', 'office_hours', 'requirements']
    for field in recommended_fields:
        if field not in service or not service[field]:
            warnings.append("Campo raccomandato mancante: {}".format(field))

    # Validazione service_name
    if 'service_name' in service:
        if len(service['service_name']) < 3:
            errors.append("service_name troppo corto")
        if len(service['service_name']) > 200:
            warnings.append("service_name molto lungo (>200 caratteri)")

    # Validazione description
    if 'description' in service:
        if len(service['description']) < 10:
            warnings.append("description troppo corta (<10 caratteri)")

    # Validazione qa_pairs
    if 'qa_pairs' in service:
        if len(service['qa_pairs']) < 3:
            warnings.append("Poche Q&A (< 3): trovate {}".format(len(service['qa_pairs'])))
        elif len(service['qa_pairs']) < 5:
            warnings.append("Q&A sotto raccomandazione (< 5): trovate {}".format(len(service['qa_pairs'])))

        for i, qa in enumerate(service['qa_pairs']):
            if 'question' not in qa or not qa['question']:
                errors.append("Q&A {}: domanda mancante".format(i+1))
            if 'answer' not in qa or not qa['answer']:
                errors.append("Q&A {}: risposta mancante".format(i+1))

            # Check lunghezza risposte
            if 'answer' in qa and len(qa['answer']) < 20:
                warnings.append("Q&A {}: risposta troppo corta".format(i+1))

    # Validazione requirements
    if 'requirements' in service:
        if isinstance(service['requirements'], list):
            if len(service['requirements']) == 0:
                warnings.append("Nessun requisito specificato")
        else:
            errors.append("requirements deve essere una lista")

    return errors, warnings


def validate_json_file(filepath):
    """Valida il file JSON dei servizi."""
    print("="*60)
    print("VALIDAZIONE: {}".format(filepath))
    print("="*60)
    print()

    # Leggi file
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print("❌ ERRORE parsing JSON: {}".format(e))
        return False, 0, 0
    except FileNotFoundError:
        print("❌ ERRORE File non trovato: {}".format(filepath))
        return False, 0, 0

    # Valida struttura
    if not isinstance(data, list):
        print("❌ ERRORE Il file deve contenere un array di servizi")
        return False, 0, 0

    print("✓ Trovati {} servizi\n".format(len(data)))

    # Valida ogni servizio
    all_errors = []
    all_warnings = []

    for i, service in enumerate(data):
        service_name = service.get('service_name', 'Unknown')
        errors, warnings = validate_service_data(service)

        if errors:
            print("❌ Servizio {} ({})".format(i+1, service_name))
            for error in errors:
                print("   ERROR: {}".format(error))
            all_errors.extend(errors)
        elif warnings:
            print("⚠️  Servizio {} ({})".format(i+1, service_name))
            for warning in warnings:
                print("   WARN: {}".format(warning))
            all_warnings.extend(warnings)
        else:
            print("✅ Servizio {} ({})".format(i+1, service_name))

    # Riepilogo
    print()
    print("="*60)
    print("RIEPILOGO")
    print("="*60)
    print("Servizi totali: {}".format(len(data)))
    print("Errori:         {}".format(len(all_errors)))
    print("Warning:        {}".format(len(all_warnings)))
    print()

    if all_errors:
        print("❌ VALIDAZIONE FALLITA")
        return False, len(all_errors), len(all_warnings)
    elif all_warnings:
        print("⚠️  VALIDAZIONE OK CON WARNING")
        return True, len(all_errors), len(all_warnings)
    else:
        print("✅ VALIDAZIONE PERFETTA")
        return True, len(all_errors), len(all_warnings)


def check_knowledge_base_files():
    """Verifica che esistano file markdown della knowledge base."""
    print("\n" + "="*60)
    print("VERIFICA FILE KNOWLEDGE BASE")
    print("="*60)
    print()

    kb_path = Path(__file__).parent.parent / 'knowledge-base'

    if not kb_path.exists():
        print("❌ Directory knowledge-base/ non trovata!")
        return False, 0

    md_files = list(kb_path.glob('*.md'))

    if not md_files:
        print("❌ Nessun file .md trovato in knowledge-base/")
        return False, 0

    print("✓ Trovati {} file Markdown\n".format(len(md_files)))

    total_size = 0
    for md_file in sorted(md_files):
        size = md_file.stat().st_size
        total_size += size

        if size == 0:
            print("❌ {} (VUOTO!)".format(md_file.name))
        elif size < 500:
            print("⚠️  {} ({} bytes - troppo piccolo?)".format(md_file.name, size))
        else:
            print("✅ {} ({} bytes)".format(md_file.name, size))

    print()
    print("Dimensione totale: {} KB".format(total_size // 1024))

    return len(md_files) > 0, len(md_files)


def main():
    """Funzione principale."""

    # File da validare
    if len(sys.argv) > 1:
        json_filename = sys.argv[1]
    else:
        # Default: usa file generato da scraping reale
        json_filename = 'services_data_real.json'

    json_path = Path(__file__).parent / json_filename

    # 1. Valida JSON
    json_valid, errors, warnings = validate_json_file(json_path)

    # 2. Valida knowledge base
    kb_valid, kb_files = check_knowledge_base_files()

    # Riepilogo finale
    print("\n" + "="*60)
    print("STATO FINALE")
    print("="*60)

    if json_valid and kb_valid:
        print("\n✅ TUTTO OK!")
        print("\nPronto per:")
        print("  python scripts/upload_knowledge_base.py")
        print("  python scripts/link_knowledge_base.py")
        return True
    elif json_valid and not kb_valid:
        print("\n⚠️  JSON OK ma Knowledge Base mancante/incompleta")
        print("\nEsegui:")
        print("  python scraper/generate_knowledge_base.py")
        return False
    else:
        print("\n❌ ERRORI TROVATI")
        print("\nCorreggi i dati prima di procedere")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
