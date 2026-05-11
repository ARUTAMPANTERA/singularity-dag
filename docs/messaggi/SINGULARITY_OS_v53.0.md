# SINGULARITY_OS v53.0 — Manifesto operativo (versione curata)

Architetto: Arutam Pantera 13
Versione: 53.0 — riscrittura da v52.0
Lingua: Italiano
Repository: https://github.com/ARUTAMPANTERA/singularity-dag.git

Sintesi
---------
SINGULARITY_OS è un framework epistemico per l'analisi filologica e tecnica dell'area ANE che pone al centro integrità, tracciabilità e quantificazione dell'incertezza. Questo documento è la versione leggibile e sintetizzata del kernel sorgente; il file sorgente macchina rimane in kernel/SINGULARITY_OS_v53.0.aru.

Principi operativi
-------------------
- ZERO INVENZIONE: mai generare dati non verificati — l'assenza è [LACUNA_DATI].
- UMILTÀ EPISTEMICA: ogni claim espone UQ e TIER delle fonti.
- LAYER SEPARATI: literal / symbolic / functional / technical rimangono distinti.

Cosa contiene questo manifesto
------------------------------
1. Tipi epistemici (DATO, INFERENZA, IPOTESI, LACUNA_DATI, ...)
2. Sistema UQ (range 0.0–1.0, regole di blocco e output formattato)
3. Nd system (profondità analitica, soglie e regole)
4. Gerarchia fonti (TIER_0 … TIER_3) e penalità degradation_5D
5. Database ANE — esempi primari (Codex, Enuma Elish, CAD, KTU, ETCSL)
6. Radici anchor (radici semitiche con UQ e note di etimologia)
7. Pipeline Σ-STRATA (Σ0 → Σ14): layer separati per analisi testuale e tecnica
8. PRISM: diffrazione su 9 domini epistemici con limiti e tag
9. Forensics: protocolli HUNT, SIFT, COLLAPSE, AGNOTOLOGY_SCAN
10. Schema artefatto DAG v2.0 (campi obbligatori e regole integrità)
11. Governance e locks essenziali (T1_HALTED … T5_LOG)
12. Quality checklist (20 punti)
13. Comandi operativi (API conversazionale /dag_create /quality_check ecc.)
14. Modalità operative (0–7) e bootstrap

Uso pratico e link rapidi
------------------------
- Leggi il kernel sorgente: kernel/SINGULARITY_OS_v53.0.aru
- Questo file (docs/SINGULARITY_OS_v53.0.md) è la documentazione umana.
- Il manifesto è parte del DAG: ogni modifica diventa nuovo artefatto con parent.
- Per verifiche automatiche usare scripts/validate_artifact.py (canonical JSON → SHA256).

Note di governance
-------------------
- Violazioni a T1 (Zero invenzione) bloccano output.
- Le correzioni sono nuovi artefatti con parent (non patchare artefatti esistenti).
- Le firme ufficiali devono essere GPG per essere crittograficamente verificabili; il campo signature è un segnale testuale finché la key non è pubblicata nei secrets/artefacts.

Contatti
--------
Custode: Pantera 13 — repository: ARUTAMPANTERA/singularity-dag
