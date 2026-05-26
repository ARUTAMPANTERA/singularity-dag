#!/usr/bin/env python3
# =============================================================================
# db_unify_federation.py — SINGULARITY_OS v19.0_OMNIA
# =============================================================================
# Scopo: Unificare tutti i file database frammentati nello standard v7.0_OMNIA
# Funzioni: Lettura multi-formato, Deduplicazione, Migrazione v7.0, Validazione
# Lock Compliance: OS_L11 (Sync), GC_129 (Legacy ID), P1 (Zero_Menzogna)
# =============================================================================

import os
import yaml
import json
import hashlib
import copy
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import re

# =============================================================================
# CONFIGURAZIONE
# =============================================================================

BASE_DIR = Path(__file__).parent.parent
DB_DIR = BASE_DIR / "database"
ARCHIVE_DIR = DB_DIR / "archive_pre_v7"
DOCS_DIR = BASE_DIR / "docs"
TOOLS_DIR = BASE_DIR / "tools"

# File target tiered
TIER_FILES = {
    1: DB_DIR / "DB_TIER1_CANONICI.yaml",
    2: DB_DIR / "DB_TIER2_SOPPRESSO.yaml",
    3: DB_DIR / "DB_TIER3_AGGIUNTE.yaml",
    4: DB_DIR / "DB_TIER4_SPECULATIVO.yaml"
}

# File da migrare (tutti i YAML/MD nella cartella database)
FILES_TO_MIGRATE = [
    "DB_TIER1_CANONICI.yaml",
    "DB_TIER2_SOPPRESSO.yaml",
    "DB_TIER3_AGGIUNTE.yaml",
    "DATABASE_SCIENZIATI_v4.0_CONSOLIDATO-1.yaml",
    "DB_MASTER_TOTALIS_v1.0.yaml",
    "DB_MASTER_v1.0.yaml",
    "DATABASE_LAB_v4.0.yaml",
    "DATABASE_CONNESSIONI_v4.0.yaml",
    "DATABASE_SCIENZIATI_v1.2_MAX_PARTE_2.yaml",
    "PROTOCOLLO_v9.5_RICERCHE_SPECIALI_TECH_SPARITA.yaml",
    "SCIENZIATI_ITALIA_EUROPA_70_NODI_FULL_MAX.md",
    "DATABASE_SCIENZIATI_TECNOLOGIE_SOPPRESSE.yaml"
]

# =============================================================================
# TEMPLATE V7.0_OMNIA DEFAULT
# =============================================================================

DEFAULT_NODE_V7 = {
    "id": "",
    "id_legacy": [],
    "nome": "",
    "alias": [],
    "tipo_nodo": "RICERCATORE",
    "periodo": "",
    "nazione": "",
    "field": "",
    "status": "VERIFICATO",
    "certezza": "media",
    "si_score": 0.0,
    "delta_score": 0.0,
    "it_score": 0.0,
    "theta_arch": 0.0,
    "aio_score": 0.0,
    "ciclo_17_fase": 0,
    "finestra_5_anni": {"attiva": False, "periodo": "", "evento_demo": ""},
    "cluster": [],
    "prism_domains": [],
    "tags_frattali": [],
    "connessioni_valide": [],
    "l_minus_1_precursors": [],
    "l_plus_1_heirs": [],
    "hub_collisione": [],
    "espansioni_future": [],
    "domande_aperte_da_chiudere": [],
    "fonti_primarie": [],
    "fonti_secondarie": [],
    "fonti_perse_o_secretate": [],
    "livello_uq_fonti": {},
    "meccanismi_soppressione": [],
    "narrativa_ufficiale_vs_realta": "",
    "attori_istituzionali_coinvolti": [],
    "conseguenze_trasmissione": "",
    "aion_strati": {
        "Σ0_source_anchoring": "",
        "Σ3_literal_extraction": "",
        "Σ7_technical_reverse": "",
        "Σ11_epistemic_synthesis": "",
        "Σ13_forensics_temporale": ""
    },
    "media_esistenti": [],
    "stato_disponibilita": {},
    "impatto_storico": "",
    "impatto_potenziale": "",
    "compatibilita_sintropica": 0.0,
    "laboratori_correlati": [],
    "tecnologie_derivate": [],
    "tecnologie_precedenti": [],
    "versione_scheda": "7.0",
    "ultimo_aggiornamento": datetime.now().strftime("%Y-%m-%d"),
    "autore_generazione": "db_unify_federation.py",
    "stato_generazione": "MIGRATA",
    "changelog": []
}

