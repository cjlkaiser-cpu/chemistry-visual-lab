/*
 * Motor del curso «La Tabla Periódica, de dentro afuera».
 * Cada lección es un <article class="lesson" data-mod="N" data-lesson="M"> con su contenido; este script añade:
 *   - barra superior, índice lateral, progreso y navegación anterior/siguiente (datos: course-data.js)
 *   - cabecera de la lección (módulo, título, duración, objetivos)
 *   - componentes: .predict (predicción que se revela), .quiz (autoevaluación con explicación),
 *     figure.sim[data-src] (simulación embebida), .ion-lab (configuración de iones; requiere data/elements.js)
 * El progreso se guarda en el navegador (localStorage); si no está disponible, el curso funciona igual.
 */
(function () {
    'use strict';
    const C = window.EIGENLAB_COURSE;
    const HERE = document.currentScript.src.replace(/[^/]*$/, '');   // .../curso-tabla-periodica/
    const KEY = 'eigenlab-curso-' + C.id;
    const lessons = C.modulos.flatMap(m => m.lecciones.map(l => ({ ...l, mod: m.n, modTitle: m.titulo, id: `${m.n}-${l.n}`,
        href: `${HERE}modulo-${m.n}/leccion-${l.n}.html` })));

    // ------------------------------------------------------------ progreso
    function load() { try { return JSON.parse(localStorage.getItem(KEY)) || { done: [] }; } catch (e) { return { done: [] }; } }
    function save(p) { try { localStorage.setItem(KEY, JSON.stringify(p)); } catch (e) { /* sin almacenamiento: sin progreso */ } }
    const progress = load();
    const isDone = id => progress.done.includes(id);
    function markDone(id, done = true) {
        progress.done = progress.done.filter(x => x !== id);
        if (done) progress.done.push(id);
        save(progress); renderChrome();
    }
    const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };

    // ------------------------------------------------------------ estructura de la página
    const article = document.querySelector('article.lesson');
    const home = document.querySelector('.course-home');
    const current = article ? lessons.find(l => l.id === `${article.dataset.mod}-${article.dataset.lesson}`) : null;
    let side, top;

    function buildChrome() {
        top = el('div', 'c-top');
        document.body.prepend(top);
        if (!article) return;
        const layout = el('div', 'c-layout');
        side = el('nav', 'c-side');
        side.setAttribute('aria-label', 'Índice del curso');
        article.replaceWith(layout);
        layout.append(side, article);
    }
    function renderChrome() {
        const avail = lessons.length, done = lessons.filter(l => isDone(l.id)).length;
        top.innerHTML = `${article ? '<button class="c-menu-btn" aria-expanded="false">☰ Índice</button>' : ''}
            <div class="crumbs"><a href="${HERE}../../../_portal/index.html">EigenLab</a> / <a href="${HERE}../index.html">Chemistry Visual Lab</a> / <a href="${HERE}index.html">${C.titulo}</a></div>
            <div class="c-progress" title="Lecciones completadas">${done}/${avail}<div class="bar"><span style="width:${done / avail * 100}%"></span></div></div>`;
        const mb = top.querySelector('.c-menu-btn');
        if (mb) mb.addEventListener('click', () => { const o = side.classList.toggle('open'); mb.setAttribute('aria-expanded', o); });
        if (side) side.innerHTML = `<h2>${C.titulo}</h2><div class="level">${C.nivel}</div>` + C.modulos.map(m => `
            <div class="c-mod${m.proximamente ? ' soon' : ''}"><div class="c-mod-title">Módulo ${m.n} · ${m.titulo}</div>
            ${m.proximamente ? '<div class="soon-note">Próximamente</div>' : '<ol>' + m.lecciones.map(l => {
                const id = `${m.n}-${l.n}`, x = lessons.find(y => y.id === id);
                return `<li><a href="${x.href}" class="${current && current.id === id ? 'current' : ''}" ${current && current.id === id ? 'aria-current="page"' : ''}>
                    <span class="num">${m.n}.${l.n}</span><span>${l.titulo}</span>${isDone(id) ? '<span class="done" aria-label="completada">✓</span>' : ''}</a></li>`;
            }).join('') + '</ol>'}</div>`).join('');
        if (home) renderHome();
        const cb = document.querySelector('.c-complete button');
        if (cb && current) { cb.classList.toggle('done', isDone(current.id)); cb.textContent = isDone(current.id) ? '✓ Lección completada' : 'Marcar como completada'; }
    }

    // ------------------------------------------------------------ cabecera y pie de la lección
    function lessonHeader() {
        const l = current;
        const head = el('header', null, `<div class="kicker">Módulo ${l.mod} · ${l.modTitle}</div><h1>${l.n}. ${l.titulo}</h1>
            <div class="meta">Lección ${l.mod}.${l.n} · unos ${l.min} minutos</div>
            <div class="objectives"><h4>Al terminar podrás</h4><ul>${l.objetivos.map(o => `<li>${o}</li>`).join('')}</ul></div>`);
        article.prepend(head);
        const i = lessons.indexOf(l), prev = lessons[i - 1], next = lessons[i + 1];
        const complete = el('div', 'c-complete', '<button type="button"></button><span>Se marca sola al responder toda la autoevaluación.</span>');
        complete.querySelector('button').addEventListener('click', () => markDone(l.id, !isDone(l.id)));
        const nav = el('nav', 'c-nav');
        nav.setAttribute('aria-label', 'Lecciones');
        nav.innerHTML = (prev ? `<a class="prev" href="${prev.href}"><small>← Anterior</small>${prev.mod}.${prev.n} ${prev.titulo}</a>` : `<a class="prev" href="${HERE}index.html"><small>← Curso</small>Índice</a>`) +
                        (next ? `<a class="next" href="${next.href}"><small>Siguiente →</small>${next.mod}.${next.n} ${next.titulo}</a>` : `<a class="next" href="${HERE}index.html"><small>Fin de los módulos disponibles</small>Volver al índice</a>`);
        article.append(complete, nav);
    }

    // ------------------------------------------------------------ componentes
    function options(box, onPick) {
        const ul = box.querySelector(':scope > .options');
        if (!ul) return [];
        const btns = [...ul.children].map(li => {
            const b = el('button', 'opt', li.innerHTML);
            b.type = 'button'; b.dataset.k = li.dataset.k; if (li.dataset.why) b.dataset.why = li.dataset.why;
            li.replaceWith(b);
            b.addEventListener('click', () => onPick(b, btns));
            return b;
        });
        return btns;
    }
    function predicts() {
        article.querySelectorAll('.predict').forEach(box => {
            const reveal = box.querySelector('.reveal');
            if (reveal) reveal.hidden = true;
            const ans = box.dataset.answer;
            options(box, (b, btns) => {
                btns.forEach(x => { x.disabled = true; });
                if (ans) { b.classList.add(b.dataset.k === ans ? 'right' : 'wrong'); btns.find(x => x.dataset.k === ans)?.classList.add('right'); }
                else b.classList.add('picked-neutral');
                if (reveal) reveal.hidden = false;
            });
        });
    }
    function quizzes() {
        article.querySelectorAll('.quiz').forEach(quiz => {
            const qs = [...quiz.querySelectorAll('.q')];
            const score = el('p', 'quiz-score');
            quiz.append(score);
            let answered = 0, right = 0;
            qs.forEach(q => {
                const ans = q.dataset.answer;
                options(q, (b, btns) => {
                    btns.forEach(x => { x.disabled = true; });
                    const ok = b.dataset.k === ans;
                    b.classList.add(ok ? 'right' : 'wrong');
                    const correct = btns.find(x => x.dataset.k === ans);
                    if (!ok) correct.classList.add('right');
                    const why = el('div', 'why ' + (ok ? 'ok' : 'ko'), (ok ? '✓ ' : '✗ ') + (b.dataset.why || '') + (!ok && correct.dataset.why ? `<br>✓ ${correct.dataset.why}` : ''));
                    q.append(why);
                    answered++; if (ok) right++;
                    score.textContent = `${right} de ${answered} correctas` + (answered === qs.length ? ` · ${right === qs.length ? '¡perfecto!' : 'repasa las explicaciones'}` : '');
                    score.classList.toggle('ok', answered === qs.length && right === qs.length);
                    if (answered === qs.length && current) markDone(current.id);
                });
            });
        });
    }
    function sims() {
        article.querySelectorAll('figure.sim[data-src]').forEach(fig => {
            const src = fig.dataset.src, h = +(fig.dataset.h || 640);
            const head = el('div', 'sim-head', `<b>▶ ${fig.dataset.title || 'Simulación'}</b><a href="${src}" target="_blank" rel="noopener">Abrir en pestaña nueva ↗</a>`);
            const btn = el('button', 'sim-load', 'Cargar la simulación aquí');
            btn.type = 'button';
            const load = () => {
                if (!btn.isConnected) return;
                const f = el('iframe');
                f.src = src; f.title = fig.dataset.title || 'Simulación';
                f.style.height = (window.innerWidth < 700 ? Math.min(h, 560) : h) + 'px';
                f.setAttribute('loading', 'lazy');
                btn.replaceWith(f);
            };
            btn.addEventListener('click', load);
            fig.prepend(head, btn);
            // se carga sola al acercarse, salvo en conexiones con ahorro de datos
            if ('IntersectionObserver' in window && !(navigator.connection && navigator.connection.saveData)) {
                const io = new IntersectionObserver(es => { if (es.some(e => e.isIntersecting)) { io.disconnect(); load(); } }, { rootMargin: '300px' });
                io.observe(fig);
            }
        });
    }

    // Laboratorio de iones: aniones añaden electrones por orden de llenado; cationes pierden primero los de mayor n
    // (y, con igual n, mayor l). Es la regla de los libros; algunos iones de lantánidos se apartan de ella.
    const ORDER = ['1s', '2s', '2p', '3s', '3p', '4s', '3d', '4p', '5s', '4d', '5p', '6s', '4f', '5d', '6p', '7s', '5f', '6d', '7p'];
    const CAP = { s: 2, p: 6, d: 10, f: 14 }, NORB = { s: 1, p: 3, d: 5, f: 7 }, LV = { s: 0, p: 1, d: 2, f: 3 };
    const NOBLE = [[2, 'He'], [10, 'Ne'], [18, 'Ar'], [36, 'Kr'], [54, 'Xe'], [86, 'Rn']];
    const SUP = '⁰¹²³⁴⁵⁶⁷⁸⁹';
    const sup = n => String(n).split('').map(d => SUP[d]).join('');
    function madelung(z) { const o = {}; let left = z; for (const s of ORDER) { if (!left) break; const n = Math.min(CAP[s[1]], left); o[s] = n; left -= n; } return o; }
    function notation(occ) {
        const tot = Object.values(occ).reduce((a, b) => a + b, 0);
        const core = NOBLE.filter(([n]) => { const c = madelung(n); return n < tot && Object.entries(c).every(([s, k]) => occ[s] === k); }).pop();
        const co = core ? madelung(core[0]) : {};
        const parts = Object.keys(occ).filter(s => occ[s] && occ[s] !== co[s]).sort((a, b) => (+a[0] - +b[0]) || (LV[a[1]] - LV[b[1]])).map(s => s + sup(occ[s]));
        return (core ? `[${core[1]}] ` : '') + (parts.join(' ') || '');
    }
    function ionOcc(e, q) {
        const occ = { ...e.ocupacion };
        if (q < 0) { let add = -q; for (const s of ORDER) { if (!add) break; const free = CAP[s[1]] - (occ[s] || 0); const n = Math.min(free, add); if (n > 0) { occ[s] = (occ[s] || 0) + n; add -= n; } } }
        for (let r = q; r > 0; r--) {
            const s = Object.keys(occ).filter(x => occ[x]).sort((a, b) => (+b[0] - +a[0]) || (LV[b[1]] - LV[a[1]]))[0];
            occ[s]--; if (!occ[s]) delete occ[s];
        }
        return occ;
    }
    const unpaired = occ => Object.entries(occ).reduce((t, [s, k]) => { const m = NORB[s[1]]; return t + (k <= m ? k : 2 * m - k); }, 0);
    function ionLabs() {
        const E = window.EIGENLAB_ELEMENTS;
        article.querySelectorAll('.ion-lab').forEach(box => {
            if (!E) { box.textContent = 'Faltan los datos de los elementos.'; return; }
            const els = E.elementos.filter(e => e.z <= 56);
            box.insertAdjacentHTML('beforeend', `<div class="controls">
                <label>Elemento <select class="il-el">${els.map(e => `<option value="${e.z}">${e.sym} · ${e.nombre}</option>`).join('')}</select></label>
                <label>Carga <select class="il-q">${[-3, -2, -1, 0, 1, 2, 3, 4].map(q => `<option value="${q}">${q > 0 ? '+' + q : q}</option>`).join('')}</select></label></div>
                <div class="out"></div>`);
            const selE = box.querySelector('.il-el'), selQ = box.querySelector('.il-q'), out = box.querySelector('.out');
            selE.value = E.elementos.find(e => e.sym === (box.dataset.el || 'Fe')).z; selQ.value = box.dataset.q || '2';
            const upd = () => {
                const e = E.elementos[+selE.value - 1], q = +selQ.value;
                if (q > e.z) { out.innerHTML = 'No quedan tantos electrones.'; return; }
                const occ = ionOcc(e, q), tot = e.z - q;
                const iso = NOBLE.find(([n]) => n === tot);
                const u = unpaired(occ);
                const name = q === 0 ? e.sym : `${e.sym}${Math.abs(q) > 1 ? sup(Math.abs(q)) : ''}${q > 0 ? '⁺' : '⁻'}`;
                out.innerHTML = `<div><span class="k">Átomo neutro (${e.z} e⁻)</span><br>${e.sym}: ${notation(e.ocupacion)}</div>
                    <div style="margin-top:8px"><span class="k">Ion ${name} (${tot} e⁻)</span><br><span class="v">${iso && q !== 0 ? `[${iso[1]}]</span> <span class="k">= ${notation(occ)}</span>` : (notation(occ) || '— (sin electrones)') + '</span>'}</div>
                    <div style="margin-top:8px"><span class="k">${u === 1 ? '1 electrón desapareado' : `${u} electrones desapareados`}${iso ? ` · isoelectrónico con el ${iso[1]}` : ''}</span></div>`;
            };
            selE.addEventListener('change', upd); selQ.addEventListener('change', upd); upd();
        });
    }

    // ------------------------------------------------------------ índice del curso
    function renderHome() {
        const next = lessons.find(l => !isDone(l.id)) || lessons[0];
        home.querySelector('.modules').innerHTML = C.modulos.map(m => `
            <section class="mod-card${m.proximamente ? ' soon' : ''}"><h2><span class="n">${m.n}</span>${m.titulo}</h2><p>${m.resumen}${m.proximamente ? ' <b>Próximamente.</b>' : ''}</p>
            ${m.lecciones.length ? '<ol>' + m.lecciones.map(l => {
                const id = `${m.n}-${l.n}`, x = lessons.find(y => y.id === id);
                return `<li><a href="${x.href}"><span class="num">${m.n}.${l.n}</span><span>${l.titulo}</span>${isDone(id) ? '<span class="done">✓</span>' : ''}<span class="min">${l.min} min</span></a></li>`;
            }).join('') + '</ol>' : ''}</section>`).join('');
        const st = home.querySelector('.start');
        st.href = next.href;
        st.textContent = progress.done.length ? `Continuar: ${next.mod}.${next.n} ${next.titulo} →` : 'Empezar el curso →';
    }

    // ------------------------------------------------------------ arranque
    buildChrome();
    if (current) { lessonHeader(); predicts(); quizzes(); sims(); ionLabs(); }
    renderChrome();
    document.addEventListener('keydown', ev => {
        if (!current || /INPUT|SELECT|TEXTAREA/.test(ev.target.tagName) || ev.altKey || ev.metaKey || ev.ctrlKey) return;
        const i = lessons.indexOf(current);
        if (ev.key === 'ArrowRight' && ev.shiftKey && lessons[i + 1]) location.href = lessons[i + 1].href;
        if (ev.key === 'ArrowLeft' && ev.shiftKey && lessons[i - 1]) location.href = lessons[i - 1].href;
    });
})();
