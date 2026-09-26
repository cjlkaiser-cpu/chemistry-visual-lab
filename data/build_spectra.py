#!/usr/bin/env python3
"""Genera data/spectra.js: líneas de emisión visibles (átomos neutros) de la base de datos del NIST.

Fuente: NIST Atomic Spectra Database (ASD), https://physics.nist.gov/asd — longitudes de onda en aire,
intensidades relativas (orientativas: dependen de la fuente de excitación, solo comparables dentro de un espectro).
Para cada línea se guardan también la probabilidad de transición A (s⁻¹), la energía del nivel superior E_k (eV)
y su degeneración g_k = 2J + 1: con ellas la simulación calcula intensidades en equilibrio térmico,
I ∝ g_k·A·exp(−E_k/kT)/λ, que sí son comparables entre líneas (las intensidades observadas no lo son).

Hidrógeno: además de las líneas del NIST se calculan las series con la fórmula de Rydberg (con masa reducida)
y se convierten de vacío a aire; el script comprueba que coinciden con el NIST.

Color: funciones de igualación de color CIE 1931 (2°), tabla oficial a 1 nm distribuida por el CVRL (UCL):
    http://www.cvrl.org/database/data/cmfs/ciexyz31_1.csv

Uso:
    python3 data/build_spectra.py            # descarga (con pausa entre peticiones) y regenera
Falla (exit 1) si alguna comprobación no se cumple.
"""
import csv
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ELEMENTS = ['H', 'He', 'Li', 'Na', 'K', 'Rb', 'Cs', 'Mg', 'Ca', 'Sr', 'Ba', 'Zn', 'Cd', 'Hg',
            'Cu', 'Fe', 'Ne', 'Ar', 'Kr', 'Xe', 'N', 'O', 'B']
LOW, HIGH = 380.0, 780.0          # visible (nm, aire), límites habituales de la CIE
MAX_LINES = 40                     # las más intensas de cada elemento
R_INF = 10973731.568160            # m⁻¹ (CODATA 2018)
ME_MP = 1 / 1836.15267343          # masa del electrón / masa del protón
R_H = R_INF / (1 + ME_MP)          # constante de Rydberg del hidrógeno (masa reducida)


def nist_url(sym):
    q = {'spectra': f'{sym} I', 'limits_type': 0, 'low_w': LOW, 'upp_w': HIGH, 'unit': 1, 'de': 0, 'format': 2,
         'line_out': 0, 'remove_js': 'on', 'en_unit': 0, 'output': 0, 'page_size': 15, 'show_obs_wl': 1,
         'show_calc_wl': 1, 'order_out': 0, 'show_av': 2, 'tsb_value': 0, 'A_out': 0, 'intens_out': 'on',
         'allowed_out': 1, 'forbid_out': 1, 'enrg_out': 'on', 'J_out': 'on', 'submit': 'Retrieve Data'}
    return 'https://physics.nist.gov/cgi-bin/ASD/lines1.pl?' + urllib.parse.urlencode(q)


def clean(v):
    return re.sub(r'^="?|"$', '', (v or '').strip()).strip('"')


def fetch(sym):
    req = urllib.request.Request(nist_url(sym), headers={'User-Agent': 'EigenLab data builder (educational; https://github.com/cjlkaiser-cpu/eigenlab)'})
    raw = urllib.request.urlopen(req, timeout=60).read().decode('utf-8', 'replace')
    lines = []
    for row in csv.DictReader(io.StringIO(raw)):
        wl = clean(row.get('obs_wl_air(nm)')) or clean(row.get('ritz_wl_air(nm)'))
        m = re.match(r'[\d.]+', clean(row.get('intens')))
        if not wl or not m:
            continue
        try:
            w, i = float(wl), float(m.group(0))
        except ValueError:
            continue
        a, ek, jk = clean(row.get('Aki(s^-1)')), clean(row.get('Ek(cm-1)')), clean(row.get('J_k'))
        try:
            a = float(a); ek = float(re.sub(r'[^\d.]', '', ek)) / 8065.544    # cm⁻¹ -> eV
            gk = 2 * (float(jk.split('/')[0]) / float(jk.split('/')[1]) if '/' in jk else float(jk)) + 1
        except (ValueError, ZeroDivisionError):
            a = ek = gk = None
        if LOW <= w <= HIGH and i > 0:
            lines.append((round(w, 3), i, a, ek, gk))
    lines.sort(key=lambda t: -t[1])
    top = sorted(lines[:MAX_LINES])
    mx = max(t[1] for t in top)
    return [{'nm': w, 'rel': round(i / mx, 4), 'A': a, 'Ek': round(ek, 4) if ek else None, 'g': gk}
            for w, i, a, ek, gk in top]


# Hidrógeno: el NIST lista las componentes de estructura fina; para el modelo térmico se usan las probabilidades
# totales n -> 2 de la serie de Balmer (Wiese y Fuhr, J. Phys. Chem. Ref. Data 38, 565, 2009), con g = 2n².
BALMER_A = {3: 4.4101e7, 4: 8.4193e6, 5: 2.5304e6, 6: 9.7320e5, 7: 4.3889e5}


