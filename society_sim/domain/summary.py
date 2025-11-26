"""
Modelos de resumen diario para SocietySim.

Este módulo define las clases de resumen que capturan métricas agregadas
de la simulación para su análisis histórico.

Example:
    >>> from society_sim.domain import DaySummary, PartySummary, CompanySummary
    >>> party_summary = PartySummary(
    ...     party_id="prog-001",
    ...     name="Partido Progresista",
    ...     popularity=45.0,
    ...     reputation=60.0,
    ... )
    >>> company_summary = CompanySummary(
    ...     company_id="tech-001",
    ...     name="TechCorp",
    ...     stock_price=120.0,
    ...     reputation=75.0,
    ...     revenue=50000.0,
    ... )
    >>> day_summary = DaySummary(
    ...     day=1,
    ...     total_revenue=500000.0,
    ...     average_stock_price=110.0,
    ...     average_satisfaction=55.0,
    ...     parties=[party_summary],
    ...     top_companies=[company_summary],
    ...     events_count=3,
    ...     active_policies_count=2,
    ... )
"""

from pydantic import BaseModel, Field


class PartySummary(BaseModel):
    """
    Resumen del estado de un partido político en un día específico.

    Attributes:
        party_id: Identificador único del partido.
        name: Nombre del partido político.
        popularity: Popularidad del partido al final del día (0.0-100.0).
        reputation: Reputación del partido al final del día (0.0-100.0).
    """

    party_id: str = Field(..., description="Identificador único del partido")
    name: str = Field(..., description="Nombre del partido político")
    popularity: float = Field(..., description="Popularidad al final del día (0.0-100.0)")
    reputation: float = Field(..., description="Reputación al final del día (0.0-100.0)")

    model_config = {
        "frozen": True,  # Los resúmenes son inmutables
    }


class CompanySummary(BaseModel):
    """
    Resumen del estado de una empresa en un día específico.

    Attributes:
        company_id: Identificador único de la empresa.
        name: Nombre comercial de la empresa.
        stock_price: Precio de la acción al final del día.
        reputation: Reputación de la empresa al final del día (0.0-100.0).
        revenue: Ingresos generados durante el día.
    """

    company_id: str = Field(..., description="Identificador único de la empresa")
    name: str = Field(..., description="Nombre comercial de la empresa")
    stock_price: float = Field(..., description="Precio de la acción al final del día")
    reputation: float = Field(..., description="Reputación al final del día (0.0-100.0)")
    revenue: float = Field(..., description="Ingresos generados durante el día")

    model_config = {
        "frozen": True,  # Los resúmenes son inmutables
    }


class DaySummary(BaseModel):
    """
    Resumen completo de métricas de un día de simulación.

    Este modelo captura el estado agregado de la simulación al final de cada día,
    permitiendo análisis histórico y seguimiento de tendencias.

    Attributes:
        day: Número del día de simulación.
        total_revenue: Suma de ingresos de todas las empresas en el día.
        average_stock_price: Precio medio de las acciones de todas las empresas.
        average_satisfaction: Satisfacción media ponderada por tamaño de los segmentos ciudadanos.
        parties: Lista de resúmenes de todos los partidos políticos.
        top_companies: Lista de resúmenes de las empresas con mayores ingresos.
        events_count: Número de eventos que ocurrieron durante el día.
        active_policies_count: Número de políticas activas al final del día.
    """

    day: int = Field(..., ge=0, description="Número del día de simulación")
    total_revenue: float = Field(
        ...,
        ge=0.0,
        description="Suma de ingresos de todas las empresas",
    )
    average_stock_price: float = Field(
        ...,
        ge=0.0,
        description="Precio medio de las acciones",
    )
    average_satisfaction: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Satisfacción media ponderada (0.0-100.0)",
    )
    parties: list[PartySummary] = Field(
        default_factory=list,
        description="Resúmenes de todos los partidos políticos",
    )
    top_companies: list[CompanySummary] = Field(
        default_factory=list,
        description="Resúmenes de las empresas con mayores ingresos",
    )
    events_count: int = Field(
        default=0,
        ge=0,
        description="Número de eventos ocurridos durante el día",
    )
    active_policies_count: int = Field(
        default=0,
        ge=0,
        description="Número de políticas activas al final del día",
    )

    model_config = {
        "frozen": True,  # Los resúmenes son inmutables
    }

