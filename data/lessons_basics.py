INTRODUCTION_BLOCKS = [

    (
        "text",
        """
Python è un linguaggio di programmazione molto utilizzato
e relativamente semplice da leggere.

Viene utilizzato in moltissimi ambiti, per esempio:

• sviluppo web
• automazione
• analisi dei dati
• machine learning
• intelligenza artificiale
• scripting

In questo corso impareremo Python gradualmente,
partendo dai concetti più semplici.
        """,
        1
    ),

    (
        "explanation",
        """
Un linguaggio di programmazione ci permette di dare
istruzioni a un computer.

Possiamo pensare a un programma come a una sequenza
di istruzioni che il computer esegue.
        """,
        2
    ),

    (
        "example",
        """
Per esempio, possiamo chiedere al computer di:

• mostrare un messaggio
• eseguire un calcolo
• memorizzare un risultato
• prendere una decisione
• ripetere un'operazione
        """,
        3
    ),

    (
        "code",
        """
print("Ciao Python")
print(2 + 3)
        """,
        4
    ),

    (
        "output",
        """
Ciao Python
5
        """,
        5
    ),

    (
        "explanation",
        """
Nel primo comando chiediamo a Python di mostrare un testo.

Nel secondo comando Python esegue prima il calcolo 2 + 3
e poi mostra il risultato.

Non preoccuparti ancora dei dettagli di print(), dei testi
o degli operatori matematici: li studieremo nelle prossime
lezioni.
        """,
        6
    ),

    (
    "text",
    """
Python ha una sintassi relativamente semplice.

Per esempio, per mostrare un messaggio possiamo usare:

print("Hello")
    """,
    7
),

(
    "code",
    """
print("Hello")
    """,
    8
),

(
    "explanation",
    """
La funzione print() permette di mostrare un valore
sullo schermo.

In questo caso stiamo mostrando il testo "Hello".

Nella prossima lezione studieremo print() in modo
più approfondito.
    """,
    9
),

(
    "warning",
    """
Python distingue tra lettere maiuscole e minuscole.

Questa caratteristica viene chiamata case sensitivity.

Per esempio:

print

e

Print

non sono la stessa cosa.
    """,
    10
),

(
    "code",
    """
print("Funziona")

Print("Non funziona")
    """,
    11
),

(
    "explanation",
    """
La prima istruzione è corretta.

La seconda genera un errore perché la funzione si chiama
print con la lettera p minuscola.

Python interpreta Print come un nome completamente diverso.
    """,
    12
),

(
    "exercise",
    """
Prova a scrivere il tuo primo programma Python.

Mostra sullo schermo il seguente messaggio:

Sto imparando Python

Suggerimento:

usa la funzione print().
    """,
    13
)
]

PRINT_BLOCKS = [

    (
        "text",
        """
print() è una delle prime funzioni che impariamo in Python.

Ci permette di mostrare informazioni sullo schermo.

Possiamo usarla per stampare testi, numeri,
risultati di calcoli e molti altri valori.
        """,
        1
    ),

    (
        "code",
        """
print("Ciao Python")
        """,
        2
    ),

    (
        "output",
        """
Ciao Python
        """,
        3
    ),

    (
        "explanation",
        """
Python legge il contenuto tra parentesi e lo mostra
nel terminale.

In questo esempio "Ciao Python" è un testo.

In Python un testo viene chiamato stringa e deve
normalmente essere scritto tra virgolette.
        """,
        4
    ),

    (
        "code",
        """
print(3)
print(3.14)
print("Ciao Python")
        """,
        5
    ),

    (
        "warning",
        """
Quando stampiamo un testo, dobbiamo usare le virgolette.

Per esempio, questo codice funziona correttamente:
        """,
        6
    ),

    (
        "code",
        """
print("Ciao")
        """,
        7
    ),

    (
        "warning",
        """
Questo invece genera un errore:
        """,
        8
    ),

    (
        "code",
        """
print(Ciao)
        """,
        9
    ),

    (
        "explanation",
        """
Senza virgolette Python interpreta Ciao come il nome
di una variabile.

Se la variabile Ciao non esiste, Python genera un errore.
        """,
        10
    ),

    (
        "text",
        """
Possiamo usare print() più volte nello stesso programma.
        """,
        11
    ),

    (
        "code",
        """
print("Nome: Marco")
print("Età: 25")
print("Corso: Python")
        """,
        12
    ),

    (
        "output",
        """
Nome: Marco
Età: 25
Corso: Python
        """,
        13
    ),

    (
        "explanation",
        """
Ogni chiamata a print() mostra normalmente il proprio
contenuto su una nuova riga.

Per questo otteniamo tre righe nell'output.
        """,
        14
    ),

    (
        "exercise",
        """
Scrivi un programma che utilizzi tre print().

Il programma deve mostrare:

1. Il tuo nome
2. La tua città
3. Il linguaggio che stai studiando

Esempio di output:

Soroosh
Torino
Python
        """,
        15
    )
]

