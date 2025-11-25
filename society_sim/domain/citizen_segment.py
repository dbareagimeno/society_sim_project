"""
Modelo de segmento ciudadano para SocietySim.

Este módulo define la clase CitizenSegment que representa un grupo de ciudadanos
agrupados por clase socioeconómica, permitiendo simular consumo y satisfacción
sin modelar individuos.

Example:
    >>> from society_sim.domain import CitizenSegment, IdeologicalBias
    >>> segmento = CitizenSegment(
    ...     id="middle-class",
    ...     name="Clase Media",
    ...     size=1_000_000,
    ...     wealth_per_capita=50_000.0,
    ...     ideological_bias=IdeologicalBias.CENTER,
    ... )
    >>> segmento.satisfaction
    50.0
    >>> segmento.total_wealth
    50000000000.0
"""

from pydantic import BaseModel, Field, computed_field, field_validator

from society_sim.domain.enums import IdeologicalBias


class CitizenSegment(BaseModel):
    """
    Representa un segmento de ciudadanos agrupados por clase socioeconómica.

    Attributes:
        id: Identificador único del segmento.
        name: Nombre del segmento (e.g., "Clase Alta", "Clase Media").
        size: Número de ciudadanos representados en el segmento.
        wealth_per_capita: Riqueza media por persona en el segmento.
        satisfaction: Satisfacción actual del segmento (0.0-100.0).
        preferred_party_id: ID del partido preferido por el segmento (opcional).
        ideological_bias: Orientación ideológica del segmento.
        consumption_rate: Porcentaje de riqueza gastado diariamente (0.0-1.0).
    """

    # Campos de identificación
    id: str = Field(..., description="Identificador único del segmento")
    name: str = Field(..., description="Nombre del segmento ciudadano")

    # Campos demográficos y económicos
    size: int = Field(
        ...,
        gt=0,
        description="Número de ciudadanos representados",
    )
    wealth_per_capita: float = Field(
        ...,
        ge=0.0,
        description="Riqueza media por persona",
    )

    # Campos dinámicos (evolucionan durante la simulación)
    satisfaction: float = Field(
        default=50.0,
        description="Satisfacción actual (0.0-100.0)",
    )

    # Campos de preferencia política
    preferred_party_id: str | None = Field(
        default=None,
        description="ID del partido preferido por el segmento",
    )
    ideological_bias: IdeologicalBias = Field(
        ...,
        description="Orientación ideológica del segmento",
    )

    # Campo de propensión al consumo
    consumption_rate: float = Field(
        default=0.1,
        ge=0.0,
        le=1.0,
        description="Porcentaje de riqueza gastado diariamente (0.0-1.0)",
    )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def total_wealth(self) -> float:
        """Calcula la riqueza total del segmento (size * wealth_per_capita)."""
        return self.size * self.wealth_per_capita

    @field_validator("satisfaction")
    @classmethod
    def validate_satisfaction_range(cls, v: float) -> float:
        """Asegura que la satisfacción esté en el rango [0, 100]."""
        if v < 0.0:
            return 0.0
        if v > 100.0:
            return 100.0
        return v

    @field_validator("consumption_rate")
    @classmethod
    def validate_consumption_rate_range(cls, v: float) -> float:
        """Asegura que el consumption_rate esté en el rango [0, 1]."""
        if v < 0.0:
            raise ValueError("consumption_rate debe ser mayor o igual a 0")
        if v > 1.0:
            raise ValueError("consumption_rate debe ser menor o igual a 1")
        return v

    model_config = {
        "frozen": False,  # Permitimos mutabilidad para actualizaciones durante la simulación
        "validate_assignment": True,  # Validar al asignar nuevos valores
    }

