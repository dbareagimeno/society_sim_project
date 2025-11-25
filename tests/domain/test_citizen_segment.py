"""
Tests unitarios para el modelo CitizenSegment.

Verifica:
- Creación de segmentos ciudadanos válidos
- Validación de campos fuera de rango
- Propiedad computada total_wealth
- Serialización/deserialización a JSON
"""

import json

import pytest
from pydantic import ValidationError

from society_sim.domain import CitizenSegment, IdeologicalBias


class TestCitizenSegmentCreation:
    """Tests de creación de segmentos ciudadanos válidos."""

    def test_create_segment_with_required_fields(self) -> None:
        """Debe crear un segmento con solo los campos requeridos."""
        segment = CitizenSegment(
            id="middle-class",
            name="Clase Media",
            size=1_000_000,
            wealth_per_capita=50_000.0,
            ideological_bias=IdeologicalBias.CENTER,
        )

        assert segment.id == "middle-class"
        assert segment.name == "Clase Media"
        assert segment.size == 1_000_000
        assert segment.wealth_per_capita == 50_000.0
        assert segment.ideological_bias == IdeologicalBias.CENTER

    def test_create_segment_has_default_values(self) -> None:
        """Debe asignar valores por defecto a campos opcionales."""
        segment = CitizenSegment(
            id="upper-class",
            name="Clase Alta",
            size=100_000,
            wealth_per_capita=500_000.0,
            ideological_bias=IdeologicalBias.CENTER_RIGHT,
        )

        assert segment.satisfaction == 50.0
        assert segment.preferred_party_id is None
        assert segment.consumption_rate == 0.1

    def test_create_segment_with_custom_values(self) -> None:
        """Debe permitir valores personalizados para campos opcionales."""
        segment = CitizenSegment(
            id="working-class",
            name="Clase Trabajadora",
            size=2_000_000,
            wealth_per_capita=25_000.0,
            ideological_bias=IdeologicalBias.LEFT,
            satisfaction=45.0,
            preferred_party_id="prog-001",
            consumption_rate=0.15,
        )

        assert segment.satisfaction == 45.0
        assert segment.preferred_party_id == "prog-001"
        assert segment.consumption_rate == 0.15

    def test_create_segment_with_all_ideologies(self) -> None:
        """Debe poder crear segmentos con cualquier ideología."""
        for ideology in IdeologicalBias:
            segment = CitizenSegment(
                id=f"segment-{ideology.value}",
                name=f"Segment {ideology.value}",
                size=100_000,
                wealth_per_capita=30_000.0,
                ideological_bias=ideology,
            )
            assert segment.ideological_bias == ideology


class TestCitizenSegmentTotalWealth:
    """Tests de la propiedad computada total_wealth."""

    def test_total_wealth_calculation(self) -> None:
        """Debe calcular correctamente la riqueza total."""
        segment = CitizenSegment(
            id="test-segment",
            name="Test Segment",
            size=1_000,
            wealth_per_capita=100_000.0,
            ideological_bias=IdeologicalBias.CENTER,
        )

        assert segment.total_wealth == 100_000_000.0  # 1000 * 100000

    def test_total_wealth_with_large_values(self) -> None:
        """Debe manejar correctamente valores grandes."""
        segment = CitizenSegment(
            id="large-segment",
            name="Large Segment",
            size=10_000_000,
            wealth_per_capita=75_000.0,
            ideological_bias=IdeologicalBias.CENTER,
        )

        expected = 10_000_000 * 75_000.0
        assert segment.total_wealth == expected

    def test_total_wealth_updates_with_changes(self) -> None:
        """total_wealth debe actualizarse cuando cambian size o wealth_per_capita."""
        segment = CitizenSegment(
            id="dynamic-segment",
            name="Dynamic Segment",
            size=1_000,
            wealth_per_capita=50_000.0,
            ideological_bias=IdeologicalBias.CENTER,
        )

        assert segment.total_wealth == 50_000_000.0

        # Cambiar wealth_per_capita
        segment.wealth_per_capita = 100_000.0
        assert segment.total_wealth == 100_000_000.0


