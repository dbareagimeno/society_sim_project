"""
Módulo de dominio de SocietySim.

Contiene los modelos de datos y tipos fundamentales del simulador.
"""

from society_sim.domain.citizen_segment import CitizenSegment
from society_sim.domain.company import Company
from society_sim.domain.enums import EventType, IdeologicalBias, Sector
from society_sim.domain.event import Event, EventEffect
from society_sim.domain.party import Party

__all__ = [
    "CitizenSegment",
    "Company",
    "Event",
    "EventEffect",
    "EventType",
    "IdeologicalBias",
    "Party",
    "Sector",
]
