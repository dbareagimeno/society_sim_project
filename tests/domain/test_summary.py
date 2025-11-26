"""
Tests unitarios para los modelos de resumen (DaySummary, PartySummary, CompanySummary).

Verifica:
- Creación de resúmenes válidos
- Validación de campos
- Serialización/deserialización a JSON
- Inmutabilidad de los modelos
"""

import json

import pytest
from pydantic import ValidationError

from society_sim.domain import CompanySummary, DaySummary, PartySummary


class TestPartySummaryCreation:
    """Tests de creación de PartySummary."""

    def test_create_party_summary(self) -> None:
        """Debe crear un resumen de partido con todos los campos."""
        summary = PartySummary(
            party_id="prog-001",
            name="Partido Progresista",
            popularity=45.0,
            reputation=60.0,
        )

        assert summary.party_id == "prog-001"
        assert summary.name == "Partido Progresista"
        assert summary.popularity == 45.0
        assert summary.reputation == 60.0

    def test_party_summary_is_frozen(self) -> None:
        """PartySummary debe ser inmutable."""
        summary = PartySummary(
            party_id="prog-001",
            name="Partido Progresista",
            popularity=45.0,
            reputation=60.0,
        )

        with pytest.raises(ValidationError):
            summary.popularity = 50.0


class TestCompanySummaryCreation:
    """Tests de creación de CompanySummary."""

    def test_create_company_summary(self) -> None:
        """Debe crear un resumen de empresa con todos los campos."""
        summary = CompanySummary(
            company_id="tech-001",
            name="TechCorp",
            stock_price=120.0,
            reputation=75.0,
            revenue=50000.0,
        )

        assert summary.company_id == "tech-001"
        assert summary.name == "TechCorp"
        assert summary.stock_price == 120.0
        assert summary.reputation == 75.0
        assert summary.revenue == 50000.0

    def test_company_summary_is_frozen(self) -> None:
        """CompanySummary debe ser inmutable."""
        summary = CompanySummary(
            company_id="tech-001",
            name="TechCorp",
            stock_price=120.0,
            reputation=75.0,
            revenue=50000.0,
        )

        with pytest.raises(ValidationError):
            summary.stock_price = 150.0


class TestDaySummaryCreation:
    """Tests de creación de DaySummary."""

    def test_create_day_summary_with_required_fields(self) -> None:
        """Debe crear un resumen de día con campos requeridos."""
        summary = DaySummary(
            day=1,
            total_revenue=500000.0,
            average_stock_price=110.0,
            average_satisfaction=55.0,
        )

        assert summary.day == 1
        assert summary.total_revenue == 500000.0
        assert summary.average_stock_price == 110.0
        assert summary.average_satisfaction == 55.0

    def test_create_day_summary_has_default_values(self) -> None:
        """Debe asignar valores por defecto a campos opcionales."""
        summary = DaySummary(
            day=1,
            total_revenue=500000.0,
            average_stock_price=110.0,
            average_satisfaction=55.0,
        )

        assert summary.parties == []
        assert summary.top_companies == []
        assert summary.events_count == 0
        assert summary.active_policies_count == 0

    def test_create_day_summary_with_all_fields(self) -> None:
        """Debe crear un resumen completo con todos los campos."""
        party_summary = PartySummary(
            party_id="prog-001",
            name="Partido Progresista",
            popularity=45.0,
            reputation=60.0,
        )
        company_summary = CompanySummary(
            company_id="tech-001",
            name="TechCorp",
            stock_price=120.0,
            reputation=75.0,
            revenue=50000.0,
        )

        summary = DaySummary(
            day=10,
            total_revenue=1_000_000.0,
            average_stock_price=150.0,
            average_satisfaction=65.0,
            parties=[party_summary],
            top_companies=[company_summary],
            events_count=5,
            active_policies_count=3,
        )

        assert summary.day == 10
        assert len(summary.parties) == 1
        assert summary.parties[0].party_id == "prog-001"
        assert len(summary.top_companies) == 1
        assert summary.top_companies[0].company_id == "tech-001"
        assert summary.events_count == 5
        assert summary.active_policies_count == 3

    def test_create_day_summary_with_multiple_parties_and_companies(self) -> None:
        """Debe poder incluir múltiples partidos y empresas."""
        parties = [
            PartySummary(
                party_id=f"party-{i}",
                name=f"Partido {i}",
                popularity=20.0 + i * 10,
                reputation=50.0,
            )
            for i in range(3)
        ]
        companies = [
            CompanySummary(
                company_id=f"company-{i}",
                name=f"Empresa {i}",
                stock_price=100.0 + i * 20,
                reputation=60.0,
                revenue=10000.0 * (i + 1),
            )
            for i in range(5)
        ]

        summary = DaySummary(
            day=5,
            total_revenue=150000.0,
            average_stock_price=180.0,
            average_satisfaction=70.0,
            parties=parties,
            top_companies=companies,
        )

        assert len(summary.parties) == 3
        assert len(summary.top_companies) == 5

    def test_day_summary_is_frozen(self) -> None:
        """DaySummary debe ser inmutable."""
        summary = DaySummary(
            day=1,
            total_revenue=500000.0,
            average_stock_price=110.0,
            average_satisfaction=55.0,
        )

        with pytest.raises(ValidationError):
            summary.day = 2


