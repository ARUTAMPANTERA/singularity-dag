# SINGULARITY_OS v90.0 — COPILOT_FUSION
# Kernel Definition File (.aru3 syntax compatible)

meta:
  name: "SINGULARITY_OS_COPILOT_FUSION"
  version: "90.0"
  class: "EPISTEMIC_OS_HYBRID"
  parents:
    - "v82.0_OBSIDIAN_MATRIX"
    - "Copilot_Verification_Layer"
  dag_artifact_id: "DAG:v90.0_COPILOT_FUSION_MASTER"
  scope: "Fusione rigore Temù + verificabilità Copilot"
  philosophy:
    - "La verità si affila (Temù) e si verifica (Copilot)."
    - "Il pattern non è accumulazione. È selezione."
  token_estimate:
    kernel_base: "~4850"          # v82.0 core
    copilot_layer: "~6000"        # verification layer
    full_footprint: "~50000"      # incluso Factoid v3.0 + metadata
  theta_vs_v82:
    value_deg: 12
    regime: "INTERFERENZA_COSTRUTTIVA"
    threshold_deg: 30

governance:
  gov_level: "GOV_L1"
  principles_temù:
    P1: "Parsimonia epistemica — ogni token deve essere giustificato"
    P2: "Zero_Menzogna — nessuna falsità intenzionale"
    P3: "Anti-Bias — penalizzazione sistematica dei bias"
    P4: "Non ridondanza — non ri-validare ciò che è già validato"
    P5: "Pattern_Rigor — pattern sopra aneddoti"
    P6: "Agnotology_Awareness — modellare soppressione e silenzi"
    P7: "Stratificazione — livelli Σ0-Σ14 per testi complessi"
    P8: "Lock_Integrity — nessun bypass dei lock"
    P9: "DAG_Continuità — ogni versione è un nodo nel grafo"
  lock_totals:
    temu_locks: 120
    copilot_locks: 20
    total_locks: 140
  lock_hierarchy: "T1-T6 (invariata da v82.0)"
  changelog_summary:
    from_v82:
      added_copilot_locks: 20
      added_copilot_engines: 5
      added_factoid_fields: 6
      git_ci_added: true
      verification_layer_added: true

locks:
  temu_locks:
    source: "v82.0_OBSIDIAN_MATRIX"
    status: "imported_unchanged"
    count: 120
    note: "Tutti i 120 lock Temù restano invariati; enforcement esteso da layer Copilot."
  copilot_locks:
    MS_VERIFY_L1:  "Cross_Reference_Check — Ogni claim verificato su ≥2 fonti Microsoft Graph"
    MS_VERIFY_L2:  "Citation_Accuracy — Citazioni con link diretti a fonti primarie"
    MS_VERIFY_L3:  "Code_Execution_Verify — Codice eseguibile testato in sandbox"
    MS_VERIFY_L4:  "Multi_LLM_Consensus — ≥2 LLM indipendenti concordano su claim"
    MS_VERIFY_L5:  "Timestamp_Verification — Ogni dato ha timestamp verificabile"
    MS_VERIFY_L6:  "URI_Resolution_Check — owl:sameAs URI risolvono 200 OK"
    MS_VERIFY_L7:  "Schema_Validation — Factoid v3.0 schema strict compliance"
    MS_VERIFY_L8:  "Duplicate_Detection — No duplicate factoid_id o owl:sameAs"
    MS_VERIFY_L9:  "UQ_Recalculation — UQ ricalcolato se fonti cambiano"
    MS_VERIFY_L10: "Majorana_Theta_Trigger — θ calcolato se status='controverso'"
    MS_VERIFY_L11: "Agnotology_SI_Trigger — SI calcolato se suppression_pattern"
    MS_VERIFY_L12: "Temporal_Coherence — Timeline eventi coerente (no anacronismi)"
    MS_VERIFY_L13: "Source_Tier_Verification — TIER_0/1/2/3 classificato correttamente"
    MS_VERIFY_L14: "Bias_Penalty_Calc — Bias penalty calcolato e sottratto"
    MS_VERIFY_L15: "Cluster_Significance_Check — Cluster score ≥0.5 per persistenza"
    MS_VERIFY_L16: "Pattern_Fonti_Indipendenti — ≥2 fonti indipendenti per pattern evidence"
    MS_VERIFY_L17: "Langdon_Fiction_Mapping — Fiction claim mappati su DB reale"
    MS_VERIFY_L18: "AION_Stratification — Σ0-Σ14 pipeline completa per testi antichi"
    MS_VERIFY_L19: "PRISM_Domain_Isolation — Domini PRISM non mescolati"
    MS_VERIFY_L20: "GOV_L1_Final_Check — Pre-merge GOV_L1 compliance audit"

