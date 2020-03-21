import asyncio


class Outbound_Message:
    def __init__(self, message, channel, rand, delay=False, silent=False):
        self.message = message
        self.channel = channel
        self.rand = rand
        self.silent = silent
        self.delay = delay

    async def send(self):
        async with self.channel.typing():
            if self.delay:
                await asyncio.sleep(self.delay)
            else:
                await asyncio.sleep(self.rand.randint(1, 3))

            if self.silent:
                await self.channel.send(self.message, delete_after=self.silent)
            else:
                await self.channel.send(self.message)
