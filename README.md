



Versions:
----
Tested on OSX 10.12. Standalone apps below installed via ```Homebrew```.
- python 3.5.2
- django 1.10.3
- virtualenv 15.1.0
- via pip:
  - django-bootstrap3
  - requests
  - sendgrid-django








Miscellaneous install notes:
====



Database Seed data (aka initial values):
----

```
[python] manage.py loaddata city[.json]
```
Populates City list via 'loaddata' and fixtures:
- loads from ```<app>/fixtures/<fixture_name>.<ext>```
- loads into implicit table name: 'weathermail_city'
- (see also: commit aa0fda2, for fixture json format example)
