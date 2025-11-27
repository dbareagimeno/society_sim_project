"""
Motor de simulación diaria para SocietySim.

Este módulo contiene la función principal `run_day` que avanza la simulación
un día, ejecutando todas las fases en orden: generación de eventos, aplicación
de eventos, aplicación de políticas, simulación de mercado, actualización de
entidades y registro de resumen.

Example:
    >>> from society_sim.domain import create_initial_world
    >>> from society_sim.engine import run_day
    >>> world = create_initial_world()
    >>> world.day
    0
    >>> new_world = run_day(world)
    >>> new_world.day
    1
"""

from society_sim.domain.world_state import WorldState


def _generate_events_phase(world: WorldState) -> WorldState:
    """
    Fase 1: Genera eventos aleatorios o narrativos para el día.

    En el futuro, esta fase usará un generador de eventos (aleatorio o LLM)
    para crear eventos que afectarán a empresas, partidos y sectores.

    Args:
        world: Estado actual del mundo.

    Returns:
        WorldState con los eventos del día generados en `events_today`.
    """
    # Stub: por ahora simplemente limpia los eventos del día anterior
    return world.model_copy(update={"events_today": []})


def _apply_events_phase(world: WorldState) -> WorldState:
    """
    Fase 2: Aplica los efectos de los eventos generados.

    Esta fase itera sobre los eventos en `events_today` y aplica sus efectos
    numéricos sobre empresas, partidos y sectores objetivo.

    Args:
        world: Estado actual del mundo con eventos generados.

    Returns:
        WorldState con los efectos de los eventos aplicados.
    """
    # Stub: implementación pendiente en US-3.4
    return world


def _apply_policies_phase(world: WorldState) -> WorldState:
    """
    Fase 3: Aplica los efectos de las políticas activas.

    Esta fase procesa las políticas gubernamentales activas, aplicando
    sus efectos sobre empresas del sector correspondiente y decrementando
    su duración restante.

    Args:
        world: Estado actual del mundo.

    Returns:
        WorldState con los efectos de políticas aplicados.
    """
    # Stub: implementación pendiente en US-4.7
    return world


def _simulate_market_phase(world: WorldState) -> WorldState:
    """
    Fase 4: Simula el mercado y las ventas del día.

    Esta fase calcula el presupuesto de consumo de los ciudadanos,
    distribuye las compras entre empresas según su atractivo y
    actualiza las métricas de ventas.

    Args:
        world: Estado actual del mundo.

    Returns:
        WorldState con las ventas del día calculadas.
    """
    # Stub: implementación pendiente en US-4.2/4.3
    return world


def _update_entities_phase(world: WorldState) -> WorldState:
    """
    Fase 5: Actualiza las entidades basándose en el día transcurrido.

    Esta fase actualiza reputación de empresas, cotización bursátil,
    satisfacción ciudadana y popularidad de partidos.

    Args:
        world: Estado actual del mundo.

    Returns:
        WorldState con entidades actualizadas.
    """
    # Stub: implementación pendiente en US-3.5, US-4.4, US-4.5, US-4.6
    return world


def _record_summary_phase(world: WorldState) -> WorldState:
    """
    Fase 6: Registra el resumen del día en el historial.

    Esta fase calcula métricas agregadas del día y las añade
    al historial para análisis posterior.

    Args:
        world: Estado actual del mundo.

    Returns:
        WorldState con el resumen del día añadido a `history`.
    """
    # Stub: implementación pendiente en US-2.2
    return world


def run_day(world: WorldState) -> WorldState:
    """
    Ejecuta un día completo de simulación.

    Esta función es el punto de entrada principal del motor de simulación.
    Ejecuta todas las fases en orden y devuelve un nuevo estado del mundo
    con el día incrementado.

    Las fases ejecutadas son:
        1. Generación de eventos
        2. Aplicación de efectos de eventos
        3. Aplicación de efectos de políticas
        4. Simulación de mercado
        5. Actualización de entidades
        6. Registro de resumen diario

    Args:
        world: Estado actual del mundo al inicio del día.

    Returns:
        Nuevo WorldState con todas las actualizaciones aplicadas
        y el contador de día incrementado en 1.

    Example:
        >>> from society_sim.domain import create_initial_world
        >>> world = create_initial_world()
        >>> world.day
        0
        >>> new_world = run_day(world)
        >>> new_world.day
        1
        >>> # Simular varios días
        >>> for _ in range(10):
        ...     world = run_day(world)
        >>> world.day
        10
    """
    # Ejecutar todas las fases en orden
    world = _generate_events_phase(world)
    world = _apply_events_phase(world)
    world = _apply_policies_phase(world)
    world = _simulate_market_phase(world)
    world = _update_entities_phase(world)
    world = _record_summary_phase(world)

    # Incrementar el día
    return world.model_copy(update={"day": world.day + 1})

