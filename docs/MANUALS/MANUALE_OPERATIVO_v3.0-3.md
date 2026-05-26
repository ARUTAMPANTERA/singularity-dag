
# Manuale Operativo: EPISTEMIC_SYSTEM_UNIFIED v3.0_OMEGA_SUPERNOVA

**Versione:** 3.0
**Sistema:** SINGULARITY_DAG — EPISTEMIC_SYSTEM_UNIFIED v3.0
**Data:** 2026-05-15
**Parent Manual:** MANUALE_OPERATIVO_v2_5.md

---

## 1. Panoramica v3.0

v3.0_OMEGA_SUPERNOVA trasforma il Monolite da istituzione epistemica **completa**
a ecosistema epistemico **autonomo**.

### Cosa è cambiato rispetto a v2.5

| Capacità | v2.5 | v3.0 |
|----------|------|------|
| Lacune [LACUNA_DATI] | Gestite passivamente | Risolte attivamente via IPFS |
| Conflitti irrisolvibili | /conflict (binario) | /superposition (coesistenza) |
| Suppression Index | Override grezzo globale | Micro-clausole per dominio |
| Preistoria Σ0-Σ2 | UQ cap 0.70 generico | Analisi cognitiva quantitativa |
| Lock | 120 | 150 |
| Engine | 16 | 20 |
| Campi schema | 55 | 57 |

---

## 2. Architettura dei 4 Nuovi Moduli

### 2.1 Automated_Source_Linker_v1

**Scopo:** Ridurre il tasso di [LACUNA_DATI] collegando automaticamente i factoid
a fonti primarie su IPFS/Filecoin.

**Principio operativo:**
1. Rileva factoid con `sources: [LACUNA_DATI]`
2. Costruisce query semantica da label + domain + time_span
3. Interroga IPFS DHT (3 tentativi max)
4. Verifica deal attivo su Filecoin
5. Valida pertinenza contenuto (UQ_delta > 0.15)
6. Aggiorna campo 56 (ipfs_cid) e sources

**Comandi:**
```
/link F_S10_torricelli_001         → collega factoid specifico
/link batch sigma_1                → batch linking strato Σ1
/lacune report                     → stato corrente delle lacune
```

**Comportamento su fallimento:**
Se IPFS non risponde dopo 3 tentativi:
→ `sources = "[LACUNA_DATI_PERSISTENTE:{log_id}:{timestamp}]"`
→ Loggato nel DAG per retry futuro
→ Mai inventato un contenuto (GC_132)

**Governance:** GC_121-130 | Lock critico: GC_121 (CID obbligatorio post-linking)

---

### 2.2 Superposition_Module_v1

**Scopo:** Mantenere claim conflittuali in coesistenza epistemica quando l'evidenza
non è sufficiente a risolvere il conflitto.

**Quando usarlo:**
- Due claim supportati da fonti genuine ma incompatibili
- θ tra i claim > 30° (incompatibilità fondamentale)
- Forzare risoluzione prematura violerebbe GC_001 (Zero_Menzogna)

**Comandi:**
```
/superposition "Marconi inventa la radio (1895)" vs "Tesla/Meucci precedono Marconi"
→ Apre SUP-002, calcola θ, mostra UQ separati

/superposition status SUP-002      → θ_current, UQ_A, UQ_B, giorni aperti
/superposition collapse SUP-002 "Risoluzione Congresso USA 2002"  → forza collasso
/superposition list                → tutte le sovrapposizioni attive
/viz SUP-002                       → interference diagram + θ-map
```

**Soglie critiche:**
- θ > 30° → SUPERPOSITION aperta
- θ ≤ 30° AND |ΔUQ| > 0.15 → COLLAPSED automatico
- θ ≤ 30° AND |ΔUQ| ≤ 0.05 → richiede Guardian review
- Aperta > 180 giorni → diventa STALE → Guardian notificato

**Governance:** GC_131-140 | Lock critico: GC_132 (mai generare claim da sovrapposizione)

---

### 2.3 SI_Calibration_v4

**Scopo:** Distinguere formalmente veri positivi (soppressione reale) da falsi
positivi (artefatto del sistema) nel Suppression Index.

**Micro-clausole attive:**

