"""
Tests unitarios para el modelo Company.

Verifica:
- Creación de empresas válidas
- Validación de campos fuera de rango
- Serialización/deserialización a JSON
"""

import json

import pytest
from pydantic import ValidationError

from society_sim.domain import Company, Sector


class TestCompanyCreation:
    """Tests de creación de empresas válidas."""

    def test_create_company_with_required_fields(self) -> None:
        """Debe crear una empresa con solo los campos requeridos."""
        company = Company(
            id="tech-001",
            name="TechCorp",
            sector=Sector.TECHNOLOGY,
            base_quality=0.8,
            base_price_level=0.6,
        )

        assert company.id == "tech-001"
        assert company.name == "TechCorp"
        assert company.sector == Sector.TECHNOLOGY
        assert company.base_quality == 0.8
        assert company.base_price_level == 0.6

    def test_create_company_has_default_dynamic_values(self) -> None:
        """Debe asignar valores por defecto a campos dinámicos."""
        company = Company(
            id="food-001",
            name="FoodMart",
            sector=Sector.FOOD,
            base_quality=0.5,
            base_price_level=0.3,
        )

        assert company.reputation == 50.0
        assert company.stock_price == 100.0
        assert company.cash == 1_000_000.0
        assert company.last_day_units_sold == 0
        assert company.last_day_revenue == 0.0

    def test_create_company_with_custom_dynamic_values(self) -> None:
        """Debe permitir valores personalizados para campos dinámicos."""
        company = Company(
            id="health-001",
            name="HealthPlus",
            sector=Sector.HEALTHCARE,
            base_quality=0.9,
            base_price_level=0.7,
            reputation=75.0,
            stock_price=250.0,
            cash=5_000_000.0,
            last_day_units_sold=100,
            last_day_revenue=50_000.0,
        )

        assert company.reputation == 75.0
        assert company.stock_price == 250.0
        assert company.cash == 5_000_000.0
        assert company.last_day_units_sold == 100
        assert company.last_day_revenue == 50_000.0

    def test_create_company_with_all_sectors(self) -> None:
        """Debe poder crear empresas en cualquier sector."""
        for sector in Sector:
            company = Company(
                id=f"{sector.value}-001",
                name=f"Company in {sector.value}",
                sector=sector,
                base_quality=0.5,
                base_price_level=0.5,
            )
            assert company.sector == sector


class TestCompanyValidation:
    """Tests de validación de campos fuera de rango."""

    def test_base_quality_below_zero_raises_error(self) -> None:
        """Debe lanzar ValidationError si base_quality < 0."""
        with pytest.raises(ValidationError) as exc_info:
            Company(
                id="test-001",
                name="TestCorp",
                sector=Sector.TECHNOLOGY,
                base_quality=-0.1,
                base_price_level=0.5,
            )
        assert "base_quality" in str(exc_info.value)

    def test_base_quality_above_one_raises_error(self) -> None:
        """Debe lanzar ValidationError si base_quality > 1."""
        with pytest.raises(ValidationError) as exc_info:
            Company(
                id="test-001",
                name="TestCorp",
                sector=Sector.TECHNOLOGY,
                base_quality=1.1,
                base_price_level=0.5,
            )
        assert "base_quality" in str(exc_info.value)

    def test_base_price_level_below_zero_raises_error(self) -> None:
        """Debe lanzar ValidationError si base_price_level < 0."""
        with pytest.raises(ValidationError) as exc_info:
            Company(
                id="test-001",
                name="TestCorp",
                sector=Sector.TECHNOLOGY,
                base_quality=0.5,
                base_price_level=-0.1,
            )
        assert "base_price_level" in str(exc_info.value)

    def test_base_price_level_above_one_raises_error(self) -> None:
        """Debe lanzar ValidationError si base_price_level > 1."""
        with pytest.raises(ValidationError) as exc_info:
            Company(
                id="test-001",
                name="TestCorp",
                sector=Sector.TECHNOLOGY,
                base_quality=0.5,
                base_price_level=1.5,
            )
        assert "base_price_level" in str(exc_info.value)

    def test_reputation_clamped_to_zero(self) -> None:
        """La reputación negativa debe ajustarse a 0."""
        company = Company(
            id="test-001",
            name="TestCorp",
            sector=Sector.TECHNOLOGY,
            base_quality=0.5,
            base_price_level=0.5,
            reputation=-10.0,
        )
        assert company.reputation == 0.0

    def test_reputation_clamped_to_hundred(self) -> None:
        """La reputación mayor a 100 debe ajustarse a 100."""
        company = Company(
            id="test-001",
            name="TestCorp",
            sector=Sector.TECHNOLOGY,
            base_quality=0.5,
            base_price_level=0.5,
            reputation=150.0,
        )
        assert company.reputation == 100.0

    def test_stock_price_zero_raises_error(self) -> None:
        """Debe lanzar ValidationError si stock_price = 0."""
        with pytest.raises(ValidationError) as exc_info:
            Company(
                id="test-001",
                name="TestCorp",
                sector=Sector.TECHNOLOGY,
                base_quality=0.5,
                base_price_level=0.5,
                stock_price=0.0,
            )
        assert "stock_price" in str(exc_info.value)

    def test_stock_price_negative_raises_error(self) -> None:
        """Debe lanzar ValidationError si stock_price < 0."""
        with pytest.raises(ValidationError) as exc_info:
            Company(
                id="test-001",
                name="TestCorp",
                sector=Sector.TECHNOLOGY,
                base_quality=0.5,
                base_price_level=0.5,
                stock_price=-50.0,
            )
        assert "stock_price" in str(exc_info.value)

    def test_cash_negative_raises_error(self) -> None:
        """Debe lanzar ValidationError si cash < 0."""
        with pytest.raises(ValidationError) as exc_info:
            Company(
                id="test-001",
                name="TestCorp",
                sector=Sector.TECHNOLOGY,
                base_quality=0.5,
                base_price_level=0.5,
                cash=-1000.0,
            )
        assert "cash" in str(exc_info.value)

    def test_validate_on_assignment(self) -> None:
        """Debe validar al modificar campos existentes."""
        company = Company(
            id="test-001",
            name="TestCorp",
            sector=Sector.TECHNOLOGY,
            base_quality=0.5,
            base_price_level=0.5,
        )

        with pytest.raises(ValidationError):
            company.stock_price = -10.0


