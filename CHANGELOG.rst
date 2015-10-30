
0.0.3
-----

Commits

- 4baf09ea2 Include some forgotten things in packaging declarations.
  https://github.com/fedora-infra/statscache/commit/4baf09ea2

0.0.2
-----

Pull Requests

- (@yazman)         #17, Documentation Updates
  https://github.com/fedora-infra/statscache/pull/17
- (@yazman)         #18, Dynamic scheduling based on plugins
  https://github.com/fedora-infra/statscache/pull/18
- (@yazman)         #19, Plugin initialization bugfix
  https://github.com/fedora-infra/statscache/pull/19
- (@yazman)         #20, Dynamic scheduling
  https://github.com/fedora-infra/statscache/pull/20
- (@yazman)         #21, Serve a JSON-P list of plugins as root index
  https://github.com/fedora-infra/statscache/pull/21
- (@yazman)         #24, Add default JSON/CSV serialization methods
  https://github.com/fedora-infra/statscache/pull/24
- (@yazman)         #26, Enable pagination of stats model queries and filtering/ordering by timestamp
  https://github.com/fedora-infra/statscache/pull/26
- (@yazman)         #27, Refactor model class creation out of plugin initialization
  https://github.com/fedora-infra/statscache/pull/27
- (@yazman)         #28, Real-time message processing and synchronized database updates
  https://github.com/fedora-infra/statscache/pull/28
- (@yazman)         #29, Update README
  https://github.com/fedora-infra/statscache/pull/29
- (@yazman)         #30, Add a 'limit' query string parameter to the plugin model endpoint
  https://github.com/fedora-infra/statscache/pull/30
- (@yazman)         #31, Persistent datagrepper connection
  https://github.com/fedora-infra/statscache/pull/31
- (@yazman)         #32, Concurrently query datagrepper during start-up
  https://github.com/fedora-infra/statscache/pull/32
- (@yazman)         #33, Streamlined API for plugins
  https://github.com/fedora-infra/statscache/pull/33
- (@vivekanand1101) #35, Fixed link for viewing api on localhost
  https://github.com/fedora-infra/statscache/pull/35
- (@yazman)         #36, Concurrency interface for plugins
  https://github.com/fedora-infra/statscache/pull/36
- (@yazman)         #37, Add missing module import
  https://github.com/fedora-infra/statscache/pull/37
- (@yazman)         #39, Make pagination of model queries mandatory
  https://github.com/fedora-infra/statscache/pull/39
- (@yazman)         #38, Web Frontend
  https://github.com/fedora-infra/statscache/pull/38
- (@yazman)         #40, Support for CSV responses to the model index
  https://github.com/fedora-infra/statscache/pull/40
- (@yazman)         #41, Pagination fixes
  https://github.com/fedora-infra/statscache/pull/41
- (@yazman)         #42, Reword reference page
  https://github.com/fedora-infra/statscache/pull/42
- (@rtnpro)         #43, Fix path to WSGI file apache conf
  https://github.com/fedora-infra/statscache/pull/43
- (@rtnpro)         #44, Update group for WSGI daemon process to 'apache'
  https://github.com/fedora-infra/statscache/pull/44

Commits

- 228437031 Update installation instructions in README
  https://github.com/fedora-infra/statscache/commit/228437031
- 8aae92f58 Add lots of docstrings
  https://github.com/fedora-infra/statscache/commit/8aae92f58
- da39cb2d3 Correct typos in README and a docstring
  https://github.com/fedora-infra/statscache/commit/da39cb2d3
- 66db2d592 Typo in docstring
  https://github.com/fedora-infra/statscache/commit/66db2d592
- 7ac384be3 Create missing bucket for one-day frequency
  https://github.com/fedora-infra/statscache/commit/7ac384be3
- 17fe46f09 Change positional arguments given by keyword
  https://github.com/fedora-infra/statscache/commit/17fe46f09
- b23ee46b0 Separate plugin loading and initialization
  https://github.com/fedora-infra/statscache/commit/b23ee46b0
- ba3870ef3 Rename ``plugin.idx`` to ``plugin.ident``
  https://github.com/fedora-infra/statscache/commit/ba3870ef3
- 2130b0021 Relocate cache buckets to respective producers
  https://github.com/fedora-infra/statscache/commit/2130b0021
- a5a45abbf Provide timestamp to handle() method of plugins
  https://github.com/fedora-infra/statscache/commit/a5a45abbf
- 1ddef6d6b Simplify time lapse/frequency classes
  https://github.com/fedora-infra/statscache/commit/1ddef6d6b
- 80262dc62 Dynamically generate producers based on plugins
  https://github.com/fedora-infra/statscache/commit/80262dc62
- dbe4835f3 Update statscache.plugins.Frequency
  https://github.com/fedora-infra/statscache/commit/dbe4835f3
- 33e310595 Synchronize producer/plugin frequencies
  https://github.com/fedora-infra/statscache/commit/33e310595
- 95640530a Update scheduling/frequency tests
  https://github.com/fedora-infra/statscache/commit/95640530a
- a054fd4cb Correct incorrect keyword parameter default
  https://github.com/fedora-infra/statscache/commit/a054fd4cb
- bee8359f4 Simplify Frequency test case method calls
  https://github.com/fedora-infra/statscache/commit/bee8359f4
- 8f1ae0e94 Include a default value for frequency epoch
  https://github.com/fedora-infra/statscache/commit/8f1ae0e94
- 8fe3d3d3b Separate frontend plugin initialization (bugfix)
  https://github.com/fedora-infra/statscache/commit/8fe3d3d3b
- 359eebca0 Add style and font resources for web interface
  https://github.com/fedora-infra/statscache/commit/359eebca0
- 00deeb5aa Configure Apache to serve static files
  https://github.com/fedora-infra/statscache/commit/00deeb5aa
- 52aaf60f5 Install resource and config. files with package
  https://github.com/fedora-infra/statscache/commit/52aaf60f5
- e2677b81c Very basic web frontend
  https://github.com/fedora-infra/statscache/commit/e2677b81c
- ec4089324 Add HTML, CSS, and JS files to manifest
  https://github.com/fedora-infra/statscache/commit/ec4089324
- fda52eec7 Remove timestamp from plugin handle() method
  https://github.com/fedora-infra/statscache/commit/fda52eec7
- e5ab141e5 Remove accidental line of commented-out code
  https://github.com/fedora-infra/statscache/commit/e5ab141e5
- f38ffa9f2 Correct frontend timestamp parsing
  https://github.com/fedora-infra/statscache/commit/f38ffa9f2
- 9433c1dde Add Moksha Hub version requirement
  https://github.com/fedora-infra/statscache/commit/9433c1dde
- 1c400e3f4 Typofix.
  https://github.com/fedora-infra/statscache/commit/1c400e3f4