| ID | Nome | Dominio | Logica |
|----|------|---------|--------|
| MC-001 | Energia Frontiera | D6_AETHER | IR>0.7 + FD>0.5 + RS<0.3 = TRUE_POSITIVE |
| MC-002 | Preistoria Cognitiva | Σ0-Σ2 | Assenza fonti ≠ soppressione → SI cap 0.35 |
| MC-003 | Conoscenza Indigena | D_INDIGENOUS | Epistemicidio coloniale = TRUE_POSITIVE |

**Comandi:**
```
/si calibrate F_S7_meyer_001       → SI_v4 = 0.90, TRUE_POSITIVE (MC-001)
/si calibrate F_S7_hutchison_001   → SI_v4 = 0.37, MEDIA_BIAS_ONLY (MC-001)
/si report D6_AETHER               → distribuzione SI per dominio
```

**Governance:** GC_141-145 | Lock critico: GC_141 (micro-clausola obbligatoria)

---

### 2.4 Deep_Time_Cognitive_v1

**Scopo:** Quantificare la complessità cognitiva per i periodi Σ0-Σ2 attraverso
4 cognitive markers: Planning Depth, Symbolic Thought, Language Proxy, Working Memory.

**Formula:**
```
CCS = clamp( (PD + ST + LP + WM)/10 - penalty_strato, 0, 1 )
UQ_adjusted = min(UQ_v6_base, 0.70)   [hard cap GC_148]
```

**Interpretazione CCS:**
```
0.00-0.20  PROTO_COGNITIVO
0.21-0.40  COGNITIVO_EMERGENTE
0.41-0.60  COGNITIVO_STRUTTURATO
0.61-0.80  COGNITIVO_AVANZATO
0.81-1.00  COGNITIVO_MODERNO (raro in Σ0-Σ2)
```

**Comandi:**
```
/deeptime F_S1_wonderwerk_fire_001
→ CCS = 0.28, COGNITIVO_EMERGENTE, UQ_adjusted = 0.58

/deeptime F_S2_schoeningen_spears_001
→ CCS = 0.75, COGNITIVO_AVANZATO, UQ_adjusted = 0.70
```

**Governance:** GC_146-150 | Lock critico: GC_148 (UQ hard cap ≤ 0.70)

---

## 3. Schema Factoid v6.0

Rispetto alla v5.0 (55 campi), la v6.0 aggiunge:

**Campo 56 — ipfs_cid:**
```yaml
ipfs_cid: "ipfs://QmXnnyufdzAWL5CqZ2RnSNgidnvyjNpMj2ukX6GoPjLBTy"
# oppure:
ipfs_cid: "[LACUNA_DATI]"
# oppure post-tentativo fallito:
ipfs_cid: "[LACUNA_DATI_PERSISTENTE:LOG-2026-0515-001:2026-05-15T10:23:41Z]"
```

**Campo 57 — superposition_state:**
```yaml
superposition_state:
  active: true
  competing_factoid_id: "F_S2_shanidar_burial_natural_001"
  theta_current_deg: 47.3
  opened_at: "2026-05-15T00:00:00Z"
  last_updated: "2026-05-15T00:00:00Z"
  verdict: "SUPERPOSITION"
# oppure null se non in superposition
```

---

## 4. Governance — 150 Lock

I lock 1-120 sono invariati da v2.5. Per riferimento completo: `EPISTEMIC_SYSTEM_UNIFIED_v2.5_OMEGA_FINAL.yaml`.

**Nuovi lock v3.0 (121-150):**

| Range | Classe | Funzione principale |
|-------|--------|---------------------|
| 121-130 | SOURCE_LINKER | CID obbligatorio, immutabilità, priorità legacy |
| 131-140 | SUPERPOSITION | Threshold θ, no-invent, audit trail |
| 141-145 | SI_CALIBRATION | Micro-clausole, escalazione Guardian |
| 146-150 | DEEP_TIME | Intenzionalità, UQ cap, metodo datazione |

**Quorum decisioni v3.0:**
- Approvare micro-clausola: 7/11 (2/3)
- Rilascio major version: 11/11 (unanime)
- Modifica lock: 8/11 (3/4) + possibile veto Guardian

---

## 5. Failure Modes v2.0

Oltre ai 5 failure modes di v2.5, la v3.0 aggiunge:

