# Skytoy

Skytoy is a simple `tkinter` and `matplotlib` implemented tool for visualising and exploring astronomy `.fits` sky 
images. Of course, this can be adjusted to accept other image inputs as it uses `imshow` for the figure displays. 

Image scaling is performed using the handy-dandy `astropy.visualisation` suite.

## Installation
This uses `python_version > 3.6`

1. Create a parent git-folder and pull the git repository:
```
mkdir ~/git_clones
cd !$
git clone https://github.com/kasekun/skytoy
cd skytoy
```

I suggest creating a virtual environment for this (and all seperate tasks you perform!)

2. If you don't have `virtualenv` already
```
pip install virtualenv
```
3. create virtual environment
```
virtualenv ~/my_virtual_enviroments/skytoy
```
4. Activate this
```
source ~/my_virtual_enviroments/skytoy/bin/activate
```
5. Now install!
```
python setup.py
```
6. Enjoy!
```
python skypages.py
```