class TestCitizenSegmentValidation:
    """Tests de validación de campos fuera de rango."""

    def test_satisfaction_clamped_to_zero(self) -> None:
        """La satisfacción negativa debe ajustarse a 0."""
        segment = CitizenSegment(
            id="test-001",
            name="TestSegment",
            size=1000,
            wealth_per_capita=50_000.0,
            ideological_bias=IdeologicalBias.CENTER,
            satisfaction=-10.0,
        )
        assert segment.satisfaction == 0.0

    def test_satisfaction_clamped_to_hundred(self) -> None:
        """La satisfacción mayor a 100 debe ajustarse a 100."""
        segment = CitizenSegment(
            id="test-001",
            name="TestSegment",
            size=1000,
            wealth_per_capita=50_000.0,
            ideological_bias=IdeologicalBias.CENTER,
            satisfaction=150.0,
        )
        assert segment.satisfaction == 100.0

    def test_size_zero_raises_error(self) -> None:
        """Debe lanzar ValidationError si size = 0."""
        with pytest.raises(ValidationError) as exc_info:
            CitizenSegment(
                id="test-001",
                name="TestSegment",
                size=0,
                wealth_per_capita=50_000.0,
                ideological_bias=IdeologicalBias.CENTER,
            )
        assert "size" in str(exc_info.value)

    def test_size_negative_raises_error(self) -> None:
        """Debe lanzar ValidationError si size < 0."""
        with pytest.raises(ValidationError) as exc_info:
            CitizenSegment(
                id="test-001",
                name="TestSegment",
                size=-1000,
                wealth_per_capita=50_000.0,
                ideological_bias=IdeologicalBias.CENTER,
            )
        assert "size" in str(exc_info.value)

    def test_wealth_per_capita_negative_raises_error(self) -> None:
        """Debe lanzar ValidationError si wealth_per_capita < 0."""
        with pytest.raises(ValidationError) as exc_info:
            CitizenSegment(
                id="test-001",
                name="TestSegment",
                size=1000,
                wealth_per_capita=-50_000.0,
                ideological_bias=IdeologicalBias.CENTER,
            )
        assert "wealth_per_capita" in str(exc_info.value)

    def test_consumption_rate_negative_raises_error(self) -> None:
        """Debe lanzar ValidationError si consumption_rate < 0."""
        with pytest.raises(ValidationError) as exc_info:
            CitizenSegment(
                id="test-001",
                name="TestSegment",
                size=1000,
                wealth_per_capita=50_000.0,
                ideological_bias=IdeologicalBias.CENTER,
                consumption_rate=-0.1,
            )
        assert "consumption_rate" in str(exc_info.value)

    def test_consumption_rate_above_one_raises_error(self) -> None:
        """Debe lanzar ValidationError si consumption_rate > 1."""
        with pytest.raises(ValidationError) as exc_info:
            CitizenSegment(
                id="test-001",
                name="TestSegment",
                size=1000,
                wealth_per_capita=50_000.0,
                ideological_bias=IdeologicalBias.CENTER,
                consumption_rate=1.5,
            )
        assert "consumption_rate" in str(exc_info.value)

    def test_validate_on_assignment(self) -> None:
        """Debe validar (clamping) al modificar campos existentes."""
        segment = CitizenSegment(
            id="test-001",
            name="TestSegment",
            size=1000,
            wealth_per_capita=50_000.0,
            ideological_bias=IdeologicalBias.CENTER,
        )

        # Modificar satisfacción fuera de rango - debe clampear
        segment.satisfaction = -50.0
        assert segment.satisfaction == 0.0

        segment.satisfaction = 200.0
        assert segment.satisfaction == 100.0

        # Modificar consumption_rate fuera de rango - debe lanzar error
        with pytest.raises(ValidationError):
            segment.consumption_rate = -0.5

        with pytest.raises(ValidationError):
            segment.consumption_rate = 2.0


