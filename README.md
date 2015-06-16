# IITBApp-Server

##Installation 
* Make sure you've python 2.7 installed
* Install python modules by `pip install -r requirements.txt`
* Copy `iitbapp/settings_user.py.sample` as `iitbapp/settings_user.py` and modify variables in `settings_user.py` accordingly
* Run `python manage.py migrate`
* Run `python manage.py runserver` 

##API Documentation
###Registration
* To check if an email is registered or not send a JSON request to `/api/registration/status` as
```
{
  "email" : "xyz@domain.com"
}
```

In response you'll get 
```
{
  "email" : "xyz@domain.com",
  "active" : false
}
```
where `active` is indicator whether this email is verified or not. If it is true then it is verified and account has been created. 

* To add new email to create account, send a JSON request to `/api/registration/add` as
```
{
  "email" : "xyz@domain.com"
}
```
This will again produce the same response as last one with `active` set to false.
