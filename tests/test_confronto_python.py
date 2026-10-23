"""
Test di confronto tra Flussogramma e Python vero.

Per ogni diagramma di prova:
  1. lo esegue nell'app (browser headless) con gli input indicati;
  2. prende il codice Python generato dall'app e lo esegue con python3, con gli stessi input;
  3. confronta l'output riga per riga e, nei casi di errore, verifica che sbaglino entrambi
     nello stesso punto.

Uso (serve Python 3 con Playwright):
    pip install playwright && playwright install chromium
    python3 tests/test_confronto_python.py [percorso/index.html]
"""
import json, os, subprocess, sys, tempfile
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'index.html'))

# ---------- costruttori dei blocchi ----------
def A(t, e): return {'t': 'assign', 'target': t, 'expr': e}
def I(t, vt='int', msg=''): return {'t': 'input', 'target': t, 'vtype': vt, 'msg': msg}
def O(e, nl=True): return {'t': 'output', 'expr': e, 'nl': nl}
def IF(c, yes, no=None): return {'t': 'if', 'cond': c, 'yes': yes, 'no': no or []}
def W(c, body): return {'t': 'while', 'cond': c, 'body': body}
def F(v, start, stop, step, body): return {'t': 'for', 'v': v, 'start': start, 'stop': stop, 'step': step, 'body': body}
def DO(body, c): return {'t': 'do', 'body': body, 'cond': c}

voto = lambda: [I('voto', 'float', '"Voto: "'),
                IF('voto >= 9', [O('"ottimo"')], [IF('voto >= 6', [O('"sufficiente"')], [O('"insufficiente"')])])]

