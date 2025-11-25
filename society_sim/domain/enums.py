"""
Enumeraciones de dominio para SocietySim.

Este módulo define los tipos enumerados básicos utilizados en toda la simulación:
- Sector: sectores económicos de las empresas
- EventType: tipos de eventos que pueden ocurrir
- IdeologicalBias: orientación ideológica de partidos y ciudadanos
"""

from enum import StrEnum


class Sector(StrEnum):
    """Sectores económicos en los que operan las empresas."""

    HOUSING = "housing"
    FOOD = "food"
    TECHNOLOGY = "technology"
    CONSTRUCTION = "construction"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"


class EventType(StrEnum):
    """Tipos de eventos que pueden ocurrir en la simulación."""

    COMPANY_SCANDAL = "company_scandal"
    COMPANY_SUCCESS = "company_success"
    SECTOR_CRISIS = "sector_crisis"
    SECTOR_BOOM = "sector_boom"
    PARTY_SCANDAL = "party_scandal"
    PARTY_SUCCESS = "party_success"
    POLICY_PROPOSAL = "policy_proposal"


class IdeologicalBias(StrEnum):
    """Orientación ideológica de partidos políticos y segmentos ciudadanos."""

    LEFT = "left"
    CENTER_LEFT = "center_left"
    CENTER = "center"
    CENTER_RIGHT = "center_right"
    RIGHT = "right"

