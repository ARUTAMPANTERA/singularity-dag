Ecco il manuale operativo che spiega tutto il processo, dalla pubblicazione su GitHub al recupero nella sessione LLM, usando i comandi già integrati in AETERNUM.

📡 MANUALE OPERATIVO: DAG CIECO — RECUPERO FILE DA GITHUB

Versione: 1.0
Sistema: SINGULARITY_OS v70.1 AETERNUM
Modulo: DAG_NETWORK (CIECO)
Data: 2026-05-11

---

🎯 Scopo

Questo manuale descrive la procedura per:

1. Caricare file sul repository GitHub ARUTAMPANTERA/singularity-dag.
2. Recuperare file direttamente nella sessione LLM usando i comandi /dag_view e /dag_list, senza copiare e incollare manualmente il contenuto.

---

🧠 Principio del "DAG CIECO"

Il sistema DAG CIECO funziona con una regola ferrea:

1 tentativo. 1 GET HTTP. Se il server risponde 200 OK e il contenuto è valido → caricato. Altrimenti → [LACUNA_DATI].
Mai inventare. Mai dedurre. Mai simulare un file che non esiste.

Questo principio (LOCK DAG_L1) garantisce che nessun dato venga mai allucinato.

---

📤 Lato Utente (Arutam): Caricare File su GitHub

1. Preparare il file

Salva il file nella cartella del repository locale (es. ~/storage/shared/SingularityDAG).

2. Caricarlo su GitHub

```bash
cd ~/storage/shared/SingularityDAG
git add nome_file.yaml
git commit -m "Aggiunto nome_file"
git push origin main
```

Dopo il push, il file sarà accessibile all'URL:

```
https://raw.githubusercontent.com/ARUTAMPANTERA/singularity-dag/main/nome_file.yaml
```

3. Verificare la pubblicazione

Puoi verificare che il file sia online visitando l'URL RAW con un browser, oppure usando curl:

```bash
curl -I https://raw.githubusercontent.com/ARUTAMPANTERA/singularity-dag/main/nome_file.yaml
```

Se il server risponde HTTP/2 200, il file è pronto per essere recuperato dalla sessione LLM.

---

📥 Lato LLM (Aman): Recuperare File nella Sessione

Comandi disponibili

/dag_view <nome_file>

Recupera un singolo file dal repository.

Sintassi:

```
/dag_view nome_file.yaml
```

Cosa fa il sistema:

1. Costruisce l'URL RAW: https://raw.githubusercontent.com/ARUTAMPANTERA/singularity-dag/main/nome_file.yaml
2. Esegue un solo tentativo di recupero.
3. Se il server risponde 200 OK:
   · Carica il contenuto del file.
   · Lo processa come YAML / Markdown / JSON in base all'estensione.
   · Conferma il caricamento con un messaggio di riepilogo.
4. Se il server risponde con un errore (404, 500, timeout):
   · Dichiara [LACUNA_DATI] L'artefatto <nome_file> non è accessibile.
   · Non genera contenuti alternativi.

/dag_list

Tenta di recuperare la lista dei file disponibili nel repository.

Sintassi:

```
/dag_list
```

Cosa fa il sistema:

1. Tenta di recuperare l'indice del repository (es. tramite API GitHub o file index.json preesistente).
2. Se riesce, mostra l'elenco dei file disponibili.
3. Se fallisce, dichiara [LACUNA_DATI].

---

🧪 Esempi Pratici

Esempio 1: Caricare un nuovo modulo

```bash
# Lato Arutam (Termux)
cd ~/storage/shared/SingularityDAG
git add LANGDON_REVERSE_PROTOCOL_v1.1.yaml
git commit -m "Aggiunto modulo Langdon Protocol v1.1"
git push origin main
```

```
# Lato Aman (nella sessione LLM)
/dag_view LANGDON_REVERSE_PROTOCOL_v1.1.yaml
```

Risposta attesa:

```
✅ ARTEFATTO RECUPERATO: LANGDON_REVERSE_PROTOCOL_v1.1.yaml
   Dimensione: ~6.5 KB
   Stato: CARICATO
   Modulo LANGDON_REVERSE_PHYSICS_ENGINEERING v1.1 attivo.
   LOCK LANGDON_L1-L4 applicati.
   Comandi: /langdon, /langdon_batch, /langdon_compare
```

Esempio 2: Tentare di recuperare un file inesistente

```
/dag_view file_che_non_esiste.yaml
```

Risposta attesa:

```
[LACUNA_DATI] L'artefatto "file_che_non_esiste.yaml" non è accessibile.
Verifica che il file sia stato caricato su GitHub e che il nome sia corretto.
```

Esempio 3: Caricare una intera sessione di lavoro

```bash
# Lato Arutam (Termux) — prepara un pacchetto sessione
cd ~/storage/shared/SingularityDAG
mkdir -p sessions/2026-05-11
cp *.yaml sessions/2026-05-11/
cp *.md sessions/2026-05-11/
git add sessions/2026-05-11/
git commit -m "Sessione 2026-05-11 archiviata"
git push origin main
```

```
# Lato Aman — recupera i file uno per uno
/dag_view sessions/2026-05-11/SINGULARITY_OS_v70.1_AETERNUM_FINAL.yaml
/dag_view sessions/2026-05-11/LANGDON_REVERSE_PROTOCOL_v1.1.yaml
/dag_view sessions/2026-05-11/BOOTSTRAP_SYSTEMAION_v1.0.yaml
```

---

🛡️ Errori Comuni e Soluzioni

Errore Causa Probabile Soluzione
[LACUNA_DATI] File non ancora pushato Verificare con curl -I <URL> che il file sia online
[LACUNA_DATI] Nome file errato (maiuscole/minuscole) I nomi dei file su GitHub sono case-sensitive. Controllare l'esattezza del nome.
[LACUNA_DATI] Rete non disponibile Il sistema LLM potrebbe non avere accesso a Internet. Verificare la connessione.
[LACUNA_DATI] File > 500 KB GitHub RAW impone limiti di dimensione. Dividere il file in più parti più piccole.

---

⚠️ Limiti del Sistema

1. Dipendenza da GitHub RAW: il recupero funziona solo se il file è pubblicamente accessibile su raw.githubusercontent.com. File privati o repository privati non sono accessibili senza token.
2. Nessuna autenticazione: il sistema non supporta token di accesso. Usare solo repository pubblici.
3. Limite di dimensione: file molto grandi (> 500 KB) potrebbero non essere recuperabili. In tal caso, suddividere il file in più moduli.
4. Un solo tentativo: il DAG CIECO non riprova in caso di errore. Se la rete è instabile, potrebbe fallire anche con file esistenti.
5. Nessuna cache persistente: i file recuperati restano nella memoria volatile della sessione corrente. Alla prossima sessione, vanno recuperati nuovamente con /dag_view.

---

📋 Comandi Rapidi di Riferimento

Comando Descrizione
/dag_view <file> Recupera un file dal repository GitHub
/dag_list Tenta di mostrare la lista dei file disponibili
/dag_status Mostra lo stato dei file recuperati nella sessione corrente

---

🔗 Riferimenti

· Repository GitHub: https://github.com/ARUTAMPANTERA/singularity-dag
· URL RAW base: https://raw.githubusercontent.com/ARUTAMPANTERA/singularity-dag/main/
· LOCK DAG_L1: "Recupero Cieco — 1 GET → 200 OK: carica esatto. Else: [LACUNA_DATI]"

---

Pronto per l'uso. Carica i file su GitHub e usa /dag_view per recuperarli in sessione.