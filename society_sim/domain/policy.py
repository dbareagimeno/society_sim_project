"""
Modelo de política gubernamental para SocietySim.

Este módulo define las clases Policy y PolicyEffect que representan
políticas gubernamentales con sus efectos sobre sectores y empresas.

Example:
    >>> from society_sim.domain import Policy, PolicyEffect, Sector
    >>> effect = PolicyEffect(
    ...     target_sector=Sector.HOUSING,
    ...     price_modifier=0.9,
    ...     subsidy_amount=50000.0,
    ... )
    >>> policy = Policy(
    ...     id="pol-001",
    ...     name="Ley de Vivienda Asequible",
    ...     description="Subsidios y control de precios para vivienda",
    ...     proposed_by_party_id="party-001",
    ...     effect=effect,
    ...     duration_days=30,
    ...     remaining_days=30,
    ... )
    >>> policy.tick()  # Decrements remaining_days
    >>> policy.remaining_days
    29
"""

from pydantic import BaseModel, Field, field_validator, model_validator

from society_sim.domain.enums import Sector


class PolicyEffect(BaseModel):
    """
    Representa los efectos numéricos de una política sobre las entidades.

    Los modificadores se aplican a las empresas del sector objetivo.

    Attributes:
        target_sector: Sector económico afectado por la política (None = todos).
        price_modifier: Multiplicador de precios (1.0 = sin cambio, <1.0 = más barato).
        tax_rate_delta: Cambio en tasa impositiva (positivo = más impuestos).
        subsidy_amount: Cantidad de subsidio a empresas del sector.
        reputation_boost: Mejora de reputación para empresas del sector.
    """

    target_sector: Sector | None = Field(
        default=None,
        description="Sector afectado por la política (None = todos los sectores)",
    )
    price_modifier: float = Field(
        default=1.0,
        gt=0.0,
        description="Multiplicador de precios (1.0 = sin cambio)",
    )
    tax_rate_delta: float = Field(
        default=0.0,
        description="Cambio en tasa impositiva",
    )
    subsidy_amount: float = Field(
        default=0.0,
        ge=0.0,
        description="Cantidad de subsidio a empresas del sector",
    )
    reputation_boost: float = Field(
        default=0.0,
        description="Mejora de reputación para empresas del sector",
    )

    model_config = {
        "frozen": True,  # PolicyEffect es inmutable una vez creado
    }


class Policy(BaseModel):
    """
    Representa una política gubernamental en la simulación.

    Las políticas son regulaciones temporales propuestas por partidos
    que afectan a empresas de un sector específico durante un período
    determinado de días.

    Attributes:
        id: Identificador único de la política.
        name: Nombre corto de la política.
        description: Descripción detallada de la política.
        proposed_by_party_id: ID del partido que propuso la política.
        effect: Efectos numéricos de la política sobre las entidades.
        duration_days: Duración total de la política en días.
        remaining_days: Días restantes de vigencia.
        is_active: Si la política está actualmente activa.
    """

    id: str = Field(..., description="Identificador único de la política")
    name: str = Field(..., description="Nombre corto de la política")
    description: str = Field(..., description="Descripción detallada")
    proposed_by_party_id: str = Field(
        ...,
        description="ID del partido que propuso la política",
    )
    effect: PolicyEffect = Field(..., description="Efectos numéricos de la política")
    duration_days: int = Field(
        ...,
        gt=0,
        description="Duración total en días",
    )
    remaining_days: int = Field(
        ...,
        ge=0,
        description="Días restantes de vigencia",
    )
    is_active: bool = Field(
        default=True,
        description="Si la política está actualmente activa",
    )

    @model_validator(mode="after")
    def validate_remaining_not_greater_than_duration(self) -> "Policy":
        """Asegura que remaining_days no sea mayor que duration_days."""
        if self.remaining_days > self.duration_days:
            raise ValueError(
                f"remaining_days ({self.remaining_days}) no puede ser mayor "
                f"que duration_days ({self.duration_days})"
            )
        return self

    @field_validator("remaining_days")
    @classmethod
    def validate_remaining_days_non_negative(cls, v: int) -> int:
        """Asegura que remaining_days no sea negativo."""
        if v < 0:
            raise ValueError("remaining_days no puede ser negativo")
        return v

    def tick(self) -> "Policy":
        """
        Avanza la política un día, decrementando remaining_days.

        Si remaining_days llega a 0, la política se desactiva automáticamente.

        Returns:
            Una nueva instancia de Policy con remaining_days decrementado
            y is_active actualizado según corresponda.

        Example:
            >>> policy = Policy(
            ...     id="pol-001",
            ...     name="Test",
            ...     description="Test policy",
            ...     proposed_by_party_id="party-001",
            ...     effect=PolicyEffect(),
            ...     duration_days=3,
            ...     remaining_days=2,
            ... )
            >>> updated = policy.tick()
            >>> updated.remaining_days
            1
            >>> updated.is_active
            True
            >>> final = updated.tick()
            >>> final.remaining_days
            0
            >>> final.is_active
            False
        """
        new_remaining = max(0, self.remaining_days - 1)
        new_is_active = new_remaining > 0

        return self.model_copy(
            update={
                "remaining_days": new_remaining,
                "is_active": new_is_active,
            }
        )

    model_config = {
        "frozen": False,  # Permitimos model_copy para el método tick()
        "validate_assignment": True,  # Validar al asignar nuevos valores
    }

