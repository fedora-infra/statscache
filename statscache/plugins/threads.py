import twisted.internet.defer as defer
import twisted.internet.threads as threads


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
        self._queue = defer.DeferredQueue(size=size, backlog=backlog)

    def enqueue(self, value):
        """ Add an item to the queue, synchronously """
        try:
            self._queue.put(value)
        except defer.QueueOverflow:
            raise Queue.OverflowError()

    def dequeue(self):
        """ Return an item from the queue, asynchronously, using a 'Future' """
        try:
            return Future(self._queue.get(), [], [])
        except defer.QueueUnderflow:
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
            """ Instantiate a 'Failure' exception wrapper

            User code should *never* need to create one of these; instances of
            this class are created by the threading system solely for the
            purpose of shielding plugin code from the underlying threading
            mechanism, which is implementation-dependent.
            """
            self.error = failure.value
            if isinstance(failure.value, defer.CancelledError):
                # Hide Twisted's original exception (shouldn't matter)
                self.error = Future.CancellationError() 
            self.stack = failure.frames

    def __init__(self,
                 source=None,
                 on_success=None,
                 on_failure=None):
        """ Instantiate a 'Future' object

        The 'source' keyword argument initializes the 'Future' to encapsulate
        an instance of the underlying threading system's representation of a
        future. User code may not rely on the stability, behavior, or
        type-validity of this parameter.
        """
        self._deferred = source or threads.Deferred()
        for f in on_success or []:
            self.on_success(f)
        for f in on_failure or []:
            self.on_failure(f)

    def on_success(self, f):
        """ Add a handler function to take the resolved value """
        self._deferred.addCallback(f)

    def on_failure(self, f):
        """ Add a handler function to take the resolved error

        The resolved error will be wrapped in a 'Future.Failure'.
        """
        self._deferred.addErrback(lambda x: f(Future.Failure(x)))

    def fire(self, result):
        """ Directly resolve this 'Future' with the given 'result' """
        try:
            self._deferred.callback(result)
        except threads.AlreadyCalledError:
            raise Future.AlreadyResolvedError()

    def fail(self, error):
        """ Directly resolve this 'Future' with the given 'result' """
        try:
            self._deferred.errback(error)
        except threads.AlreadyCalledError:
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
            source=threads.fail(error),
            on_failure=on_failure
        )

    @staticmethod
    def success(result, on_success=None, on_failure=None):
        """ Create a 'Future' pre-resolved with the given 'result' (success)

        Because this 'Future' cannot fail, the error handlers given by
        'on_failure' will be ignored.
        """
        return Future(
            source=threads.succeed(result),
            on_success=on_success
        )

    @staticmethod
    def compute(f, on_success=None, on_failure=None):
        """ Create a 'Future' for an asynchronous computation

        A fiber (i.e., green or lightweight thread) will be spawned to perform
        the computation.
        """
        return lambda *args, **kwargs: Future(
            source=threads.deferToThread(f, *args, **kwargs),
            on_success=on_success,
            on_failure=on_failure
        )


# Decorator synonym for 'Future.compute'
asynchronous = Future.compute
