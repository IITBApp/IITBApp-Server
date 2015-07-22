# IITBApp-Server

##Installation 
* Make sure you've python 2.7 installed
* Install python modules by `pip install -r requirements.txt`
* Copy `iitbapp/settings_user.py.sample` as `iitbapp/settings_user.py` and modify variables in `settings_user.py` accordingly
* Run `python manage.py migrate`
* Run `python manage.py runserver`