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


Example
-------

1. It searches for the file "requires.txt" in the directory of
   "egg_resolver.py".
2. It opens this file and parses it line by line. Format of each line is
   something like "django_cms==2.2".
3. For each line it searches for a suitable .egg directory in the directories
   of sys.path. This could be "django_cms-2.2-py2.7.egg" for the example above.
4. If a .egg directory was found, the resolver looks in
   "package.egg/EGG-INFO/requires.txt" for other requirements and adds them to
   "sys.path", too.