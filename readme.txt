# Create a new virtual environment
python -m venv .venv
# Activate a virtual environment
./.venv/Scripts/Activate.ps1 	# Windows
	#on mac: source ./.venv/bin/activate
# Update pip
python -m pip install --upgrade pip

# Install requirements 
pip install django
pip install channels
pip install pillow

# start the development Server
python manage.py runserver



## TODO:
 - Fix Logout page to actually work
 - make profile pictures actually show
 - figure out way to demo chat rooms