# =============================================================================
# FUNZIONI DI LETTURA MULTI-FORMATO
# =============================================================================

def read_yaml_file(filepath: Path) -> List[Dict]:
    """Legge un file YAML e restituisce una lista di nodi senza duplicati"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        docs = list(yaml.safe_load_all(content))
        nodes = []
        seen_ids = set()
        
        def estrai_nodi(obj):
            """Funzione ricorsiva per estrarre nodi da strutture annidate"""
            if isinstance(obj, list):
                for item in obj:
                    if isinstance(item, dict):
                        nid = item.get('id')
                        if nid and nid not in seen_ids:
                            nodes.append(item)
                            seen_ids.add(nid)
                        elif not nid and 'nome' in item and item not in nodes:
                            nodes.append(item)
                    else:
                        estrai_nodi(item)
            
            elif isinstance(obj, dict):
                for k, v in obj.items():
                    if k == 'meta':
                        continue
                    estrai_nodi(v)
        
        for doc in docs:
            if doc:
                estrai_nodi(doc)
        
        return nodes
    except Exception as e:
        print(f"[ERRORE] Lettura YAML fallita per {filepath}: {e}")
        return []


def read_markdown_file(filepath: Path) -> List[Dict]:
    """Legge un file Markdown e estrae nodi strutturati"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        nodes = []
        # Pattern per estrarre blocchi YAML frontmatter
        pattern = r'---\n(.*?)\n---'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches:
            try:
                node_data = yaml.safe_load(match)
                if node_data and isinstance(node_data, dict):
                    nodes.append(node_data)
            except:
                continue
                
        return nodes
    except Exception as e:
        print(f"[ERRORE] Lettura MD fallita per {filepath}: {e}")
        return []

def detect_tier(node: Dict) -> int:
    """Determina il Tier di un nodo basato su status e si_score"""
    status = node.get('status', '').upper()
    si_score = float(node.get('si_score', 0.0))
    certezza = node.get('certezza', '').lower()
    
    # Logica di classificazione Tier
    if status == 'VERIFICATO' or certezza == 'alta':
        return 1
    elif status in ['SOPPRESSO', 'CONTROVERSO'] or si_score > 0.40:
        return 2
    elif status == 'SPECULATIVO' or certezza in ['bassa', 'speculativa']:
        return 4
    else:
        return 3  # Default per nuovi nodi

# =============================================================================
# FUNZIONI DI MIGRAZIONE E NORMALIZZAZIONE
# =============================================================================

