import base64

from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from tests.fixtures import base_settings, get_all_berries_mock

client = TestClient(app)


def test_growth_time_graphs_success(mocker, get_all_berries_mock, base_settings):
    """Test that the /growthTimeGraphs endpoint returns a valid HTML response with a histogram."""

    mock_frequencies = {"3": 1, "4": 1}
    get_frequencies_mock = mocker.MagicMock(return_value=mock_frequencies)
    mocker.patch("app.routers.berries.get_frequencies", get_frequencies_mock)

    mock_image_data = b"mocked_image_data"
    image_data_b64 = base64.b64encode(mock_image_data).decode("utf-8")
    get_histogram_mock = mocker.MagicMock(return_value=mock_image_data)
    mocker.patch("app.routers.berries.plots.get_histogram", get_histogram_mock)

    response = client.get("/growthTimeGraphs")

    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers["content-type"]
    assert response.template.name == "growth_time_graphs.html"
    assert response.context["histogram_data"] == image_data_b64
    get_frequencies_mock.assert_called_once_with([3, 4])
    get_histogram_mock.assert_called_once_with(
        mock_frequencies,
        xlabel="Growth Time [hours]",
        ylabel="Frequency",
    )