- 22e0a0924 Re-arrange how db tables get created.
  https://github.com/fedora-infra/statscache/commit/22e0a0924
- fc420f3b7 Create a helper function for JSON[-P] handling
  https://github.com/fedora-infra/statscache/commit/fc420f3b7
- 6a931d559 Implement a web interface index route
  https://github.com/fedora-infra/statscache/commit/6a931d559
- 432e9a8e8 Generate a 404 response for nonexistent models
  https://github.com/fedora-infra/statscache/commit/432e9a8e8
- ccaf3bbed Add a 404 error string to the layout route
  https://github.com/fedora-infra/statscache/commit/ccaf3bbed
- 734203762 Remove unused variable
  https://github.com/fedora-infra/statscache/commit/734203762
- 8f0f4de40 Add default JSON and CSV serializer methods
  https://github.com/fedora-infra/statscache/commit/8f0f4de40
- 5887db45f Choose acceptable response content-types
  https://github.com/fedora-infra/statscache/commit/5887db45f
- 99abb2c73 Use Flask error handling
  https://github.com/fedora-infra/statscache/commit/99abb2c73
- 08a867e52 Fix CSV serialization
  https://github.com/fedora-infra/statscache/commit/08a867e52
- 514de7881 Combine helper function with sole user
  https://github.com/fedora-infra/statscache/commit/514de7881
- 90e076939 Relocate plugin model URL endpoints under '/api/'
  https://github.com/fedora-infra/statscache/commit/90e076939
- 037ad3633 Add SQLAlchemy query paginator class
  https://github.com/fedora-infra/statscache/commit/037ad3633
- 871c780ed Reword comment to fit in an 80-character line
  https://github.com/fedora-infra/statscache/commit/871c780ed
- 6c8e0ad39 Reword URL endpoint docstrings
  https://github.com/fedora-infra/statscache/commit/6c8e0ad39
- 14f393b71 Allow basic query filtering from web interface
  https://github.com/fedora-infra/statscache/commit/14f393b71
- 8266427d6 Customize pagination
  https://github.com/fedora-infra/statscache/commit/8266427d6
- 52d26188f Allow pagination of JSON-P model queries
  https://github.com/fedora-infra/statscache/commit/52d26188f
- 28b759090 Correct behavior of 'paginate' URL argument
  https://github.com/fedora-infra/statscache/commit/28b759090
- b706ef1e2 Use urllib for query string formatting
  https://github.com/fedora-infra/statscache/commit/b706ef1e2
- b394cf258 Use HTTP headers to control pagination
  https://github.com/fedora-infra/statscache/commit/b394cf258
- f5f1ed4db Correct outdated comment
  https://github.com/fedora-infra/statscache/commit/f5f1ed4db
- cca89c9de Correct use of mutable default argument
  https://github.com/fedora-infra/statscache/commit/cca89c9de
- e0e23bfdd Correct typo in last commit
  https://github.com/fedora-infra/statscache/commit/e0e23bfdd
- 0c255d742 Disallow dynamic model class creation
  https://github.com/fedora-infra/statscache/commit/0c255d742
- 9da4e013a Refactor backend plugin initialization
  https://github.com/fedora-infra/statscache/commit/9da4e013a
- 5ba974627 Add plugins to ready list after initialization
  https://github.com/fedora-infra/statscache/commit/5ba974627
- 111434171 Restructure plugin system
  https://github.com/fedora-infra/statscache/commit/111434171
- 681551c1b Centralize backlog query
  https://github.com/fedora-infra/statscache/commit/681551c1b
- 62afa19a1 Initialize fedmsg.meta in consumer initialization
  https://github.com/fedora-infra/statscache/commit/62afa19a1
- ca474db72 Make the frequency epoch a mandatory parameter
  https://github.com/fedora-infra/statscache/commit/ca474db72
- 6a64e6bb6 Rename Frequency to Schedule
  https://github.com/fedora-infra/statscache/commit/6a64e6bb6
- e718fd02f Python 3 compatibility fix
  https://github.com/fedora-infra/statscache/commit/e718fd02f
- ed88eacea Reflow code
  https://github.com/fedora-infra/statscache/commit/ed88eacea
- 33f069346 Fix typo
  https://github.com/fedora-infra/statscache/commit/33f069346
- 144b76435 Correct plugin backlog delta behavior
  https://github.com/fedora-infra/statscache/commit/144b76435
- 3639576bf Update statistics epoch for easier testing
  https://github.com/fedora-infra/statscache/commit/3639576bf
- 48143cb07 Correct BasePlugin.latest() behavior
  https://github.com/fedora-infra/statscache/commit/48143cb07
- 1f9305346 Fix backlog processing behavior
  https://github.com/fedora-infra/statscache/commit/1f9305346
- 5bab8c771 Update docstring
  https://github.com/fedora-infra/statscache/commit/5bab8c771
- 4d30faed9 Update README
  https://github.com/fedora-infra/statscache/commit/4d30faed9
- 6a840c693 Typo fix in README
  https://github.com/fedora-infra/statscache/commit/6a840c693
- d274b2c8f Persistent connections for datagrepper requests
  https://github.com/fedora-infra/statscache/commit/d274b2c8f
- 4ac9ab019 Add URL parameter to limit rows
  https://github.com/fedora-infra/statscache/commit/4ac9ab019
- 53e230027 Update docstring
  https://github.com/fedora-infra/statscache/commit/53e230027
- 425bec715 Correct variable name
  https://github.com/fedora-infra/statscache/commit/425bec715
- 099fb7a51 Query datagrepper concurrently during start-up
  https://github.com/fedora-infra/statscache/commit/099fb7a51
- 2874e1fae Simplify datagrepper generator code
  https://github.com/fedora-infra/statscache/commit/2874e1fae
- a3053c695 Add commented-out datagrepper profiling code
  https://github.com/fedora-infra/statscache/commit/a3053c695
- 765456b93 Add configuration option for datagrepper workers
  https://github.com/fedora-infra/statscache/commit/765456b93
- 32578f9be Enable datagrepper profiling by configuration
  https://github.com/fedora-infra/statscache/commit/32578f9be
- e30986541 Remove dead variable
  https://github.com/fedora-infra/statscache/commit/e30986541
- c5fee325c Remove dead imports
  https://github.com/fedora-infra/statscache/commit/c5fee325c
- 88e4c151c Consolidate public API under statscache.api
  https://github.com/fedora-infra/statscache/commit/88e4c151c
- ff0ec0097 Remove dead import
  https://github.com/fedora-infra/statscache/commit/ff0ec0097
- 0d8782218 Reorganize plugin API as statscache.plugins
  https://github.com/fedora-infra/statscache/commit/0d8782218
- 0ffb48a31 Update docstrings
  https://github.com/fedora-infra/statscache/commit/0ffb48a31