CASES = [
  # nome, blocchi, input, errore atteso ('' = nessuno)
  ('precedenza e divisioni', [
      O('-2 ** 2, 2 ** -1, 2 ** 3 ** 2, (-2) ** 2'),
      O('7 // 2, -7 // 2, 7 % 3, -7 % 3, 7 % -3, -6 % 3'),
      O('7.0 // 2, -7.5 % 2, 10 / 2, 1 / 3, 0.1 + 0.2'),
      O('1 + 2 * 3 - 4 / 2, (1 + 2) * 3, not 1 == 2, 1 < 2 and 2 < 3 or False')], [], ''),
  ('interi grandi', [
      O('2 ** 64, 2 ** 100, 10 ** 20 + 1'),
      O('123456789 * 987654321, 9007199254740993 + 0, 2 ** 53 + 1'),
      O('-(2 ** 70) // 3, (2 ** 70) % 7, abs(-(10 ** 25)), int(1e20)'),
      A('f', '1'), F('i', '1', '31', '1', [A('f', 'f * i')]), O('"30! =", f'),
      O('f // 1000, f % 1000, f / f, len(str(f))')], [], ''),
  ('formato dei float', [
      O('1e16, 1e15, 1e-5, 0.0001, 123.0, -0.0, 2.5e-7, 1.5e300 * 1e10'),
      O('2 ** 0.5, 1 / 7, 100.0, 3.0 * 2, float(7), 10 ** -2'),
      O('round(2.5), round(3.5), round(-2.5), round(0.125, 2), round(2.675, 2), round(1234, -2), round(1250, -2)'),
      O('f"{0.125:.2f} {2.5:.0f} {3.5:.0f} {3.14159:.3f} {2.675:.2f} {1/3:.4f}"'),
      O('f"|{7:>5}|{\'ab\':<4}|{\'x\':^5}|{42:d}|{3.14159:8.2f}|"')], [], ''),
  ('booleani, confronti, sequenze', [
      O('True + True, True and 0, 0 or "x", not "", None'),
      O('3 < 5 < 4, 1 == 1.0, "a" < "b", [1, 2] == [1, 2], [1, 2] < [1, 3]'),
      O('"ab" * 3, [0] * 3, 3 in [1, 2, 3], "c" not in "ciao", "" * 5, [1] * -1'),
      O('[1, "a", 2.0, True, None, [3]], []'),
      O('"x\'y", ["it\'s", \'say "hi"\', "a\\\\b"]')], [], ''),
  ('funzioni predefinite', [
      O('int("42") + 1, int(" -7 "), float("2.5") * 2, int(7.9), int(-7.9), str(3.0), str(10 ** 20)'),
      O('abs(-3.5), min(3, 1, 2), max([4, 9, 2]), sum([1, 2.5]), sum([]), sorted([3, 1, 2]), sorted("bca")'),
      O('len("ciao"), list("abc"), bool(0), bool("no"), bool([])'),
      O('math.sqrt(16), math.floor(-2.5), math.ceil(2.1), math.pi, math.floor(7), math.log(math.e), math.log(8, 2)')], [], ''),
  ('metodi di liste e stringhe', [
      A('l', '[]'), A('', 'l.append(3)'), A('', 'l.append(1)'), A('', 'l.insert(0, 9)'), A('', 'l.append(1)'),
      O('l, l.count(1), l.index(1)'), A('x', 'l.pop()'), A('y', 'l.pop(0)'), O('x, y, l'),
      A('', 'l.sort()'), O('l'), A('', 'l.reverse()'), O('l'), A('', 'l.remove(3)'), O('l'),
      A('r', 'l.append(5)'), O('r'),
      A('s', '"  Ciao Mondo  "'), O('s.strip().upper(), s.lower(), s.split(), "a-b-c".split("-")'),
      O('"-".join(["a", "b"]), "banana".replace("a", "o"), "banana".find("n"), "banana".count("a"), "x".find("z")'),
      O('"ciao".startswith("ci"), "123".isdigit(), "pippo".capitalize(), "abc"[-1], [1, 2, 3][-2]')], [], ''),
  ('alias delle liste', [
      A('a', '[1, 2]'), A('b', 'a'), A('', 'b.append(3)'), O('a'),
      A('m', '[[0] * 2] * 2'), A('m[0][0]', '5'), O('m'),
      A('c', 'a + [4]'), A('', 'c.append(5)'), O('a, c')], [], ''),
  ('cicli for', [
      F('i', '10', '0', '-3', [O('i', False), O('" "', False)]), O(''),
      F('i', '5', '5', '1', [O('"mai"')]), O('"i dopo:", i'),
      F('j', '0', '3', '', [F('k', '', 'j', '', [O('j * 10 + k', False), O('";"', False)])]), O('""'),
      A('n', '3'), F('i', '0', 'n', '1', [A('n', 'n + 1')]), O('n')], [], ''),
  ('somma da 1 a N', [I('n', 'int', '"N? "'), A('somma', '0'), F('i', '1', 'n + 1', '1', [A('somma', 'somma + i')]),
                      O('"La somma è", somma')], ['5'], ''),
  ('voto 9.5', voto(), ['9.5'], ''),
  ('voto 6', voto(), ['6'], ''),
  ('voto 4', voto(), [' 4 '], ''),
  ('while e ripeti', [
      A('n', '5'), W('n > 0', [O('n', False), A('n', 'n - 2')]), O('" fine", n'),
      A('k', '10'), DO([O('"una volta"'), A('k', 'k + 1')], 'k < 5'), O('k')], [], ''),
  ('input di testo', [I('nome', 'str', '"Nome: "'), I('vuoto', 'str'), O('"Ciao", nome + "!", len(vuoto), [nome, vuoto]')],
      ['Mario Rossi', ''], ''),
  ('input bool True', [I('ok', 'bool', '"Hai finito? "'), IF('ok', [O('"bene"')], [O('"continua"')]), O('ok, not ok')], ['True'], ''),
  ('input bool False', [I('ok', 'bool'), I('altro', 'bool'), O('ok or altro, ok and altro, [ok, altro]')], ['False', 'True'], ''),
  ('input numeri grandi e decimali', [I('a', 'int'), I('b', 'float', '"b="'), O('a * a, b * 2, a + b')],
      ['123456789012345678901234567890', '1e3'], ''),
  ('f-string e print', [
      A('x', '3'), A('nome', '"Ada"'), O('f"{nome} ha {x * 2} anni e {x / 2} mesi"'),
      O('"a"', False), O('"b"'), O(''), O('1, "due", 3.0, [4], None, True'),
      O('f"{{graffe}} {x!r}"' if False else 'f"{{graffe}} {[x, nome]}"')], [], ''),
  ('ERR divisione per zero', [A('x', '0'), O('"prima"'), O('5 / x'), O('"dopo"')], [], 'ZeroDivisionError'),
  ('ERR modulo per zero', [O('5 % 0')], [], 'ZeroDivisionError'),
  ('ERR variabile inesistente', [A('somma', '1'), O('Somma')], [], 'NameError'),
  ('ERR indice', [A('l', '[1, 2]'), O('l[0]'), O('l[2]')], [], 'IndexError'),
  ('ERR testo + numero', [A('n', '5'), O('"n = " + n')], [], 'TypeError'),
  ('ERR int di testo', [A('x', 'int("abc")')], [], 'ValueError'),
  ('ERR passo zero', [F('i', '0', '5', '0', [O('i')])], [], 'ValueError'),
  ('ERR confronto tipi', [O('3 < "4"')], [], 'TypeError'),
  ('ERR remove assente', [A('l', '[1]'), A('', 'l.remove(5)')], [], 'ValueError'),
  ('ERR pop lista vuota', [A('l', '[]'), A('', 'l.pop()')], [], 'IndexError'),
  ('ERR stringa immutabile', [A('s', '"ciao"'), A('s[0]', '"C"')], [], 'TypeError'),
  ('ERR float overflow', [O('10.0 ** 400')], [], 'OverflowError'),
]