class TestDaySummaryValidation:
    """Tests de validación de campos."""

    def test_day_cannot_be_negative(self) -> None:
        """Debe rechazar día negativo."""
        with pytest.raises(ValidationError) as exc_info:
            DaySummary(
                day=-1,
                total_revenue=500000.0,
                average_stock_price=110.0,
                average_satisfaction=55.0,
            )
        assert "day" in str(exc_info.value)

    def test_total_revenue_cannot_be_negative(self) -> None:
        """Debe rechazar ingresos totales negativos."""
        with pytest.raises(ValidationError) as exc_info:
            DaySummary(
                day=1,
                total_revenue=-1000.0,
                average_stock_price=110.0,
                average_satisfaction=55.0,
            )
        assert "total_revenue" in str(exc_info.value)

    def test_average_stock_price_cannot_be_negative(self) -> None:
        """Debe rechazar precio medio de acciones negativo."""
        with pytest.raises(ValidationError) as exc_info:
            DaySummary(
                day=1,
                total_revenue=500000.0,
                average_stock_price=-10.0,
                average_satisfaction=55.0,
            )
        assert "average_stock_price" in str(exc_info.value)

    def test_average_satisfaction_cannot_be_negative(self) -> None:
        """Debe rechazar satisfacción media negativa."""
        with pytest.raises(ValidationError) as exc_info:
            DaySummary(
                day=1,
                total_revenue=500000.0,
                average_stock_price=110.0,
                average_satisfaction=-5.0,
            )
        assert "average_satisfaction" in str(exc_info.value)

    def test_average_satisfaction_cannot_exceed_hundred(self) -> None:
        """Debe rechazar satisfacción media mayor a 100."""
        with pytest.raises(ValidationError) as exc_info:
            DaySummary(
                day=1,
                total_revenue=500000.0,
                average_stock_price=110.0,
                average_satisfaction=105.0,
            )
        assert "average_satisfaction" in str(exc_info.value)

    def test_events_count_cannot_be_negative(self) -> None:
        """Debe rechazar conteo de eventos negativo."""
        with pytest.raises(ValidationError) as exc_info:
            DaySummary(
                day=1,
                total_revenue=500000.0,
                average_stock_price=110.0,
                average_satisfaction=55.0,
                events_count=-1,
            )
        assert "events_count" in str(exc_info.value)

    def test_active_policies_count_cannot_be_negative(self) -> None:
        """Debe rechazar conteo de políticas activas negativo."""
        with pytest.raises(ValidationError) as exc_info:
            DaySummary(
                day=1,
                total_revenue=500000.0,
                average_stock_price=110.0,
                average_satisfaction=55.0,
                active_policies_count=-1,
            )
        assert "active_policies_count" in str(exc_info.value)


