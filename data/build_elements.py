#!/usr/bin/env python3
"""Genera data/elements.js: las 118 elementos con datos de fuente única y validados.

Fuente: tabla periódica de PubChem (NIH), dominio público. Reúne masas atómicas estándar (IUPAC),
configuraciones electrónicas del estado fundamental (NIST), energías de ionización (NIST),
electronegatividad de Pauling, radio de van der Waals, afinidad electrónica, puntos de fusión y
ebullición, densidad, estado estándar y año de descubrimiento.
    https://pubchem.ncbi.nlm.nih.gov/periodic-table/

Disposición: recomendación IUPAC (grupo 3 = Sc, Y, Lu, Lr; bloque f = La–Yb y Ac–No).

Uso:
    python3 data/build_elements.py                 # descarga PubChem y regenera
    python3 data/build_elements.py pubchem.json    # usa una copia local
El script falla (exit 1) si alguna comprobación de coherencia no se cumple.
"""
import json
import os
import re
import sys
import urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
URL = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/JSON'

NOMBRES = [  # nombres en español (IUPAC / RSEQ, 2016), índice = Z - 1
    'Hidrógeno', 'Helio', 'Litio', 'Berilio', 'Boro', 'Carbono', 'Nitrógeno', 'Oxígeno', 'Flúor', 'Neón',
    'Sodio', 'Magnesio', 'Aluminio', 'Silicio', 'Fósforo', 'Azufre', 'Cloro', 'Argón', 'Potasio', 'Calcio',
    'Escandio', 'Titanio', 'Vanadio', 'Cromo', 'Manganeso', 'Hierro', 'Cobalto', 'Níquel', 'Cobre', 'Zinc',
    'Galio', 'Germanio', 'Arsénico', 'Selenio', 'Bromo', 'Kriptón', 'Rubidio', 'Estroncio', 'Itrio', 'Circonio',
    'Niobio', 'Molibdeno', 'Tecnecio', 'Rutenio', 'Rodio', 'Paladio', 'Plata', 'Cadmio', 'Indio', 'Estaño',
    'Antimonio', 'Teluro', 'Yodo', 'Xenón', 'Cesio', 'Bario', 'Lantano', 'Cerio', 'Praseodimio', 'Neodimio',
    'Prometio', 'Samario', 'Europio', 'Gadolinio', 'Terbio', 'Disprosio', 'Holmio', 'Erbio', 'Tulio', 'Iterbio',
    'Lutecio', 'Hafnio', 'Tantalio', 'Wolframio', 'Renio', 'Osmio', 'Iridio', 'Platino', 'Oro', 'Mercurio',
    'Talio', 'Plomo', 'Bismuto', 'Polonio', 'Astato', 'Radón', 'Francio', 'Radio', 'Actinio', 'Torio',
    'Protactinio', 'Uranio', 'Neptunio', 'Plutonio', 'Americio', 'Curio', 'Berkelio', 'Californio', 'Einstenio', 'Fermio',
    'Mendelevio', 'Nobelio', 'Laurencio', 'Rutherfordio', 'Dubnio', 'Seaborgio', 'Bohrio', 'Hasio', 'Meitnerio', 'Darmstatio',
    'Roentgenio', 'Copernicio', 'Nihonio', 'Flerovio', 'Moscovio', 'Livermorio', 'Teneso', 'Oganesón',
]
CATEGORIAS = {  # GroupBlock de PubChem -> clave interna
    'Nonmetal': 'no-metal', 'Noble gas': 'gas-noble', 'Alkali metal': 'alcalino',
    'Alkaline earth metal': 'alcalinoterreo', 'Metalloid': 'metaloide', 'Halogen': 'halogeno',
    'Post-transition metal': 'post-transicion', 'Transition metal': 'transicion',
    'Lanthanide': 'lantanido', 'Actinide': 'actinido',
}
# Sublimación a 1 atm: el punto de fusión tabulado es bajo presión (As: 1090 K a 28 atm; sublima a ~887 K)
SUBLIMA = {'As'}
# Valores medidos que corrigen a PubChem (que da estimaciones o valores antiguos), con su fuente.
CORRECCIONES = {
    ('Fr', 'ei'): (4.0727, 'S. V. Andreev y cols., Phys. Rev. Lett. 59, 1274 (1987)'),
    ('At', 'ei'): (9.3175, 'S. Rothe y cols., Nature Communications 4, 1835 (2013)'),
    ('F', 'ae'): (3.4012, 'C. Blondel, C. Delsart y F. Goldfarb, J. Phys. B 34, L281 (2001)'),
    ('At', 'ae'): (2.4159, 'D. Leimbach y cols., Nature Communications 11, 3824 (2020)'),
}
# Valores que no son medidas (extrapolaciones o asignaciones aproximadas): se marcan con «≈».
ESTIMADOS = {
    'Fr': ['fusion', 'en'], 'At': ['fusion', 'densidad', 'en'], 'Ra': ['densidad'],
    'Cf': ['en'], 'Es': ['en'], 'Fm': ['fusion', 'en'], 'Md': ['fusion', 'en'], 'No': ['fusion', 'en'], 'Lr': ['fusion', 'en'],
}
MADELUNG = ['1s', '2s', '2p', '3s', '3p', '4s', '3d', '4p', '5s', '4d', '5p', '6s', '4f', '5d', '6p', '7s', '5f', '6d', '7p']
CAP = {'s': 2, 'p': 6, 'd': 10, 'f': 14}
NOBLE = {'He': 2, 'Ne': 10, 'Ar': 18, 'Kr': 36, 'Xe': 54, 'Rn': 86}


