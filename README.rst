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
infrastructure.  When new messages arrive, it will pass them off to plugins
that will calculate and store various statistics.  If we want a new kind of
statistic to be kept, we write a new plugin for it.  It will come with a tiny
flask frontend, much like datagrepper, that allows you to query for this or
that stat in this or that format (csv, json, maybe html or svg too but that
might be overkill).  The idea being that we can then build neater smarter
frontends that can render fedmsg-based activity very quickly.. and perhaps
later drill-down into the *details* kept in datagrepper.
