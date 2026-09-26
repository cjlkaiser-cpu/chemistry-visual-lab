// Estructura del curso «La Tabla Periódica, de dentro afuera». La usan course.js (navegación, progreso)
// y tools/build_catalog.py (buscador). Cada lección vive en modulo-N/leccion-M.html.
window.EIGENLAB_COURSE = {
  "id": "tabla-periodica",
  "titulo": "La Tabla Periódica, de dentro afuera",
  "subtitulo": "De Mendeléyev a la mecánica cuántica: por qué la tabla tiene esta forma y qué nos dice",
  "nivel": "Bachillerato y primeros cursos universitarios, con bloques «Profundizar»",
  "modulos": [
    {
      "n": 1, "titulo": "El orden de los elementos",
      "resumen": "Cómo pasamos de una lista de sustancias a una ley con poder predictivo.",
      "lecciones": [
        {"n": 1, "titulo": "¿Qué es un elemento?", "min": 15,
         "objetivos": ["Distinguir elemento, átomo, isótopo y compuesto", "Relacionar el número atómico Z con la identidad del elemento", "Interpretar la masa atómica como media isotópica"]},
        {"n": 2, "titulo": "Buscando un orden", "min": 15,
         "objetivos": ["Conocer las tríadas de Döbereiner y la ley de las octavas", "Explicar qué hizo distinto Mendeléyev en 1869", "Reconocer el valor científico de dejar huecos"]},
        {"n": 3, "titulo": "Las predicciones de Mendeléyev", "min": 20,
         "objetivos": ["Predecir propiedades de un elemento a partir de sus vecinos", "Comparar las predicciones de 1871 con los valores reales", "Entender por qué una predicción confirmada convierte una clasificación en teoría"]},
        {"n": 4, "titulo": "Moseley: el número atómico", "min": 15,
         "objetivos": ["Explicar por qué la tabla se ordena por Z y no por masa", "Identificar las inversiones de masa (Ar–K, Co–Ni, Te–I)", "Relacionar la ley de Moseley con la carga nuclear"]},
        {"n": 5, "titulo": "La tabla hoy", "min": 15,
         "objetivos": ["Leer periodos, grupos y familias en la tabla actual", "Conocer la recomendación IUPAC sobre el grupo 3", "Saber cómo se crean y nombran los elementos superpesados"]}
      ]
    },
    {
      "n": 2, "titulo": "Dentro del átomo",
      "resumen": "La luz de los átomos revela niveles de energía; tres reglas deciden dónde van los electrones.",
      "lecciones": [
        {"n": 1, "titulo": "La luz de los átomos", "min": 15,
         "objetivos": ["Distinguir espectro continuo y espectro de líneas", "Relacionar cada línea con un salto entre niveles: E = hc/λ", "Usar los espectros para identificar elementos"]},
        {"n": 2, "titulo": "Niveles de energía: el hidrógeno", "min": 20,
         "objetivos": ["Calcular longitudes de onda con la fórmula de Rydberg", "Relacionar las series de Lyman, Balmer y Paschen con los niveles", "Conocer el alcance y los límites del modelo de Bohr"]},
        {"n": 3, "titulo": "Orbitales y números cuánticos", "min": 20,
         "objetivos": ["Describir los números cuánticos n, l, mₗ y mₛ", "Relacionar l con la forma de los orbitales s, p, d y f", "Deducir la capacidad de cada subcapa: 2(2l + 1)"]},
        {"n": 4, "titulo": "Tres reglas: Madelung, Pauli y Hund", "min": 20,
         "objetivos": ["Escribir configuraciones electrónicas con la regla n + l", "Aplicar el principio de exclusión de Pauli", "Aplicar la regla de Hund y contar electrones desapareados"]},
        {"n": 5, "titulo": "Las excepciones", "min": 15,
         "objetivos": ["Identificar las excepciones de Cr y Cu", "Explicar la estabilidad de las subcapas semillenas y llenas", "Reconocer por qué la regla n + l es una aproximación"]}
      ]
    },
    {
      "n": 3, "titulo": "La forma de la tabla",
      "resumen": "Bloques, grupos y valencia: la estructura electrónica dibujada en dos dimensiones.",
      "lecciones": [
        {"n": 1, "titulo": "Bloques s, p, d y f", "min": 15,
         "objetivos": ["Relacionar la anchura de cada bloque con la capacidad de su subcapa", "Localizar un elemento en la tabla a partir de su configuración", "Explicar por qué el bloque f se dibuja aparte"]},
        {"n": 2, "titulo": "Electrones de valencia y grupos", "min": 15,
         "objetivos": ["Contar electrones de valencia en los bloques s y p", "Explicar por qué los elementos de un grupo se parecen", "Usar la notación de gas noble"]},
        {"n": 3, "titulo": "Iones y su configuración", "min": 20,
         "objetivos": ["Escribir la configuración de cationes y aniones", "Aplicar que los metales de transición pierden primero los electrones ns", "Relacionar la carga habitual de un ion con su grupo"]}
      ]
    },
    {
      "n": 4, "titulo": "Tendencias periódicas",
      "resumen": "Carga nuclear efectiva, radio, ionización, electronegatividad y carácter metálico.",
      "lecciones": [
        {"n": 1, "titulo": "Carga nuclear efectiva", "min": 20,
         "objetivos": ["Explicar el apantallamiento de los electrones internos", "Calcular Z_ef con las reglas de Slater", "Usar Z_ef para explicar las tendencias dentro de un periodo y de un grupo"]},
        {"n": 2, "titulo": "El tamaño de los átomos y de los iones", "min": 15,
         "objetivos": ["Describir la tendencia del radio en periodos y grupos", "Distinguir radio covalente, metálico, de van der Waals e iónico", "Ordenar por tamaño una serie isoelectrónica"]},
        {"n": 3, "titulo": "Energía de ionización", "min": 20,
         "objetivos": ["Relacionar la energía de ionización con Z_ef y la distancia al núcleo", "Explicar las irregularidades Be–B y N–O", "Deducir el grupo de un elemento con sus energías de ionización sucesivas"]},
        {"n": 4, "titulo": "Afinidad electrónica y electronegatividad", "min": 20,
         "objetivos": ["Distinguir afinidad electrónica (átomo aislado) y electronegatividad (átomo enlazado)", "Leer la escala de Pauling y su tendencia", "Predecir el tipo de enlace con la diferencia de electronegatividad"]},
        {"n": 5, "titulo": "Carácter metálico y dos sorpresas", "min": 15,
         "objetivos": ["Describir la tendencia del carácter metálico", "Explicar la contracción lantánida y sus consecuencias", "Reconocer las relaciones diagonales"]}
      ]
    },
    {
      "n": 5, "titulo": "Familias",
      "resumen": "Alcalinos, halógenos, gases nobles, metales de transición, lantánidos y actínidos.",
      "lecciones": [
        {"n": 1, "titulo": "Alcalinos y alcalinotérreos", "min": 15,
         "objetivos": ["Relacionar la configuración ns¹ y ns² con los iones M⁺ y M²⁺", "Explicar por qué la reactividad crece al bajar en el grupo", "Interpretar los colores de llama como espectros de emisión"]},
        {"n": 2, "titulo": "Halógenos", "min": 15,
         "objetivos": ["Relacionar la configuración ns² np⁵ con el ion X⁻ y la molécula X₂", "Explicar el paso de gas a sólido con las fuerzas de London", "Predecir reacciones de desplazamiento con el poder oxidante"]},
        {"n": 3, "titulo": "Gases nobles", "min": 15,
         "objetivos": ["Relacionar la capa completa con su baja reactividad", "Conocer los compuestos de xenón y kriptón y su historia", "Explicar por qué la reactividad crece al bajar"]},
        {"n": 4, "titulo": "Metales de transición", "min": 20,
         "objetivos": ["Escribir la configuración de iones de transición", "Explicar los estados de oxidación variables", "Relacionar el color y el magnetismo con la subcapa d incompleta"]},
        {"n": 5, "titulo": "Lantánidos y actínidos", "min": 20,
         "objetivos": ["Explicar la química uniforme de los lantánidos", "Relacionar la contracción lantánida con su separación", "Distinguir el comportamiento de los primeros actínidos"]}
      ]
    },
    {
      "n": 6, "titulo": "Más allá de la tabla",
      "resumen": "Origen cósmico, efectos relativistas, superpesados y los elementos de la tecnología.",
      "lecciones": [
        {"n": 1, "titulo": "De dónde vienen los elementos", "min": 20,
         "objetivos": ["Identificar las fuentes de los elementos: Big Bang, estrellas, supernovas, rayos cósmicos", "Explicar por qué la fusión estelar se detiene en el grupo del hierro", "Interpretar la curva de abundancias del sistema solar"]},
        {"n": 2, "titulo": "Más allá del hierro: captura de neutrones", "min": 20,
         "objetivos": ["Explicar la captura de neutrones y la desintegración β⁻", "Distinguir los procesos s y r", "Relacionar los picos de abundancia con los números mágicos"]},
        {"n": 3, "titulo": "Efectos relativistas", "min": 20,
         "objetivos": ["Estimar la velocidad del electrón 1s con v/c ≈ Zα", "Explicar la contracción de los orbitales s y p", "Relacionar la relatividad con el color del oro y el mercurio líquido"]},
        {"n": 4, "titulo": "Los superpesados", "min": 15,
         "objetivos": ["Describir cómo se sintetizan los elementos superpesados", "Conocer los últimos elementos nombrados", "Explicar qué es la isla de estabilidad"]},
        {"n": 5, "titulo": "Los elementos de la tecnología", "min": 15,
         "objetivos": ["Identificar los elementos de un teléfono móvil y su función", "Conocer el concepto de materia prima crítica", "Relacionar la escasez y el reciclado con la química de los elementos"]}
      ]
    }
  ]
};
