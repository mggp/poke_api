from httpx import HTTPStatusError
import pytest
from app.services.pokebase_client import BerryClient
from app.services.schemas import Berry
from tests.services.choices.mock_data import cheri_detail, pecha_detail


@pytest.mark.asyncio
async def test_berry_client_gets_all_details_from_api(mocker):
    mock_client = mocker.AsyncMock()
    mock_client.get.side_effect = [
        mocker.Mock(
            json=lambda: mocker.Mock(
                results=[
                    {"name": "cheri", "url": "url1"},
                    {"name": "pecha", "url": "url2"},
                ],
                next=None,
            )
        ),
        mocker.Mock(json=lambda: cheri_detail),
        mocker.Mock(json=lambda: pecha_detail),
    ]

    mocker.patch("httpx.AsyncClient", return_value=mock_client)

    client = BerryClient(base_url="fake_url")
    berries = await client.get_all_details()

    assert mock_client.get.call_count == 3

    mock_client.get.assert_any_call("fake_url/v2/berry")
    mock_client.get.assert_any_call("url1")
    mock_client.get.assert_any_call("url2")

    assert isinstance(berries, list)
    assert len(berries) == 2
    assert all(isinstance(berry, Berry) for berry in berries)
    assert berries[0].name == "cheri"
    assert berries[0].growth_time == 10
    assert berries[1].name == "pecha"
    assert berries[1].growth_time == 5


@pytest.mark.asyncio
async def test_berry_client_raises_error_on_invalid_url(mocker):
    mock_client = mocker.AsyncMock()
    mock_client.get.side_effect = HTTPStatusError(
        "Not Found", request=mocker.Mock(), response=mocker.Mock(status_code=404)
    )

    mocker.patch("httpx.AsyncClient", return_value=mock_client)

    client = BerryClient(base_url="fake_url")

    with pytest.raises(HTTPStatusError):
        await client.get_all_details()

    mock_client.get.assert_called_once_with("fake_url/v2/berry")
    assert mock_client.get.call_count == 1
    assert mock_client.get.call_args[0][0] == "fake_url/v2/berry"