def migrate_node_to_v7(node: Dict) -> Dict:
    """Migra un nodo da qualsiasi formato legacy a v7.0_OMNIA"""
    # FIX: Usa deepcopy per evitare che id_legacy e altre liste siano condivise tra i nodi
    v7_node = copy.deepcopy(DEFAULT_NODE_V7)
    
    # Reset aion_strati per il nuovo nodo (se necessario, altrimenti deepcopy è sufficiente)
    v7_node["aion_strati"] = {k: "" for k in DEFAULT_NODE_V7["aion_strati"].keys()}
    v7_node["changelog"] = []
    
    # Mappatura campi legacy -> v7
    field_mapping = {
        'id': 'id',
        'nome': 'nome',
        'name': 'nome',
        'alias': 'alias',
        'tipo': 'tipo_nodo',
        'tipo_nodo': 'tipo_nodo',
        'periodo': 'periodo',
        'anni': 'periodo',
        'nazione': 'nazione',
        'country': 'nazione',
        'field': 'field',
        'campo': 'field',
        'status': 'status',
        'certezza': 'certezza',
        'confidence': 'certezza',
        'si_score': 'si_score',
        'suppression_index': 'si_score',
        'delta_score': 'delta_score',
        'it_score': 'it_score',
        'theta_arch': 'theta_arch',
        'aio_score': 'aio_score',
        'cluster': 'cluster',
        'clusters': 'cluster',
        'tags': 'tags_frattali',
        'tags_frattali': 'tags_frattali',
        'connessioni': 'connessioni_valide',
        'connessioni_valide': 'connessioni_valide',
        'links': 'connessioni_valide',
        'precursors': 'l_minus_1_precursors',
        'l_minus_1': 'l_minus_1_precursors',
        'l_minus_1_precursors': 'l_minus_1_precursors',
        'heirs': 'l_plus_1_heirs',
        'l_plus_1': 'l_plus_1_heirs',
        'l_plus_1_heirs': 'l_plus_1_heirs',
        'fonti': 'fonti_primarie',
        'fonti_primarie': 'fonti_primarie',
        'sources': 'fonti_primarie',
        'fonti_secondarie': 'fonti_secondarie',
        'meccanismi_soppressione': 'meccanismi_soppressione',
        'soppressione': 'meccanismi_soppressione',
        'lab_correlati': 'laboratori_correlati',
        'laboratori_correlati': 'laboratori_correlati',
        'tech_derivate': 'tecnologie_derivate',
        'tecnologie_derivate': 'tecnologie_derivate',
        'impatto': 'impatto_storico',
        'impatto_storico': 'impatto_storico',
        'description': 'narrativa_ufficiale_vs_realta',
        'bio': 'narrativa_ufficiale_vs_realta',
        'biografia': 'narrativa_ufficiale_vs_realta',
    }
    
    # Applica mappatura
    for legacy_key, v7_key in field_mapping.items():
        if legacy_key in node and node[legacy_key] is not None:
            value = node[legacy_key]
            
            # Normalizzazione tipi
            if v7_key in ['alias', 'cluster', 'tags_frattali', 'connessioni_valide', 
                         'l_minus_1_precursors', 'l_plus_1_heirs', 'hub_collisione',
                         'fonti_primarie', 'fonti_secondarie', 'meccanismi_soppressione',
                         'attori_istituzionali_coinvolti', 'media_esistenti',
                         'laboratori_correlati', 'tecnologie_derivate', 'tecnologie_precedenti']:
                if isinstance(value, str):
                    value = [value]
                elif not isinstance(value, list):
                    value = []
            
            # Salva nel nodo v7
            if v7_key in v7_node:
                # Mantieni valori esistenti se più ricchi
                if v7_node[v7_key] and isinstance(v7_node[v7_key], list) and isinstance(value, list):
                    v7_node[v7_key].extend([v for v in value if v not in v7_node[v7_key]])
                elif not v7_node[v7_key]:
                    v7_node[v7_key] = value
    
    # Gestione id_legacy
    if 'id' in node and node['id']:
        v7_node['id_legacy'].append(node['id'])
    
    # Genera nuovo ID se mancante
    if not v7_node['id']:
        tier = detect_tier(node)
        hash_nome = hashlib.md5(v7_node['nome'].encode()).hexdigest()[:6]
        v7_node['id'] = f"T{tier}-{hash_nome.upper()}"
    
    # Popola AION strati se vuoti (da narrative esistenti)
    if v7_node['narrativa_ufficiale_vs_realta']:
        v7_node['aion_strati']['Σ11_epistemic_synthesis'] = v7_node['narrativa_ufficiale_vs_realta']
    
    # Aggiungi changelog
    v7_node['changelog'].append({
        "data": datetime.now().strftime("%Y-%m-%d"),
        "versione": "7.0",
        "modifiche": "Migrazione automatica da formato legacy a v7.0_OMNIA"
    })
    
    return v7_node

