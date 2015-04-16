# Interactive data for the web - Bokeh for web developers

This repo supports the [talk I gave at PyCon 2015](https://us.pycon.org/2015/schedule/presentation/369/).

The video for the talk is available [on YouTube](https://www.youtube.com/watch?v=O5OvOLK-xqQ).

This repo contains:

* presentation - the presentation slides 
* washmap - the django application that displays the visualizations
* server - the bokeh server configuration
* notebooks - the notebooks I used to prototype the visualization & experiment with different things

This is not production code, it doesn't have tests, it's not optimized, its designed to explain some features of [bokeh](http://bokeh.pydata.org). Feel free to take snippets and use them wisely if they're 
useful, but don't expect miracles.  Feel free to ask questions via the github issues. But don't forget to checkout the following great bokeh resources:

* [bokeh.pydata.org](http://bokeh.pydata.org/en/latest/)
* [mailing list](https://groups.google.com/a/continuum.io/forum/#!forum/bokeh)
* [bokeh github repo](https://github.com/bokeh/bokeh)

I highly reccomend downloading and running the bokeh examples (they are much more extensive than the [gallery](http://bokeh.pydata.org/en/latest/docs/gallery.html)). The examples
are at [https://github.com/bokeh/bokeh/tree/master/examples](https://github.com/bokeh/bokeh/tree/master/examples).

## Talk Description

Interactive data visualization libraries are mostly a JavaScript stronghold. The new Python library, Bokeh, provides a simple, clean way to make more shiny things. Although it comes from the data science community, it has a lot to offer web developers. For a visualization you might have built in d3.js, I'll show how to build it in Bokeh, how to test it, and how to hook it into your web app.

## Installation

### Pre-reqs

I have run this repo on Ubuntu 14.04 and OSX. Things I already had:

* [heroku toolbelt](https://toolbelt.heroku.com/) - which gives you foreman
* mysql
* git
* anaconda or miniconda - [http://continuum.io/downloads](http://continuum.io/downloads)
* (Optional) News Cycle font - [http://www.fontsquirrel.com/fonts/news-cycle](http://www.fontsquirrel.com/fonts/news-cycle)

### Install and run the django app, the ipython notebooks, and the server.

#### Install 

Using conda and pip for dependencies (because conda doesn't have them all)

```bash
$ conda create -n washmap_bokeh python=2.7
$ source activate washmap_bokeh
$ conda install --file conda-requirements.txt
$ pip install -r requirements.txt
```

Often it's necessary to re-activate your env so that the bins are available.

```bash
$ source deactive
$ source activate washmap_bokeh
```

#### Run server

```bash
$ cd server
$ source .env
$ foreman start
```

#### Run django app

* Set up your database
 * Create a MySQL db called `washmap`
 * Create a user called `washmap` with a password
 * Load washmap.sql into your new database

* Create private_settings.py and edit
 * copy private_settings.py.example to private_settings.py
 * edit private_settings.py with your `washmap` user's password and with a secret key

(Note you can call the database whatever you want, the main settings file is
in main/settings.py)

Run washmap

```bash
$ cd washmap
$ ./manage.py runserver 0.0.0.0:8001
```

#### Run notebooks

```bash
$ cd notebooks
$ ipython notebook
```


### For the revealjs presentation

* Install [Node.js](http://nodejs.org/)
* Install [Grunt](http://gruntjs.com/getting-started#installing-the-cli)
* Enter presentation directory
 * ```$ cd presentation```
* Install dependencies
 * ```$ npm install ```
* Get other servers running (the presentation links to views on the django app, this needs to be running)
 * plot server at 4444 (see "Run server" above)
 * washmap django app at 8001 (See "Run django app" above)
* Serve the presentation and monitor source files for changes
 * ```$ grunt serve ```

## Notes
This repo contains a small patch to the 0.8.2 bokehjs. This issue has now been [fixed](https://github.com/bokeh/bokeh/issues/2116) 
and will be in 0.9.
