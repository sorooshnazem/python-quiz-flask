# Python Quiz Platform

Applicazione web sviluppata con **Flask** dedicata all'apprendimento e alla verifica delle conoscenze di Python.

Gli utenti possono registrarsi, effettuare il login, rispondere a quiz casuali, accumulare punti e confrontare il proprio risultato con quello degli altri utenti.

L'applicazione include inoltre un'area amministrativa protetta per la gestione delle domande del quiz.

## Demo online

L'applicazione è disponibile online su PythonAnywhere:

**https://sorooshnazem.pythonanywhere.com**

## Video demo

È disponibile un breve video dimostrativo:

[Guarda il video demo](docs/demo.mp4)

## Funzionalità principali

* Registrazione utenti
* Login e logout
* Gestione delle sessioni
* Password memorizzate tramite hashing
* Quiz con domande casuali
* Quattro opzioni per ogni domanda
* Verifica automatica della risposta
* Incremento del punteggio per ogni risposta corretta
* Salvataggio del punteggio nel database
* Classifica utenti
* Ruolo amministratore
* Area Admin protetta
* Aggiunta di nuove domande
* Modifica di domande e opzioni
* Eliminazione delle domande
* Selezione della risposta corretta tramite dropdown
* Interfaccia realizzata con Bootstrap

## Tecnologie utilizzate

### Backend

* Python
* Flask
* SQLite
* Werkzeug
* python-dotenv

### Frontend

* HTML
* Jinja2
* Bootstrap

### Deployment

* PythonAnywhere

## Struttura del progetto

```text
python-quiz-flask/
│
├── app.py
├── requirements.txt
├── pyproject.toml
├── README.md
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── quiz.html
│   ├── ranking.html
│   ├── admin.html
│   └── edit_question.html
│
└── docs/
    └── demo.mp4
```

## Database

L'applicazione utilizza SQLite.

### Tabella `users`

```text
users
├── id
├── username
├── password
├── nickname
├── score
└── role
```

Il campo `role` permette di distinguere tra:

```text
user
admin
```

### Tabella `questions`

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

## Quiz

Quando un utente autenticato accede al quiz, viene estratta casualmente una domanda dal database.

```text
Utente autenticato
        ↓
Domanda casuale
        ↓
Selezione risposta
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

La risposta corretta viene verificata dal backend utilizzando l'identificativo della domanda.

## Area Admin

L'area amministrativa è accessibile esclusivamente agli utenti con:

```text
role = admin
```

L'amministratore può:

* visualizzare le domande presenti
* aggiungere nuove domande
* modificare domanda e opzioni
* scegliere la risposta corretta
* eliminare domande

Questa sezione implementa quindi le principali operazioni CRUD:

```text
Create
Read
Update
Delete
```

## Installazione locale

Clonare il repository:

```bash
git clone https://github.com/sorooshnazem/python-quiz-flask.git
```

Entrare nella cartella:

```bash
cd python-quiz-flask
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

Aprire:

```text
http://127.0.0.1:5000
```

## Sicurezza

Le password degli utenti non vengono salvate in chiaro.

Werkzeug viene utilizzato per hashing e verifica delle password.

La `SECRET_KEY` di Flask viene caricata tramite variabile d'ambiente e il file `.env` non viene incluso nel repository Git.

Le route amministrative verificano inoltre che l'utente autenticato abbia ruolo `admin`.

## Evoluzione futura

Il progetto è pensato per essere esteso gradualmente.

Possibili sviluppi futuri:

* organizzazione dei quiz per argomento
* livelli di difficoltà
* lezioni Python
* monitoraggio dei progressi
* quiz associati alle lezioni
* nuovi corsi dedicati a Git e Bash

Queste funzionalità non sono ancora implementate e rappresentano possibili evoluzioni future della piattaforma.

## Autore

Progetto sviluppato da **Soroosh Nazem**.
