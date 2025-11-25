# SocietySim – Simulador de sociedad por línea de comandos

## 1. Descripción

SocietySim es un simulador simplificado de una sociedad compuesto por:

- Empresas organizadas por sectores.
- Partidos políticos con popularidad y reputación.
- Ciudadanos agrupados en segmentos socioeconómicos.
- Un sistema de eventos diarios (0–5 por día) que afectan:
  - La reputación y cotización bursátil de las empresas.
  - La popularidad y reputación de los partidos.
  - Las políticas activas que impactan sectores concretos.

El simulador se ejecuta por línea de comandos y muestra logs con la evolución diaria
de la “sociedad”. En una fase posterior, se podrá añadir:

- Integración con una API de LLM para generar eventos narrativos y políticas.
- Una API HTTP para exponer los resultados.
- Un pequeño BI / dashboard para visualizar la historia de la simulación.

## 2. Objetivos del proyecto

- Probar el uso de un IDE con IA (Cursor) en un proyecto autocontenido.
- Diseñar y desarrollar una arquitectura limpia para simulación discreta por días.
- Experimentar con un sistema de reputación, mercado y “política” mínima.
- Dejar el proyecto listo para futuras extensiones (LLM, API, BI).

## 3. Funcionalidades clave (MVP)

1. **Simulación diaria**
   - El sistema avanza día a día (ticks).
   - Cada día se generan entre 0 y 5 eventos aleatorios.
   - Se simula un mercado donde los ciudadanos consumen productos de las empresas.
   - Se actualizan reputación de empresas, stock/cotización y satisfacción de ciudadanos.
   - Se recalcula la popularidad de los partidos políticos.

2. **Empresas**
   - Pertenecen a un sector (p. ej. vivienda, construcción, alimentación, tecnología).
   - Tienen parámetros base:
     - Calidad del servicio.
     - Nivel de precio.
   - Tienen estado dinámico:
     - Reputación.
     - Cotización bursátil.
     - Ventas diarias (unidades y volumen).

3. **Partidos políticos**
   - Tienen popularidad y reputación.
   - Uno o varios pueden estar en el gobierno.
   - Sus decisiones (políticas) afectan a sectores y empresas.
   - Ganan o pierden popularidad según el efecto global sobre la sociedad
     y según eventos (p. ej. escándalos).

4. **Ciudadanos (segmentos)**
   - Agrupados en segmentos (clases socioeconómicas, por ejemplo).
   - Cada segmento tiene:
     - Tamaño (número de ciudadanos representados).
     - Riqueza media.
     - Satisfacción.
     - Preferencias políticas e ideológicas.
   - Consumidores en el mercado: eligen empresas en función de reputación y precio.

5. **Eventos**
   - Tipos básicos:
     - Impactos sobre empresas concretas.
     - Impactos sobre sectores completos.
     - Escándalos de partidos.
     - Propuestas de políticas.
   - Cada evento tiene:
     - Día en que ocurre.
     - Narrativa (texto libre).
     - Targets (empresas, partidos o sectores).
     - Efectos numéricos (cambios en reputación y popularidad).

6. **Logs de CLI**
   - Al final de cada día:
     - Resumen de ingresos totales.
     - Precio medio de las acciones.
     - Satisfacción media ciudadana.
     - Popularidad de los partidos.
     - Reputación y cotización de las empresas principales.

## 4. Modelo conceptual (resumen)

Entidades principales:

- `Company` (empresa)
- `Party` (partido político)
- `CitizenSegment` (segmento de ciudadanos)
- `Policy` (política)
- `Event` (evento)
- `WorldState` (estado global + historial)

Cada día:

1. Se generan eventos.
2. Los eventos modifican reputaciones, popularidades y políticas activas.
3. Se simula el mercado (ventas de empresas, consumo de ciudadanos).
4. Se actualizan reputación de empresas y precio de sus acciones.
5. Se actualizan satisfacción de ciudadanos y popularidad de partidos.
6. Se registra un resumen del día (para histórico).

## 5. Arquitectura propuesta

La arquitectura se divide en tres capas principales:

- `domain/`: modelos de datos y tipos de dominio.
- `engine/`: lógica de simulación (avance diario, fases del día).
- `events/`: generadores de eventos (random, LLM, etc.).
- `cli/`: punto de entrada por línea de comandos.

Estructura sugerida:

```text
society_sim/
  pyproject.toml / requirements.txt
  society_sim/
    __init__.py
    domain/
      __init__.py
      types.py          # dataclasses y enums de Company, Party, CitizenSegment, Policy, Event, WorldState, etc.
    engine/
      __init__.py
      run_day.py        # función principal para simular un día
      phases/           # (opcional) submódulos para cada fase del día
    events/
      __init__.py
      base.py           # interfaz abstracta de generador de eventos
      random_generator.py
      llm_generator.py  # (fase posterior)
  cli/
    main.py             # script CLI
  tests/
    ...
```

