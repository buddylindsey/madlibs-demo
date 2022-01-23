import asyncio
import logging

import aiohttp
from django.http import HttpResponse
from django.utils.decorators import classonlymethod
from django.views.generic import View
from django.views.generic.base import ContextMixin

logger = logging.getLogger(__name__)


class WordGenerator:
    async def retrieve_word(self, session, part):
        url = f"https://reminiscent-steady-albertosaurus.glitch.me/{part}"
        async with session.get(url) as res:
            if res.ok:
                data = await res.text()
                return data

            logger.info("Word API did not return 200. It maybe down.")
            raise Exception("Did not get a good response from word server")

    async def generate_words(self):
        """
        Return a verb, adjective, and noun for use in a madlib.
        """
        async with aiohttp.ClientSession() as session:
            verb_task = asyncio.ensure_future(self.retrieve_word(session, "verb"))
            adjective_task = asyncio.ensure_future(
                self.retrieve_word(session, "adjective")
            )
            noun_task = asyncio.ensure_future(self.retrieve_word(session, "noun"))

            results = await asyncio.gather(verb_task, adjective_task, noun_task)

            return {"verb": results[0], "adjective": results[1], "noun": results[2]}


class AsyncView(View):
    """
    Base view for allowing async with class based views.
    """
    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view


class MadlibView(ContextMixin, AsyncView):
    sentence = (
        "It was a {adjective} day. I went downstairs to see if I could "
        '{verb} dinner. I asked, "Does the stew need fresh {noun}?"'
    )

    async def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        words = await WordGenerator().generate_words()
        context.update(words)
        return context

    async def get(self, request, *args, **kwargs):
        context_data = await self.get_context_data()
        return HttpResponse(self.sentence.format(**context_data))
