"""
Tests unitarios para el modelo Party.

Verifica:
- Creación de partidos válidos
- Validación de campos fuera de rango (clamping)
- Serialización/deserialización a JSON
"""

import json

from society_sim.domain import IdeologicalBias, Party


class TestPartyCreation:
    """Tests de creación de partidos válidos."""

    def test_create_party_with_required_fields(self) -> None:
        """Debe crear un partido con solo los campos requeridos."""
        party = Party(
            id="prog-001",
            name="Partido Progresista",
            ideology=IdeologicalBias.CENTER_LEFT,
        )

        assert party.id == "prog-001"
        assert party.name == "Partido Progresista"
        assert party.ideology == IdeologicalBias.CENTER_LEFT

    def test_create_party_has_default_values(self) -> None:
        """Debe asignar valores por defecto a campos dinámicos."""
        party = Party(
            id="cons-001",
            name="Partido Conservador",
            ideology=IdeologicalBias.RIGHT,
        )

        assert party.popularity == 20.0
        assert party.reputation == 50.0
        assert party.in_government is False

    def test_create_party_with_custom_values(self) -> None:
        """Debe permitir valores personalizados para campos dinámicos."""
        party = Party(
            id="centro-001",
            name="Partido Centrista",
            ideology=IdeologicalBias.CENTER,
            popularity=45.0,
            reputation=70.0,
            in_government=True,
        )

        assert party.popularity == 45.0
        assert party.reputation == 70.0
        assert party.in_government is True

    def test_create_party_with_all_ideologies(self) -> None:
        """Debe poder crear partidos con cualquier ideología."""
        for ideology in IdeologicalBias:
            party = Party(
                id=f"{ideology.value}-001",
                name=f"Partido {ideology.value}",
                ideology=ideology,
            )
            assert party.ideology == ideology


class TestPartyValidation:
    """Tests de validación de campos fuera de rango."""

    def test_popularity_clamped_to_zero(self) -> None:
        """La popularidad negativa debe ajustarse a 0."""
        party = Party(
            id="test-001",
            name="TestParty",
            ideology=IdeologicalBias.CENTER,
            popularity=-10.0,
        )
        assert party.popularity == 0.0

    def test_popularity_clamped_to_hundred(self) -> None:
        """La popularidad mayor a 100 debe ajustarse a 100."""
        party = Party(
            id="test-001",
            name="TestParty",
            ideology=IdeologicalBias.CENTER,
            popularity=150.0,
        )
        assert party.popularity == 100.0

    def test_reputation_clamped_to_zero(self) -> None:
        """La reputación negativa debe ajustarse a 0."""
        party = Party(
            id="test-001",
            name="TestParty",
            ideology=IdeologicalBias.CENTER,
            reputation=-25.0,
        )
        assert party.reputation == 0.0

    def test_reputation_clamped_to_hundred(self) -> None:
        """La reputación mayor a 100 debe ajustarse a 100."""
        party = Party(
            id="test-001",
            name="TestParty",
            ideology=IdeologicalBias.CENTER,
            reputation=200.0,
        )
        assert party.reputation == 100.0

    def test_validate_on_assignment(self) -> None:
        """Debe validar (clamping) al modificar campos existentes."""
        party = Party(
            id="test-001",
            name="TestParty",
            ideology=IdeologicalBias.CENTER,
        )

        # Modificar popularidad fuera de rango - debe clampear
        party.popularity = -50.0
        assert party.popularity == 0.0

        party.popularity = 200.0
        assert party.popularity == 100.0

        # Modificar reputación fuera de rango - debe clampear
        party.reputation = -100.0
        assert party.reputation == 0.0

        party.reputation = 300.0
        assert party.reputation == 100.0


class TestPartySerialization:
    """Tests de serialización y deserialización JSON."""

    def test_serialize_to_json(self) -> None:
        """Debe poder serializar un partido a JSON."""
        party = Party(
            id="prog-001",
            name="Partido Progresista",
            ideology=IdeologicalBias.LEFT,
            popularity=35.0,
            reputation=60.0,
            in_government=True,
        )

        json_str = party.model_dump_json()
        data = json.loads(json_str)

        assert data["id"] == "prog-001"
        assert data["name"] == "Partido Progresista"
        assert data["ideology"] == "left"
        assert data["popularity"] == 35.0
        assert data["reputation"] == 60.0
        assert data["in_government"] is True

    def test_deserialize_from_json(self) -> None:
        """Debe poder deserializar un partido desde JSON."""
        json_data = {
            "id": "cons-001",
            "name": "Partido Conservador",
            "ideology": "right",
            "popularity": 40.0,
            "reputation": 55.0,
            "in_government": False,
        }

        party = Party.model_validate(json_data)

        assert party.id == "cons-001"
        assert party.name == "Partido Conservador"
        assert party.ideology == IdeologicalBias.RIGHT
        assert party.popularity == 40.0
        assert party.reputation == 55.0
        assert party.in_government is False

    def test_roundtrip_serialization(self) -> None:
        """Debe mantener los datos tras serializar y deserializar."""
        original = Party(
            id="centro-001",
            name="Partido Centrista",
            ideology=IdeologicalBias.CENTER,
            popularity=50.0,
            reputation=75.0,
            in_government=True,
        )

        # Serializar y deserializar
        json_str = original.model_dump_json()
        restored = Party.model_validate_json(json_str)

        assert restored.id == original.id
        assert restored.name == original.name
        assert restored.ideology == original.ideology
        assert restored.popularity == original.popularity
        assert restored.reputation == original.reputation
        assert restored.in_government == original.in_government


class TestPartyEdgeCases:
    """Tests de casos límite."""

    def test_boundary_values_accepted(self) -> None:
        """Debe aceptar valores en los límites exactos."""
        party = Party(
            id="edge-001",
            name="EdgeCase Party",
            ideology=IdeologicalBias.CENTER_RIGHT,
            popularity=0.0,
            reputation=0.0,
            in_government=False,
        )

        assert party.popularity == 0.0
        assert party.reputation == 0.0

    def test_maximum_values_accepted(self) -> None:
        """Debe aceptar valores máximos válidos."""
        party = Party(
            id="max-001",
            name="MaxPopularity Party",
            ideology=IdeologicalBias.CENTER_LEFT,
            popularity=100.0,
            reputation=100.0,
            in_government=True,
        )

        assert party.popularity == 100.0
        assert party.reputation == 100.0

    def test_government_toggle(self) -> None:
        """Debe poder cambiar el estado de gobierno."""
        party = Party(
            id="toggle-001",
            name="Toggle Party",
            ideology=IdeologicalBias.CENTER,
            in_government=False,
        )

        assert party.in_government is False

        party.in_government = True
        assert party.in_government is True

        party.in_government = False
        assert party.in_government is False