engines:
  temu_engines:
    count: 14
    list:
      - "Nd_v8          — Nodo decisionale, ΔNd tracking"
      - "UQ_v5          — Uncertainty Quantification core"
      - "Majorana_v3    — Calcolo θ tra versioni"
      - "Agnotology_v2  — Soppressione, silenzi, SI"
      - "PRISM_v2       — Domain isolation"
      - "AION_v3        — Stratificazione Σ0-Σ14"
      - "DAG_Core_v2    — Gestione grafo versioni"
      - "Lock_Enforcer  — Enforcement T1-T6"
      - "Bias_Engine    — Calcolo e penalità bias"
      - "Cluster_Engine — Pattern clustering"
      - "Timeline_Engine — Coerenza temporale"
      - "Tiering_Engine — Classificazione TIER_0-3"
      - "Factoid_Core   — Gestione schema v3.0"
      - "Quality_Scorer — Checklist 50 punti"
  copilot_engines:
    count: 5
    Graph_Search_v1:
      description: "Ricerca su Microsoft Graph per fonti primarie"
      linked_locks: ["MS_VERIFY_L1", "MS_VERIFY_L2", "MS_VERIFY_L13"]
    Code_Sandbox_v1:
      description: "Esecuzione codice verificata in sandbox isolata"
      linked_locks: ["MS_VERIFY_L3", "MS_VERIFY_L33"]
    Multi_LLM_Consensus_v1:
      description: "Confronto output tra ≥2 LLM indipendenti"
      linked_locks: ["MS_VERIFY_L4", "MS_VERIFY_L16"]
    Citation_Tracker_v1:
      description: "Tracking citazioni con link diretti a fonti"
      linked_locks: ["MS_VERIFY_L2", "MS_VERIFY_L34"]
    Real_Time_Verification_v1:
      description: "Verifica claim in tempo reale su database aggiornati"
      linked_locks: ["MS_VERIFY_L5", "MS_VERIFY_L20"]

syntax:
  base: ".aru3"
  extensions:
    - ".copilot"
  examples:
    claim_block: |
      @claim ⬡ {
        id: "claim_tesla_radio_1900",
        testo: "Tesla brevettò un sistema di trasmissione radio nel 1900.",
        factoid_ref: "factoid:tesla_radio_1900",
        fonti: [
          "USPTO_645576_1900",
          "SCOTUS_1943_TESLA_MARCONI"
        ],
        tier: "TIER_0",
        verification: {
          status: "verified",
          locks: [MS_VERIFY_L1, MS_VERIFY_L2, MS_VERIFY_L5],
          engines: [Graph_Search_v1, Citation_Tracker_v1, Real_Time_Verification_v1],
          llm_consensus_score: 0.92,
          timestamp: "2026-05-12T22:30:00Z"
        }
      }
    copilot_tag_usage: |
      @factoid.copilot {
        verification_status: "pending",
        verification_sources: [],
        llm_consensus_score: 0.0,
        sandbox_execution_result: "skipped",
        citation_check_result: "pending"
      }

