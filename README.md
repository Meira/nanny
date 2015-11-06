### Nanny watches over your cheeky Python programs

Nanny is an extensible watchdog app. You can add Python classes that
are called `nannies`, which all must inherit from the generic Nanny
class.

app.py is a sample app that sends excerpts from a famous poem by a
famous Russian poet. Substitute your email in the file app.py line 69,
and run `python nanny.py app.py` to find out which poem :)

Nannies write logs to an sqlite database. Run `nanny.py --stat app` to
view statistics for the application called `app.py`.