VARIABLES_BLOCKS = [

    (
        "text",
        """
Una variabile è un nome che utilizziamo per memorizzare un valore.

Possiamo immaginare una variabile come una scatola con un'etichetta.

L'etichetta è il nome della variabile.
Dentro la scatola troviamo il valore.
        """,
        1
    ),

    (
        "code",
        """
name = "Marco"
        """,
        2
    ),

    (
        "explanation",
        """
In questo esempio:

name è il nome della variabile.

= è l'operatore di assegnazione.

"Marco" è il valore che viene memorizzato nella variabile.
        """,
        3
    ),

    (
        "example",
        """
Possiamo visualizzare il valore di una variabile usando print().
        """,
        4
    ),

    (
        "code",
        """
name = "Marco"

print(name)
        """,
        5
    ),

    (
        "output",
        """
Marco
        """,
        6
    ),

    (
        "text",
        """
Una variabile può contenere tipi di dati diversi.

Per esempio possiamo memorizzare:

- testo
- numeri interi
- numeri decimali
- valori booleani
        """,
        7
    ),

    (
        "code",
        """
name = "Anna"
age = 25
height = 1.68
is_student = True
        """,
        8
    ),

    (
        "explanation",
        """
Qui abbiamo quattro variabili diverse:

name contiene un testo.

age contiene un numero intero.

height contiene un numero decimale.

is_student contiene un valore booleano.
        """,
        9
    ),

    (
        "text",
        """
Il valore di una variabile può cambiare durante l'esecuzione
del programma.
        """,
        10
    ),

    (
        "code",
        """
score = 10

print(score)

score = 20

print(score)
        """,
        11
    ),

    (
        "output",
        """
10
20
        """,
        12
    ),

    (
        "explanation",
        """
All'inizio score contiene 10.

Successivamente assegniamo il valore 20 alla stessa variabile.

Il vecchio valore viene sostituito.
        """,
        13
    ),

    (
        "warning",
        """
Il simbolo = in Python significa assegnazione.

Non significa "uguale" nel senso matematico.

Quando scriviamo:

x = 5

stiamo dicendo:

assegna il valore 5 alla variabile x.
        """,
        14
    ),

    (
        "code",
        """
x = 5
y = x

print(y)
        """,
        15
    ),

    (
        "output",
        """
5
        """,
        16
    ),

    (
        "explanation",
        """
Quando scriviamo:

y = x

Python prende il valore attualmente contenuto in x
e lo assegna a y.

Dato che x contiene 5, anche y conterrà 5.
        """,
        17
    ),

    (
        "text",
        """
I nomi delle variabili devono seguire alcune regole.

Sono validi, per esempio:
        """,
        18
    ),

    (
        "code",
        """
name = "Luca"
user_age = 30
score2 = 100
        """,
        19
    ),

    (
        "warning",
        """
Un nome di variabile:

- non può iniziare con un numero
- non può contenere spazi
- non dovrebbe usare parole riservate di Python
- distingue tra maiuscole e minuscole
        """,
        20
    ),

    (
        "code",
        """
age = 25
Age = 40

print(age)
print(Age)
        """,
        21
    ),

    (
        "output",
        """
25
40
        """,
        22
    ),

    (
        "explanation",
        """
age e Age sono due variabili diverse.

Python è case-sensitive, quindi distingue tra lettere
maiuscole e minuscole.
        """,
        23
    ),

    (
        "example",
        """
Vediamo ora un esempio leggermente più realistico.

Creiamo alcune variabili per descrivere uno studente.
        """,
        24
    ),

    (
        "code",
        """
student_name = "Sara"
student_age = 22
course = "Python"
score = 85

print(student_name)
print(student_age)
print(course)
print(score)
        """,
        25
    ),

    (
        "output",
        """
Sara
22
Python
85
        """,
        26
    ),

    (
        "exercise",
        """
Crea quattro variabili:

name
age
city
language

Inserisci valori a tua scelta.

Poi utilizza print() per mostrare tutte le variabili.
        """,
        27
    ),

    (
        "exercise",
        """
Esercizio un po' più difficile.

Crea una variabile chiamata score con valore 10.

Stampala.

Poi cambia il suo valore in 25 e stampala nuovamente.

Quale sarà l'output?
        """,
        28
    )
]

