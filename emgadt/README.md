Deployment steps on EMGADT:

Step0: install system-level dependencies if needed
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git pip virtualenv zip
```

Step1: create virtual env and install reqs into it using reset-env.sh script in the upper folder
```
../reset-env.sh
```
Step2: configure s3secrets.json
```
cp ../config/template_of_s3secret.json ~/s3secret.json
vi ~/s3secret.json
```
Step3: fine tune config.yaml in this folder if necessary
```
vi config.yaml
```
Step4: install nginx and configure adtg site using the "adtg.site-def-nginx" file 
```
sudo apt-get install nginx

sudo su -
cp adtg.site-def-nginx /etc/nginx/sites-available/adtg
cd /etc/nginx/sites-enabled
unlink default
ln -s /etc/nginx/sites-available/adtg
systemctl restart nginx
```
Step5: for testing purpose, launch and stop the ADTGenerator service using the scripts in this folder
```
./run.sh &
./stop.sh
```
Step6: configure adtg under systemctl as a service
```
sudo cp adtg.service /usr/lib/systemd/system/adtg.service
sudo systemctl daemon-reload
sudo systemctl start adtg
```
Step7: check the log
```
tail -f adtg.log
```

- 
