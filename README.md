# Flussogramma

Editor di **diagrammi di flusso** per imparare a programmare, pensato come passaggio verso **Python**.
Si disegna il diagramma con i blocchi, lo si esegue passo per passo e si vede subito il codice Python equivalente.

👉 **Apri l'applicazione:** https://pg-laboratorio.github.io/flussogramma/

Funziona nel browser, anche da tablet e telefono. Non serve installare nulla né creare un account.

---

## Come si usa

1. Clicca un **+** sulle frecce e scegli il blocco da inserire.
2. Clicca un blocco per modificarlo, copiarlo, tagliarlo o eliminarlo.
3. Premi **Esegui** per far girare il programma, oppure **Passo** per avanzare un blocco alla volta.
4. Guarda la **console** (output e input) e la tabella delle **variabili**.
5. Nella scheda **Codice** trovi il programma tradotto in Python e in pseudocodice.

Un blocco con il bordo rosso tratteggiato contiene un errore: cliccalo per leggere cosa non va.

## I blocchi

| Blocco | Forma | In Python |
|---|---|---|
| Assegna | rettangolo | `somma = somma + i` |
| Input | parallelogramma blu | `n = int(input("Inserisci n: "))` |
| Output | parallelogramma verde | `print("La somma è", somma)` |
| Se (if) | rombo rosso | `if n % 2 == 0:` … `else:` |
| Mentre (while) | rombo viola | `while n > 0:` |
| Per (for) | esagono viola | `for i in range(1, 11):` |
| Ripeti… mentre | rombo viola in fondo | `while True:` … `if not (...): break` |
| Commento | nota | `# testo` |

## Le regole sono quelle di Python

- **Le variabili non si dichiarano**: nascono la prima volta che ricevono un valore (Assegna, Input o ciclo `for`).
- Maiuscole e minuscole contano: `Somma` e `somma` sono variabili diverse.
- I tipi sono quelli di Python: `int`, `float`, `str`, `bool`, `list`. Per esempio `10 / 2` vale `5.0`.
- Il ciclo **Per** funziona come `range()`: la **fine è esclusa**. Per contare da 1 a 10 scrivi Inizio `1` e Fine `11`.
- Per unire testo e numeri usa la virgola nell'Output, `str(x)` oppure una f-string: `f"Media: {media:.2f}"`.

Operatori e funzioni disponibili:

```
+  -  *  /  //  %  **          ==  !=  <  >  <=  >=  in
and  or  not  True  False  None
abs int float str bool len round min max sum sorted list
math.sqrt math.floor math.ceil math.pi math.log
random.randint(a, b) random.random() random.choice(lista)
lista.append(x)  lista.pop()  testo.upper()  testo.split()  ...
```

## Salvare e consegnare il lavoro

- Il diagramma resta salvato **nel browser** che stai usando (non su altri computer).
- **Salva / Apri → Scarica file .json** salva il diagramma come file: è quello da consegnare o da riaprire in seguito.
- **Esporta PDF** crea un PDF da stampare (una pagina o più pagine, con il codice Python in fondo se vuoi) oppure un'immagine PNG.

## Per il docente

L'applicazione è un unico file `index.html`, senza server e senza raccolta di dati.
La libreria per i PDF ([jsPDF](https://github.com/parallax/jsPDF), licenza MIT) è inclusa nella cartella `vendor/`, così l'esportazione funziona anche se la rete della scuola blocca i CDN.

Per pubblicarla su GitHub Pages: **Settings → Pages → Build and deployment → Deploy from a branch**, ramo `main`, cartella `/ (root)`.

## Licenza

Codice rilasciato con licenza [MIT](LICENSE).