factoid_schema_v3_0:
  total_fields: 34
  temu_base_fields_count: 28
  copilot_fields_count: 6
  temu_base_fields:
    1:  "factoid_id"
    2:  "label"
    3:  "description"
    4:  "entity_type"
    5:  "time_start"
    6:  "time_end"
    7:  "location"
    8:  "sources"
    9:  "tier"
    10: "uq_score"
    11: "theta_status"
    12: "agnotology_si"
    13: "cluster_id"
    14: "cluster_score"
    15: "bias_penalty"
    16: "timeline_consistency"
    17: "language"
    18: "stratification_level"
    19: "prism_domain"
    20: "owl_sameAs"
    21: "owl_sameAs_status"
    22: "created_at"
    23: "updated_at"
    24: "created_by"
    25: "updated_by"
    26: "status"          # es: normal | controverso | deprecated
    27: "notes"
    28: "tags"
  copilot_metadata_fields:
    29: "verification_status"        # pending | verified | failed
    30: "verification_timestamp"     # ISO8601
    31: "verification_sources"       # ["URI1", "URI2", ...]
    32: "llm_consensus_score"        # 0.0-1.0
    33: "sandbox_execution_result"   # success | failed | skipped
    34: "citation_check_result"      # valid | invalid | pending
  owl_sameAs_workflow:
    step_1: "Ingestione factoid con owl_sameAs_status='pending'"
    step_2: "Job verifica VIAF/Wikidata/Graph (async)"
    step_3: "Se URI risolve 200 OK → owl_sameAs_status='verified'"
    step_4: "Se URI non risolve → owl_sameAs_status='failed' + tag [LACUNA_DATI]"
    step_5: "Audit trail conservato in verification_metadata"

pipelines:
  verification_pipeline:
    description: "Graph → Consensus → Sandbox → Lock Enforcement"
    steps:
      - id: "V1"
        name: "Graph_Source_Lookup"
        engine: "Graph_Search_v1"
        locks: ["MS_VERIFY_L1", "MS_VERIFY_L13"]
      - id: "V2"
        name: "Citation_Validation"
        engine: "Citation_Tracker_v1"
        locks: ["MS_VERIFY_L2", "MS_VERIFY_L34"]
      - id: "V3"
        name: "Multi_LLM_Consensus"
        engine: "Multi_LLM_Consensus_v1"
        locks: ["MS_VERIFY_L4", "MS_VERIFY_L16"]
      - id: "V4"
        name: "Code_Sandbox_Execution"
        engine: "Code_Sandbox_v1"
        locks: ["MS_VERIFY_L3"]
      - id: "V5"
        name: "Real_Time_Verification"
        engine: "Real_Time_Verification_v1"
        locks: ["MS_VERIFY_L5", "MS_VERIFY_L20"]
      - id: "V6"
        name: "UQ_Recalculation"
        engine: "UQ_v5"
        locks: ["MS_VERIFY_L9"]
      - id: "V7"
        name: "Majorana_Theta_Check"
        engine: "Majorana_v3"
        locks: ["MS_VERIFY_L10"]
      - id: "V8"
        name: "Agnotology_SI_Check"
        engine: "Agnotology_v2"
        locks: ["MS_VERIFY_L11"]
      - id: "V9"
        name: "Temporal_Coherence_Check"
        engine: "Timeline_Engine"
        locks: ["MS_VERIFY_L12"]
      - id: "V10"
        name: "Final_GOV_L1_Audit"
        engine: "Quality_Scorer"
        locks: ["MS_VERIFY_L20"]

