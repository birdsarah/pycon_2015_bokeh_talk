### To setup locally

Add a new conda environment (I had problems with py34 on heroku, so using py27):

    $ conda create -n env_name python=2.7

Edit `config.py` as appropriate (e.g. comment out `model_backend` to use default non-redis)
    
Install requirements with conda, and start app

    $ conda install --file conda-requirements.txt
    $ foreman start

### To setup on heroku

Configure heroku to use the conda buildpack and add your secret keys:

    $ heroku config:set BUILDPACK_URL=https://github.com/kennethreitz/conda-buildpack.git
    $ heroku config:set FLASK_SECRET_KEY='an actually secret key'
    $ heroku config:set BOKEH_SECRET_KEY='another secret key'

To run with redis, add the heroku add on rediscloud (the 25 level is free):

    $ heroku addons:add rediscloud:25 

Then, as normal, push to heroku to deploy