def hydrogen_params(lines):
    for l in lines:
        for n, a in BALMER_A.items():
            if abs(vac_to_air(rydberg(2, n)) - l['nm']) < 0.05:
                l['A'], l['g'], l['Ek'] = a, 2 * n * n, round(13.598 * (1 - 1 / n ** 2), 4)


def fetch_cmf():
    req = urllib.request.Request('http://www.cvrl.org/database/data/cmfs/ciexyz31_1.csv', headers={'User-Agent': 'EigenLab data builder'})
    rows = [r.split(',') for r in urllib.request.urlopen(req, timeout=60).read().decode().split('\n') if r.strip()]
    table = {int(r[0]): [float(v) for v in r[1:4]] for r in rows}
    if abs(table[555][1] - 1.0) > 1e-9:
        sys.exit('CMF: ȳ(555 nm) debería valer 1')
    return {'desde_nm': int(LOW), 'paso_nm': 1,
            'xyz': [[float(f'{v:.7g}') for v in table[nm]] for nm in range(int(LOW), int(HIGH) + 1)]}


def vac_to_air(nm):
    """Índice de refracción del aire estándar (Morton 2000, a partir de Edlén/Ciddor)."""
    s2 = (1e3 / nm) ** 2          # (1/λ en µm)²
    n = 1 + 8.34254e-5 + 2.406147e-2 / (130 - s2) + 1.5998e-4 / (38.9 - s2)
    return nm / n


def rydberg(n_low, n_up):
    inv = R_H * (1 / n_low ** 2 - 1 / n_up ** 2)
    return 1e9 / inv               # nm en vacío


def hydrogen_series():
    names = {1: 'Lyman', 2: 'Balmer', 3: 'Paschen'}
    out = []
    for nl, name in names.items():
        for nu in range(nl + 1, nl + 12):
            vac = rydberg(nl, nu)
            out.append({'serie': name, 'n_inf': nl, 'n_sup': nu, 'vacio_nm': round(vac, 4),
                        'aire_nm': round(vac_to_air(vac), 4) if vac > 200 else None})
    return out


def main():
    data = {}
    for sym in ELEMENTS:
        for attempt in range(3):
            try:
                data[sym] = fetch(sym)
                break
            except Exception as e:     # red intermitente: reintentar
                print(f'{sym}: reintento ({e})')
                time.sleep(3)
        else:
            sys.exit(f'No se pudo descargar {sym}')
        print(f'{sym:3} {len(data[sym]):3} líneas · más intensa {max(data[sym], key=lambda l: l["rel"])["nm"]} nm')
        time.sleep(1)               # cortesía con el servidor del NIST

    hydrogen_params(data['H'])
    # --- validación
    errors = []
    h = hydrogen_series()
    balmer = {l['n_sup']: l['aire_nm'] for l in h if l['serie'] == 'Balmer'}
    for n_up, ref in {3: 656.279, 4: 486.135, 5: 434.047, 6: 410.174}.items():   # NIST, aire
        if abs(balmer[n_up] - ref) > 0.01:
            errors.append(f'Balmer n={n_up}: Rydberg {balmer[n_up]} nm frente a NIST {ref} nm')
        if not any(abs(l['nm'] - ref) < 0.02 for l in data['H']):
            errors.append(f'H: falta la línea de Balmer {ref} nm en los datos del NIST')
    for ref in (588.995, 589.592):
        if not any(abs(l['nm'] - ref) < 0.01 for l in data['Na']):
            errors.append(f'Na: falta la línea D {ref} nm')
    if not any(abs(l['nm'] - 546.07) < 0.02 for l in data['Hg']):
        errors.append('Hg: falta la línea verde de 546,07 nm')
    for sym, L in data.items():
        withA = sum(1 for l in L if l['A'])
        if withA < max(2, len(L) // 3):
            print(f'aviso: {sym} solo tiene A en {withA}/{len(L)} líneas (el modelo térmico usará esas)')
    for e in errors:
        print('ERROR', e)
    if errors:
        sys.exit(1)

    out = {'fuente': 'NIST Atomic Spectra Database · https://physics.nist.gov/asd', 'generado': date.today().isoformat(),
           'rango_nm': [LOW, HIGH], 'nota': 'Longitudes de onda en aire. Intensidades relativas dentro de cada espectro (orientativas).',
           'rydberg_H_m-1': R_H, 'lineas': data, 'hidrogeno_series': h,
           'cmf_cie1931': fetch_cmf(), 'fuente_cmf': 'CIE 1931 2° (CVRL, UCL) · http://www.cvrl.org'}
    js = ('// Generado por data/build_spectra.py — no editar a mano.\n'
          'window.EIGENLAB_SPECTRA = ' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n')
    open(os.path.join(HERE, 'spectra.js'), 'w', encoding='utf-8').write(js)
    print(f'OK · {len(data)} elementos · Balmer por Rydberg coincide con el NIST (< 0,01 nm) · '
          f'{os.path.getsize(os.path.join(HERE, "spectra.js")) // 1024} KB')


if __name__ == '__main__':
    main()