PRELUDE = '''import sys
def input(prompt=""):
    sys.stdout.write(str(prompt))
    s = sys.stdin.readline()
    if s.endswith("\\n"): s = s[:-1]
    sys.stdout.write(s + "\\n")
    return s
'''

def run_python(code, inputs):
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(PRELUDE + code + '\n'); path = f.name
    p = subprocess.run([sys.executable, '-I', path], input=''.join(x + '\n' for x in inputs),
                       capture_output=True, text=True, timeout=20)
    os.unlink(path)
    err = ''
    if p.returncode:
        last = p.stderr.strip().splitlines()[-1] if p.stderr.strip() else '?'
        err = last.split(':')[0]
    return p.stdout.rstrip('\n').split('\n') if p.stdout else [], err, p.stderr

def run_app(pg, body, inputs):
    pg.click('#btnIO')
    pg.fill('#ioText', json.dumps({'body': body}))
    pg.click('#ioLoad')
    pg.click('#tabCode'); pg.click('[data-lang=python]')
    code = pg.inner_text('#code')
    pg.click('#tabRun')
    pg.eval_on_selector('#speed', 'e=>{e.value=0;e.oninput()}')
    pg.click('#btnRun')
    queue = list(inputs)
    for _ in range(400):
        st = pg.inner_text('#status')
        if st in ('Terminato', 'Errore'): break
        if st == 'Attende un input':
            if not queue: return None, 'input in più richiesto', code, ''
            pg.fill('#inField', queue.pop(0)); pg.click('#inBtn')
        pg.wait_for_timeout(25)
    lines = pg.evaluate("Array.from(document.querySelectorAll('#console .ln.out')).map(d=>d.textContent)")
    errs = pg.evaluate("Array.from(document.querySelectorAll('#console .ln.err')).map(d=>d.textContent)")
    return lines, pg.inner_text('#status'), code, ' | '.join(errs)

def main():
    ok = 0; fails = []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        errors = []; pg.on('pageerror', lambda e: errors.append(str(e)))
        pg.goto('file://' + PAGE); pg.wait_for_timeout(300)
        for name, body, inputs, exp_err in CASES:
            app_lines, status, code, app_err = run_app(pg, body, inputs)
            py_lines, py_err, py_stderr = run_python(code, inputs)
            problems = []
            if app_lines is None: problems.append(status)
            else:
                if app_lines != py_lines:
                    for k in range(max(len(app_lines), len(py_lines))):
                        a = app_lines[k] if k < len(app_lines) else '<nessuna riga>'
                        q = py_lines[k] if k < len(py_lines) else '<nessuna riga>'
                        if a != q: problems.append(f'riga {k+1}\n      app:    {a}\n      python: {q}')
                if exp_err:
                    if status != 'Errore': problems.append(f'l\'app doveva fermarsi con un errore ({exp_err})')
                    if py_err != exp_err: problems.append(f'Python: atteso {exp_err}, ottenuto {py_err or "nessun errore"}')
                else:
                    if status != 'Terminato': problems.append(f'l\'app si è fermata: {app_err}')
                    if py_err: problems.append(f'Python ha dato errore: {py_stderr.strip().splitlines()[-1]}')
            if problems:
                fails.append(name); print(f'✗ {name}'); [print('   ', x) for x in problems]
            else:
                ok += 1; print(f'✓ {name}' + (f'   [errore in entrambi: {exp_err} — app: {app_err[:90]}]' if exp_err else ''))
        # ciclo infinito: solo nell'app (in Python non terminerebbe)
        lines, status, code, err = run_app(pg, [A('x', '0'), W('True', [A('x', 'x + 1')])], [])
        if status == 'Errore' and 'troppi passi' in err.lower(): ok += 1; print('✓ ciclo infinito fermato dal limite di sicurezza')
        else: fails.append('ciclo infinito'); print('✗ ciclo infinito:', status, err)
        if errors: print('ERRORI JAVASCRIPT:', errors)
        b.close()
    print(f'\n{ok} superati, {len(fails)} falliti')
    sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
