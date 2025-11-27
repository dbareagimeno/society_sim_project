"""
Módulo del motor de simulación de SocietySim.

Contiene la lógica principal para avanzar la simulación día a día,
incluyendo generación de eventos, simulación de mercado, actualización
de entidades y registro de histórico.
"""

from society_sim.engine.run_day import run_day

__all__ = [
    "run_day",
]
