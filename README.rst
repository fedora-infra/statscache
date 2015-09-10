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

In the main statscache repo directory, run ``fedmsg-hub`` to start the
daemon.  You should see lots of fun stats being stored in stdout.  To launch
the web interface (which currently only serves JSON and CSV responses), run
``python statscache/app.py`` in the same directory.  You can now view a list of
the available plugins in JSON by visiting
``localhost:5000/api/``, and you can retrieve the
statistics recorded by a given plugin by appending its identifier to that same
URL.

You can run the tests with ``python setup.py test``.

How it works
------------

When a message arrives, a *fedmsg consumer* receives it and hands a copy to
each loaded plugin for processing.  Each plugin internally caches the results
of this message processing until a *polling producer* instructs it to update
its database model and empty its cache.  The frequency at which the polling
producer does so is configurable at the application level and is set to one
second by default.

There are base sqlalchemy models that each of the plugins should use to store
their results (and we can add more types of base models as we discover new
needs).  But the important thing to know about the base models is that they are
responsible for knowing how to serialize themselves to different formats for
the REST API (e.g., render ``.to_csv()`` and ``.to_json()``).

Even though statscache is intended to be a long-running service, the occasional
reboot is inevitable.  However, having breaks in the processed history of
fedmsg data may lead some plugins to produce inaccurate statistics.  Luckily,
statscache comes built-in with a mechanism to transparently handle this.  On
start-up, statscache checks the timestamp of each plugin's most recent database
update and queries datagrepper for the fedmsg data needed to fill in any gaps.
On the other hand, if a plugin specifically does not need a continuous view of
the fedmsg history, then it may specify a "backlog delta," which is the
maximum backlog of fedmsg data that would be useful to it.
