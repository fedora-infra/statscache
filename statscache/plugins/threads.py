import twisted.internet.defer as twisted
import twisted.internet.threads as twisted


__all__ = [
    'Queue',
    'Future',
    'asynchronous',
]


class Queue(object):
    """ A non-blocking queue for use with asynchronous code """

    class OverflowError(Exception):
        """ The queue has overflown """
        pass

    class UnderflowError(Exception):
        """ The queue has underflown """
        pass

    def __init__(self, size=None, backlog=None):
        self._queue = twisted.DeferredQueue(size=size, backlog=backlog)

    def enqueue(self, value):
        """ Add an item to the queue, synchronously """
        try:
            self._queue.put(value)
        except twisted.QueueOverflow:
            raise Queue.OverflowError()

    def dequeue(self):
        """ Return an item from the queue, asynchronously, using a 'Future' """
        try:
            return Future(self._queue.get(), [], [])
        except twisted.QueueUnderflow:
            raise Queue.UnderflowError()


class Future(object):
    """ An asynchronously computed value """

    class AlreadyResolvedError(Exception):
        """ The 'Future' has either already succeeded or already failed """
        pass

    class CancellationError(Exception):
        """ The 'Future' has been cancelled """
        pass

    class Failure(object):
        """ Wrapper for exceptions thrown during asynchronous execution

        An instance of this class contains two attributes of consequence:
        'error', which is the exception instance raised in the asynchronous
        function, and 'stack', which is a list of stack frames in the same
        format used by 'inspect.stack'.
        """

        def __init__(self, failure):
            """ The semantics of this method are implementation-dependent """
            self.error = failure.value
            if isinstance(failure.value, twisted.CancelledError):
                # Hide Twisted's original exception (shouldn't matter)
                self.error = Future.CancellationError() 
            self.stack = failure.frames

    def __init__(self,
                 from_deferred=None,
                 on_success=None,
                 on_failure=None):
        """ Instantiate a 'Future' object

        The 'from_deferred' keyword argument initializes the 'Future' to
        encapsulate an instance of 'twisted.internet.defer.Deferred'; however,
        note that the usage of Twisted by the statscache is considered an
        implementation detail and subject to change.
        """
        self._deferred = from_deferred or twisted.Deferred()
        deferred.addCallbacks(on_success or [])
        for f in on_failure or []:
            self.on_failure(f)

    def on_success(self, f):
        """ Add a handler function to take the resolved value """
        self._deferred.addCallback(f)

    def on_failure(self, f):
        """ Add a handler function to take the resolved error

        The resolved error will be wrapped in a 'Future.Failure'.
        """
        self._deferred.addErrback(lambda x: f(Failure(x)))

    def fire(self, result):
        """ Directly resolve this 'Future' with the given 'result' """
        try:
            self._deferred.callback(result)
        except twisted.AlreadyCalledError:
            raise Future.AlreadyResolvedError()

    def fail(self, error):
        """ Directly resolve this 'Future' with the given 'result' """
        try:
            self._deferred.errback(error)
        except twisted.AlreadyCalledError:
            raise Future.AlreadyResolvedError()

    def quit(self):
        """ Quit (i.e., cancel) this 'Future' """
        self._deferred.cancel()

    @staticmethod
    def failure(error, on_success=None, on_failure=None):
        """ Create a 'Future' pre-resolved with the given 'error' (failure)

        Because this 'Future' cannot succeed, the success handlers given by
        'on_success' will be ignored.
        """
        return Future(
            from_deferred=twisted.fail(error),
            on_failure=on_failure
        )

    @staticmethod
    def success(result, on_success=None, on_failure=None):
        """ Create a 'Future' pre-resolved with the given 'result' (success)

        Because this 'Future' cannot fail, the error handlers given by
        'on_failure' will be ignored.
        """
        return Future(
            from_deferred=twisted.succeed(result),
            on_success=on_success
        )

    @staticmethod
    def compute(f, on_success=None, on_failure=None):
        """ Create a 'Future' for an asynchronous computation

        A fiber (i.e., green or lightweight thread) will be spawned to perform
        the computation.
        """
        return lambda *args, **kwargs: Future(
            from_deferred=twisted.deferToThread(f, *args, **kwargs),
            on_success=on_success,
            on_failure=on_failure
        )


# Decorator synonym for 'Future.compute'
asynchronous = Future.compute
