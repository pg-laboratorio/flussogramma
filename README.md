# Flussogramma

Editor di **diagrammi di flusso** per imparare a programmare, pensato come passaggio verso **Python**.
Si disegna il diagramma con i blocchi, lo si esegue passo per passo e si vede subito il codice Python equivalente.

👉 **Apri l'applicazione:** https://pg-laboratorio.github.io/flussogramma/

Funziona nel browser, anche da tablet e telefono. Non serve installare nulla né creare un account.

---

## Come si usa

1. Clicca un **+** sulle frecce e scegli il blocco da inserire.
2. Clicca un blocco per modificarlo, copiarlo, tagliarlo o eliminarlo.
3. **Trascina** un blocco su un altro punto **+** per spostarlo, anche dentro un Se o un ciclo. Tieni premuto **Ctrl** mentre lo rilasci per farne una copia; **Esc** annulla. Da tastiera: seleziona il blocco con Tab e usa **Alt+↑ / Alt+↓**.
4. Con **Casella di testo** aggiungi un riquadro per il testo del problema, i dati di input e output o qualche appunto. Trascinalo dove vuoi, allargalo dal triangolino in basso a destra, cliccalo per modificarlo o cambiarne il colore. Le caselle non vengono eseguite e non compaiono nel codice, ma vengono salvate con il diagramma ed esportate nel PDF.
5. Premi **Esegui** per far girare il programma, oppure **Passo** per avanzare un blocco alla volta.
6. Guarda la **console** (output e input) e la tabella delle **variabili**. Il pulsante **Pannello**, in alto a destra, nasconde o mostra la colonna con console, variabili e codice per lasciare più spazio al diagramma; quando esegui il programma il pannello si riapre da solo.
7. Nella scheda **Codice** trovi il programma tradotto in Python e in pseudocodice.

Un blocco con il bordo rosso tratteggiato contiene un errore: cliccalo per leggere cosa non va.

## I blocchi

| Blocco | Forma | In Python |
|---|---|---|
| Assegna | rettangolo | `somma = somma + i` |
| Input | parallelogramma blu | `n = int(input("Inserisci n: "))` |
| Output | parallelogramma verde | `print(f"La somma è {somma}")` |
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
- L'**Input** può leggere un `int`, un `float`, un `str` o un `bool`. Per un `bool` si scrive `True` o `False` e in Python diventa `x = input() == "True"`.
- Per unire testo e numeri usa una f-string, con le variabili tra graffe: `f"La somma è {somma}"`, `f"Media: {media:.2f}"`.

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


## Licenza

Codice rilasciato con licenza [MIT](LICENSE).