class TestCompanySerialization:
    """Tests de serialización y deserialización JSON."""

    def test_serialize_to_json(self) -> None:
        """Debe poder serializar una empresa a JSON."""
        company = Company(
            id="tech-001",
            name="TechCorp",
            sector=Sector.TECHNOLOGY,
            base_quality=0.8,
            base_price_level=0.6,
        )

        json_str = company.model_dump_json()
        data = json.loads(json_str)

        assert data["id"] == "tech-001"
        assert data["name"] == "TechCorp"
        assert data["sector"] == "technology"
        assert data["base_quality"] == 0.8
        assert data["base_price_level"] == 0.6

    def test_deserialize_from_json(self) -> None:
        """Debe poder deserializar una empresa desde JSON."""
        json_data = {
            "id": "food-001",
            "name": "FoodMart",
            "sector": "food",
            "base_quality": 0.5,
            "base_price_level": 0.3,
            "reputation": 60.0,
            "stock_price": 150.0,
            "cash": 2_000_000.0,
            "last_day_units_sold": 50,
            "last_day_revenue": 10_000.0,
        }

        company = Company.model_validate(json_data)

        assert company.id == "food-001"
        assert company.name == "FoodMart"
        assert company.sector == Sector.FOOD
        assert company.reputation == 60.0
        assert company.stock_price == 150.0

    def test_roundtrip_serialization(self) -> None:
        """Debe mantener los datos tras serializar y deserializar."""
        original = Company(
            id="health-001",
            name="HealthPlus",
            sector=Sector.HEALTHCARE,
            base_quality=0.9,
            base_price_level=0.7,
            reputation=80.0,
            stock_price=200.0,
            cash=3_000_000.0,
            last_day_units_sold=200,
            last_day_revenue=100_000.0,
        )

        # Serializar y deserializar
        json_str = original.model_dump_json()
        restored = Company.model_validate_json(json_str)

        assert restored.id == original.id
        assert restored.name == original.name
        assert restored.sector == original.sector
        assert restored.base_quality == original.base_quality
        assert restored.base_price_level == original.base_price_level
        assert restored.reputation == original.reputation
        assert restored.stock_price == original.stock_price
        assert restored.cash == original.cash
        assert restored.last_day_units_sold == original.last_day_units_sold
        assert restored.last_day_revenue == original.last_day_revenue


class TestCompanyEdgeCases:
    """Tests de casos límite."""

    def test_boundary_values_accepted(self) -> None:
        """Debe aceptar valores en los límites exactos."""
        company = Company(
            id="edge-001",
            name="EdgeCase",
            sector=Sector.FINANCE,
            base_quality=0.0,
            base_price_level=1.0,
            reputation=0.0,
            stock_price=0.01,
            cash=0.0,
        )

        assert company.base_quality == 0.0
        assert company.base_price_level == 1.0
        assert company.reputation == 0.0
        assert company.stock_price == 0.01
        assert company.cash == 0.0

    def test_maximum_values_accepted(self) -> None:
        """Debe aceptar valores máximos válidos."""
        company = Company(
            id="max-001",
            name="MaxCorp",
            sector=Sector.CONSTRUCTION,
            base_quality=1.0,
            base_price_level=1.0,
            reputation=100.0,
            stock_price=999_999_999.99,
            cash=999_999_999_999.99,
        )

        assert company.base_quality == 1.0
        assert company.reputation == 100.0