## 6. Flujo de simulación por día

Flujo conceptual que debe implementar el motor:

1. **Generación de eventos**
   - Un generador (por ahora, aleatorio) produce entre 0 y 5 eventos para ese día.
   - Más adelante, un generador basado en LLM se conectará a una API externa.

2. **Aplicación de eventos**
   - Se aplican los efectos numéricos de los eventos sobre:
     - Reputación de empresas.
     - Popularidad y reputación de partidos.
     - Creación o modificación de políticas activas.

3. **Aplicación de políticas**
   - Cada política activa puede afectar numéricamente:
     - A un sector (p. ej. precio máximo, impuestos, subvenciones).
     - A los ingresos o costes de las empresas afectadas.

4. **Simulación del mercado**
   - Cada segmento ciudadano decide cuánto gastar (por ejemplo, porcentaje de su riqueza).
   - Reparte ese gasto entre empresas según su reputación y “nivel de precio”.
   - Se calculan unidades vendidas e ingresos de cada empresa.

5. **Actualización de empresas**
   - Las empresas actualizan:
     - Reputación (por ejemplo, basada en ventas relativas y eventos).
     - Cotización (por ejemplo, basada en ingresos y cambios de reputación).

6. **Actualización de ciudadanos y partidos**
   - Se recalcula la satisfacción de los segmentos ciudadanos según:
     - Resultados de mercado.
     - Políticas activas.
   - Se recalcula la popularidad de los partidos según:
     - Satisfacción global.
     - Eventos específicos (escándalos, éxitos).

7. **Registro de resumen**
   - Se almacena un `DaySummary` con:
     - Día.
     - Ingresos totales.
     - Precio medio de las acciones.
     - Satisfacción media ciudadana.
     - Popularidad de cada partido.

## 7. Requisitos

- Python 3.10+ (recomendado)
- Gestor de paquetes:
  - `pip` o `pipx`, o uso de `poetry`/`pipenv` si se desea.

Dependencias mínimas (MVP):

- No imprescindible nada externo, opcionalmente:
  - `rich` para logs coloreados.
  - `pydantic`/`dataclasses-json` si se quiere serializar a JSON fácilmente.

## 8. Puesta en marcha (MVP)

Pasos esperados (pueden ajustarse al estilo de tooling preferido):

1. Crear entorno virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # en Windows: .venv\Scripts\activate
   ```

2. Instalar dependencias (cuando estén definidas):

   ```bash
   pip install -r requirements.txt
   ```

3. Ejecutar la simulación por defecto (por ejemplo, 30 días):

   ```bash
   python -m cli.main
   ```

   o bien:

   ```bash
   python cli/main.py
   ```

4. Observar los logs en consola con la evolución diaria de:
   - Ingresos.
   - Precio medio de las acciones.
   - Satisfacción media.
   - Popularidad de cada partido.
   - Indicadores básicos de cada empresa.

## 9. Extensiones previstas (más adelante)

- **Generador de eventos con LLM**
  - Implementar un módulo que:
    - Resuma el estado actual del mundo a un JSON compacto.
    - Envíe un prompt a un LLM externo pidiendo entre 0 y 5 eventos nuevos en un formato estructurado.
    - Parse los eventos recibidos y los aplique al estado.

- **Persistencia y exportación de datos**
  - Guardar el histórico completo de `DaySummary` y snapshots en:
    - JSON.
    - CSV.
  - Permitir reanudar simulaciones desde un estado guardado.

- **API HTTP**
  - Exponer:
    - Estado actual.
    - Histórico de días.
  - Endpoints para:
    - Avanzar N días.
    - Resetear el mundo.

- **BI / dashboard**
  - Aplicación sencilla (web o notebook) para visualizar:
    - Gráficos de popularidad de partidos.
    - Evolución de cotizaciones por empresa.
    - Satisfacción media de la población.

## 10. Roadmap sugerido

1. Definir modelos de dominio (`domain/types.py`).
2. Implementar motor diario básico (`engine/run_day.py`) con:
   - Generación aleatoria de eventos.
   - Simulación de mercado muy simplificada.
3. Implementar CLI (`cli/main.py`) que ejecute N días y muestre logs.
4. Ajustar fórmulas y parámetros hasta obtener dinámicas interesantes.
5. Añadir persistencia sencilla (dump a JSON/CSV).
6. Implementar generador de eventos basado en LLM.
7. (Opcional) Añadir API HTTP y BI.
