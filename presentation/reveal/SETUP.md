Getting things running:

* presentation at 8000 - grunt serve
* plot server at 4444 - export PORT=4444 | source activate server | foreman start
* washmap django app at 8001 - source activate washmap | ./manage.py runserver 0.0.0.0:8001
* uncomment custom.js in ~/.ipython/profile_default/static
* ipython notebook at 8888 - source activate washmap | ./manage.py shell_plus --notebook