- 7f36c5f33 Add extensive docstring to plugin base class
  https://github.com/fedora-infra/statscache/commit/7f36c5f33
- f45004a38 Remove accidental import
  https://github.com/fedora-infra/statscache/commit/f45004a38
- a7216fd13 Create plugin worker threads API
  https://github.com/fedora-infra/statscache/commit/a7216fd13
- df185202c Elaborate in threading interface docstrings
  https://github.com/fedora-infra/statscache/commit/df185202c
- c7cc60f68 Choose worker thread counts by number of cores
  https://github.com/fedora-infra/statscache/commit/c7cc60f68
- add465fa4 Create asychronous plugin abstract base class
  https://github.com/fedora-infra/statscache/commit/add465fa4
- ce8d75dad Revise StatsConsumer logging statements
  https://github.com/fedora-infra/statscache/commit/ce8d75dad
- 355a3e88c Expand docstring
  https://github.com/fedora-infra/statscache/commit/355a3e88c
- b0811be4e Fix bad variable reference
  https://github.com/fedora-infra/statscache/commit/b0811be4e
- b1d873fb9 Ensure worker thread respawn on completion
  https://github.com/fedora-infra/statscache/commit/b1d873fb9
- 5f82001f9 Correct Twisted imports
  https://github.com/fedora-infra/statscache/commit/5f82001f9
- 4f6a65f36 Update README.rst
  https://github.com/fedora-infra/statscache/commit/4f6a65f36
- 79bd6db94 Improve error logging for worker threads
  https://github.com/fedora-infra/statscache/commit/79bd6db94
- 64257f8cb Properly import logger for plugin base classes
  https://github.com/fedora-infra/statscache/commit/64257f8cb
- 8cff32793 Specifically list symbols to export as plugin API
  https://github.com/fedora-infra/statscache/commit/8cff32793
- ad1af027f Fix symbol reference from wrong module
  https://github.com/fedora-infra/statscache/commit/ad1af027f
- b6f6f9366 Correct addition of callbacks in futures
  https://github.com/fedora-infra/statscache/commit/b6f6f9366
- a8136468b Correct inner class reference
  https://github.com/fedora-infra/statscache/commit/a8136468b
- d192dc5f1 Conceal Twisted's callback composition
  https://github.com/fedora-infra/statscache/commit/d192dc5f1
- a7736cee2 Add missing module import
  https://github.com/fedora-infra/statscache/commit/a7736cee2
- 2a3261739 Revise template hierarchy
  https://github.com/fedora-infra/statscache/commit/2a3261739
- aebd10535 Stylistic changes to model feed web page
  https://github.com/fedora-infra/statscache/commit/aebd10535
- 1e0af56ac Remove underscore.js dependency
  https://github.com/fedora-infra/statscache/commit/1e0af56ac
- d7ea8d852 Perform proper HTML escaping in model feed
  https://github.com/fedora-infra/statscache/commit/d7ea8d852
- d7af56d00 Remove redundant sorting in model feed
  https://github.com/fedora-infra/statscache/commit/d7af56d00
- e748ae6e3 Slight revision of feed JavaScript
  https://github.com/fedora-infra/statscache/commit/e748ae6e3
- 99324d37c Remove unnecessary argument to error template
  https://github.com/fedora-infra/statscache/commit/99324d37c
- 76baf6d72 Create placeholder reference web page
  https://github.com/fedora-infra/statscache/commit/76baf6d72
- b8260a3e4 Reduce font size of model feed rows
  https://github.com/fedora-infra/statscache/commit/b8260a3e4
- 9815b87aa Include plugin description on model feed web page
  https://github.com/fedora-infra/statscache/commit/9815b87aa
- 450b5583b Reduce size of statscache name in header
  https://github.com/fedora-infra/statscache/commit/450b5583b
- d580dba15 Create placeholder getting started web page
  https://github.com/fedora-infra/statscache/commit/d580dba15
- b3a12295e Redirect web index requests to getting started
  https://github.com/fedora-infra/statscache/commit/b3a12295e
- 5bab27955 Visual updates to model feed web page
  https://github.com/fedora-infra/statscache/commit/5bab27955
- 533d45807 Decrease the statscache header font size (again)
  https://github.com/fedora-infra/statscache/commit/533d45807
- 5919b809d Create placeholder dashboard web page
  https://github.com/fedora-infra/statscache/commit/5919b809d
- 6880da479 Load model feed via AJAX
  https://github.com/fedora-infra/statscache/commit/6880da479
- 2297807e4 Include Bootstrap JavaScript
  https://github.com/fedora-infra/statscache/commit/2297807e4
- 3ebec59e9 Update Bootstrap CSS to v3.3.5
  https://github.com/fedora-infra/statscache/commit/3ebec59e9
- 4fc0c910f Include Bootstrap's Glyphicons font
  https://github.com/fedora-infra/statscache/commit/4fc0c910f
- 4f7371057 Rename the "fonts" folder to "font"
  https://github.com/fedora-infra/statscache/commit/4f7371057
- 31ec29c84 Install common Bootstrap plugins
  https://github.com/fedora-infra/statscache/commit/31ec29c84
- d7aa1374c Refine CSS rules in feed.css
  https://github.com/fedora-infra/statscache/commit/d7aa1374c
- b0b95d8a6 Install moment.js
  https://github.com/fedora-infra/statscache/commit/b0b95d8a6
- ba4096a97 Install datetime-picker plugin for Bootstrap
  https://github.com/fedora-infra/statscache/commit/ba4096a97
- ed63a4021 Reflow base template
  https://github.com/fedora-infra/statscache/commit/ed63a4021
- ff1b72c64 Load Moment.js prior to the datetime-picker plugin
  https://github.com/fedora-infra/statscache/commit/ff1b72c64
- 761685cf4 Do not provide JSON data to web feed template
  https://github.com/fedora-infra/statscache/commit/761685cf4
- 43fc655d9 Add loading status and error message
  https://github.com/fedora-infra/statscache/commit/43fc655d9
- a577603d9 Minor code clean-up in model feed web view
  https://github.com/fedora-infra/statscache/commit/a577603d9
- b7e6fe6b8 Add missing ID to primary table element
  https://github.com/fedora-infra/statscache/commit/b7e6fe6b8
- 2b40140e4 Add start/stop datetime-pickers to model feed view
  https://github.com/fedora-infra/statscache/commit/2b40140e4
- b1a902925 Suppress potential duplication of API requests
  https://github.com/fedora-infra/statscache/commit/b1a902925
- 75c02fea7 Include jQuery "appear" plugin
  https://github.com/fedora-infra/statscache/commit/75c02fea7
- acee85c6c Continuous scrolling in web view of model feed
  https://github.com/fedora-infra/statscache/commit/acee85c6c
