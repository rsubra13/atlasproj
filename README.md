AtlasParse - Chat String parse sample Application 
=========

  
  -----------------------------------------------
  

Description
----
  
This code takes a chat message string and returns a JSON string containing information about its contents. 

1. @mentions - A way to mention a user. Always starts with an '@' and ends when hitting a non-word character.
(http://help.hipchat.com/knowledgebase/articles/64429-how-do-mentions-work-)

2. Emoticons - We need to consider 'custom' emoticons which are ASCII strings, no longer than 15 characters, contained in parenthesis. You can assume that anything matching this format is an emoticon. (http://hipchat-emoticons.nyh.name)

3. Links - Any URLs contained in the message, along with the page's title.

Examples:
---------
For example, calling your function with the following inputs should result in the corresponding return values.

```sh
Input: "@chris you around?"
Return (string):
{
  "mentions": [
    "chris"
  ]
}

Input: "Good morning! (megusta) (coffee)"
Return (string):
{
  "emoticons": [
    "megusta",
    "coffee"
  ]
}


Input: "Olympics are starting soon; http://www.nbcolympics.com"
Return (string):
{
  "links": [
    {
      "url": "http://www.nbcolympics.com",
      "title": "NBC Olympics | 2014 NBC Olympics in Sochi Russia"
    }
  ]
}


Input: "@bob @john (success) such a cool feature; https://twitter.com/jdorfman/status/430511497475670016"
Return (string):
{
  "mentions": [
    "bob",
    "john"
  ],
  "emoticons": [
    "success"
  ]
  "links": [
    {
      "url": "https://twitter.com/jdorfman/status/430511497475670016",
      "title": "Twitter / jdorfman: nice @littlebigdetail from ..."
    }
  ]
}
```

Assumptions:



Version
----
1.0

Testing the project
----

The project can be tested 2 ways. 

I) CLI :

1. Run ``messageDecode.py``		 like a normal python script
2. Provide your own chat string (please see above section for examples)
3. Get the formatted JSON output in the console. 

II) Webapplication :

The webapp is not hosted but a demo is given @ (https://www.youtube.com/watch?v=Ou1nndcva54&feature=em-upload_owner) 


Following are the ways of installing and testing the webapp. 

Installation 
--------------
a) Git repo clone:
```sh
$ git clone https://github.com/rsubra13/atlasproj.git


```
b) 
*Installing virtualenv*

It is a good practice to install all the packages in a virtual environment. 
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
c) *PostGRESQL server* 

* Make sure PostGRESQL is installed in your and system and it is running properly. Please create the database and use the POSTGRES connection string as given in ``config.py``

d) *Startup script*
```sh
$ python run.py
```

