# Python Quiz Web Application

Applicazione web sviluppata con **Flask** che permette agli utenti di registrarsi, effettuare il login, partecipare a un quiz, accumulare punti e confrontare il proprio risultato con quello degli altri utenti.

L'applicazione include inoltre una sezione meteo che consente di cercare una città e visualizzare le previsioni per i tre giorni successivi tramite API esterna.

## Demo online

L'applicazione è disponibile online su PythonAnywhere:

**https://sorooshnazem.pythonanywhere.com**

## Video demo

È disponibile un breve video dimostrativo che mostra la navigazione tra le principali funzionalità dell'applicazione:

[Guarda il video demo](docs/demo.mp4)

## Funzionalità principali

* Registrazione di nuovi utenti
* Controllo dell'unicità di username e nickname
* Verifica della conferma password
* Password salvate tramite hashing
* Login e logout
* Gestione della sessione utente
* Accesso protetto alla pagina del quiz
* Domande estratte casualmente dal database
* Quattro possibili risposte per ogni domanda
* Verifica automatica della risposta
* Incremento del punteggio di 10 punti per ogni risposta corretta
* Salvataggio del punteggio nel database
* Classifica degli utenti ordinata per punteggio
* Ricerca meteo tramite città
* Previsioni meteo per tre giorni
* Interfaccia realizzata con Bootstrap
* Deploy dell'applicazione su PythonAnywhere

## Tecnologie utilizzate

### Backend

* Python
* Flask
* SQLite
* Werkzeug
* Python Dotenv

### Frontend

* HTML
* Jinja2
* Bootstrap

### API

* Open-Meteo Geocoding API
* Open-Meteo Forecast API

### Deployment

* PythonAnywhere

## Struttura del progetto

```text
python_quiz_project/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── quiz.html
│   └── ranking.html
│
├── static/
│
└── docs/
    └── demo.mp4
```

## Database

L'applicazione utilizza un database SQLite.

La tabella `users` contiene le informazioni principali degli utenti:

```text
users
├── id
├── username
├── password
├── nickname
└── score
```

La tabella `questions` contiene le domande del quiz:

```text
questions
├── id
├── question
├── option1
├── option2
├── option3
├── option4
└── correct_answer
```

Il database viene inizializzato automaticamente dall'applicazione se non è già presente.

## Quiz

Quando un utente autenticato accede alla pagina del quiz, viene estratta casualmente una domanda dal database.

Il flusso principale è:

```text
Utente autenticato
        ↓
Domanda casuale
        ↓
Selezione della risposta
        ↓
Verifica nel database
        ↓
Risposta corretta?
       / \
     sì   no
      |    |
   +10     0
      |
Aggiornamento punteggio
```

La risposta corretta non viene inviata direttamente al browser. Il frontend invia l'identificativo della domanda e il backend recupera dal database la risposta corretta.

## Meteo

L'utente può inserire il nome di una città nella Home Page.

Il processo è composto da due chiamate API:

```text
Nome città
    ↓
Open-Meteo Geocoding API
    ↓
Latitudine + Longitudine
    ↓
Open-Meteo Forecast API
    ↓
Previsioni per 3 giorni
```

Per ogni giorno vengono mostrati:

* giorno della settimana
* data
* temperatura massima
* temperatura minima
* condizioni meteorologiche

## Installazione locale

Clonare il repository:

```bash
git clone <URL_DEL_REPOSITORY>
```

Entrare nella cartella:

```bash
cd python_quiz_project
```

Creare un ambiente virtuale:

```bash
python -m venv venv
```

Attivarlo su Windows:

```bash
venv\Scripts\activate
```

Su Linux/macOS:

```bash
source venv/bin/activate
```

Installare le dipendenze:

```bash
pip install -r requirements.txt
```

Creare un file `.env` nella root del progetto:

```text
SECRET_KEY=your-secret-key
```

Avviare l'applicazione:

```bash
python app.py
```

Aprire quindi:

```text
http://127.0.0.1:5000
```

## Sicurezza

Le password degli utenti non vengono salvate in chiaro nel database.

L'applicazione utilizza le funzioni di hashing di Werkzeug per memorizzare e verificare le password.

La `SECRET_KEY` di Flask viene caricata tramite variabile d'ambiente e il file `.env` non viene incluso nel repository Git.

## Autore

Progetto sviluppato da **Soroosh Nazem**.
