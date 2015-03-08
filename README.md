Atlassian Sample Project
=========

  
  -----------------------------------------------
  
  > Description:
  
  > Assumptions:



Version
----
1.0

Installation
--------------

```sh
$ git clone https://github.com/rsubra13/atlasproj.git


```

*Installing virtualenv*

```sh
$ cd venv
$ virtualenv venv

New python executable in venv/bin/python
Installing setuptools, pip...done.

In Unix-Like Systems
$ source venv/bin/activate 

In Windows-Systems
$ source venv/Source/activate 

$ pip install -r requirements.txt

Presently there is an error while installing requirements.txt
"pg_config executable not found".

This can be overcome by installing "libpq-dev" and "python-dev".
$ sudo apt-get install libpq-dev python-dev
```
*PostGRESQL server* 

* Make sure PostGRESQL is installed in your and system and it is running properly

*Startup script*
```sh
$ python run.py
```


License
----

Open License