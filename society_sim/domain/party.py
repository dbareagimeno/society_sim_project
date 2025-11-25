"""
Modelo de partido político para SocietySim.

Este módulo define la clase Party que representa un partido político en la simulación
con sus atributos de ideología, popularidad y participación en el gobierno.

Example:
    >>> from society_sim.domain import Party, IdeologicalBias
    >>> partido = Party(
    ...     id="prog-001",
    ...     name="Partido Progresista",
    ...     ideology=IdeologicalBias.CENTER_LEFT,
    ... )
    >>> partido.popularity
    20.0
    >>> partido.reputation
    50.0
    >>> partido.in_government
    False
"""

from pydantic import BaseModel, Field, field_validator

from society_sim.domain.enums import IdeologicalBias


class Party(BaseModel):
    """
    Representa un partido político en la simulación.

    Attributes:
        id: Identificador único del partido.
        name: Nombre del partido político.
        ideology: Orientación ideológica del partido.
        popularity: Popularidad actual del partido (0.0-100.0).
        reputation: Reputación actual del partido (0.0-100.0).
        in_government: Indica si el partido está en el gobierno.
    """

    # Campos de identificación
    id: str = Field(..., description="Identificador único del partido")
    name: str = Field(..., description="Nombre del partido político")
    ideology: IdeologicalBias = Field(..., description="Orientación ideológica")

    # Campos dinámicos (evolucionan durante la simulación)
    popularity: float = Field(
        default=20.0,
        description="Popularidad actual (0.0-100.0)",
    )
    reputation: float = Field(
        default=50.0,
        description="Reputación actual (0.0-100.0)",
    )
    in_government: bool = Field(
        default=False,
        description="Indica si el partido está en el gobierno",
    )

    @field_validator("popularity")
    @classmethod
    def validate_popularity_range(cls, v: float) -> float:
        """Asegura que la popularidad esté en el rango [0, 100]."""
        if v < 0.0:
            return 0.0
        if v > 100.0:
            return 100.0
        return v

    @field_validator("reputation")
    @classmethod
    def validate_reputation_range(cls, v: float) -> float:
        """Asegura que la reputación esté en el rango [0, 100]."""
        if v < 0.0:
            return 0.0
        if v > 100.0:
            return 100.0
        return v

    model_config = {
        "frozen": False,  # Permitimos mutabilidad para actualizaciones durante la simulación
        "validate_assignment": True,  # Validar al asignar nuevos valores
    }