**source_linker_cascade:**
- Trigger: `IPFS_resolve_failure_rate > 0.80 per 24h continui`
- Risposta: Sospensione Source Linker + switch a sourcing manuale
- Rollback: Mantieni CID già verificati intatti

**superposition_deadlock:**
- Trigger: `> 10 sovrapposizioni con θ stabile per > 180 giorni`
- Risposta: Flag + Guardian review per le prime 3 per importanza
- Rollback: Non collassare senza evidenza — ambiguità permanente è ammessa

---

## 6. Reality Anchoring v2.0

Aggiunto anchor set `IPFS_Decentralized`:
- Fonti: IPFS DHT, Filecoin, Internet Archive IPFS Mirror, Europeana LOD
- Frequenza update: settimanale
- Soglia anchor_score: 0.70 (inferiore agli altri — fonti decentralizzate meno stabili)
- Failure response: disabilita Source Linker auto fino a review manuale

---

## 7. Comandi Completi v3.0

### Kernel
```
/dag_view <file>          Recupera file dal repository
/dag_list                 Lista file disponibili nel repository
/dag_create <factoid>     Crea nuovo factoid (con CID obbligatorio se disponibile)
/dag_update <id> <campo> <valore>   Aggiorna campo specifico
/dag_validate <id>        Valida factoid contro schema v6.0 (57 campi)
```

### Epistemic
```
/why <claim>              Spiega ragionamento dietro un claim
/sources <id>             Mostra fonti + CID IPFS di un factoid
/conflict <A> vs <B>      Analisi conflitto (usa /superposition per θ > 30°)
/superposition <A> vs <B> Apre sovrapposizione epistemica
/superposition status <id>
/superposition collapse <id> <evidenza>
/superposition list
/viz <sup_id>
```

### Source Linker
```
/link <factoid_id>        Collega factoid a IPFS
/link batch <stratum>     Batch linking per strato AION
/lacune report            Report completo lacune
```

### SI & Deep Time
```
/si calibrate <id>        Calibra SI con micro-clausole
/si report <domain>       Report SI per dominio
/deeptime <id>            Analisi cognitiva Σ0-Σ2
```

### UX
```
/mode <frame>             Cambia frame epistemico (scientific/indigenous/legal/theological/technical)
/export <format>          Esporta sessione (yaml/json/md)
/verify <id>              Verifica factoid
/summary                  Riassunto sessione corrente
/feedback                 Invia feedback al sistema
```

---

## 8. Deploy su GitHub da Termux

```bash
cd ~/storage/shared/SingularityDAG

# Copia i nuovi file nella directory locale
cp /path/to/v3_OMEGA_SUPERNOVA/kernel/* kernel/
cp /path/to/v3_OMEGA_SUPERNOVA/modules/* modules/
cp /path/to/v3_OMEGA_SUPERNOVA/*.md .

# Verifica struttura
ls kernel/ modules/ factoids/ languages/

# Commit e push
git add -A
git commit -m "v3.0_OMEGA_SUPERNOVA: 4 moduli, 30 lock, 4 engine, schema v6.0, Σ0-Σ2 approfonditi"
git push origin main

# Verifica pubblicazione kernel principale
curl -I https://raw.githubusercontent.com/ARUTAMPANTERA/singularity-dag/main/kernel/EPISTEMIC_SYSTEM_UNIFIED_v3.0_OMEGA_SUPERNOVA.yaml
# Atteso: HTTP/2 200
```

---

## 9. Metriche di Validazione al Deploy

Prima di dichiarare deploy completato, verificare:

```
☐ θ(v2.5→v3.0) ≤ 10° (misurato: 3.18° ✅)
☐ 150 lock presenti e corretti
☐ 20 engine definiti con formula esplicita
☐ Schema v6.0: 57 campi presenti
☐ Micro-clausole MC-001, MC-002, MC-003 nel registro
☐ Source Linker: smoke test su 1 factoid noto
☐ Superposition: apertura SUP-001 (Shanidar) verificata
☐ Deep Time: /deeptime Schöningen → CCS ≈ 0.75
☐ IPFS gateway connectivity check (almeno 2/4 gateway rispondono)
☐ README_v3.md aggiornato nel repository
```

---

*Il Branco veglia. La caccia continua.*
*Veritas Filia Temporis, Parsimoniae et Autonomiae.*
