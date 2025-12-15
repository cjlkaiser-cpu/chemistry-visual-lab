# Chemistry Visual Lab

Laboratorio virtual interactivo de simulaciones de química para educación secundaria y universitaria. Colección de 17 simulaciones HTML5 que cubren temas fundamentales de química general, química orgánica, termodinámica y electroquímica.

## Características

- **17 simulaciones interactivas** con visualizaciones en tiempo real
- **3 simulaciones con Three.js** para visualización molecular 3D avanzada
- **Sin dependencias de servidor** - funciona directamente en el navegador
- **Diseño responsive** - adaptable a diferentes tamaños de pantalla
- **Interfaz moderna** con tema oscuro y controles intuitivos

## Simulaciones Incluidas

### Estructura Atómica y Molecular
| Simulación | Descripción | Tecnología |
|------------|-------------|------------|
| **Modelo de Bohr** | Niveles de energía y transiciones electrónicas | Canvas 2D |
| **Orbitales Atómicos** | Visualización 3D de nubes de densidad electrónica (s, p, d) | Three.js |
| **Geometría VSEPR** | Geometría molecular 3D con 22 moléculas | Three.js |
| **Isomería Geométrica** | Isómeros cis-trans/E-Z con propiedades físicas | Three.js |
| **Tendencias Periódicas** | Radio atómico, electronegatividad, energía de ionización | Canvas 2D |

### Termodinámica y Equilibrio
| Simulación | Descripción | Tecnología |
|------------|-------------|------------|
| **Gases Reales** | Ecuación de Van der Waals vs gas ideal | Canvas 2D |
| **Diagrama de Fases** | Transiciones de fase del agua | Canvas 2D |
| **Calorimetría** | Transferencia de calor y equilibrio térmico | Canvas 2D |
| **Equilibrio de Le Chatelier** | Respuesta del equilibrio a perturbaciones | Canvas 2D |
| **Solubilidad** | Curvas de solubilidad y saturación | Canvas 2D |

### Cinética y Reacciones
| Simulación | Descripción | Tecnología |
|------------|-------------|------------|
| **Cinética de Colisiones** | Teoría de colisiones y velocidad de reacción | Canvas 2D |
| **Reactivo Limitante** | Estequiometría y rendimiento de reacciones | Canvas 2D |
| **Decaimiento Radiactivo** | Vida media y constante de desintegración | Canvas 2D |

### Electroquímica y Ácido-Base
| Simulación | Descripción | Tecnología |
|------------|-------------|------------|
| **Celda Galvánica** | Pilas electroquímicas y potenciales de reducción | Canvas 2D |
| **Ecuación de Nernst** | Potencial de celda bajo condiciones no estándar | Canvas 2D |
| **Titulación Ácido-Base** | Curvas de titulación y puntos de equivalencia | Canvas 2D |

## Uso

1. Clona o descarga el repositorio
2. Abre `index.html` en cualquier navegador moderno
3. Navega por las simulaciones desde el menú principal

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/chemistry-visual-lab.git

# Abrir en el navegador
open chemistry-visual-lab/index.html
```

## Tecnologías

- **HTML5 Canvas** - Renderizado 2D para gráficos y animaciones
- **Three.js r128** - Visualización 3D de moléculas con WebGL
- **CSS3** - Diseño responsive con variables CSS y gradientes
- **JavaScript ES6+** - Lógica de simulación y cálculos

## Simulaciones 3D Destacadas

### Geometría VSEPR
Visualiza la geometría molecular basada en la teoría VSEPR con:
- 22 moléculas predefinidas (BeCl₂ a IF₅)
- Enlaces simples, dobles y triples
- Pares solitarios con efecto de transparencia
- Etiquetas de ángulos de enlace
- Controles OrbitControls para rotación libre

### Orbitales Atómicos
Explora la distribución de densidad electrónica con:
- Orbitales s, p y d hasta n=4
- Muestreo Monte Carlo para densidad de probabilidad
- Visualización por fase (función de onda positiva/negativa)
- Gráfica de distribución radial P(r)
- Hasta 25,000 puntos con blending aditivo

### Isomería Geométrica
Compara isómeros cis-trans con:
- 4 compuestos representativos
- Propiedades físicas reales (P.F., P.E., momento dipolar)
- Comparación visual instantánea
- Moléculas con dobles enlaces destacados

## Estructura del Proyecto

```
Chemistry Visual Lab/
├── index.html              # Página principal con navegación
├── README.md               # Este archivo
├── modelo-bohr.html        # Modelo atómico de Bohr
├── orbitales.html          # Orbitales atómicos 3D
├── vsepr.html              # Geometría molecular 3D
├── isomeria.html           # Isomería geométrica 3D
├── tendencias.html         # Tendencias periódicas
├── gases-reales.html       # Ecuación de Van der Waals
├── diagrama-fases.html     # Diagrama de fases
├── calorimetria.html       # Calorimetría
├── le-chatelier.html       # Equilibrio de Le Chatelier
├── solubilidad.html        # Curvas de solubilidad
├── cinetica-colisiones.html # Teoría de colisiones
├── reactivo-limitante.html # Estequiometría
├── decaimiento.html        # Decaimiento radiactivo
├── celda-galvanica.html    # Celdas electroquímicas
├── nernst.html             # Ecuación de Nernst
└── titulacion.html         # Titulación ácido-base
```

## Compatibilidad

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

Requiere soporte para WebGL para las simulaciones 3D.

## Licencia

MIT License - Uso libre para propósitos educativos.

## Créditos

Desarrollado como recurso educativo para la enseñanza de química.