- 35ede3928 Remove unnecessary variable
  https://github.com/fedora-infra/statscache/commit/35ede3928
- 9a56e58f0 Remove unneeded Bootstrap plugins
  https://github.com/fedora-infra/statscache/commit/9a56e58f0
- 932cd6b01 Add ordering dropdown menu to view of model feed
  https://github.com/fedora-infra/statscache/commit/932cd6b01
- cbe3a628d Add comment on model feed template
  https://github.com/fedora-infra/statscache/commit/cbe3a628d
- c2e1c9bb2 Reload model feed on ordering selection
  https://github.com/fedora-infra/statscache/commit/c2e1c9bb2
- 5c963d647 Suppress unnecessary model feed reloads
  https://github.com/fedora-infra/statscache/commit/5c963d647
- efee3db99 Remove unused CSS file
  https://github.com/fedora-infra/statscache/commit/efee3db99
- c2ca73177 Convert tabs to spaces (1:4)
  https://github.com/fedora-infra/statscache/commit/c2ca73177
- 6b6f369c3 Initial version of 'Getting started' page
  https://github.com/fedora-infra/statscache/commit/6b6f369c3
- f0e1fbf51 Add custom CSS rules to layout template
  https://github.com/fedora-infra/statscache/commit/f0e1fbf51
- 30db8d958 Correct conditional page width
  https://github.com/fedora-infra/statscache/commit/30db8d958
- 76baa3157 Correct example plugin in getting started
  https://github.com/fedora-infra/statscache/commit/76baa3157
- 619e9d7e4 Explain plugin entry-points in getting started
  https://github.com/fedora-infra/statscache/commit/619e9d7e4
- e042ac988 Move utility JS methods to base template
  https://github.com/fedora-infra/statscache/commit/e042ac988
- 8d16d7950 Add comment regarding widget to base template
  https://github.com/fedora-infra/statscache/commit/8d16d7950
- e6491b2e4 Initial write of API reference web page
  https://github.com/fedora-infra/statscache/commit/e6491b2e4
- 910b96c3c Fix incorrect header name in web page
  https://github.com/fedora-infra/statscache/commit/910b96c3c
- a7943241c Initial version of dashboard web page
  https://github.com/fedora-infra/statscache/commit/a7943241c
- c1e1ad787 Separate the web endpoints from the APIs
  https://github.com/fedora-infra/statscache/commit/c1e1ad787
- a6cd0d8d1 Install static resources accessibly to Apache
  https://github.com/fedora-infra/statscache/commit/a6cd0d8d1
- 730a75321 Make pagination of model queries mandatory
  https://github.com/fedora-infra/statscache/commit/730a75321
- 84347f80e Do not install package data in setup.py
  https://github.com/fedora-infra/statscache/commit/84347f80e
- 749a9582d Support for CSV responses to the model index
  https://github.com/fedora-infra/statscache/commit/749a9582d
- b949affad Fix plugin_model() handling of query argument
  https://github.com/fedora-infra/statscache/commit/b949affad
- 68223d204 Fix docstring of statscache.app.paginate()
  https://github.com/fedora-infra/statscache/commit/68223d204
- 5dd7c9c96 Load maximum/default rows per page from config.
  https://github.com/fedora-infra/statscache/commit/5dd7c9c96
- d45b5f230 Reword reference page
  https://github.com/fedora-infra/statscache/commit/d45b5f230
- 0b329a45a Fix path to WSGI file apache conf
  https://github.com/fedora-infra/statscache/commit/0b329a45a
- 9b1f13eef Update group for WSGI daemon process to 'apache'
  https://github.com/fedora-infra/statscache/commit/9b1f13eef
- 11b6ac2fc Remove CHANGELOG header.
  https://github.com/fedora-infra/statscache/commit/11b6ac2fc

0.5.2
-----

- Typofix. `75c8b6945 <https://github.com/fedora-infra/fmn.consumer/commit/75c8b6945d4cf3c7114f29ffd12eee3cf3a1fa7b>`_
- Merge pull request #59 from fedora-infra/feature/typofix `ab230258f <https://github.com/fedora-infra/fmn.consumer/commit/ab230258f53ca0bb92cf5a507facc60823677454>`_
- Another typofix. `4cde6763e <https://github.com/fedora-infra/fmn.consumer/commit/4cde6763e8e670873534d23fed887c178eef644d>`_
- A third typofix. `823c18d51 <https://github.com/fedora-infra/fmn.consumer/commit/823c18d51d5a602b8bf5ffe077e9952a7a5f6051>`_
- Use dict interface to bunch. `6c891692c <https://github.com/fedora-infra/fmn.consumer/commit/6c891692c5595f4cf9822bee6b42a33f141af5ed>`_
- The base url has a trailing slash already. `6c1b6a0a5 <https://github.com/fedora-infra/fmn.consumer/commit/6c1b6a0a5c4cc15b693657edbfee0b0ed4315a27>`_
- Merge pull request #60 from fedora-infra/feature/typofix2 `b9dfff68e <https://github.com/fedora-infra/fmn.consumer/commit/b9dfff68e0e1805e96916e7a47eae81ecfd9a666>`_

0.5.1
-----

- Oneshot bugfix. `cf777fe26 <https://github.com/fedora-infra/fmn.consumer/commit/cf777fe26bd38dba03b28e8d08f830066f152d86>`_
- Merge pull request #57 from fedora-infra/feature/oneshot-bugfix `c412a46e4 <https://github.com/fedora-infra/fmn.consumer/commit/c412a46e47f16e12c1d7902a55752473089c2905>`_
- When constructing fake recipient dict, make sure to populate all needed values. `ba1491709 <https://github.com/fedora-infra/fmn.consumer/commit/ba1491709709030c93c2068a9603ebf3820500b9>`_
- Merge pull request #58 from fedora-infra/feature/flesh-out `be328ad72 <https://github.com/fedora-infra/fmn.consumer/commit/be328ad72d7f205b2c1bb0b47b48a0b33b734fa5>`_

0.5.0
-----

