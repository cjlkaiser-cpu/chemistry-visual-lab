# Chemistry Visual Lab - Documentación Técnica

## Descripción

El **Chemistry Visual Lab** contiene **17 simulaciones** interactivas que cubren todo el espectro de química general: desde estructura atómica hasta química nuclear. Cada simulación implementa modelos científicos rigurosos con visualización en Canvas 2D y Three.js para moléculas 3D.

## Simulaciones (17 Total)

### Estructura Atómica (2)
1. **Modelo de Bohr** - Saltos electrónicos, espectros de emisión
2. **Orbitales** - Visualización 3D de orbitales s, p, d, f (Three.js)

### Enlace Químico (2)
3. **VSEPR** - Geometría molecular interactiva 3D
4. **Enlaces** - Covalente, iónico, metálico por electronegatividad

### Estados de la Materia (2)
5. **Gases Reales** - Van der Waals: (P + an²/V²)(V-nb) = nRT
6. **Diagrama de Fases** - Punto triple y punto crítico

### Estequiometría (1)
7. **Reactivo Limitante** - Fábrica visual de moléculas

### Termodinámica (1)
8. **Calorimetría** - q = mcΔT, transferencia de calor

### Equilibrio Químico (2)
9. **Le Chatelier** - Respuesta a perturbaciones
10. **Solubilidad** - K_sp, precipitados

### Cinética Química (1)
11. **Cinética-Colisiones** - Arrhenius: k = A·e^(-E_a/RT)

### Ácidos y Bases (1)
12. **Titulación** - Curva pH en tiempo real

### Electroquímica (2)
13. **Celda Galvánica** - Zn-Cu, flujo de electrones
14. **Nernst** - E = E° - (RT/nF)ln(Q)

### Química Orgánica (1)
15. **Isomería** - Cis-trans, modelos 3D

### Química Nuclear (1)
16. **Decaimiento** - N(t) = N₀e^(-λt)

### Tabla Periódica (1)
17. **Tendencias** - Radio atómico, energía de ionización

## Modelos Científicos

- **Bohr:** Órbitas cuantizadas, E_n = -R_H(1/n²)
- **VSEPR:** Repulsión de pares electrónicos
- **Van der Waals:** Correcciones a gases ideales
- **Maxwell-Boltzmann:** Distribución de energías
- **Arrhenius:** Dependencia exponencial con T
- **Nernst:** Potencial vs concentración

## Tecnología

### Three.js (3D)
Simulaciones: VSEPR, Orbitales, Isomería
- OrbitControls para rotación
- Geometrías: Sphere, Box, LineSegments
- Lighting: Ambient + Point

### Canvas 2D
14 simulaciones con renderizado 2D
- Maxwell-Boltzmann histogramas
- Gráficas de titulación
- Partículas en movimiento

## Ecuaciones Clave

```
Bohr:
E_n = -13.6 eV / n²

Van der Waals:
(P + an²/V²)(V-nb) = nRT

Michaelis-Menten:
v = Vmax[S]/(Km+[S])

Arrhenius:
k = A · exp(-E_a/RT)

Henderson-Hasselbalch:
pH = pKa + log([A⁻]/[HA])

Nernst:
E = E° - (RT/nF)ln(Q)
```

## Paleta de Colores por Categoría

- Estructura Atómica: Cyan `#22d3ee`
- Enlace Químico: Púrpura `#a855f7`
- Estados: Azul `#3b82f6`
- Equilibrio: Verde `#4ade80`
- Cinética: Naranja `#fb923c`
- Ácidos/Bases: Rosa `#ec4899`

## Referencias

**Archivo más grande:** cinetica-colisiones.html (1,634 líneas)
**Total:** 17 simulaciones, ~18,000 líneas de código

---

**Última actualización:** 2026-01-10
