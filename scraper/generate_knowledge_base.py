#!/usr/bin/env python3
"""
Genera file Markdown per knowledge base da services_data_real.json.
Crea un file .md per ogni servizio in knowledge-base/
"""

import json
from pathlib import Path
import re

def slugify(text):
    """Converte testo in slug per filename."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def generate_markdown(service):
    """Genera contenuto Markdown per un servizio."""

    title = service['service_name']
    description = service.get('description', '')
    url = service.get('url', '')
    office_hours = service.get('office_hours', 'Non specificato')
    requirements = service.get('requirements', [])
    qa_pairs = service.get('qa_pairs', [])
    cost = service.get('cost', '')

    # Template Markdown ottimizzato per Vapi RAG
    markdown = f"""# {title}

## Descrizione

{description}

## Informazioni Generali

**Orari di apertura**: {office_hours}

"""

    if cost:
        markdown += f"**Costo**: {cost}\n\n"

    if url:
        markdown += f"**Link**: {url}\n\n"

    # Documenti necessari
    if requirements:
        markdown += "## Documenti Necessari\n\n"
        for req in requirements[:10]:  # Max 10
            markdown += f"- {req}\n"
        markdown += "\n"

    # Procedura (generico)
    markdown += """## Procedura

1. Prenota un appuntamento chiamando il numero 0432 905511 o tramite l'assistente virtuale
2. Presenta i documenti necessari presso l'ufficio comunale
3. Attendi l'erogazione del servizio secondo i tempi previsti

"""

    # FAQ
    if qa_pairs:
        markdown += "## Domande Frequenti (FAQ)\n\n"
        for idx, qa in enumerate(qa_pairs, 1):
            question = qa['question']
            answer = qa['answer']
            markdown += f"### {question}\n\n{answer}\n\n"

    # Footer
    markdown += """---

*Per maggiori informazioni o per prenotare un appuntamento, contatta:*
- **Telefono**: 0432 905511
- **Email**: [protocollo@comune.codroipo.ud.it](mailto:protocollo@comune.codroipo.ud.it)
- **Sito web**: [www.comune.codroipo.ud.it](https://www.comune.codroipo.ud.it)
"""

    return markdown

def generate_all_knowledge_base():
    """Genera tutti i file knowledge base."""

    # Leggi dati estratti
    json_path = Path(__file__).parent / 'services_data_real.json'

    if not json_path.exists():
        print("❌ File services_data_real.json non trovato!")
        print("\nEsegui prima:")
        print("  python scraper/scrape_real.py")
        return False

    with open(json_path, 'r', encoding='utf-8') as f:
        services = json.load(f)

    print("="*60)
    print("GENERAZIONE KNOWLEDGE BASE")
    print("="*60)
    print()
    print(f"Servizi da processare: {len(services)}")
    print()

    # Crea directory knowledge-base se non esiste
    kb_dir = Path(__file__).parent.parent / 'knowledge-base'
    kb_dir.mkdir(exist_ok=True)

    # Pulisci vecchi file (opzionale)
    cleanup = input("Vuoi pulire i file esistenti in knowledge-base/? [s/N]: ").lower()
    if cleanup == 's':
        for old_file in kb_dir.glob('*.md'):
            old_file.unlink()
            print(f"✓ Rimosso: {old_file.name}")
        print()

    # Genera file per ogni servizio
    generated = 0
    for service in services:
        title = service['service_name']
        slug = slugify(title)

        # Nome file
        filename = f"{slug}.md"
        filepath = kb_dir / filename

        # Genera markdown
        markdown_content = generate_markdown(service)

        # Salva file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"✓ Creato: {filename}")
        generated += 1

    print()
    print("="*60)
    print("KNOWLEDGE BASE GENERATA!")
    print("="*60)
    print(f"\n✓ {generated} file Markdown creati in knowledge-base/")
    print("\nProssimo step:")
    print("  python scripts/upload_knowledge_base.py")
    print("  python scripts/link_knowledge_base.py")

    return True

if __name__ == "__main__":
    import sys
    success = generate_all_knowledge_base()
    sys.exit(0 if success else 1)
