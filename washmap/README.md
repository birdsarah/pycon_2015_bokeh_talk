### Using conda and pip for dependencies

(because conda doesn't have them all)

```bash
$ conda create -n washmap_bokeh python=2.7
$ source activate washmap_bokeh
$ conda install --file conda-requirements.txt
$ pip install -r requirements.txt
```
