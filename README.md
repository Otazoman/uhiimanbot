# UhiimanBot  
Obtain RSS feeds and post to each social networking site with labels  

# Technologies Used  
python3.11.5  
ubuntu22.04LTS  
mongo6.0  

# Introduction Method  
## pyenv  update
```
$ git config --global url."https://".insteadOf git://
$ pyenv update
$ pyenv install $(pyenv install -l | grep -v '[a-zA-Z]' | grep -e '\s3\.?*' | tail -1)
```

##  app install
```
$ cd path
$ git clone https://github.com/Otazoman/uhiimanbot_dev.git appname  
$ cd appname
$ pyenv local 3.11.5
$ pip install psycopg2-binary
$ pip install -r requirements.txt

※Tips if pip error occured
$ sudo ln -s /usr/lib/x86_64-linux-gnu/libffi.so.8 /usr/lib/x86_64-linux-gnu/libffi.so.7
```

## mongoDB Install
```
// Delete old version
$ sudo systemctl disable mongod
$ sudo systemctl stop mongod
$ sudo apt purge mongodb-org*
$ sudo rm -r /var/log/mongodb
$ sudo rm -r /var/lib/mongodb

// Install New Version
$ sudo apt update
$ sudo apt -y install wget gnupg software-properties-common ca-certificates lsb-release
# sudo su
# wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | gpg --dearmor -o /etc/apt/trusted.gpg.d/mongodb-6.gpg
# echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list
# exit
$ sudo apt update
$ sudo apt install -y mongodb-org
$ sudo systemctl enable mongod
$ sudo systemctl start mongod

//Adminuser create
$ mongosh
test> use admin
switched to db admin
admin> db.createUser({
 user: "youradminname",
 pwd: "ypurpassword",
 roles: [
  {
   role: "userAdminAnyDatabase",
   db: "admin"
  },
 ]
});
> db.auth("youradminname", "yourpassword")

$ sudo vi /etc/mongod.conf
------------------------
#security:
security:
  authorization: enabled
------------------------

// APP database user create
$ sudo systemctl restart mongod
$ mongosh
> use yourdbname
> db.createUser({
  user: "yourusername",
  pwd: "yourpassword",
  roles: [
   { role: "userAdmin", db: "yourcollection" },
   { role: "dbAdmin", db: "yourcollection" },
   { role: "readWrite", db: "yourcollection" }
  ]
 }
);
```  

# Crontab sample
```  
00 * * * * cd /path/appname && /yourpath/.pyenv/shims/python /path/appname/app.py
```  
# Overall test code execution
```  
$ cd /path/appname/tests/
$ ./after_operate.sh --run-tests
```  

# How to start the application  
```  
$ cd /path/appname/
$ python app.py
```  