DATA_TYPES_BLOCKS = [

    (
        "text",
        """
In Python ogni valore ha un tipo.

Il tipo ci dice che genere di informazione stiamo utilizzando
e quali operazioni possiamo eseguire su quel valore.

In questa lezione vedremo quattro tipi fondamentali:

• str   → testo
• int   → numeri interi
• float → numeri decimali
• bool  → valori True o False
        """,
        1
    ),

    (
        "example",
        """
Vediamo subito quattro valori diversi.
        """,
        2
    ),

    (
        "code",
        """
name = "Anna"
age = 25
height = 1.68
is_student = True
        """,
        3
    ),

    (
        "explanation",
        """
Le quattro variabili contengono tipi diversi:

name contiene una stringa (str).

age contiene un numero intero (int).

height contiene un numero decimale (float).

is_student contiene un valore booleano (bool).
        """,
        4
    ),

    # ---------------------------------------------------------
    # STRING
    # ---------------------------------------------------------

    (
        "text",
        """
1. Stringhe — str

Una stringa rappresenta del testo.

Le stringhe vengono normalmente scritte tra virgolette.
        """,
        5
    ),

    (
        "code",
        """
name = "Marco"
city = "Torino"
language = "Python"

print(name)
print(city)
print(language)
        """,
        6
    ),

    (
        "output",
        """
Marco
Torino
Python
        """,
        7
    ),

    (
        "explanation",
        """
Anche un testo composto da numeri rimane una stringa
se viene scritto tra virgolette.

Per esempio:

"25"

non è la stessa cosa di:

25
        """,
        8
    ),

    (
        "code",
        """
age_text = "25"
age_number = 25
        """,
        9
    ),

    (
        "warning",
        """
"25" e 25 sembrano simili quando li leggiamo,
ma per Python sono valori di tipo diverso.

"25" è una stringa.

25 è un numero intero.

Questa differenza diventerà molto importante quando
inizieremo a fare calcoli e conversioni.
        """,
        10
    ),

    # ---------------------------------------------------------
    # INTEGER
    # ---------------------------------------------------------

    (
        "text",
        """
2. Numeri interi — int

Il tipo int rappresenta numeri interi,
cioè numeri senza parte decimale.

Possono essere positivi, negativi oppure zero.
        """,
        11
    ),

    (
        "code",
        """
age = 25
temperature = -3
score = 0

print(age)
print(temperature)
print(score)
        """,
        12
    ),

    (
        "output",
        """
25
-3
0
        """,
        13
    ),

    (
        "example",
        """
Con i numeri possiamo eseguire operazioni matematiche.
        """,
        14
    ),

    (
        "code",
        """
a = 10
b = 5

print(a + b)
print(a - b)
print(a * b)
        """,
        15
    ),

    (
        "output",
        """
15
5
50
        """,
        16
    ),

    # ---------------------------------------------------------
    # FLOAT
    # ---------------------------------------------------------

    (
        "text",
        """
3. Numeri decimali — float

Il tipo float viene utilizzato per rappresentare
numeri con una parte decimale.

In Python utilizziamo il punto e non la virgola
come separatore decimale.
        """,
        17
    ),

    (
        "code",
        """
height = 1.75
price = 9.99
temperature = -2.5

print(height)
print(price)
print(temperature)
        """,
        18
    ),

    (
        "output",
        """
1.75
9.99
-2.5
        """,
        19
    ),

    (
        "warning",
        """
Scrivere:

price = 9.99

è corretto.

Scrivere:

price = 9,99

non rappresenta il numero decimale 9.99 in Python.

Per i numeri decimali utilizziamo il punto.
        """,
        20
    ),

    # ---------------------------------------------------------
    # BOOLEAN
    # ---------------------------------------------------------

    (
        "text",
        """
4. Boolean — bool

Un valore booleano può avere soltanto due valori:

True
False

I booleani vengono utilizzati per rappresentare
condizioni vere o false.
        """,
        21
    ),

    (
        "code",
        """
is_student = True
is_admin = False

print(is_student)
print(is_admin)
        """,
        22
    ),

    (
        "output",
        """
True
False
        """,
        23
    ),

    (
        "warning",
        """
True e False iniziano con una lettera maiuscola.

Quindi:

True

è corretto.

true

non rappresenta il valore booleano True in Python.
        """,
        24
    ),

    # ---------------------------------------------------------
    # TYPE()
    # ---------------------------------------------------------

    (
        "text",
        """
Come possiamo sapere il tipo di un valore?

Python mette a disposizione la funzione type().

type() ci permette di controllare il tipo di un valore
o di una variabile.
        """,
        25
    ),

    (
        "code",
        """
name = "Sara"
age = 30
height = 1.70
is_student = True

print(type(name))
print(type(age))
print(type(height))
print(type(is_student))
        """,
        26
    ),

    (
        "output",
        """
<class 'str'>
<class 'int'>
<class 'float'>
<class 'bool'>
        """,
        27
    ),

    (
        "explanation",
        """
L'output di type() ci permette di identificare
il tipo di ogni variabile.

str significa string.

int significa integer.

float rappresenta un numero decimale.

bool significa boolean.
        """,
        28
    ),

    # ---------------------------------------------------------
    # TYPES CAN CHANGE
    # ---------------------------------------------------------

    (
        "text",
        """
In Python una variabile può anche ricevere successivamente
un valore di tipo diverso.
        """,
        29
    ),

    (
        "code",
        """
value = 10

print(value)
print(type(value))

value = "Hello"

print(value)
print(type(value))
        """,
        30
    ),

    (
        "output",
        """
10
<class 'int'>
Hello
<class 'str'>
        """,
        31
    ),

    (
        "explanation",
        """
All'inizio value contiene il numero intero 10.

Successivamente assegniamo alla stessa variabile
la stringa "Hello".

Python permette quindi alla stessa variabile di contenere,
in momenti diversi, valori di tipo diverso.
        """,
        32
    ),

    # ---------------------------------------------------------
    # COMPARISON
    # ---------------------------------------------------------

    (
        "example",
        """
Confrontiamo ora alcuni valori che sembrano simili.
        """,
        33
    ),

    (
        "code",
        """
a = 10
b = 10.0
c = "10"
d = True

print(type(a))
print(type(b))
print(type(c))
print(type(d))
        """,
        34
    ),

    (
        "output",
        """
<class 'int'>
<class 'float'>
<class 'str'>
<class 'bool'>
        """,
        35
    ),

    (
        "explanation",
        """
Anche se alcuni valori possono sembrare simili,
il loro tipo può essere completamente diverso.

10 è int.

10.0 è float.

"10" è str.

True è bool.

Capire questa differenza è fondamentale per evitare
molti errori nei programmi Python.
        """,
        36
    ),

    # ---------------------------------------------------------
    # EXERCISES
    # ---------------------------------------------------------

    (
        "exercise",
        """
Crea quattro variabili:

name = il tuo nome
age = la tua età
height = la tua altezza
is_student = True oppure False

Poi stampa il valore di tutte le variabili.
        """,
        37
    ),

    (
        "exercise",
        """
Ora usa type() per scoprire il tipo delle quattro variabili
dell'esercizio precedente.

Prima di eseguire il programma, prova a prevedere
quale sarà il risultato.
        """,
        38
    ),

    (
        "exercise",
        """
Qual è il tipo di ciascuno dei seguenti valori?

"100"

100

100.5

False

"True"

Prova prima a rispondere senza eseguire il codice.

Poi verifica le tue risposte usando type().
        """,
        39
    )
]