class TestSummarySerialization:
    """Tests de serialización y deserialización JSON."""

    def test_serialize_party_summary_to_json(self) -> None:
        """Debe poder serializar PartySummary a JSON."""
        summary = PartySummary(
            party_id="prog-001",
            name="Partido Progresista",
            popularity=45.0,
            reputation=60.0,
        )

        json_str = summary.model_dump_json()
        data = json.loads(json_str)

        assert data["party_id"] == "prog-001"
        assert data["name"] == "Partido Progresista"
        assert data["popularity"] == 45.0
        assert data["reputation"] == 60.0

    def test_serialize_company_summary_to_json(self) -> None:
        """Debe poder serializar CompanySummary a JSON."""
        summary = CompanySummary(
            company_id="tech-001",
            name="TechCorp",
            stock_price=120.0,
            reputation=75.0,
            revenue=50000.0,
        )

        json_str = summary.model_dump_json()
        data = json.loads(json_str)

        assert data["company_id"] == "tech-001"
        assert data["name"] == "TechCorp"
        assert data["stock_price"] == 120.0
        assert data["reputation"] == 75.0
        assert data["revenue"] == 50000.0

    def test_serialize_day_summary_to_json(self) -> None:
        """Debe poder serializar DaySummary completo a JSON."""
        party_summary = PartySummary(
            party_id="prog-001",
            name="Partido Progresista",
            popularity=45.0,
            reputation=60.0,
        )
        company_summary = CompanySummary(
            company_id="tech-001",
            name="TechCorp",
            stock_price=120.0,
            reputation=75.0,
            revenue=50000.0,
        )

        summary = DaySummary(
            day=10,
            total_revenue=1_000_000.0,
            average_stock_price=150.0,
            average_satisfaction=65.0,
            parties=[party_summary],
            top_companies=[company_summary],
            events_count=5,
            active_policies_count=3,
        )

        json_str = summary.model_dump_json()
        data = json.loads(json_str)

        assert data["day"] == 10
        assert data["total_revenue"] == 1_000_000.0
        assert data["average_stock_price"] == 150.0
        assert data["average_satisfaction"] == 65.0
        assert len(data["parties"]) == 1
        assert data["parties"][0]["party_id"] == "prog-001"
        assert len(data["top_companies"]) == 1
        assert data["top_companies"][0]["company_id"] == "tech-001"
        assert data["events_count"] == 5
        assert data["active_policies_count"] == 3

    def test_deserialize_day_summary_from_json(self) -> None:
        """Debe poder deserializar DaySummary desde JSON."""
        json_data = {
            "day": 15,
            "total_revenue": 750000.0,
            "average_stock_price": 200.0,
            "average_satisfaction": 70.0,
            "parties": [
                {
                    "party_id": "cons-001",
                    "name": "Partido Conservador",
                    "popularity": 30.0,
                    "reputation": 55.0,
                }
            ],
            "top_companies": [
                {
                    "company_id": "food-001",
                    "name": "FoodMart",
                    "stock_price": 180.0,
                    "reputation": 80.0,
                    "revenue": 75000.0,
                }
            ],
            "events_count": 3,
            "active_policies_count": 2,
        }

        summary = DaySummary.model_validate(json_data)

        assert summary.day == 15
        assert summary.total_revenue == 750000.0
        assert len(summary.parties) == 1
        assert summary.parties[0].party_id == "cons-001"
        assert len(summary.top_companies) == 1
        assert summary.top_companies[0].company_id == "food-001"

    def test_roundtrip_serialization(self) -> None:
        """Debe mantener los datos tras serializar y deserializar."""
        original = DaySummary(
            day=20,
            total_revenue=2_000_000.0,
            average_stock_price=250.0,
            average_satisfaction=80.0,
            parties=[
                PartySummary(
                    party_id="party-1",
                    name="Partido 1",
                    popularity=40.0,
                    reputation=65.0,
                ),
                PartySummary(
                    party_id="party-2",
                    name="Partido 2",
                    popularity=35.0,
                    reputation=55.0,
                ),
            ],
            top_companies=[
                CompanySummary(
                    company_id="company-1",
                    name="Empresa 1",
                    stock_price=300.0,
                    reputation=90.0,
                    revenue=100000.0,
                )
            ],
            events_count=8,
            active_policies_count=4,
        )

        # Serializar y deserializar
        json_str = original.model_dump_json()
        restored = DaySummary.model_validate_json(json_str)

        assert restored.day == original.day
        assert restored.total_revenue == original.total_revenue
        assert restored.average_stock_price == original.average_stock_price
        assert restored.average_satisfaction == original.average_satisfaction
        assert len(restored.parties) == len(original.parties)
        assert len(restored.top_companies) == len(original.top_companies)
        assert restored.events_count == original.events_count
        assert restored.active_policies_count == original.active_policies_count


class TestSummaryEdgeCases:
    """Tests de casos límite."""

    def test_day_zero_is_valid(self) -> None:
        """Debe aceptar día 0 como válido (inicio de simulación)."""
        summary = DaySummary(
            day=0,
            total_revenue=0.0,
            average_stock_price=100.0,
            average_satisfaction=50.0,
        )

        assert summary.day == 0

    def test_boundary_satisfaction_values(self) -> None:
        """Debe aceptar valores límite de satisfacción."""
        # Satisfacción mínima
        summary_min = DaySummary(
            day=1,
            total_revenue=100.0,
            average_stock_price=100.0,
            average_satisfaction=0.0,
        )
        assert summary_min.average_satisfaction == 0.0

        # Satisfacción máxima
        summary_max = DaySummary(
            day=1,
            total_revenue=100.0,
            average_stock_price=100.0,
            average_satisfaction=100.0,
        )
        assert summary_max.average_satisfaction == 100.0

    def test_empty_lists_are_valid(self) -> None:
        """Debe aceptar listas vacías de partidos y empresas."""
        summary = DaySummary(
            day=1,
            total_revenue=500000.0,
            average_stock_price=110.0,
            average_satisfaction=55.0,
            parties=[],
            top_companies=[],
        )

        assert summary.parties == []
        assert summary.top_companies == []

    def test_zero_counts_are_valid(self) -> None:
        """Debe aceptar conteos en cero."""
        summary = DaySummary(
            day=1,
            total_revenue=500000.0,
            average_stock_price=110.0,
            average_satisfaction=55.0,
            events_count=0,
            active_policies_count=0,
        )

        assert summary.events_count == 0
        assert summary.active_policies_count == 0

