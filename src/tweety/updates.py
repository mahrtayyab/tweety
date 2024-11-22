import asyncio
from .utils import get_running_loop


class UpdateMethods:

    def on(self, event):
        def decorator(f):
            self.add_event_handler(f, event)
            return f

        return decorator

    def add_event_handler(self, callback, event):
        self._event_builders.append((event, callback))

    async def _run_until_disconnected(self):
        tasks = []
        for event in self._event_builders:
            update = event[0](self, event[1])
            task = get_running_loop().create_task(update.start())
            tasks.append(task)
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            raise asyncio.CancelledError

    def run_until_disconnected(self):
        if get_running_loop().is_running():
            return self._run_until_disconnected()
        try:
            return get_running_loop().run_until_complete(self._run_until_disconnected())
        except KeyboardInterrupt:
            raise asyncio.CancelledError




