#!/usr/bin/env python3
"""
validate_artifact.py
Validatore minimale per artefatti DAG schema v2.0.
Uso: python3 validate_artifact.py <input_json_path> [--output <output_json_path>]

Output: genera un report di validazione JSON nel percorso di output (default: artifacts/DAG_VALIDATION_REPORT_001.json)
Il report contiene i risultati della validazione e una copia dei metadati richiesti dallo schema.
"""
import sys
import json
import hashlib
import datetime
from typing import Any, Dict, List

# Enumerazione consentita per node_role (schema v2.0 - valori noti dal kernel)
ALLOWED_NODE_ROLES = {"GIAGUARO", "LINGUA_SACRA", "ARCHITETTO", "GUARDIANO", "TATTICO", "UNKNOWN"}


def is_iso8601(s: str) -> bool:
    try:
        # datetime.fromisoformat supports most ISO8601 forms in recent Python
        datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
        return True
    except Exception:
        return False


def compute_sha256_of_json(obj: Any) -> str:
    canonical = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    h = hashlib.sha256()
    h.update(canonical.encode("utf-8"))
    return h.hexdigest()


def validate_artifact(obj: Dict[str, Any]) -> List[str]:
    errs: List[str] = []

    # Required top-level fields
    required = [
        "artifact_id",
        "content_hash",
        "parent_ids",
        "operation",
        "input",
        "output_summary",
        "majorana_angle",
        "uq",
        "nd",
        "timestamp_utc",
        "provenance",
        "node_role",
        "signature"
    ]

    for key in required:
        if key not in obj:
            errs.append(f"Campo mancante: {key}")

    if errs:
        return errs

    # artifact_id
    if not isinstance(obj["artifact_id"], str) or not obj["artifact_id"].startswith("DAG:"):
        errs.append("artifact_id deve essere stringa che inizia con 'DAG:'")

    # parent_ids
    if not isinstance(obj["parent_ids"], list):
        errs.append("parent_ids deve essere una lista")
    else:
        if not all(isinstance(p, str) for p in obj["parent_ids"]):
            errs.append("Ogni parent_id deve essere stringa")

    # output_summary maxlength 500
    if not isinstance(obj["output_summary"], str):
        errs.append("output_summary deve essere stringa")
    else:
        if len(obj["output_summary"]) > 500:
            errs.append("output_summary supera 500 caratteri")

    # majorana_angle numeric (0-180)
    try:
        angle = float(obj["majorana_angle"])
        if not (0.0 <= angle <= 180.0):
            errs.append("majorana_angle deve essere tra 0 e 180")
    except Exception:
        errs.append("majorana_angle deve essere numerico")

    # uq in [0,1]
    try:
        uq = float(obj["uq"])
        if not (0.0 <= uq <= 1.0):
            errs.append("uq deve essere tra 0.0 e 1.0")
    except Exception:
        errs.append("uq deve essere numerico")

    # nd in [0,10]
    try:
        nd = float(obj["nd"])
        if not (0.0 <= nd <= 10.0):
            errs.append("nd deve essere tra 0.0 e 10.0")
    except Exception:
        errs.append("nd deve essere numerico")

    # timestamp_utc ISO8601
    if not isinstance(obj["timestamp_utc"], str) or not is_iso8601(obj["timestamp_utc"]):
        errs.append("timestamp_utc deve essere ISO8601 valido")

    # content_hash format 64 hex chars if present
    ch = obj.get("content_hash", "")
    if not isinstance(ch, str) or not (len(ch) == 64 and all(c in "0123456789abcdef" for c in ch.lower())):
        errs.append("content_hash dovrebbe essere SHA256 esadecimale (64 chars). Se ignoto: 'TO_BE_COMPUTED_BY_SCRIPT' accettabile e verrà ricalcolato.")

    # node_role
    nr = obj.get("node_role")
    if not isinstance(nr, str):
        errs.append("node_role deve essere stringa")
    else:
        if nr.upper() not in ALLOWED_NODE_ROLES:
            errs.append(f"node_role '{nr}' non in elenco consentito; valori noti: {sorted(ALLOWED_NODE_ROLES)}")

    # signature basic check
    if not isinstance(obj.get("signature"), str) or len(obj.get("signature")) < 8:
        errs.append("signature sembra non valida o troppo corta")

    return errs


def main(argv: List[str]):
    if len(argv) < 2:
        print("Usage: python3 validate_artifact.py <input_json> [--output <output_json>]")
        sys.exit(2)

    input_path = argv[1]
    output_path = "artifacts/DAG_VALIDATION_REPORT_001.json"
    if "--output" in argv:
        try:
            idx = argv.index("--output")
            output_path = argv[idx + 1]
        except Exception:
            print("Argomento --output richiede un percorso")
            sys.exit(2)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            obj = json.load(f)
    except Exception as e:
        print(f"Errore lettura input: {e}")
        sys.exit(3)

    errors = validate_artifact(obj)

    # Se content_hash è placeholder, ricalcolare dal contenuto dell'artefatto originale
    recalculated_hash = compute_sha256_of_json(obj)

    report = {
        "artifact_id": "DAG:VALIDATION_REPORT_001",
        "content_hash": "TO_BE_COMPUTED_BY_SCRIPT",
        "parent_ids": [obj.get("artifact_id", "DAG:UNKNOWN_PARENT")],
        "operation": "validation_report",
        "input": input_path,
        "output_summary": "",
        "majorana_angle": obj.get("majorana_angle", 0),
        "uq": 1.0 if not errors else 0.75,
        "nd": obj.get("nd", 0),
        "timestamp_utc": datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "provenance": "SINGULARITY_OS_v52.0_VALIDATION",
        "node_role": "GUARDIANO",
        "signature": "ARUTAM_COLLECTIVE_SEAL"
    }

    if errors:
        report["output_summary"] = f"VALIDATION_FAILED: {len(errors)} error(s)"
        report["details"] = {"errors": errors}
        report["uq"] = 0.25
    else:
        report["output_summary"] = "VALIDATION_PASSED: artefatto conforme allo schema v2.0"
        # aggiorno content_hash del report come hash del report effettivo
        report["uq"] = 0.99

    # Inserisco il content_hash reale dell'artefatto input come metadata
    report["input_content_hash_calculated"] = recalculated_hash

    # Calcolo content hash del report stesso
    report_hash = compute_sha256_of_json(report)
    report["content_hash"] = report_hash

    # Scrivo report su file
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Errore scrittura report: {e}")
        sys.exit(4)

    # Stampa sintesi
    print("VALIDATION REPORT GENERATO:")
    print(f" - input: {input_path}")
    print(f" - output: {output_path}")
    print(f" - input_content_sha256: {recalculated_hash}")
    print(f" - report_content_sha256: {report_hash}")
    print(f" - status: {'PASSED' if not errors else 'FAILED'}")

    sys.exit(0 if not errors else 5)


if __name__ == '__main__':
    main(sys.argv)
