"""
Módulo de dominio de SocietySim.

Contiene los modelos de datos y tipos fundamentales del simulador.
"""

from society_sim.domain.citizen_segment import CitizenSegment
from society_sim.domain.company import Company
from society_sim.domain.enums import EventType, IdeologicalBias, Sector
from society_sim.domain.event import Event, EventEffect
from society_sim.domain.factory import create_initial_world
from society_sim.domain.party import Party
from society_sim.domain.policy import Policy, PolicyEffect
from society_sim.domain.summary import CompanySummary, DaySummary, PartySummary
from society_sim.domain.world_state import WorldState

__all__ = [
    "CitizenSegment",
    "Company",
    "CompanySummary",
    "DaySummary",
    "Event",
    "EventEffect",
    "EventType",
    "IdeologicalBias",
    "Party",
    "PartySummary",
    "Policy",
    "PolicyEffect",
    "Sector",
    "WorldState",
    "create_initial_world",
]
