"""
Módulo de dominio de SocietySim.

Contiene los modelos de datos y tipos fundamentales del simulador.
"""

from society_sim.domain.company import Company
from society_sim.domain.enums import EventType, IdeologicalBias, Sector

__all__ = [
    "Company",
    "EventType",
    "IdeologicalBias",
    "Sector",
]