INPUT_BLOCKS = [

    (
        "text",
        """
Finora i nostri programmi utilizzavano valori scritti
direttamente nel codice.

Ma spesso vogliamo che sia l'utente a inserire
un'informazione.

In Python possiamo farlo con la funzione input().
        """,
        1
    ),

    (
        "example",
        """
Vediamo il caso più semplice.

Il programma aspetta che l'utente scriva qualcosa
e prema Invio.
        """,
        2
    ),

    (
        "code",
        """
input()
        """,
        3
    ),

    (
        "explanation",
        """
Quando Python incontra input(), il programma si ferma
temporaneamente e aspetta un valore inserito dall'utente.

Dopo che l'utente preme Invio, il programma può continuare.
        """,
        4
    ),

    # ---------------------------------------------------------
    # PROMPT
    # ---------------------------------------------------------

    (
        "text",
        """
Possiamo inserire un messaggio dentro input() per spiegare
all'utente che cosa deve scrivere.

Questo messaggio viene spesso chiamato prompt.
        """,
        5
    ),

    (
        "code",
        """
input("Come ti chiami? ")
        """,
        6
    ),

    (
        "example",
        """
Durante l'esecuzione potremmo vedere:

Come ti chiami? Marco

In questo esempio "Marco" è stato scritto dall'utente,
non dal programmatore.
        """,
        7
    ),

    # ---------------------------------------------------------
    # SAVE INPUT
    # ---------------------------------------------------------

    (
        "text",
        """
Normalmente non vogliamo soltanto ricevere il valore.

Vogliamo anche conservarlo per poterlo utilizzare
successivamente.

Possiamo quindi salvare il risultato di input()
dentro una variabile.
        """,
        8
    ),

    (
        "code",
        """
name = input("Come ti chiami? ")

print(name)
        """,
        9
    ),

    (
        "example",
        """
Se l'utente scrive:

Sara

il risultato sarà:

Come ti chiami? Sara
Sara
        """,
        10
    ),

    (
        "explanation",
        """
Vediamo cosa succede passo dopo passo.

1. Python esegue input().
2. Il programma mostra "Come ti chiami?".
3. L'utente scrive Sara.
4. input() restituisce "Sara".
5. Il valore viene assegnato alla variabile name.
6. print(name) mostra il valore salvato.
        """,
        11
    ),

    # ---------------------------------------------------------
    # USE THE VALUE
    # ---------------------------------------------------------

    (
        "text",
        """
Una volta memorizzato il valore in una variabile,
possiamo utilizzarlo più volte.
        """,
        12
    ),

    (
        "code",
        """
name = input("Come ti chiami? ")

print("Ciao!")
print(name)
        """,
        13
    ),

    (
        "example",
        """
Se l'utente inserisce Luca:

Come ti chiami? Luca
Ciao!
Luca
        """,
        14
    ),

    # ---------------------------------------------------------
    # MULTIPLE INPUTS
    # ---------------------------------------------------------

    (
        "text",
        """
Un programma può chiedere più informazioni all'utente.

Ogni risposta può essere memorizzata in una variabile
diversa.
        """,
        15
    ),

    (
        "code",
        """
name = input("Nome: ")
city = input("Città: ")
language = input("Linguaggio preferito: ")

print(name)
print(city)
print(language)
        """,
        16
    ),

    (
        "example",
        """
Una possibile esecuzione è:

Nome: Anna
Città: Torino
Linguaggio preferito: Python

Anna
Torino
Python
        """,
        17
    ),

    # ---------------------------------------------------------
    # IMPORTANT: INPUT RETURNS STRING
    # ---------------------------------------------------------

    (
        "text",
        """
C'è una caratteristica molto importante di input():

il valore restituito da input() è una stringa.

Questo succede anche quando l'utente inserisce
soltanto numeri.
        """,
        18
    ),

    (
        "code",
        """
age = input("Quanti anni hai? ")

print(age)
print(type(age))
        """,
        19
    ),

    (
        "example",
        """
Supponiamo che l'utente inserisca:

25

L'output di type(age) sarà:

<class 'str'>
        """,
        20
    ),

    (
        "explanation",
        """
Anche se l'utente ha scritto 25, Python ha ricevuto
il valore come testo.

Quindi:

25

in questo caso viene trattato come:

"25"

Il tipo della variabile age è quindi str, non int.
        """,
        21
    ),

    # ---------------------------------------------------------
    # COMMON PROBLEM
    # ---------------------------------------------------------

    (
        "warning",
        """
Questo può creare problemi quando vogliamo fare
operazioni matematiche.

Per esempio, questo codice non funziona come potremmo
aspettarci:

age = input("Età: ")
next_age = age + 1

Il problema è che age è una stringa mentre 1 è un intero.

Prima di fare il calcolo dobbiamo convertire il valore.

Vedremo come farlo nella prossima lezione:
Type Conversion.
        """,
        22
    ),

    # ---------------------------------------------------------
    # EXERCISES
    # ---------------------------------------------------------

    (
        "exercise",
        """
Crea un programma che chieda all'utente il suo nome.

Salva la risposta in una variabile chiamata name.

Poi mostra il valore usando print().
        """,
        23
    ),

    (
        "exercise",
        """
Crea un programma che chieda:

- nome
- città
- linguaggio di programmazione preferito

Salva ogni risposta in una variabile diversa
e poi mostra tutte le risposte.
        """,
        24
    ),

    (
        "exercise",
        """
Prova questo programma:

age = input("Inserisci la tua età: ")

print(age)
print(type(age))

Inserisci un numero come 20.

Prima di eseguire il programma prova a prevedere:

Quale sarà il valore di age?

Quale sarà il suo tipo?
        """,
        25
    )
]