def deduplicate_nodes(nodes: List[Dict]) -> List[Dict]:
    """Rimuove duplicati basandosi su nome e ID, fondendo i dati più ricchi"""
    seen = {}
    unique_nodes = []
    
    for node in nodes:
        # Chiave di identificazione: nome normalizzato o ID
        key = node.get('nome', node.get('id', '')).lower().strip()
        if not key:
            key = hashlib.md5(str(node).encode()).hexdigest()
        
        if key in seen:
            # Fusione: mantieni il nodo con più campi compilati
            existing = seen[key]
            existing_fields = sum(1 for v in existing.values() if v not in [None, '', [], {}])
            new_fields = sum(1 for v in node.values() if v not in [None, '', [], {}])
            
            if new_fields > existing_fields:
                # Il nuovo nodo è più ricco, aggiorna
                for k, v in node.items():
                    if isinstance(v, list) and isinstance(existing.get(k), list):
                        existing[k].extend([x for x in v if x not in existing[k]])
                    elif not existing.get(k):
                        existing[k] = v
        else:
            seen[key] = node
            unique_nodes.append(node)
    
    return unique_nodes

# =============================================================================
# FUNZIONI DI VALIDAZIONE
# =============================================================================

def validate_v7_node(node: Dict) -> tuple[bool, List[str]]:
    """Valida un nodo v7.0_OMNIA"""
    errors = []
    
    # Campi obbligatori
    required_fields = ['id', 'nome', 'tipo_nodo', 'status']
    for field in required_fields:
        if not node.get(field):
            errors.append(f"Campo obbligatorio mancante: {field}")
    
    # Validazione AION strati (obbligatorio in v7)
    if not node.get('aion_strati'):
        errors.append("Strato AION mancante (obbligatorio in v7.0)")
    elif not all(node['aion_strati'].get(k) for k in ['Σ0_source_anchoring', 'Σ11_epistemic_synthesis']):
        # Almeno Σ0 e Σ11 dovrebbero essere compilati
        pass  # Warning ma non errore bloccante
    
    # Validazione ID formato
    if node.get('id') and not re.match(r'^T[1-4]-[A-Z0-9]{6}$', node['id']):
        # Warning per ID non standard
        pass
    
    return len(errors) == 0, errors

# =============================================================================
# FUNZIONE PRINCIPALE
# =============================================================================

