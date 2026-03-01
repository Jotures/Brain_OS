# RESPUESTAS: TAREA 02 CUESTIONARIO COMPRENSIÓN LECTORA
## CURSO: INVESTIGACIÓN OPERATIVA
## ESTUDIANTE: QUISPE HUALLPA, RUBEN JOSUE

**1. ¿Qué es la programación lineal y cómo se formula matemáticamente?**
La programación lineal (PL) es una técnica de optimización matemática utilizada para resolver problemas donde se busca maximizar o minimizar una función objetivo lineal, sujeta a un conjunto de restricciones también lineales. Matemáticamente, se formula mediante:
- Una **función objetivo**: $Z = c_1x_1 + c_2x_2 + ... + c_nx_n$ (a maximizar o minimizar).
- Un conjunto de **restricciones lineales**: $a_{i1}x_1 + a_{i2}x_2 + ... + a_{in}x_n \leq b_i$.
- **Condiciones de no negatividad**: $x_j \geq 0$.

**2. Diferentes métodos de resolución. ¿Cuál consideras más eficiente en el mundo real y por qué?**
En el mundo real, el **Método Simplex** y los **Algoritmos de Punto Interior** son los más eficientes. El Simplex es ampliamente preferido para problemas prácticos de gran escala debido a su robustez y a que, aunque teóricamente existen casos lentos, en la práctica converge rápidamente a la solución óptima. Sin embargo, para problemas extremadamente grandes (millones de variables), los métodos de punto interior suelen ser superiores.

**3. Aplicaciones más relevantes. Elige una y discútela en profundidad.**
La PL se aplica en logística, finanzas, salud y manufactura. Una aplicación crucial es la **Optimización del Transporte (Logística)**: Permite determinar las rutas y cargas óptimas para enviar productos desde múltiples centros de distribución hacia diversos puntos de venta, minimizando el costo total de transporte sin exceder la capacidad de los vehículos ni incumplir con la demanda de los clientes.

**4. ¿Es realista suponer relaciones lineales siempre? ¿Por qué?**
No siempre es realista. En la práctica, muchos fenómenos presentan rendimientos marginales decrecientes o economías de escala que no son lineales. Por ejemplo, duplicar la inversión en publicidad no siempre duplica las ventas. La linealidad es una simplificación útil para modelar, pero problemas más complejos requieren programación no lineal o entera.

**5. Ejemplo de RRHH: ¿Cómo ayuda la PL a la eficiencia organizacional?**
Ayuda a asignar al personal adecuado a los proyectos correctos, maximizando el aprovechamiento de habilidades específicas y minimizando costos de contratación y capacitación. Garantiza que cada tarea esté cubierta por alguien competente sin sobredimensionar la plantilla.

**6. ¿Qué factores determinan si se debe maximizar o minimizar?**
El factor determinante es el objetivo económico o de gestión:
- Se **maximiza** cuando la función objetivo representa ingresos, utilidades, beneficios o eficiencia.
- Se **minimiza** cuando representa costos, tiempos, riesgos o desperdicio de recursos.

**7. ¿Cómo han transformado los avances tecnológicos (software) la resolución de problemas de PL?**
Software como MATLAB, Excel (Solver), Gurobi y LINDO han eliminado la necesidad de cálculos manuales tediosos, permitiendo resolver modelos con miles de variables en segundos. Esto ha democratizado el uso de la IO, permitiendo que las empresas tomen decisiones basadas en datos en tiempo real.

**8. ¿Por qué es crucial en la toma de decisiones empresariales y gestión de recursos?**
Es crucial porque permite una gestión científica de la escasez. En un entorno de recursos limitados, la PL garantiza que se tome la decisión óptima (la mejor posible), eliminando la intuición subjetiva y reduciendo el margen de error en la asignación estratégica.

**9. ¿Qué tipo de problemas no se pueden abordar adecuadamente con esta técnica?**
Problemas que involucran variables altamente inciertas o estocásticas (que requieren programación estocástica), problemas con relaciones curvas o complejas (no lineales), o aquellos donde las decisiones son cualitativas y no pueden traducirse a funciones matemáticas numéricas.