TYPE_CONVERSION_BLOCKS = [

    (
        "text",
        """
A volte abbiamo un valore di un certo tipo,
ma abbiamo bisogno di utilizzarlo come un altro tipo.

Python ci permette di convertire un valore
da un tipo a un altro.

Questa operazione viene chiamata type conversion
o type casting.

In questa lezione vedremo principalmente:

• int()
• float()
• str()
• bool()
        """,
        1
    ),

    # ---------------------------------------------------------
    # WHY CONVERSION?
    # ---------------------------------------------------------

    (
        "text",
        """
Per capire perché la conversione è importante,
riprendiamo il problema visto nella lezione su input().

Ricorda:

input() restituisce sempre una stringa.
        """,
        2
    ),

    (
        "code",
        """
age = input("Quanti anni hai? ")

print(type(age))
        """,
        3
    ),

    (
        "example",
        """
Se l'utente inserisce:

25

type(age) restituisce:

<class 'str'>
        """,
        4
    ),

    (
        "warning",
        """
Questo significa che non possiamo semplicemente scrivere:

age = input("Età: ")
next_age = age + 1

age è una stringa.

1 è un numero intero.

Prima dobbiamo convertire age.
        """,
        5
    ),

    # ---------------------------------------------------------
    # INT()
    # ---------------------------------------------------------

    (
        "text",
        """
1. int()

La funzione int() prova a convertire un valore
in un numero intero.
        """,
        6
    ),

    (
        "code",
        """
age = "25"

age = int(age)

print(age)
print(type(age))
        """,
        7
    ),

    (
        "output",
        """
25
<class 'int'>
        """,
        8
    ),

    (
        "explanation",
        """
All'inizio age contiene:

"25"

quindi è una stringa.

Con:

int(age)

convertiamo "25" nel numero intero 25.

Dopo la conversione possiamo utilizzare age
nei calcoli matematici.
        """,
        9
    ),

    # ---------------------------------------------------------
    # INPUT + INT
    # ---------------------------------------------------------

    (
        "text",
        """
Ora possiamo risolvere il problema della lezione precedente.
        """,
        10
    ),

    (
        "code",
        """
age = input("Quanti anni hai? ")

age = int(age)

next_age = age + 1

print(next_age)
        """,
        11
    ),

    (
        "example",
        """
Se l'utente inserisce:

25

il programma calcola:

25 + 1

e mostra:

26
        """,
        12
    ),

    (
        "explanation",
        """
Seguiamo il programma passo dopo passo.

1. L'utente inserisce 25.

2. input() restituisce "25".

3. int(age) converte "25" in 25.

4. age + 1 diventa 25 + 1.

5. Il risultato è 26.
        """,
        13
    ),

    # ---------------------------------------------------------
    # SHORTER VERSION
    # ---------------------------------------------------------

    (
        "text",
        """
Possiamo anche eseguire input() e int()
nella stessa istruzione.
        """,
        14
    ),

    (
        "code",
        """
age = int(input("Quanti anni hai? "))

print(age + 1)
        """,
        15
    ),

    (
        "explanation",
        """
Python esegue prima la funzione più interna:

input()

e successivamente:

int()

Possiamo immaginare il flusso così:

input → stringa → int → numero intero
        """,
        16
    ),

    # ---------------------------------------------------------
    # FLOAT()
    # ---------------------------------------------------------

    (
        "text",
        """
2. float()

La funzione float() converte un valore
in un numero decimale.
        """,
        17
    ),

    (
        "code",
        """
price = "19.99"

price = float(price)

print(price)
print(type(price))
        """,
        18
    ),

    (
        "output",
        """
19.99
<class 'float'>
        """,
        19
    ),

    (
        "example",
        """
Possiamo utilizzarlo anche direttamente con input().
        """,
        20
    ),

    (
        "code",
        """
height = float(input("Inserisci la tua altezza: "))

print(height)
print(type(height))
        """,
        21
    ),

    # ---------------------------------------------------------
    # STR()
    # ---------------------------------------------------------

    (
        "text",
        """
3. str()

str() converte un valore in una stringa.
        """,
        22
    ),

    (
        "code",
        """
age = 25

age_text = str(age)

print(age_text)
print(type(age_text))
        """,
        23
    ),

    (
        "output",
        """
25
<class 'str'>
        """,
        24
    ),

    (
        "explanation",
        """
Il valore visualizzato sembra ancora 25.

Ma il tipo è cambiato.

Prima avevamo:

25      → int

Dopo str():

"25"    → str

Questa distinzione è molto importante:
il modo in cui un valore appare sullo schermo
non ci dice necessariamente quale sia il suo tipo.
        """,
        25
    ),

    # ---------------------------------------------------------
    # BOOL()
    # ---------------------------------------------------------

    (
        "text",
        """
4. bool()

Python permette anche di convertire valori
in booleani utilizzando bool().

Per ora vediamo soltanto alcuni esempi semplici.
Studieremo i booleani più approfonditamente
quando parleremo delle condizioni.
        """,
        26
    ),

    (
        "code",
        """
print(bool(1))
print(bool(0))
print(bool("Python"))
print(bool(""))
        """,
        27
    ),

    (
        "output",
        """
True
False
True
False
        """,
        28
    ),

    (
        "explanation",
        """
In questi esempi:

1 diventa True.

0 diventa False.

Una stringa non vuota come "Python" diventa True.

Una stringa vuota "" diventa False.

Approfondiremo questo comportamento più avanti.
        """,
        29
    ),

    # ---------------------------------------------------------
    # INVALID CONVERSION
    # ---------------------------------------------------------

    (
        "warning",
        """
Non tutte le conversioni sono possibili.

Per esempio:

int("25")

funziona perché "25" rappresenta un numero intero.

Ma:

int("hello")

non può essere convertito in un numero.
        """,
        30
    ),

    (
        "code",
        """
number = int("hello")
        """,
        31
    ),

    (
        "explanation",
        """
Questo codice genera un ValueError.

Python non sa trasformare la parola "hello"
in un numero intero.

Più avanti, nella sezione Exceptions,
impareremo a gestire correttamente questi errori.
        """,
        32
    ),

    # ---------------------------------------------------------
    # COMPLETE EXAMPLE
    # ---------------------------------------------------------

    (
        "example",
        """
Mettiamo insieme ciò che abbiamo imparato finora.

Creiamo un piccolo programma che chiede
due numeri all'utente e calcola la loro somma.
        """,
        33
    ),

    (
        "code",
        """
number1 = int(input("Primo numero: "))
number2 = int(input("Secondo numero: "))

result = number1 + number2

print(result)
        """,
        34
    ),

    (
        "example",
        """
Se l'utente inserisce:

Primo numero: 10
Secondo numero: 5

il programma mostra:

15
        """,
        35
    ),

    (
        "explanation",
        """
Questo piccolo programma utilizza già diversi
concetti studiati nelle lezioni precedenti:

input() riceve i valori.

int() li converte.

Le variabili memorizzano i valori.

+ esegue il calcolo.

print() mostra il risultato.
        """,
        36
    ),

    # ---------------------------------------------------------
    # EXERCISES
    # ---------------------------------------------------------

    (
        "exercise",
        """
Chiedi all'utente la sua età.

Converti il valore in int.

Poi mostra l'età che avrà l'anno prossimo.

Esempio:

Età: 20

Output:

21
        """,
        37
    ),

    (
        "exercise",
        """
Chiedi all'utente il prezzo di un prodotto.

Usa float() per convertire il valore.

Poi stampa il prezzo.
        """,
        38
    ),

    (
        "exercise",
        """
Crea un piccolo programma che chieda due numeri
all'utente.

Converti entrambi in int.

Calcola e mostra:

• somma
• differenza
• prodotto

Prova prima a costruirlo da solo usando soltanto
quello che hai imparato finora.
        """,
        39
    )
]