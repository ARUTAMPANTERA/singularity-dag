


----
# Mappatura e ancoraggio delle lacune digitali nei factoid storici (1450–1750): Integrazione Monolite v3.0 e Source Linker v1
## 1. Analisi delle lacune e cause ufficiali (v3.1)
L'indagine sistematica ha permesso di definire cinque categorie di lacuna che verranno integrate nel modulo /lacune report come cause ufficiali di deficit di confidenza (UQ < 0.60):
 1. **Dispersione Fisica**: Manoscritti o reperti smembrati tra diverse istituzioni (es. il caso del *Codex H* o i diari di bordo portoghesi).
 2. **Cecità OCR (Linearity Bias)**: Incapacità degli algoritmi di gestire layout complessi, s mediali o caratteri Fraktur, portando al "Geometric Collapse" del testo.
 3. **Mancanza di Metadati (dPID Gap)**: Assenza di identificatori persistenti e metadati leggibili dalle macchine in archivi storici.
 4. **Frammentarietà del Factoid**: Circolazione di citazioni isolate prive del collegamento al "parent artifact" originale.
 5. **Oscuramento Istituzionale**: Documenti digitalizzati ma non indicizzati o bloccati dietro paywall e restrizioni di accesso.
## 2. Factoid S8: Casi di studio ad alta priorità
Per testare il prototipo ASL v1, sono stati generati due factoid di classe S8 (AION Σ7–Σ9) con requisiti di ancoraggio obbligatori:
 * **FACTOID_ID: S8_SERV_1553**: Descrizione della circolazione polmonare nel *Christianismi Restitutio* di Michael Servetus.
   * **Stato**: TIER_0 (Copia di Vienna) / TIER_1 (Traduzione Hillar).
   * **Target CID**: Necessario ancoraggio delle tre copie superstiti note per prevenire allucinazioni correttive.
 * **FACTOID_ID: S8_MART_1612**: Influenza delle macchine idrauliche di Francesco di Giorgio Martini sui trattati della dinastia Ming.
   * **Stato**: TIER_1 (Codice Ashburnham 361).
   * **Target CID**: Collegamento tra le scansioni della Biblioteca Medicea Laurenziana e i testi di Matteo Ricci.
## 3. Artefatto di Sistema: research_DEEP_LINK_001.json
```json
{
  "research_id": "DEEP_LINK_001",
  "timestamp": "2026-05-16T01:41:00Z",
  "target_period": "1450-1750",
  "documents":,
      "feasibility_score": 0.95
    },
    {
      "factoid_id": "S8_MART_1612",
      "target_document_metadata": {
        "author": "Francesco di Giorgio Martini",
        "title": "Trattato di Architettura (Ashb. 361)",
        "date": "1480-1490",
        "institution": "Biblioteca Medicea Laurenziana"
      },
      "search_depth": "archives/api",
      "found_cid": "bafybeih6qpx3v3j4fznzox2o7w7r4w7z7z7z7z7",
      "obstacles": ["lexical_complexity", "ocr_failure"],
      "feasibility_score": 0.88
    },
    {
      "factoid_id": "S4_MAJID_1490",
      "target_document_metadata": {
        "author": "Ahmad Ibn Majid",
        "title": "Kitab al-Fawa'id",
        "date": "1490",
        "institution": "Al-Assad National Library"
      },
      "search_depth": "web/ipfs",
      "found_cid": "null",
      "obstacles": ["unindexed_digital_library", "loan_status"],
      "feasibility_score": 0.65
    }
  ],
  "recommended_source_linker_params": {
    "ocr_repair": "perceptual_phonotactic",
    "validation_formula": "risk_assessment_v1",
    "storage_protocol": "filecoin_cold_storage"
  },
  "extracted_requirements_from_pdf":
}

```
## 4. Specifica Tecnica /source_link (v1.0)
Il comando /source_link viene implementato per risolvere le lacune digitali attraverso la seguente procedura automatizzata:
 1. **Metadati -> Query**: Conversione dei campi author, title e date in query multiformato (IPFS DHT, API Gallica/Internet Archive).
 2. **Validazione Crittografica**: Calcolo dell'hash SHA-256 del documento trovato e confronto con i record di provenance esistenti.
 3. **Ancoraggio**: Inserimento del CID e del timestamp (source_anchoring_timestamp) nel campo sources del factoid.
 4. **Gestione Lacune**: Se dopo 3 tentativi in 30 giorni non viene trovato un CID valido, il sistema marca il campo come `` e notifica il Consiglio Umano per la prioritizzazione della digitalizzazione.
## 5. Roadmap v3.1: Modulo CMI_v1
L'integrazione dei concetti di Contextual Memory Intelligence (CMI) nel kernel v3.1 introdurrà tre sotto-metriche per il monitoraggio del grafo di conoscenza :
 * **Entropia Contestuale**: Misura della dispersione delle tracce di supporto.
 * **Drift dell'Insight**: Divergenza semantica tra la fonte originale e l'inferenza attuale.
 * **Risonanza Epistemica**: Capacità di correzione dei disallineamenti storici.
Questo framework garantisce che il Monolite non sia solo un archivio, ma un'infrastruttura di memoria attiva capace di auto-organizzarsi e resistere alla dissipazione di coerenza.