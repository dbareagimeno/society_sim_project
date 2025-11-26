"""
Modelo del estado del mundo para SocietySim.

Este módulo define la clase WorldState que contiene todo el estado de la simulación
en un momento dado, incluyendo empresas, partidos, segmentos ciudadanos, políticas
activas, eventos del día e historial.

Example:
    >>> from society_sim.domain import (
    ...     WorldState, Company, Party, CitizenSegment, Sector, IdeologicalBias
    ... )
    >>> company = Company(
    ...     id="tech-001",
    ...     name="TechCorp",
    ...     sector=Sector.TECHNOLOGY,
    ...     base_quality=0.8,
    ...     base_price_level=0.6,
    ... )
    >>> party = Party(
    ...     id="prog-001",
    ...     name="Partido Progresista",
    ...     ideology=IdeologicalBias.CENTER_LEFT,
    ... )
    >>> segment = CitizenSegment(
    ...     id="middle-class",
    ...     name="Clase Media",
    ...     size=1_000_000,
    ...     wealth_per_capita=50_000.0,
    ...     ideological_bias=IdeologicalBias.CENTER,
    ... )
    >>> world = WorldState(
    ...     companies=[company],
    ...     parties=[party],
    ...     citizen_segments=[segment],
    ... )
    >>> world.day
    0
    >>> world.get_company_by_id("tech-001").name
    'TechCorp'
"""

from pydantic import BaseModel, Field, model_validator

from society_sim.domain.citizen_segment import CitizenSegment
from society_sim.domain.company import Company
from society_sim.domain.enums import Sector
from society_sim.domain.event import Event
from society_sim.domain.party import Party
from society_sim.domain.policy import Policy
from society_sim.domain.summary import DaySummary


class WorldState(BaseModel):
    """
    Representa el estado completo del mundo de la simulación en un momento dado.

    Este modelo es el contenedor principal que agrupa todas las entidades
    y métricas de la simulación, permitiendo obtener una vista completa
    del estado actual del mundo simulado.

    Attributes:
        day: Día actual de la simulación (empieza en 0).
        companies: Lista de empresas activas en la simulación.
        parties: Lista de partidos políticos.
        citizen_segments: Lista de segmentos ciudadanos.
        active_policies: Lista de políticas gubernamentales activas.
        events_today: Lista de eventos ocurridos en el día actual.
        history: Historial de resúmenes diarios de la simulación.
    """

    # Día actual de la simulación
    day: int = Field(
        default=0,
        ge=0,
        description="Día actual de la simulación",
    )

    # Entidades principales
    companies: list[Company] = Field(
        ...,
        description="Lista de empresas activas en la simulación",
    )
    parties: list[Party] = Field(
        ...,
        description="Lista de partidos políticos",
    )
    citizen_segments: list[CitizenSegment] = Field(
        ...,
        description="Lista de segmentos ciudadanos",
    )

    # Estado dinámico
    active_policies: list[Policy] = Field(
        default_factory=list,
        description="Lista de políticas gubernamentales activas",
    )
    events_today: list[Event] = Field(
        default_factory=list,
        description="Lista de eventos ocurridos en el día actual",
    )

    # Historial
    history: list[DaySummary] = Field(
        default_factory=list,
        description="Historial de resúmenes diarios de la simulación",
    )

    @model_validator(mode="after")
    def validate_minimum_entities(self) -> "WorldState":
        """
        Valida que exista al menos 1 empresa, 1 partido y 1 segmento ciudadano.

        Raises:
            ValueError: Si no hay al menos una entidad de cada tipo requerido.
        """
        if len(self.companies) < 1:
            raise ValueError("WorldState requiere al menos 1 empresa")
        if len(self.parties) < 1:
            raise ValueError("WorldState requiere al menos 1 partido político")
        if len(self.citizen_segments) < 1:
            raise ValueError("WorldState requiere al menos 1 segmento ciudadano")
        return self

    def get_company_by_id(self, company_id: str) -> Company | None:
        """
        Busca una empresa por su identificador.

        Args:
            company_id: Identificador único de la empresa.

        Returns:
            La empresa si existe, None en caso contrario.

        Example:
            >>> world.get_company_by_id("tech-001")
            Company(id='tech-001', ...)
        """
        for company in self.companies:
            if company.id == company_id:
                return company
        return None

    def get_party_by_id(self, party_id: str) -> Party | None:
        """
        Busca un partido político por su identificador.

        Args:
            party_id: Identificador único del partido.

        Returns:
            El partido si existe, None en caso contrario.

        Example:
            >>> world.get_party_by_id("prog-001")
            Party(id='prog-001', ...)
        """
        for party in self.parties:
            if party.id == party_id:
                return party
        return None

    def get_segment_by_id(self, segment_id: str) -> CitizenSegment | None:
        """
        Busca un segmento ciudadano por su identificador.

        Args:
            segment_id: Identificador único del segmento.

        Returns:
            El segmento si existe, None en caso contrario.

        Example:
            >>> world.get_segment_by_id("middle-class")
            CitizenSegment(id='middle-class', ...)
        """
        for segment in self.citizen_segments:
            if segment.id == segment_id:
                return segment
        return None

    def get_companies_by_sector(self, sector: Sector) -> list[Company]:
        """
        Obtiene todas las empresas que operan en un sector específico.

        Args:
            sector: Sector económico a filtrar.

        Returns:
            Lista de empresas del sector (puede estar vacía).

        Example:
            >>> world.get_companies_by_sector(Sector.TECHNOLOGY)
            [Company(id='tech-001', ...), Company(id='tech-002', ...)]
        """
        return [company for company in self.companies if company.sector == sector]

    model_config = {
        "frozen": False,  # Permitimos mutabilidad para actualizaciones durante la simulación
        "validate_assignment": True,  # Validar al asignar nuevos valores
    }

