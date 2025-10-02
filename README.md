NutriFlow is a digital platform for active people, athletes, and those looking to improve their diet. It is also for users who need a personalized and flexible meal plan based on their goals, dietary restrictions, and budget.

By William Henao, Nicolas Zapata and Samuel Deossa.

---

## Mejoras de Arquitectura y Patrones de Diseño

A continuación, se documentan las refactorizaciones y patrones de diseño implementados para mejorar la calidad, mantenibilidad y extensibilidad del software.

### 1. Inversión de Dependencias en el Importador de Datos

Esta actividad se centró en refactorizar el comando de gestión `import_csv`.

*   **Problema Identificado:** Inicialmente, el comando (`import_csv`) estaba fuertemente acoplado a la lógica de bajo nivel para leer y procesar un archivo CSV específico. La clase `Command` contenía código para abrir el archivo, leerlo línea por línea y crear objetos en la base de datos. Esto violaba el Principio de Inversión de Dependencias (D de SOLID), ya que un módulo de alto nivel (la política de importación) dependía directamente de un detalle de bajo nivel (el formato CSV).

*   **Solución Aplicada:**
    1.  Se definió una **abstracción** (`ProductImporter`) en `supermarket/services.py`, una interfaz con un método `import_products()`.
    2.  Se creó una **implementación concreta** (`CSVProductImporter`) que hereda de la abstracción y contiene la lógica específica para leer archivos CSV.
    3.  Se modificó el comando `import_csv` para que dependa únicamente de la abstracción `ProductImporter`. La instancia concreta del importador es **inyectada** en el comando en tiempo de ejecución.

*   **Mejoras Obtenidas:**
    *   **Desacoplamiento:** El comando ya no conoce los detalles de la fuente de datos, solo sabe cómo trabajar con la interfaz `ProductImporter`.
    *   **Flexibilidad y Extensibilidad:** El sistema ahora puede soportar nuevos formatos de datos (JSON, XML, etc.) simplemente creando nuevas clases que implementen la interfaz, sin modificar el comando existente.
    *   **Testabilidad:** Es más fácil probar el comando de forma aislada, proporcionando un "doble de prueba" (mock) que implemente la interfaz `ProductImporter`.

### 2. Patrón Factory para la Creación de Importadores

Esta actividad se construyó sobre la refactorización anterior para gestionar la creación de los diferentes tipos de importadores.

*   **Problema Identificado:** Aunque la Inversión de Dependencias desacopló el comando, el propio comando todavía tenía la responsabilidad de decidir qué clase concreta de importador instanciar (ej. `importer = CSVProductImporter(...)`). Si se añadían más importadores, el comando necesitaría una lógica condicional (`if/elif/else`) para seleccionar el correcto, violando el Principio Abierto/Cerrado.

*   **Solución Aplicada:**
    1.  Se implementó el **Patrón Factory (Fábrica)** a través de una clase `ImporterFactory` en `supermarket/services.py`.
    2.  Esta fábrica tiene un método estático `get_importer(file_path)` que centraliza la lógica de selección. Analiza la extensión del archivo y devuelve una instancia del importador concreto correspondiente (`CSVProductImporter`, `JSONProductImporter`, etc.).
    3.  El comando `import_csv` fue modificado para usar esta fábrica. Ahora, en lugar de crear la instancia directamente, simplemente le pide a la fábrica que le proporcione el importador adecuado: `importer = ImporterFactory.get_importer(file_path)`.

*   **Mejoras Obtenidas:**
    *   **Centralización de la Creación:** La lógica para crear importadores ahora reside en un único lugar, facilitando su gestión.
    *   **Principio Abierto/Cerrado:** El comando `import_csv` ahora está "cerrado" a modificaciones pero "abierto" a extensiones. Para soportar un nuevo formato, solo se necesita modificar la fábrica, sin tocar el código del comando.
    *   **Código más Limpio:** Se elimina la lógica condicional de instanciación del cliente (el comando), resultando en un código más limpio y con una responsabilidad más clara.

### 3. Patrón Facade para la Generación de Planes de Comida

Esta actividad se aplicó para simplificar la vista (controlador) `generate_meal_plan`.

*   **Problema Identificado:** La vista `generate_meal_plan` contenía una cantidad excesiva de lógica de negocio. Orquestaba la obtención de datos, la construcción de un *prompt* complejo para la IA, la llamada a la API externa, el parseo y validación de la respuesta, y la gestión de la sesión. Esto hacía que la vista fuera difícil de leer, probar y mantener, violando el principio de Responsabilidad Única.

*   **Solución Aplicada:**
    1.  Se implementó el **Patrón Facade (Fachada)** creando la clase `MealPlanFacade` en un nuevo archivo `ia/services.py`.
    2.  Toda la lógica compleja del subsistema de generación de planes (interacción con la base de datos, la API de OpenAI, etc.) se movió al interior de esta fachada.
    3.  La fachada expone un único método simple, `generate_plan()`, que orquesta todas las operaciones internas y devuelve un resultado claro (ya sea los datos del plan o un error).
    4.  La vista `generate_meal_plan` fue refactorizada para ser un cliente simple de la fachada. Ahora solo instancia `MealPlanFacade` y llama a su método `generate_plan()`, encargándose únicamente de la interacción HTTP (gestión de sesión y renderizado de plantillas).

*   **Mejoras Obtenidas:**
    *   **Separación de Capas:** Se logra una clara separación entre la capa de presentación (la vista) y la capa de lógica de negocio (la fachada).
    *   **Simplificación del Controlador:** La vista es ahora mucho más simple, limpia y centrada en sus responsabilidades de controlador.
    *   **Encapsulación y Reusabilidad:** El complejo subsistema de IA está encapsulado y puede ser reutilizado fácilmente por otras partes de la aplicación sin duplicar código.
    *   **Mejora en la Testabilidad:** La fachada puede ser probada de forma unitaria e independiente de la capa web.
