class EventBus:
    ARGUSEVENTNAME = "argus.event.received"

    def __init__(self):
        self.subscribers = {}

    def subscribe(self, subscriber, method_name):
        if self.ARGUSEVENTNAME not in self.subscribers:
            self.subscribers[self.ARGUSEVENTNAME] = []
        self.subscribers[self.ARGUSEVENTNAME].append((subscriber, method_name))

    def publish(self, data=None):
        subscribers = self.subscribers.get(self.ARGUSEVENTNAME, [])
        for subscriber, method_name in subscribers:
            if hasattr(subscriber, method_name):
                method = getattr(subscriber, method_name)
                method(data)
