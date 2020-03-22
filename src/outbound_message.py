import asyncio


class Outbound_Message:
    def __init__(self, message, channel, delay, silent=False):
        self.message = message
        self.channel = channel
        self.silent = silent
        self.delay = delay

    async def send(self):
        async with self.channel.typing():
            await asyncio.sleep(self.delay)

            if self.silent:
                await self.channel.send(self.message, delete_after=self.silent)
            else:
                await self.channel.send(self.message)