- Make the help and confirmation templates for IRC configurable. `700b4da3f <https://github.com/fedora-infra/fmn.consumer/commit/700b4da3fd9f0182394178e1423cf6d8feeef489>`_
- Make the help and confirmation templates for email configurable. `5a6223568 <https://github.com/fedora-infra/fmn.consumer/commit/5a62235682db75a851e2d84d435d070600729e98>`_
- Merge pull request #47 from fedora-infra/feature/configurable-help-message `95b06b47d <https://github.com/fedora-infra/fmn.consumer/commit/95b06b47d0ce33794ef034f44316f26bb78c1e03>`_
- Use a better default email address... `3b38543d3 <https://github.com/fedora-infra/fmn.consumer/commit/3b38543d35bba1a3fa42f571bb33f2bca4972854>`_
- Merge pull request #48 from fedora-infra/feature/better-default-email `173804c4b <https://github.com/fedora-infra/fmn.consumer/commit/173804c4ba87b92cea38e895a512a34a541ab901>`_
- Implement one-shot filters in the consumer `32b701b02 <https://github.com/fedora-infra/fmn.consumer/commit/32b701b0234b145dd418fd642d632563ded90a75>`_
- Improve findability of the hacking document `e6b38542c <https://github.com/fedora-infra/fmn.consumer/commit/e6b38542ca360d32587d8526e17518d8fe18507c>`_
- Merge pull request #49 from fedora-infra/oneshot `02d064d07 <https://github.com/fedora-infra/fmn.consumer/commit/02d064d07ef7b2f73feebd0cd6700a2749efafa9>`_
- Merge pull request #50 from fedora-infra/docs `98f93a3d0 <https://github.com/fedora-infra/fmn.consumer/commit/98f93a3d00165d31f09bc10da94b81373468fd80>`_
- Employ the verbose value to send more or less details in a digest email. `f932a05cf <https://github.com/fedora-infra/fmn.consumer/commit/f932a05cf9a017ba87f7e0501e335ac731185b8b>`_
- Merge pull request #51 from fedora-infra/feature/verbosity `65f9e9bf8 <https://github.com/fedora-infra/fmn.consumer/commit/65f9e9bf8da4a8bd7d4d47986d3b5d644ccbe7bc>`_
- Queued messages won't have this at first. `b97a8c05c <https://github.com/fedora-infra/fmn.consumer/commit/b97a8c05cee141cf30f9c951c8bb486db9c5ee20>`_
- Default to True. `b7c656541 <https://github.com/fedora-infra/fmn.consumer/commit/b7c6565415fd34c0c7880adc55c93c08c6981562>`_
- Move utils to their own file for re-use. `118ce38d1 <https://github.com/fedora-infra/fmn.consumer/commit/118ce38d103c1c14374fa24d0550de09f37db77b>`_
- Make mail handler deal with bad emails. `e5716e65e <https://github.com/fedora-infra/fmn.consumer/commit/e5716e65e657a10ab138fe17db3e5c3b01739d5a>`_
- Only prefix irc messages with topic if we're 'marking up' messages. `a7d71f540 <https://github.com/fedora-infra/fmn.consumer/commit/a7d71f5401ae0b6f9d2fd3cd8d9018e6295cbe07>`_
- Merge pull request #52 from fedora-infra/feature/deal-with-bad-emails `1bafaea91 <https://github.com/fedora-infra/fmn.consumer/commit/1bafaea91505250721b95c7079eee47703f99e13>`_
- Merge pull request #53 from fedora-infra/feature/simpler-irc-format `496b70148 <https://github.com/fedora-infra/fmn.consumer/commit/496b7014845995693992f44459228ab72f1b7bb0>`_
- Only append the "triggered by" link to emails if the user wants it. `53a1a13f3 <https://github.com/fedora-infra/fmn.consumer/commit/53a1a13f30034843089802c55941a15c735ba143>`_
- Merge pull request #55 from fedora-infra/feature/mail-footer `a58b5d736 <https://github.com/fedora-infra/fmn.consumer/commit/a58b5d736ac4ec560d565e70766cb587159b8460>`_
- Manually prepend the subtitle to the longform `27740a6b5 <https://github.com/fedora-infra/fmn.consumer/commit/27740a6b5c618c71948367667e8159816c41d032>`_
- Merge pull request #56 from fedora-infra/feature/de-duplicate-subtitle `6ba39eba0 <https://github.com/fedora-infra/fmn.consumer/commit/6ba39eba022ce8421cb1deccd1da202f252b59fe>`_

0.4.5
-----

- Randomize preference list per-thread. `2aa92ed0d <https://github.com/fedora-infra/fmn.consumer/commit/2aa92ed0dd8004df33b3c6de62b047caa895f96a>`_
- Merge pull request #43 from fedora-infra/feature/randomize `fab6f4dd5 <https://github.com/fedora-infra/fmn.consumer/commit/fab6f4dd54b0cc58546cff8c83eab97cbbbdbb94>`_
- Use the first portion of the hostname here. `79ada97ae <https://github.com/fedora-infra/fmn.consumer/commit/79ada97ae9560ea1ba424c22cef76e52114d883e>`_
- Add a zoo of X-Fedmsg-* headers to email messages. `1b5822dd4 <https://github.com/fedora-infra/fmn.consumer/commit/1b5822dd4079fc714a98d8487c742a39dc8c4f4f>`_
- Merge pull request #45 from fedora-infra/feature/fedmsg-email-headers `025fa1667 <https://github.com/fedora-infra/fmn.consumer/commit/025fa1667304077d22bc59498f236247e52e54d0>`_
- Drop junk suffixes and add some performance debugging. `9f7a1f3aa <https://github.com/fedora-infra/fmn.consumer/commit/9f7a1f3aaab0f43af3a3c9551a62b019499df90b>`_
- Merge pull request #46 from fedora-infra/feature/debugging `89ae2c441 <https://github.com/fedora-infra/fmn.consumer/commit/89ae2c4418d64f95cad9d22cd23df2726a72b0d7>`_
- Also junk. `5d62ff231 <https://github.com/fedora-infra/fmn.consumer/commit/5d62ff231a917dd673379b43621941a900bcf4ed>`_

0.4.4
-----

- Initialize the cache at startup. `e9d5cdcff <https://github.com/fedora-infra/fmn.consumer/commit/e9d5cdcff1f6cc2f1df428466f3e889a37c8ac59>`_
- Only refresh the prefs cache for single users when we can. `b8af37260 <https://github.com/fedora-infra/fmn.consumer/commit/b8af3726026cb9bf3a637abb69a38e9b7cecb3d6>`_
- Merge pull request #42 from fedora-infra/feature/per-person-cache-refresh `34774c5ca <https://github.com/fedora-infra/fmn.consumer/commit/34774c5cac62ec27d5389a1aa4a78701a6d8684f>`_

0.4.3
-----

