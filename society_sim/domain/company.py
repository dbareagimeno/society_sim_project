"""
Modelo de empresa para SocietySim.

Este módulo define la clase Company que representa una empresa en la simulación
con sus atributos estáticos (sector, calidad base, nivel de precio) y dinámicos
(reputación, cotización, efectivo, ventas).

Example:
    >>> from society_sim.domain import Company, Sector
    >>> empresa = Company(
    ...     id="tech-001",
    ...     name="TechCorp",
    ...     sector=Sector.TECHNOLOGY,
    ...     base_quality=0.8,
    ...     base_price_level=0.6,
    ... )
    >>> empresa.reputation
    50.0
    >>> empresa.stock_price
    100.0
"""

from pydantic import BaseModel, Field, field_validator

from society_sim.domain.enums import Sector


class Company(BaseModel):
    """
    Representa una empresa en la simulación.

    Attributes:
        id: Identificador único de la empresa (UUID o slug).
        name: Nombre comercial de la empresa.
        sector: Sector económico en el que opera.
        base_quality: Calidad base de productos/servicios (0.0-1.0).
        base_price_level: Nivel de precio relativo (0.0-1.0, donde 1.0 = caro).
        reputation: Reputación actual de la empresa (0.0-100.0).
        stock_price: Precio de la acción en bolsa (> 0).
        cash: Efectivo disponible (>= 0).
        last_day_units_sold: Unidades vendidas en el último día.
        last_day_revenue: Ingresos del último día.
    """

    # Campos estáticos (identificación y características base)
    id: str = Field(..., description="Identificador único de la empresa")
    name: str = Field(..., description="Nombre comercial de la empresa")
    sector: Sector = Field(..., description="Sector económico de operación")
    base_quality: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Calidad base de productos/servicios (0.0-1.0)",
    )
    base_price_level: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Nivel de precio relativo (0.0=barato, 1.0=caro)",
    )

    # Campos dinámicos (evolucionan durante la simulación)
    # Nota: reputation usa validador personalizado para clamping en lugar de ge/le
    reputation: float = Field(
        default=50.0,
        description="Reputación actual (0.0-100.0)",
    )
    stock_price: float = Field(
        default=100.0,
        gt=0.0,
        description="Precio de la acción (> 0)",
    )
    cash: float = Field(
        default=1_000_000.0,
        ge=0.0,
        description="Efectivo disponible (>= 0)",
    )

    # Métricas diarias (se actualizan cada día de simulación)
    last_day_units_sold: int = Field(
        default=0,
        ge=0,
        description="Unidades vendidas en el último día",
    )
    last_day_revenue: float = Field(
        default=0.0,
        ge=0.0,
        description="Ingresos del último día",
    )

    @field_validator("reputation")
    @classmethod
    def validate_reputation_range(cls, v: float) -> float:
        """Asegura que la reputación esté en el rango [0, 100]."""
        if v < 0.0:
            return 0.0
        if v > 100.0:
            return 100.0
        return v

    @field_validator("stock_price")
    @classmethod
    def validate_stock_price_positive(cls, v: float) -> float:
        """Asegura que el precio de la acción sea positivo."""
        if v <= 0.0:
            raise ValueError("stock_price debe ser mayor que 0")
        return v

    @field_validator("base_quality", "base_price_level")
    @classmethod
    def validate_zero_to_one_range(cls, v: float) -> float:
        """Asegura que los valores base estén en el rango [0, 1]."""
        if v < 0.0 or v > 1.0:
            raise ValueError("El valor debe estar en el rango [0.0, 1.0]")
        return v

    model_config = {
        "frozen": False,  # Permitimos mutabilidad para actualizaciones durante la simulación
        "validate_assignment": True,  # Validar al asignar nuevos valores
    }

