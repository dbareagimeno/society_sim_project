"""
Modelo de evento para SocietySim.

Este módulo define las clases Event y EventEffect que representan
acontecimientos en la simulación con sus efectos numéricos sobre
las entidades del mundo.

Example:
    >>> from society_sim.domain import Event, EventEffect, EventType, Sector
    >>> effect = EventEffect(reputation_delta=-15.0, stock_price_delta_percent=-5.0)
    >>> event = Event(
    ...     id="evt-001",
    ...     day=5,
    ...     event_type=EventType.COMPANY_SCANDAL,
    ...     narrative="La empresa TechCorp sufre un escándalo de corrupción",
    ...     target_company_ids=["tech-001"],
    ...     effect=effect,
    ... )
    >>> event.event_type
    <EventType.COMPANY_SCANDAL: 'company_scandal'>
"""

from pydantic import BaseModel, Field

from society_sim.domain.enums import EventType, Sector


class EventEffect(BaseModel):
    """
    Representa los efectos numéricos de un evento sobre las entidades.

    Los deltas se aplican a las entidades objetivo del evento.
    Valores positivos indican mejora, negativos indican deterioro.

    Attributes:
        reputation_delta: Cambio en reputación de empresas/partidos.
        popularity_delta: Cambio en popularidad de partidos.
        stock_price_delta_percent: Cambio porcentual en precio de acciones.
        satisfaction_delta: Cambio en satisfacción de ciudadanos.
    """

    reputation_delta: float = Field(
        default=0.0,
        description="Cambio en reputación de empresas o partidos",
    )
    popularity_delta: float = Field(
        default=0.0,
        description="Cambio en popularidad de partidos",
    )
    stock_price_delta_percent: float = Field(
        default=0.0,
        description="Cambio porcentual en precio de acciones",
    )
    satisfaction_delta: float = Field(
        default=0.0,
        description="Cambio en satisfacción de segmentos ciudadanos",
    )

    model_config = {
        "frozen": True,  # EventEffect es inmutable una vez creado
    }


class Event(BaseModel):
    """
    Representa un evento que ocurre en la simulación.

    Los eventos son acontecimientos puntuales que afectan a empresas,
    partidos políticos o sectores económicos, modificando sus métricas
    según los efectos definidos.

    Attributes:
        id: Identificador único del evento.
        day: Día de la simulación en que ocurre el evento.
        event_type: Tipo de evento (escándalo, éxito, crisis, etc.).
        narrative: Descripción textual del evento para narrativa.
        target_company_ids: IDs de empresas afectadas por el evento.
        target_party_ids: IDs de partidos afectados por el evento.
        target_sectors: Sectores económicos afectados por el evento.
        effect: Efectos numéricos del evento sobre las entidades.
    """

    id: str = Field(..., description="Identificador único del evento")
    day: int = Field(..., ge=0, description="Día de la simulación en que ocurre")
    event_type: EventType = Field(..., description="Tipo de evento")
    narrative: str = Field(..., description="Descripción textual del evento")
    target_company_ids: list[str] = Field(
        default_factory=list,
        description="IDs de empresas afectadas",
    )
    target_party_ids: list[str] = Field(
        default_factory=list,
        description="IDs de partidos afectados",
    )
    target_sectors: list[Sector] = Field(
        default_factory=list,
        description="Sectores económicos afectados",
    )
    effect: EventEffect = Field(..., description="Efectos numéricos del evento")

    model_config = {
        "frozen": True,  # Events son inmutables una vez creados
    }