- Remove extra lines from desc on PyPI `5610bbe15 <https://github.com/fedora-infra/fmn.consumer/commit/5610bbe153b756cc55f68fa031768cf649390bd7>`_
- Remove extra newlines. `021d2d68f <https://github.com/fedora-infra/fmn.consumer/commit/021d2d68fbc0dd7bb407f5ba64ad6e5e219552c0>`_
- Merge pull request #39 from msabramo/remove_extra_lines_from_desc_on_PyPI `d3829e77e <https://github.com/fedora-infra/fmn.consumer/commit/d3829e77e8045d1af9896dabcd7e8b59941a86a9>`_
- Convert Nones to empty strings here. `a58edbf0e <https://github.com/fedora-infra/fmn.consumer/commit/a58edbf0e16095ac730d1038f18d2ccd983e4fe4>`_
- Merge branch 'develop' of github.com:fedora-infra/fmn.consumer into develop `ae5fba089 <https://github.com/fedora-infra/fmn.consumer/commit/ae5fba0891e66e7fde45b85ac6d0652fb0ed2966>`_
- Include anitya messages, which start with org.release-monitoring.* `9e30e4283 <https://github.com/fedora-infra/fmn.consumer/commit/9e30e4283db9633f4ca4987050f7042c3fc0ee87>`_
- Merge pull request #40 from fedora-infra/feature/include-anitya `884e922ad <https://github.com/fedora-infra/fmn.consumer/commit/884e922ad580d4c58067408a31e6ccee26ebbd11>`_

0.4.1
-----

- Add forgotten import. `42f0f0460 <https://github.com/fedora-infra/fmn.consumer/commit/42f0f0460c46a06b54c5c558e59755c1f896d9cf>`_
- Undo tuple arguments to email module. `21e6ba0cf <https://github.com/fedora-infra/fmn.consumer/commit/21e6ba0cf3eb28d5215a5db40e522c61f7cccb7a>`_
- Merge pull request #33 from fedora-infra/feature/further-email-fixes `bf2505232 <https://github.com/fedora-infra/fmn.consumer/commit/bf25052325d6dc1117ee0695177aae466a2850bf>`_
- Make autocreate configurable for staging.  Fixes #34. `02d000ad8 <https://github.com/fedora-infra/fmn.consumer/commit/02d000ad81b121ff82a2988cfc6b2f504ae761e4>`_
- Only create account for sponsee. `be3043ea6 <https://github.com/fedora-infra/fmn.consumer/commit/be3043ea6b6acdfd913f94f294cb96bee26b397d>`_
- Merge pull request #35 from fedora-infra/feature/autocreate `e89f298b1 <https://github.com/fedora-infra/fmn.consumer/commit/e89f298b169243862d8f41cb71f337f1722d6df8>`_
- Merge pull request #36 from fedora-infra/feature/distinguish `40f293182 <https://github.com/fedora-infra/fmn.consumer/commit/40f2931829bdc004291d0b0910f6569b1c3a2b26>`_
- Create new accounts for new fedbadges users. `d6515106a <https://github.com/fedora-infra/fmn.consumer/commit/d6515106a87f7cafe4cc9561f37b484383815e2b>`_
- Merge branch 'feature/distinguish' into develop `16f7ba50c <https://github.com/fedora-infra/fmn.consumer/commit/16f7ba50c8e6b17d112423abb8d7a918c4510952>`_
- Log about it. `c226b87f2 <https://github.com/fedora-infra/fmn.consumer/commit/c226b87f296b4e76c9398ca8107ba93d8d895112>`_
- Use the new msg2long_form API. `20fa62aa0 <https://github.com/fedora-infra/fmn.consumer/commit/20fa62aa08639a0337ebabc295798eef01d74cc5>`_
- Also use long_form for batch emails. `67b43f1f1 <https://github.com/fedora-infra/fmn.consumer/commit/67b43f1f158262071a2c0d914d6bda90eb12d7dc>`_
- Include link with long_form. `f3dfa33e2 <https://github.com/fedora-infra/fmn.consumer/commit/f3dfa33e29651347b86754eb7a78ce37ba279cf5>`_
- Digest for IRC messages. `1e81bdf12 <https://github.com/fedora-infra/fmn.consumer/commit/1e81bdf12f78464311c4f4d18264c6218be89c8f>`_
- Merge pull request #37 from fedora-infra/feature/long-form `be92413d3 <https://github.com/fedora-infra/fmn.consumer/commit/be92413d36543f239121c39b96806efa45a22f30>`_
- Further comment. `8cc18db11 <https://github.com/fedora-infra/fmn.consumer/commit/8cc18db11b36893882d9b875b217d284ad797b6c>`_
- Merge pull request #38 from fedora-infra/feature/irc-digest `9abaea8e4 <https://github.com/fedora-infra/fmn.consumer/commit/9abaea8e489097b42aedaead73829065e741df08>`_

0.3.1
-----

- Log errors from the routine polling producers. `a00e51c10 <https://github.com/fedora-infra/fmn.consumer/commit/a00e51c1026d33a4bf925397f2e20b5823f4249c>`_
- Try to get encoding right with email messages. `1b604dbe6 <https://github.com/fedora-infra/fmn.consumer/commit/1b604dbe6855a9c82134c74c498944fd872412bc>`_
- Use to_bytes. `580bac101 <https://github.com/fedora-infra/fmn.consumer/commit/580bac101be0b44065140a39ffdf91fd66703462>`_
- The unicode sandwich is king. `ec40383c7 <https://github.com/fedora-infra/fmn.consumer/commit/ec40383c79442f9e9628b75faeb922042fd6cc35>`_
- Somehow we got this backwards. `0024b43ae <https://github.com/fedora-infra/fmn.consumer/commit/0024b43ae81933e8df7768c47847cd7fbb6ca905>`_
- Merge pull request #32 from fedora-infra/feature/consumer-errors `fe20ca060 <https://github.com/fedora-infra/fmn.consumer/commit/fe20ca0601f768c8eb05ea74233cb978885538fb>`_
- Merge pull request #31 from fedora-infra/feature/producer-errors `a138144e9 <https://github.com/fedora-infra/fmn.consumer/commit/a138144e9a253667b089ef9f5bf435616e50112a>`_

0.3.0
-----