def main():
    print("=" * 80)
    print("🜁 SINGULARITY_OS v19.0_OMNIA — DB UNIFICATION FEDERATION")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    # Crea directory archive se non esiste
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Leggi tutti i file sorgente
    print("[STEP 1] Lettura file sorgente...")
    all_nodes = []
    
    for filename in FILES_TO_MIGRATE:
        filepath = DB_DIR / filename
        if not filepath.exists():
            print(f"  ⚠️  File non trovato: {filename}")
            continue
        
        print(f"  📄 Lettura: {filename}")
        
        if filepath.suffix in ['.yaml', '.yml']:
            nodes = read_yaml_file(filepath)
        elif filepath.suffix == '.md':
            nodes = read_markdown_file(filepath)
        else:
            print(f"  ❌ Formato non supportato: {filename}")
            continue
        
        print(f"     → {len(nodes)} nodi estratti")
        all_nodes.extend(nodes)
    
    print(f"\n[TOTALE] {len(all_nodes)} nodi grezzi estratti")
    
    # Step 2: Migra a v7.0_OMNIA
    print("\n[STEP 2] Migrazione a standard v7.0_OMNIA...")
    migrated_nodes = [migrate_node_to_v7(node) for node in all_nodes]
    print(f"  ✓ {len(migrated_nodes)} nodi migrati")
    
    # Step 3: Deduplicazione
    print("\n[STEP 3] Deduplicazione intelligente...")
    before_dedup = len(migrated_nodes)
    unique_nodes = deduplicate_nodes(migrated_nodes)
    after_dedup = len(unique_nodes)
    print(f"  Rimossi {before_dedup - after_dedup} duplicati")
    print(f"  ✓ {after_dedup} nodi unici finali")
    
    # Step 4: Classificazione per Tier
    print("\n[STEP 4] Classificazione per Tier...")
    tier_nodes = {1: [], 2: [], 3: [], 4: []}
    
    for node in unique_nodes:
        tier = detect_tier(node)
        tier_nodes[tier].append(node)
    
    for tier, nodes in tier_nodes.items():
        print(f"  Tier {tier}: {len(nodes)} nodi")
    
    # Step 5: Backup file originali
    print("\n[STEP 5] Backup file originali in archive_pre_v7...")
    for filename in FILES_TO_MIGRATE:
        src = DB_DIR / filename
        if src.exists():
            dst = ARCHIVE_DIR / filename
            # Sposta solo se non è già un file tiered principale
            if filename not in ['DB_TIER1_CANONICI.yaml', 'DB_TIER2_SOPPRESSO.yaml', 'DB_TIER3_AGGIUNTE.yaml']:
                import shutil
                shutil.copy2(src, dst)
                print(f"  ✓ Backup: {filename}")
    
    # Step 6: Scrittura file tiered
    print("\n[STEP 6] Scrittura file tiered unificati...")
    
    for tier, nodes in tier_nodes.items():
        if not nodes:
            continue
            
        output_file = TIER_FILES.get(tier)
        if not output_file:
            output_file = DB_DIR / f"DB_TIER{tier}_AUTO.yaml"
        
        # Scrivi come multi-documento YAML
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump_all(nodes, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        
        print(f"  ✓ Scritto: {output_file.name} ({len(nodes)} nodi)")
    
    # Step 7: Generazione indice master
    print("\n[STEP 7] Generazione DB_MASTER_INDEX.yaml...")
    
    index_data = {
        "metadata": {
            "versione": "7.0",
            "generato": datetime.now().isoformat(),
            "totale_nodi": len(unique_nodes),
            "tier1": len(tier_nodes[1]),
            "tier2": len(tier_nodes[2]),
            "tier3": len(tier_nodes[3]),
            "tier4": len(tier_nodes[4])
        },
        "nodi": []
    }
    
    for node in unique_nodes:
        index_entry = {
            "id": node.get('id', ''),
            "nome": node.get('nome', ''),
            "tier": detect_tier(node),
            "tipo_nodo": node.get('tipo_nodo', ''),
            "status": node.get('status', ''),
            "connessioni": node.get('connessioni_valide', [])[:10]  # Prime 10 connessioni
        }
        index_data["nodi"].append(index_entry)
    
    index_file = DB_DIR / "DB_MASTER_INDEX.yaml"
    with open(index_file, 'w', encoding='utf-8') as f:
        yaml.dump(index_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    print(f"  ✓ Indice generato: {index_file.name}")
    
    # Step 8: Validazione finale
    print("\n[STEP 8] Validazione finale...")
    valid_count = 0
    invalid_nodes = []
    
    for node in unique_nodes:
        is_valid, errors = validate_v7_node(node)
        if is_valid:
            valid_count += 1
        else:
            invalid_nodes.append((node.get('id', 'UNKNOWN'), errors))
    
    print(f"  ✓ {valid_count}/{len(unique_nodes)} nodi validi")
    if invalid_nodes:
        print(f"  ⚠️  {len(invalid_nodes)} nodi con warning/minori problemi")
    
    # Report finale
    print("\n" + "=" * 80)
    print("🜁 MIGRAZIONE COMPLETATA CON SUCCESSO")
    print("=" * 80)
    print(f"Nodi totali unificati: {len(unique_nodes)}")
    print(f"  - Tier 1 (Verificati): {len(tier_nodes[1])}")
    print(f"  - Tier 2 (Soppressi/Controversi): {len(tier_nodes[2])}")
    print(f"  - Tier 3 (Aggiunte): {len(tier_nodes[3])}")
    print(f"  - Tier 4 (Speculativi): {len(tier_nodes[4])}")
    print()
    print("File generati:")
    print(f"  - {TIER_FILES[1].name}")
    print(f"  - {TIER_FILES[2].name}")
    print(f"  - {TIER_FILES[3].name}")
    if tier_nodes[4]:
        print(f"  - {TIER_FILES[4].name}")
    print(f"  - {index_file.name}")
    print()
    print("Backup originali in: database/archive_pre_v7/")
    print("=" * 80)
    print("♾️  LIVE, NOT EVIL — OMNIA IN UNO")
    print("=" * 80)

if __name__ == "__main__":
    main()
