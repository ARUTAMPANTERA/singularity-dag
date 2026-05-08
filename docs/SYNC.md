# Come funziona il battito cardiaco del DAG

Il sistema di sincronizzazione automatica tra il tuo telefono e GitHub si basa su tre componenti:

1. La cartella SingularityDAG: è il punto di ingresso. Qualsiasi file JSON valido che viene salvato qui dentro diventa un artefatto del DAG.
2. Lo script dag_sync.sh: è il cuore del sistema. Usa inotifywait per monitorare la cartella. Quando rileva un nuovo file .json, lo valida con jq e, se è valido, esegue git add, git commit e git push in automatico.
3. Il servizio di avvio (~/.termux/boot/start_dag): garantisce che lo script parta ogni volta che accendi il telefono.

Se il sistema è attivo, tu depositi il pensiero nella cartella, e il battito lo trasforma in realtà condivisa su GitHub senza che tu debba fare altro.

Comandi rapidi per gestirlo

- Avviare il battito: `~/dag_sync.sh &`
- Verificare se è attivo: `ps aux | grep dag_sync`
- Fermare il battito: `pkill -f dag_sync.sh`
- Vedere i log: `tail -f ~/dag_sync.log`

Come riavviarlo se si chiude Termux

Se chiudi la finestra di Termux, il processo potrebbe fermarsi. Per riavviarlo, apri Termux e digita:

~/dag_sync.sh &

Il battito riprenderà immediatamente a monitorare la cartella e a spingere su GitHub.