def madelung(z):
    occ, left = {}, z
    for sub in MADELUNG:
        if left == 0:
            break
        n = min(CAP[sub[1]], left)
        occ[sub] = n
        left -= n
    return occ


def expand(config, by_symbol):
    """'[Ar]3d5 4s1' -> {'1s':2, ..., '3d':5, '4s':1} (orden de Madelung)."""
    occ = {}
    m = re.match(r'\[(\w+)\]', config)
    if m:
        occ.update(madelung(NOBLE[m.group(1)]))
    for sub, n in re.findall(r'(\d[spdf])(\d+)', config):
        occ[sub] = int(n)
    return {k: occ[k] for k in MADELUNG if occ.get(k)}


def normalize(config):
    """Reordena las subcapas tras el gas noble por n y luego por l, la notación del NIST
    (no el orden de llenado): '[Xe]6s1 4f14 5d10' -> '[Xe]4f14 5d10 6s1', '[Ar]4s2 3d6' -> '[Ar]3d6 4s2'."""
    m = re.match(r'(\[\w+\])?\s*(.*)', config)
    core, rest = m.group(1) or '', m.group(2)
    subs = re.findall(r'(\d[spdf])(\d+)', rest)
    subs.sort(key=lambda t: (int(t[0][0]), 'spdf'.index(t[0][1])))
    return (core + ' '.join(a + b for a, b in subs)).strip()


def position(z):
    """(periodo, grupo|None, bloque, fila, columna) en la disposición IUPAC de 18 columnas + bloque f."""
    starts = [(1, 1), (3, 2), (11, 3), (19, 4), (37, 5), (55, 6), (87, 7)]
    period = max(p for s, p in starts if z >= s)
    if 57 <= z <= 70 or 89 <= z <= 102:   # bloque f (La–Yb, Ac–No)
        row = 9 if z <= 70 else 10
        return period, None, 'f', row, 3 + (z - (57 if z <= 70 else 89))
    first = dict((p, s) for s, p in starts)[period]
    k = z - first                               # índice dentro del periodo
    if period == 1:
        group = 1 if z == 1 else 18
    elif period in (2, 3):
        group = k + 1 if k < 2 else k + 11
    elif period in (4, 5):
        group = k + 1
    else:                                       # periodos 6 y 7: tras el bloque f
        group = k + 1 if k < 2 else k - 13     # k=16 (Lu, Lr) -> grupo 3
    block = 's' if group in (1, 2) or z == 2 else 'p' if group >= 13 else 'd'
    return period, group, block, period, group


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def build(raw):
    cols = raw['Table']['Columns']['Column']
    rows = [dict(zip(cols, r['Cell'])) for r in raw['Table']['Row']]
    by_symbol = {r['Symbol']: r for r in rows}
    out = []
    for r in rows:
        z = int(r['AtomicNumber'])
        period, group, block, row, col = position(z)
        conf = r['ElectronConfiguration']
        predicted_conf = '(predicted)' in conf
        conf_clean = normalize(conf.replace('(predicted)', '').strip())
        state = r['StandardState']
        year = r['YearDiscovered']
        out.append({
            'z': z, 'sym': r['Symbol'], 'nombre': NOMBRES[z - 1], 'name_en': r['Name'],
            'masa': num(r['AtomicMass']), 'periodo': period, 'grupo': group, 'bloque': block,
            'fila': row, 'col': col, 'categoria': CATEGORIAS.get(r['GroupBlock'], 'desconocida'),
            'config': conf_clean, 'config_predicha': predicted_conf, 'ocupacion': expand(conf_clean, by_symbol),
            'en': num(r['Electronegativity']), 'radio': num(r['AtomicRadius']), 'ei': num(r['IonizationEnergy']),
            'ae': num(r['ElectronAffinity']), 'fusion': num(r['MeltingPoint']), 'ebullicion': num(r['BoilingPoint']),
            'densidad': num(r['Density']),
            'estado': {'Solid': 'solido', 'Liquid': 'liquido', 'Gas': 'gas'}.get(state.replace('Expected to be a ', '').strip(), None),
            'estado_predicho': state.startswith('Expected'),
            'anio': None if year == 'Ancient' else int(year) if year.isdigit() else None,
            'antiguedad': year == 'Ancient',
            'oxidacion': r['OxidationStates'],
            'sublima': r['Symbol'] in SUBLIMA,
        })
        e = out[-1]
        e['estimado'] = ESTIMADOS.get(e['sym'], [])
        for (sym, k), (v, src) in CORRECCIONES.items():
            if sym == e['sym']:
                e[k] = v
                e.setdefault('fuentes', {})[k] = src
    return out