- I want to know about this. `91c56fa82 <https://github.com/fedora-infra/fmn.consumer/commit/91c56fa82a60b20d31d8da4e1b8a10fc306dcb68>`_
- This gives a 2.5x speedup in production. `8c74fa5ce <https://github.com/fedora-infra/fmn.consumer/commit/8c74fa5cecb01fa031d6725f25f869818d157dc1>`_
- This probably shouldn't be turned off by default.  It makes development harder. `92a1531fe <https://github.com/fedora-infra/fmn.consumer/commit/92a1531fe87f07d049d65026c2e8306d5cb7ddb5>`_
- Add some fas credentials at startup. `1991e2a9e <https://github.com/fedora-infra/fmn.consumer/commit/1991e2a9ed4c9428a5b2ba67abb60d50b55ec04b>`_
- long live threebot! `982b2fed1 <https://github.com/fedora-infra/fmn.consumer/commit/982b2fed1bc883722408b0a8c03914fad82772f6>`_
- Invalidate cache for group membership. `6e672c64a <https://github.com/fedora-infra/fmn.consumer/commit/6e672c64a26a1e64538767e409a441cadab66404>`_
- Merge pull request #26 from fedora-infra/feature/group_maintainer `f3706f142 <https://github.com/fedora-infra/fmn.consumer/commit/f3706f142a77cf3dd8c7395c4a495c4e18f9b9f7>`_
- When someone is added to the packager group create its user locally with the default rules `2ed504e2a <https://github.com/fedora-infra/fmn.consumer/commit/2ed504e2a71a9e95c0b4fb3e7dc149827a729d93>`_
- Refresh FMN's cache and pep8 fixes `10070e118 <https://github.com/fedora-infra/fmn.consumer/commit/10070e1186adca7cf4cc40919c024f2a938e9fa6>`_
- Merge pull request #27 from fedora-infra/rules_for_new_packagers `58349cdf4 <https://github.com/fedora-infra/fmn.consumer/commit/58349cdf47baaa01e4400da8054765a8946cb0c1>`_
- Throw a lock around cached preference refresh. `c58bbcbb3 <https://github.com/fedora-infra/fmn.consumer/commit/c58bbcbb3352b2079b6816e3184271d3a0995258>`_
- Merge pull request #28 from fedora-infra/feature/lock-on-pref-update `1c6a1271a <https://github.com/fedora-infra/fmn.consumer/commit/1c6a1271a48d10900a79c4b0661bbc10f11cf059>`_
- Fix bugs introduced in 2ed504e2a71a9e95c0b4fb3e7dc149827a729d93 `02fd14d53 <https://github.com/fedora-infra/fmn.consumer/commit/02fd14d5394c87acccf13c71d81ba14c22171f37>`_
- Fix incorrect fas message structure. `750148bcc <https://github.com/fedora-infra/fmn.consumer/commit/750148bccfebba0a4f00eb4617f828432d7d0272>`_
- pep8 `c8069b98b <https://github.com/fedora-infra/fmn.consumer/commit/c8069b98b1b5adb3a90b1feaa1512a09c64f06c6>`_
- When creating new Fedora users, enable by default. `dc4544ea1 <https://github.com/fedora-infra/fmn.consumer/commit/dc4544ea181f88b3eba6409ef46ae89b80a9fc27>`_
- Merge pull request #29 from fedora-infra/feature/possibly-active-by-default `bb4b183c8 <https://github.com/fedora-infra/fmn.consumer/commit/bb4b183c827231d606a94f3bc8557552480b4dca>`_
- Don't tack on delta if its in the future :clock1: :heavy_dollar_sign: `860d6a8a6 <https://github.com/fedora-infra/fmn.consumer/commit/860d6a8a665a9e9781c8e8b6256011d9216dcbdd>`_
- Merge pull request #30 from fedora-infra/feature/futuro `b435dbb05 <https://github.com/fedora-infra/fmn.consumer/commit/b435dbb05c158f460be1c87842a7d383b4d6908e>`_

0.2.7
-----

- Typofix. `a759ebc2d <https://github.com/fedora-infra/fmn.consumer/commit/a759ebc2d033e6cc7d1b92757b10fe76df68170f>`_

0.2.6
-----

- This thing doesn't actually have access to the config. `44b0bf075 <https://github.com/fedora-infra/fmn.consumer/commit/44b0bf075d1c1263b60a6bb43a3cd55cb89d134f>`_
- Merge pull request #23 from fedora-infra/feature/irc-bugfix `97effdc52 <https://github.com/fedora-infra/fmn.consumer/commit/97effdc52dd3b9b41827e56a314216f11072133b>`_
- Typofix. `a3cf9477f <https://github.com/fedora-infra/fmn.consumer/commit/a3cf9477f61139bc3bc250b62b752315d411f2b2>`_
- Merge pull request #24 from fedora-infra/feature/typofix `37ceca209 <https://github.com/fedora-infra/fmn.consumer/commit/37ceca209df200ead054edf0d93b28b3d29b108d>`_
- fix: updated IRC message formatting `528eaf619 <https://github.com/fedora-infra/fmn.consumer/commit/528eaf619cbd6a990395788a3fe91ff1033c2ea1>`_
- fix: added whitespace as requested by upstream `f157a3308 <https://github.com/fedora-infra/fmn.consumer/commit/f157a3308a6d92d945d13080f6e4991296ae7e88>`_
- Merge pull request #25 from Rorosha/develop `d42317d75 <https://github.com/fedora-infra/fmn.consumer/commit/d42317d75458b9922be140ba483d95be90b49933>`_

0.2.5
-----

- Fix missed session in the email backend. `2935d2c2d <https://github.com/fedora-infra/fmn.consumer/commit/2935d2c2dae72361ad55898920f27ab4db2deb18>`_
- Intelligent pkgdb2 cache invalidation. `b31f56223 <https://github.com/fedora-infra/fmn.consumer/commit/b31f562236ea8334ce5bfe210209b90c4d470523>`_
- Merge pull request #22 from fedora-infra/feature/pkgdb2-cache-invalidation `0a8bbc930 <https://github.com/fedora-infra/fmn.consumer/commit/0a8bbc930f103f1a90aa9a02d717198febe1210f>`_

0.2.4
-----

- Tweak config for development. `8843a4cde <https://github.com/fedora-infra/fmn.consumer/commit/8843a4cde486337c4a89d80c72624de7bf195efc>`_
- Only reconnect to IRC if not shutting down. `e9f0caf7f <https://github.com/fedora-infra/fmn.consumer/commit/e9f0caf7f9b3cf8e75c88165255cb604346754f4>`_
- Merge pull request #19 from fedora-infra/feature/careful-with-the-irc-reconnects `69b4522f4 <https://github.com/fedora-infra/fmn.consumer/commit/69b4522f4dacb2fe03281c7fcdd0fe419b41d9c0>`_
- Avoid logging so much unnecessarily. `c3d59803d <https://github.com/fedora-infra/fmn.consumer/commit/c3d59803d3e20c7c3731280fe6daf7213f173b23>`_
- Use the new caching mechanism from fmn.lib. `0239451cc <https://github.com/fedora-infra/fmn.consumer/commit/0239451ccd8dffca2cec22916aaa6dc34940af56>`_
- Merge pull request #20 from fedora-infra/feature/cream `716e54d6c <https://github.com/fedora-infra/fmn.consumer/commit/716e54d6cd63e1b373a9549d0263f53754f2d923>`_
- Add a relative arrow date to the irc message `296868357 <https://github.com/fedora-infra/fmn.consumer/commit/29686835749e1106bf4360606d0b922fc4abe5bd>`_
- Merge pull request #21 from fedora-infra/feature/relative-date `7ca396cf0 <https://github.com/fedora-infra/fmn.consumer/commit/7ca396cf02ed96a991eeb9a2ef947eba3d979aca>`_
- Link to dev instructions from the README. `2a35183f2 <https://github.com/fedora-infra/fmn.consumer/commit/2a35183f223f0a7c6dabec1a4c91cb12335ee1d3>`_
- Add a way to disable a backend alltogether. `6e4fa1287 <https://github.com/fedora-infra/fmn.consumer/commit/6e4fa12879f50c4b1f9fa6bfb18d3f1d0d110b36>`_
- Reorganize backend to not keep session as a state attribute. `67fbd80ac <https://github.com/fedora-infra/fmn.consumer/commit/67fbd80ac49b2f982dc1e73fc9f20e23550b4a2b>`_
- Employ new presentation bools. `7d039fb78 <https://github.com/fedora-infra/fmn.consumer/commit/7d039fb78c3be94c457049e7dadbcf898464bc92>`_
- Handle colorizing IRC messages. `7c5df91d8 <https://github.com/fedora-infra/fmn.consumer/commit/7c5df91d8370d0eb904e74516004a10fbc00146b>`_

