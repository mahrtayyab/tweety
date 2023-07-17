import threading


class UpdateMethods:

    def on(self, event):
        def decorator(f):
            self.add_event_handler(f, event)
            return f

        return decorator

    def add_event_handler(self, callback, event):
        self._event_builders.append((event, callback))

    def run_until_disconnected(self):
        for event in self._event_builders:
            threading.Thread(target=event[0], args=(self.request, event[1])).start()




