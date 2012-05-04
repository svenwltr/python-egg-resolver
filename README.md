python-egg-resolver
===================

This could be a possible alternative to virtual env. It is a small
&quot;bootstrap&quot; file, that takes care about loading the right egg files
in the pythonpath.

Usage
-----

1. Copy (or link) the file "egg_resolver.py" somewhere into your package.
2. Create a file "requires.txt" next to the file "egg_resolver.py".
3. Call "egg_resolver.resolve()" in each script file.