0.2.3
-----

- Adapt to the new url scheme. `deded804b <https://github.com/fedora-infra/fmn.consumer/commit/deded804b9caa38e54dbe5e3cc0b1149b17bf112>`_
- .total_seconds compat for python 2.6. `3590f0166 <https://github.com/fedora-infra/fmn.consumer/commit/3590f0166bed474881d7d8a03feecb46e160a837>`_
- Fix typo in mail backend. `751112c43 <https://github.com/fedora-infra/fmn.consumer/commit/751112c43316bcd0382643b1534e34f44523223a>`_
- Update handle_batch to use the new detail model. `627cb8d2c <https://github.com/fedora-infra/fmn.consumer/commit/627cb8d2cba533c8aedc8682202257a609685c52>`_
- Continue on if we happen to send a message batch. `62c700053 <https://github.com/fedora-infra/fmn.consumer/commit/62c700053ea0bad85dec42b9412c1dd349145275>`_
- Make digest emails a little bit nicer. `63c775402 <https://github.com/fedora-infra/fmn.consumer/commit/63c775402c9339d0f7f0af865e5c7645966c4a8c>`_
- Try to reconnect if irc connection fails. `0e2792dd1 <https://github.com/fedora-infra/fmn.consumer/commit/0e2792dd156b69ae74c324dd04d2ce8032aa23e6>`_
- Shorten links with dagd for irc. `b0ff7e84c <https://github.com/fedora-infra/fmn.consumer/commit/b0ff7e84cf5a1acfbada18a506943f653f548b37>`_
- Merge pull request #10 from fedora-infra/feature/retry-irc-connect `42b009840 <https://github.com/fedora-infra/fmn.consumer/commit/42b009840fe6cf002adf9a4e8cce6d80effa66e0>`_
- Merge pull request #11 from fedora-infra/feature/shorten-with-dagd `708b7089d <https://github.com/fedora-infra/fmn.consumer/commit/708b7089dcc59fee29f4944bfeeb1b09199565c1>`_
- Provide shortlinks back to filters that trigger messages. `80bf02ac5 <https://github.com/fedora-infra/fmn.consumer/commit/80bf02ac5dbb8350b9159e573915d4b415350fdc>`_
- Merge pull request #13 from fedora-infra/feature/short-backlinks `27b1cfbff <https://github.com/fedora-infra/fmn.consumer/commit/27b1cfbffed8a0353a53fbd3c88d3f7a5a26f290>`_
- Queue and flush messages when lost client. `ccf3ca741 <https://github.com/fedora-infra/fmn.consumer/commit/ccf3ca74135eecc0308f276ee583a5e572fb7cf8>`_
- Merge branch 'develop' into feature/queue-when-no-clients `5474d3460 <https://github.com/fedora-infra/fmn.consumer/commit/5474d346063f02c8edc759c782f22e7481fbfc2d>`_
- Handle incomplete recipient dict. `23cd5dea3 <https://github.com/fedora-infra/fmn.consumer/commit/23cd5dea3134a129cbd2a54073818981d7ace281>`_
- Merge pull request #14 from fedora-infra/feature/queue-when-no-clients `c4f0879c5 <https://github.com/fedora-infra/fmn.consumer/commit/c4f0879c57398fdb5475ee3d8c6dd47fd6e7f9a4>`_

0.2.2
-----

- Some prep work for Android `de2c03ba5 <https://github.com/fedora-infra/fmn.consumer/commit/de2c03ba5782adf14ee3a804bef29e19c70f3225>`_
- Attempt to add registration id updating `7e12c86ab <https://github.com/fedora-infra/fmn.consumer/commit/7e12c86ab5159d3aa7e23815d9bf2263b8c27f06>`_
- Add base_url to all messages, nuke unused vars `d6c68b84a <https://github.com/fedora-infra/fmn.consumer/commit/d6c68b84a1a9a1eca5b32b2aa03aad52f4eb71d3>`_
- Merge pull request #4 from fedora-infra/android `d2acbf84f <https://github.com/fedora-infra/fmn.consumer/commit/d2acbf84f86c420dbb794bd55d0bc2e53a729b1b>`_

0.2.1
-----

- Shorten string. `d614743fc <https://github.com/fedora-infra/fmn.consumer/commit/d614743fcc256364871206c6b40d6f556e5f2d5d>`_

0.2.0
-----

- And that's why it wasn't working in stg. `011cec80d <https://github.com/fedora-infra/fmn.consumer/commit/011cec80db0393d25755986428e5935bd2c81bf5>`_
- Add forgotten import. `ae164330e <https://github.com/fedora-infra/fmn.consumer/commit/ae164330e92a6058b27c21a78e6f0cf9218fa91c>`_
- Protect against nonexistant preference. `e18cadcf5 <https://github.com/fedora-infra/fmn.consumer/commit/e18cadcf54e0e97f8e37e9d53ef8e1ddb86567a0>`_
- config for pkgdb queries. `00965738e <https://github.com/fedora-infra/fmn.consumer/commit/00965738eb0045b0a08d2bb0ff42e84a4bc5f13d>`_
- Some defaults for dogpile cache. `a1a375898 <https://github.com/fedora-infra/fmn.consumer/commit/a1a375898cb6afb9a4677f2a443479b663747a39>`_

0.1.3
-----

- Include the forgotten fmn.consumer.backends module. `3ec8712e0 <https://github.com/fedora-infra/fmn.consumer/commit/3ec8712e08ebeeb641ab52a10c5414b146cd02a6>`_

0.1.2
-----

- Include license and changelog. `5b05968e7 <https://github.com/fedora-infra/fmn.consumer/commit/5b05968e7a99187a19469b14ee642234770528f3>`_

0.1.1
-----

- Add fedmsg config stuff. `a6e444bc3 <https://github.com/fedora-infra/fmn.consumer/commit/a6e444bc3664099bc3f5a424f354c7b0e302e876>`_
