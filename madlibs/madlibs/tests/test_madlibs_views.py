import pytest
from unittest.mock import patch, Mock
import aiohttp

from aioresponses import aioresponses

from madlibs.views import WordGenerator, MadlibView


@pytest.mark.asyncio
class TestWordGenerator:
    async def test_retrieve_word(self):
        wg = WordGenerator()
        with aioresponses() as mocked:
            mocked.get(
                "https://reminiscent-steady-albertosaurus.glitch.me/verb",
                status=200,
                body="verb",
            )
            async with aiohttp.ClientSession() as session:
                result = await wg.retrieve_word(session, "verb")

            assert result == "verb"

    async def test_retrieve_word_api_error(self):
        wg = WordGenerator()
        with aioresponses() as mocked:
            mocked.get(
                "https://reminiscent-steady-albertosaurus.glitch.me/verb",
                status=500,
                body="verb",
            )
            async with aiohttp.ClientSession() as session:
                with pytest.raises(Exception):
                    await wg.retrieve_word(session, "verb")

    @patch("madlibs.views.WordGenerator.retrieve_word")
    async def test_generate_words(self, mock_retrieve):
        mock_retrieve.side_effect = ["verb", "adjective", "noun"]
        wg = WordGenerator()

        rest = await wg.generate_words()

        assert rest == {"adjective": "adjective", "noun": "noun", "verb": "verb"}


@pytest.mark.asyncio
class TestMadlibView:
    @patch("madlibs.views.MadlibView.get_context_data")
    async def test_get(self, mock_context_data):
        mock_context_data.return_value = {
            "verb": "vb",
            "adjective": "adj",
            "noun": "noun",
        }
        mv = MadlibView()

        response = await mv.get(None)

        assert (
            response.content
            == b'It was a adj day. I went downstairs to see if I could vb dinner. I asked, "Does the stew need fresh noun?"'
        )

    @patch("madlibs.views.WordGenerator.generate_words")
    async def test_get_context_data(self, mock_generate):
        mock_generate.return_value = {
            "verb": "verb",
            "adjective": "adj",
            "noun": "noun",
        }
        mv = MadlibView()
        data = await mv.get_context_data()
        assert data == {"verb": "verb", "adjective": "adj", "noun": "noun", "view": mv}
