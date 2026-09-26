#!/usr/bin/env python3
"""Genera data/origin.js: origen nucleosintético y abundancia de los elementos en el sistema solar.

Fuentes:
  - Origen: tabla periódica de J. A. Johnson (Ohio State; blog SDSS, 2017; Science 363, 474, 2019), en la
    digitalización de CMG Lee para Wikimedia Commons (CC BY-SA 3.0). El SVG incluye la tabla de datos
    en el script que lo genera. Precisión: unos pocos puntos porcentuales; hasta tres fuentes por elemento.
        https://commons.wikimedia.org/wiki/File:Nucleosynthesis_periodic_table.svg
  - Abundancias: E. Anders y N. Grevesse, Geochim. Cosmochim. Acta 53, 197 (1989), vía la página de datos
    «Abundances of the elements» de Wikipedia (columna Y2, relativa a Si = 1, con incertidumbre).

Correcciones respecto a la digitalización (siguiendo a Johnson 2019): los elementos que en el sistema
solar solo existen por desintegración de U y Th (Po–Pa) se marcan como «desintegración»; Np y Pu, que
solo existen en trazas o sintetizados, como «sintéticos».

Uso:
    python3 data/build_origin.py
El script falla (exit 1) si alguna comprobación no se cumple.
"""
import json
import os
import re
import sys
import urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'EigenLab-data/1.0 (educational; https://cjlkaiser-cpu.github.io/eigenlab)'}
SVG_URL = 'https://upload.wikimedia.org/wikipedia/commons/3/31/Nucleosynthesis_periodic_table.svg'
AB_URL = 'https://en.wikipedia.org/w/index.php?title=Abundances_of_the_elements_(data_page)&action=raw'

SOURCES = {  # código del SVG -> (clave, nombre)
    'b': ('bigbang', 'Big Bang'),
    'j': ('rayos', 'Fisión por rayos cósmicos'),
    'y': ('baja', 'Estrellas de baja masa (fase AGB)'),
    'o': ('neutrones', 'Fusión de estrellas de neutrones'),
    'g': ('masivas', 'Supernovas de estrellas masivas'),
    'c': ('enanas', 'Explosión de enanas blancas (tipo Ia)'),
    'z': ('sintetico', 'Sin isótopos de vida larga (trazas o síntesis humana)'),
}
DECAY = ['Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Pa']
SYNTHETIC = ['Np', 'Pu']


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode('utf-8')


def origins(svg):
    block = svg[svg.index("datass = [[field.strip()"):]
    block = block.split("'''", 1)[1].split("'''", 1)[0]
    x_max = 185  # igual que en el script del SVG
    out = {}
    for z, line in enumerate(block.strip('\n').split('\n'), 1):
        f = [x.strip() for x in line.split('|')]
        if not f[0]:
            continue
        x, codes = float(f[3]), list(f[4])
        fr = (2 * x * x if x * 2 < x_max else 4 * x * x_max - 2 * x * x - x_max * x_max) / x_max ** 2
        fs = ([1.0] if len(codes) == 1 else [fr, 1 - fr] if len(codes) == 2
              else [fr * .45, fr * .55, 1 - fr] if z == 2 else [fr * .37, fr * .63, 1 - fr])
        out[f[0]] = {SOURCES[c][0]: round(v, 3) for c, v in zip(codes, fs)}
    for s in DECAY:
        out[s] = {'desintegracion': 1.0}
    for s in SYNTHETIC:
        out[s] = {'sintetico': 1.0}
    return out


def abundances(wiki):
    sec = wiki[wiki.index('==Sun and Solar System=='):wiki.index('==See also==')]
    ab = {}
    for row in sec.split('\n|-\n'):
        m = re.search(r'<!--\s*(\d+)\s+(\w+)\s*-->', row)
        y2 = re.search(r'<!--Y2-->style="[^"]*" data-sort-value="([\d.eE+-]+)"\|([^\n]*)', row)
        if m and y2 and float(y2.group(1)) > 0:
            unc = re.search(r'\(([\d.]+)%\)', y2.group(2))
            ab[m.group(2)] = {'n': float(y2.group(1)) * 1e6, 'inc': float(unc.group(1)) if unc else None}  # Si = 10⁶
    return ab


def validate(org, ab):
    err = []
    if len(org) != 103:
        err.append(f'origen: {len(org)} elementos, se esperaban 103 (H–Lr)')
    for s, d in org.items():
        if abs(sum(d.values()) - 1) > 0.002:
            err.append(f'{s}: las fracciones suman {sum(d.values()):.3f}')
    # referencias independientes: fracción del proceso r y de supernovas Ia (literatura: Eu ≈ 0,95, Au ≈ 0,94, Ba ≈ 0,15, Fe(Ia) ≈ 0,6)
    checks = [('Eu', 'neutrones', .85, 1), ('Au', 'neutrones', .85, 1), ('Ba', 'neutrones', .05, .3), ('Fe', 'enanas', .45, .75), ('H', 'bigbang', 1, 1)]
    for s, k, lo, hi in checks:
        v = org[s].get(k, 0)
        if not lo <= v <= hi:
            err.append(f'{s}: fracción {k} = {v} fuera de [{lo}, {hi}]')
    if not 2.7e10 < ab['H']['n'] < 2.9e10 or not 0.85e6 < ab['Fe']['n'] < 0.95e6:
        err.append('abundancias: H o Fe fuera de lo esperado (Anders y Grevesse: H 2,79·10¹⁰, Fe 9,0·10⁵)')
    if len(ab) < 80:
        err.append(f'abundancias: solo {len(ab)} elementos')
    return err


def main():
    org, ab = origins(get(SVG_URL)), abundances(get(AB_URL))
    err = validate(org, ab)
    for e in err:
        print('ERROR', e)
    if err:
        sys.exit(1)
    data = {
        'fuente_origen': 'J. A. Johnson (2017, 2019), digitalización de CMG Lee (Wikimedia Commons, CC BY-SA 3.0)',
        'fuente_abundancia': 'E. Anders y N. Grevesse, Geochim. Cosmochim. Acta 53, 197 (1989); número de átomos por cada 10⁶ de Si',
        'generado': date.today().isoformat(),
        'fuentes': {k: n for k, n in SOURCES.values()} | {'desintegracion': 'Solo por desintegración de U y Th'},
        'origen': org,
        'abundancia': ab,
    }
    js = ('// Generado por data/build_origin.py — no editar a mano.\n'
          'window.EIGENLAB_ORIGIN = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
    open(os.path.join(HERE, 'origin.js'), 'w', encoding='utf-8').write(js)
    print(f'origen: {len(org)} elementos · abundancias: {len(ab)} · {os.path.getsize(os.path.join(HERE, "origin.js")) // 1024} KB')


if __name__ == '__main__':
    main()
