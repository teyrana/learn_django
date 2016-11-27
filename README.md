



Versions:
----
Tested on OSX 10.12. Standalone apps below installed via <code>Homebrew</code>.
- python 3.5.2
- django 1.10.3
- virtualenv 15.1.0
- pip:
  - django-bootstrap3

Miscellaneous install notes:
====


TODO:
----
- Setup Users (emails)
- Setup email senders


Database Seed data (aka initial values):
----

```
[python] manage.py loaddata city[.json]
```

Populates City list via 'loaddata' and fixtures:
- loads from <code>&lt;app&gt;/fixtures/&lt;fixture&gt;.&lt;ext&gt;</code>
- loads into implicit table name: 'weathermail_city'
- (see also: commit aa0fda2, for fixture json format example)
