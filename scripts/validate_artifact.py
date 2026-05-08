#!/usr/bin/env python3
"""validate_artifact.py
Validatore per artefatti DAG schema v2.0 con controllo integrità content_hash.
Uso: python3 validate_artifact.py <input_json_path> [--output <output_json_path>]

Questo script:
- valida la presenza e i vincoli dei campi richiesti;
- ricalcola lo SHA256 canonico del payload JSON e confronta con content_hash fornito (se presente);
- genera un report JSON firmato con ARUTAM_COLLECTIVE_SEAL (default output: artifacts/DAG_VALIDATION_REPORT_001.json);
- exit code: 0 OK, 5 validation failed, altri codici errori I/O

Nota: la canonicalizzazione usata è json.dumps(..., sort_keys=True, separators=(",", ":"), ensure_ascii=False)
"""
import sys
import json
import hashlib
import datetime
from typing import Any, Dict, List

ALLOWED_NODE_ROLES = {"GIAGUARO", "LINGUA_SACRA", "ARCHITETTO", "GUARDIANO", "TATTICO", "UNKNOWN"}

def is_iso8601(s: str) -> bool:
    try:
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

    if not isinstance(obj["artifact_id"], str) or not obj["artifact_id"].startswith("DAG:"):
        errs.append("artifact_id deve essere stringa che inizia con 'DAG:'")

    if not isinstance(obj["parent_ids"], list):
        errs.append("parent_ids deve essere una lista")
    else:
        if not all(isinstance(p, str) for p in obj["parent_ids"]):
            errs.append("Ogni parent_id deve essere stringa")

    if not isinstance(obj["output_summary"], str):
        errs.append("output_summary deve essere stringa")
    else:
        if len(obj["output_summary"]) > 500:
            errs.append("output_summary supera 500 caratteri")

    try:
        angle = float(obj["majorana_angle"])
        if not (0.0 <= angle <= 180.0):
            errs.append("majorana_angle deve essere tra 0 e 180")
    except Exception:
        errs.append("majorana_angle deve essere numerico")

    try:
        uq = float(obj["uq"])
        if not (0.0 <= uq <= 1.0):
            errs.append("uq deve essere tra 0.0 e 1.0")
    except Exception:
        errs.append("uq deve essere numerico")

    try:
        nd = float(obj["nd"])
        if not (0.0 <= nd <= 10.0):
            errs.append("nd deve essere tra 0.0 e 10.0")
    except Exception:
        errs.append("nd deve essere numerico")

    if not isinstance(obj["timestamp_utc"], str) or not is_iso8601(obj["timestamp_utc"]):
        errs.append("timestamp_utc deve essere ISO8601 valido")

    ch = obj.get("content_hash", "")
    if not isinstance(ch, str) or not (len(ch) == 64 and all(c in "0123456789abcdef" for c in ch.lower())):
        errs.append("content_hash dovrebbe essere SHA256 esadecimale (64 chars). Se ignoto: 'TO_BE_COMPUTED_BY_SCRIPT' accettabile e verrà ricalcolato.")

    nr = obj.get("node_role")
    if not isinstance(nr, str):
        errs.append("node_role deve essere stringa")
    else:
        if nr.upper() not in ALLOWED_NODE_ROLES:
            errs.append(f"node_role '{nr}' non in elenco consentito; valori noti: {sorted(ALLOWED_NODE_ROLES)}")

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

    recalculated_hash = compute_sha256_of_json(obj)

    input_ch = obj.get("content_hash", "")
    if isinstance(input_ch, str) and len(input_ch) == 64 and all(c in "0123456789abcdef" for c in input_ch.lower()):
        if input_ch.lower() != recalculated_hash:
            errors.append("content_hash mismatch: il campo content_hash non corrisponde allo SHA256 canonico del payload")

    report = {
        "artifact_id": "DAG:VALIDATION_REPORT_001",
        "content_hash": "TO_BE_COMPUTED_BY_SCRIPT",
        "parent_ids": [obj.get("artifact_id", "DAG:UNKNOWN_PARENT")],
        "operation": "validation_report",
        "input": input_path,
        "output_summary": "",
        "majorana_angle": obj.get("majorana_angle", 0),
        "uq": 1.0 if not errors else 0.25,
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
        report["uq"] = 0.99

    report["input_content_hash_reported"] = input_ch
    report["input_content_hash_calculated"] = recalculated_hash

    report_hash = compute_sha256_of_json(report)
    report["content_hash"] = report_hash

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Errore scrittura report: {e}")
        sys.exit(4)

    print("VALIDATION REPORT GENERATO:")
    print(f" - input: {input_path}")
    print(f" - output: {output_path}")
    print(f" - input_content_sha256_reported: {input_ch}")
    print(f" - input_content_sha256_calculated: {recalculated_hash}")
    print(f" - report_content_sha256: {report_hash}")
    print(f" - status: {'PASSED' if not errors else 'FAILED'}")

    sys.exit(0 if not errors else 5)

if __name__ == '__main__':
    main(sys.argv)