def validate(els):
    errors, notes = [], []
    if [e['z'] for e in els] != list(range(1, 119)):
        errors.append('faltan elementos o no están ordenados por Z')
    cells = {}
    for e in els:
        cells.setdefault((e['fila'], e['col']), []).append(e['sym'])
        tot = sum(e['ocupacion'].values())
        if tot != e['z']:
            errors.append(f"{e['sym']}: la configuración suma {tot} electrones, no {e['z']}")
        for sub, n in e['ocupacion'].items():
            if n > CAP[sub[1]]:
                errors.append(f"{e['sym']}: {sub} con {n} electrones (máximo {CAP[sub[1]]})")
        for k, lo, hi in (('en', 0.7, 4.0), ('ei', 3.5, 25.0), ('radio', 100, 400), ('masa', 1, 300)):
            if e[k] is not None and not lo <= e[k] <= hi:
                errors.append(f"{e['sym']}: {k}={e[k]} fuera de rango [{lo}, {hi}]")
        if e['fusion'] and e['ebullicion'] and e['fusion'] > e['ebullicion'] and e['sym'] not in SUBLIMA:
            errors.append(f"{e['sym']}: fusión > ebullición")
        if e['ocupacion'] != madelung(e['z']):
            notes.append(e['sym'])
    for cell, syms in cells.items():
        if len(syms) > 1:
            errors.append(f'celda {cell} ocupada por {syms}')
    # comprobaciones de disposición IUPAC
    by = {e['sym']: e for e in els}
    for sym, g in (('Sc', 3), ('Y', 3), ('Lu', 3), ('Lr', 3), ('He', 18), ('Og', 18), ('Fe', 8), ('Au', 11)):
        if by[sym]['grupo'] != g:
            errors.append(f'{sym} debería estar en el grupo {g}')
    inversions = [f"{a['sym']}>{b['sym']}" for a, b in zip(els, els[1:]) if a['masa'] and b['masa'] and a['masa'] > b['masa']]
    return errors, notes, inversions


def main():
    raw = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else json.load(urllib.request.urlopen(URL, timeout=30))
    els = build(raw)
    errors, exceptions, inversions = validate(els)
    for e in errors:
        print('ERROR', e)
    if errors:
        sys.exit(1)
    data = {
        'fuente': 'PubChem Periodic Table (NIH) · https://pubchem.ncbi.nlm.nih.gov/periodic-table/',
        'generado': date.today().isoformat(),
        'disposicion': 'IUPAC: grupo 3 = Sc, Y, Lu, Lr; bloque f = La–Yb, Ac–No',
        'unidades': {'masa': 'u', 'en': 'Pauling', 'radio': 'pm (van der Waals)', 'ei': 'eV', 'ae': 'eV',
                     'fusion': 'K', 'ebullicion': 'K', 'densidad': 'g/cm³'},
        'excepciones_madelung': exceptions,
        'elementos': els,
    }
    js = ('// Generado por data/build_elements.py — no editar a mano.\n'
          'window.EIGENLAB_ELEMENTS = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
    open(os.path.join(HERE, 'elements.js'), 'w', encoding='utf-8').write(js)
    print(f'118 elementos válidos · {len(exceptions)} excepciones a Madelung: {" ".join(exceptions)}')
    print(f'inversiones de masa (orden por Z, no por masa): {" ".join(inversions)}')
    print(f'{os.path.getsize(os.path.join(HERE, "elements.js")) // 1024} KB')


if __name__ == '__main__':
    main()
