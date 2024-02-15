import os
from queue import Queue
from threading import Thread
from app.chat.callbacks.stream import StreamingHandler

# The flask current_app stuff is a hack because the starting of a new thread was throwing
# a framework error indicating that the new thread was outside of the application context.
# This doesn't seem like a problem to me, but I'm new to Python and flask, so I will take
# the instructor's word for it for now.
from flask import current_app

class StreamableChain:
    def stream(self, input):
        queue = Queue()
        handler = StreamingHandler(queue)

        def task(app_context):
            app_context.push()
            self(input, callbacks=[handler])

        Thread(target=task, args=[current_app.app_context()]).start()

        while True:
            token = queue.get()

            if token is None:
                break

            yield token