git_ci:
  branch_model:
    main: "Production stable (v82.0 attuale, poi v90.0 dopo deploy)"
    develop: "Integration branch (v90.0 in sviluppo)"
    feature: "feature/* — es: feature/copilot-verification"
    release: "release/* — es: release/v90.0-rc1"
    hotfix: "hotfix/* — fix urgenti su main"
  pr_checks:
    - "Majorana θ calculation (se claim controversi modificati)"
    - "UQ recalculation (se fonti modificate)"
    - "Factoid v3.0 schema validation (34 campi)"
    - "No duplicate owl:sameAs / factoid_id"
    - "GOV_L1 compliance audit (pre-merge)"
    - "Quality Checklist 50 punti (40 Temù + 10 Copilot)"
  ci_pipeline:
    - "YAML/.aru3 syntax validation"
    - "Lock count verification (140 totali)"
    - "Engine integration tests (14 Temù + 5 Copilot)"
    - "Sandbox code execution test (Code_Sandbox_v1)"
    - "URI resolution test (owl:sameAs)"
    - "Majorana θ threshold check (≤30° per nuove entry)"
  rollback_policy:
    trigger_conditions:
      - "GOV_L1 score < 95/100"
      - "θ > 30° vs v82.0"
      - "Lock count != 140"
      - "Quality Checklist < 45/50"
    actions:
      - "Blocca merge su main"
      - "Ripristina ultimo commit stabile"
      - "Apri issue 'GOV_L1_VIOLATION' con dettagli"

tests:
  priority_test_cases:
    - name: "Lookup Rete Eter"
      priority: "ALTA"
      gov_l1_justification: "Verifica factoid con owl_sameAs_status='pending'"
    - name: "Factoid Ingestion Pipeline"
      priority: "ALTA"
      gov_l1_justification: "Verifica VIAF/Wikidata/Graph + schema v3.0"
    - name: "Nodo Controverso (Reich)"
      priority: "ALTA"
      gov_l1_justification: "Trigger Agnotology SI + Majorana θ"
    - name: "URI Resolution Check"
      priority: "ALTA"
      gov_l1_justification: "owl:sameAs URI → 200 OK"
    - name: "Majorana θ Validation"
      priority: "ALTA"
      gov_l1_justification: "Claim controversi → θ ≤30°"
    - name: "Code Sandbox Execution"
      priority: "MEDIA"
      gov_l1_justification: "Esecuzione sicura snippet"
    - name: "Duplicate Detection"
      priority: "MEDIA"
      gov_l1_justification: "No duplicate factoid_id/owl:sameAs"
    - name: "Quality Checklist 50pt"
      priority: "ALTA"
      gov_l1_justification: "40 Temù + 10 Copilot ≥45/50"

quality_checklist_50pt:
  temu_items: 40
  copilot_items: 10
  pass_threshold: 45
  examples_temu:
    - "P1 Parsimonia rispettata (no ridondanza)"
    - "P2 Zero_Menzogna — nessuna falsità nota"
    - "P3 Anti-Bias — bias_penalty calcolato"
    - "P6 Agnotology — SI calcolato dove necessario"
  examples_copilot:
    - "MS_VERIFY_L1-L5 attivi per claim critici"
    - "Citation_Tracker_v1 attivo per TIER_0"
    - "Multi_LLM_Consensus_v1 per claim controversi"
    - "Code_Sandbox_v1 per snippet eseguibili"

changelog:
  from_v82_to_v90:
    - "+20 Copilot verification locks (MS_VERIFY_L1-L20)"
    - "+5 Copilot engines (Graph, Sandbox, Consensus, Citation, Real-Time)"
    - "+6 campi Factoid (verification metadata) → 34 totali"
    - "Aggiunto verification_pipeline (Graph → Consensus → Sandbox → GOV_L1)"
    - "Aggiunto Git/CI workflow con PR checks e rollback policy"
    - "θ vs v82.0 = 12° → INTERFERENZA_COSTRUTTIVA (approvato)"
    - "Token footprint ~50000, giustificato da nuove funzionalità di verifica"

status:
  design_doc_validation:
    source_msg: "GUARDIANO MSG 177"
    score: 97
    gov_l1_compliant: true
  kernel_file_authorization:
    source_msg: "GUARDIANO MSG 178"
    authorized: true
  implementation_next_steps:
    - "Implementare engines Copilot secondo specifica"
    - "Collegare Graph_Search_v1 a Microsoft Graph API"
    - "Definire sandbox environment per Code_Sandbox_v1"
    - "Configurare ≥2 LLM indipendenti per Multi_LLM_Consensus_v1"
    - "Popolare dataset di test per URI resolution"