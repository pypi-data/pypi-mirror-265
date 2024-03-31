"""
Example of how to use the client    
"""

from typing import Dict

from argus import Argus


class Testsub:
    def on_event(self, argus_event: Dict[str, str]) -> None:
        print(argus_event.get("Action"))
        print(argus_event.get("ActionDescription"))
        print(argus_event.get("Name"))
        print(argus_event.get("Timestamp"))


subscriber = Testsub()

argus = Argus()  # Optionally you can pass the host and port, and auth credentials inclusive.

argus.subscribe(subscriber, "on_event")
argus.connect(timeout=60)
argus.close()
