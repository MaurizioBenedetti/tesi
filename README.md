#Introduzione
Questo repository riguarda il project work per l'anno accademico 2024-2025 della matricola 0312300041, traccia 1.4.

Il codice presentato si prefigge di gestire un ipotetica catena di alberghi ed offre funzionalità base per la gestione delle prenotazioni quali creazione, visualizzazione, modifica e cancellazione.

Il progetto e' basato su di uno stack Django e presenta la recipe docker per implementare la soluzione con 3 componenti principali:

1. Container NGINX, che espone il servizio sulla porta 1337, per production use il file nginx.conf va ovviamente cambiato
2. Container gunicorn, che esegue l'applicazione Django
3. Container PostgreSQL, che esegue un container con PostgreSQL e volume persistente



#Come procedere con la build

Per eseguire la build della soluzione basta girare il docker compose con il seguente comando:

sudo docker compose up -d --build

Prima di eseguire la build, vale la pena customizzare il file .env presente nella root del progetto. Contiene dei valori di default che vanno customizzati, in partiolare le password di default di postgres e della Django admin.

La soluzione non prevede al momento la configurazione di una terminazione SSL, espone su porta 1337 HTTP non cifrato.


