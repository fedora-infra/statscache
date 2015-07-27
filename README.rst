statscache
==========

A daemon to build and keep fedmsg statistics.

**Motivation**: we have a neat service called `datagrepper
<https://apps.fedoraproject.org/datagrepper>`_ with which you can query the
history of the `fedmsg <http://fedmsg.com>`_ bus.  It is cool, but insufficient
for some more advanced reporting and analysis that we would like to do.  Take,
for example, the `releng-dash <https://apps.fedoraproject.org/releng-dash>`_.
In order to render the page, it has to make a dozen or more requests to
datagrepper to try and find the 'latest' events from large awkward pages of
results.  Consequently, it takes a long time to load.

Enter, statscache.  It is a plugin to the fedmsg-hub that sits listening in our
infrastructure.  When new messages arrive, it will pass them off to `plugins
<https://github.com/fedora-infra/statscache_plugins>`_ that will calculate and
store various statistics.  If we want a new kind of statistic to be kept, we
write a new plugin for it.  It will come with a tiny flask frontend, much like
datagrepper, that allows you to query for this or that stat in this or that
format (csv, json, maybe html or svg too but that might be overkill).  The idea
being that we can then build neater smarter frontends that can render
fedmsg-based activity very quickly.. and perhaps later drill-down into the
*details* kept in datagrepper.

It is kind of like a `data mart <http://en.wikipedia.org/wiki/Data_mart>`_.

How to run it
-------------

Create a virtualenv, and git clone this directory and the statscache_plugins
repo.

Run ``python setup.py develop`` in the ``statscache`` dir first and then run it
in ``statscache_plugins``.

Lastly, in the main statscache repo directory, run: ``fedmsg-hub`` to start the
daemon.  You should see lots of fun stats being stored in stdout.

You can run the tests with ``python setup.py test``.

How it works
------------

When a message arrives, a *fedmsg consumer* receives it and places a copy of it
into each of several **buckets**.  These buckets correspond to different time
windows over which we want to process messages.

Those buckets correspond to several **producers** which wake up at different
time intervals.  For instance, right now we have a one-second producer, a
five-second producer and a one-minute producer.  These producers wake up at
their specified interval and empty *their* bucket.  They then pass the contents
of their bucket to all the registered plugins so those can calculate the
appropriate stats for that timeframe.

There are base sqlalchemy models that each of the plugins should use to store
their results (and we can add more types of base models as we discover new
needs).  But the important thing to know about the base models is that they are
responsible for knowing how to serialize themselves to different formats for
the REST API (i.e., render ``.to_csv()`` and ``.to_json()``, etc.)
