import pytest

from reusables.main import save_base64_image


class TestSaveBase64Image:
    @pytest.mark.asyncio
    async def test_rejects_non_data_uri_strings(self):
        result = await save_base64_image("not-an-image")

        assert result is None

    @pytest.mark.asyncio
    async def test_rejects_malformed_base64_payload(self):
        result = await save_base64_image("data:image/png;base64,not-valid!!!")

        assert result is None