class TestCitizenSegmentSerialization:
    """Tests de serialización y deserialización JSON."""

    def test_serialize_to_json(self) -> None:
        """Debe poder serializar un segmento a JSON."""
        segment = CitizenSegment(
            id="middle-class",
            name="Clase Media",
            size=1_000_000,
            wealth_per_capita=50_000.0,
            ideological_bias=IdeologicalBias.CENTER,
            satisfaction=55.0,
            preferred_party_id="centro-001",
            consumption_rate=0.12,
        )

        json_str = segment.model_dump_json()
        data = json.loads(json_str)

        assert data["id"] == "middle-class"
        assert data["name"] == "Clase Media"
        assert data["size"] == 1_000_000
        assert data["wealth_per_capita"] == 50_000.0
        assert data["ideological_bias"] == "center"
        assert data["satisfaction"] == 55.0
        assert data["preferred_party_id"] == "centro-001"
        assert data["consumption_rate"] == 0.12
        assert data["total_wealth"] == 50_000_000_000.0

    def test_deserialize_from_json(self) -> None:
        """Debe poder deserializar un segmento desde JSON."""
        json_data = {
            "id": "upper-class",
            "name": "Clase Alta",
            "size": 100_000,
            "wealth_per_capita": 500_000.0,
            "ideological_bias": "center_right",
            "satisfaction": 70.0,
            "preferred_party_id": "cons-001",
            "consumption_rate": 0.08,
        }

        segment = CitizenSegment.model_validate(json_data)

        assert segment.id == "upper-class"
        assert segment.name == "Clase Alta"
        assert segment.size == 100_000
        assert segment.wealth_per_capita == 500_000.0
        assert segment.ideological_bias == IdeologicalBias.CENTER_RIGHT
        assert segment.satisfaction == 70.0
        assert segment.preferred_party_id == "cons-001"
        assert segment.consumption_rate == 0.08
        assert segment.total_wealth == 50_000_000_000.0

    def test_roundtrip_serialization(self) -> None:
        """Debe mantener los datos tras serializar y deserializar."""
        original = CitizenSegment(
            id="working-class",
            name="Clase Trabajadora",
            size=2_000_000,
            wealth_per_capita=25_000.0,
            ideological_bias=IdeologicalBias.LEFT,
            satisfaction=40.0,
            preferred_party_id="prog-001",
            consumption_rate=0.2,
        )

        # Serializar y deserializar
        json_str = original.model_dump_json()
        restored = CitizenSegment.model_validate_json(json_str)

        assert restored.id == original.id
        assert restored.name == original.name
        assert restored.size == original.size
        assert restored.wealth_per_capita == original.wealth_per_capita
        assert restored.ideological_bias == original.ideological_bias
        assert restored.satisfaction == original.satisfaction
        assert restored.preferred_party_id == original.preferred_party_id
        assert restored.consumption_rate == original.consumption_rate
        assert restored.total_wealth == original.total_wealth


class TestCitizenSegmentEdgeCases:
    """Tests de casos límite."""

    def test_boundary_values_accepted(self) -> None:
        """Debe aceptar valores en los límites exactos."""
        segment = CitizenSegment(
            id="edge-001",
            name="EdgeCase Segment",
            size=1,
            wealth_per_capita=0.0,
            ideological_bias=IdeologicalBias.CENTER,
            satisfaction=0.0,
            consumption_rate=0.0,
        )

        assert segment.size == 1
        assert segment.wealth_per_capita == 0.0
        assert segment.satisfaction == 0.0
        assert segment.consumption_rate == 0.0
        assert segment.total_wealth == 0.0

    def test_maximum_values_accepted(self) -> None:
        """Debe aceptar valores máximos válidos."""
        segment = CitizenSegment(
            id="max-001",
            name="MaxValues Segment",
            size=100_000_000,
            wealth_per_capita=10_000_000.0,
            ideological_bias=IdeologicalBias.CENTER,
            satisfaction=100.0,
            consumption_rate=1.0,
        )

        assert segment.satisfaction == 100.0
        assert segment.consumption_rate == 1.0

    def test_preferred_party_id_can_be_none(self) -> None:
        """Debe permitir preferred_party_id como None."""
        segment = CitizenSegment(
            id="no-preference",
            name="Sin Preferencia",
            size=500_000,
            wealth_per_capita=40_000.0,
            ideological_bias=IdeologicalBias.CENTER,
            preferred_party_id=None,
        )

        assert segment.preferred_party_id is None

    def test_preferred_party_id_can_be_set(self) -> None:
        """Debe permitir cambiar preferred_party_id."""
        segment = CitizenSegment(
            id="changeable",
            name="Changeable Segment",
            size=500_000,
            wealth_per_capita=40_000.0,
            ideological_bias=IdeologicalBias.CENTER,
            preferred_party_id=None,
        )

        assert segment.preferred_party_id is None

        segment.preferred_party_id = "new-party-001"
        assert segment.preferred_party_id == "new-party-001"

        segment.preferred_party_id = None
        assert segment.preferred_party_id is None

