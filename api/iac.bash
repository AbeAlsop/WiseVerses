#!/bin/bash

#Requires sudo

cd /home
mkdir www
cd www

#Clone repository
ssh-keygen -t ed25519 -C "abealsop@gmail.com"
ssh-agent -s /bin/bash
ssh-add .ssh/id_ed25519
git clone https://github.com/AbeAlsop/WiseVerses.git wiseverses/

cd /home/www/wiseverses/api/ || exit
ln -s /home/www/wiseverses ~/wiseverses

apt install python3-pip uvicorn python3.12-venv gunicorn -y
python3 -m venv wiseverses-venv
source wiseverses-venv/bin/activate
pip install -r requirements.txt

#TODO populate keys
cat << EOF > "wiseverses/api/.env"
OPENAI_API_KEY=
PINECONE_API_KEY=
LOG_FILE_PATH=/var/log/wiseverses.log
EOF

#For rapid debugging
#uvicorn webAPI:app --reload --port 80 &

cat << EOF > "gunicorn_conf.py"
bind = "0.0.0.0:8000"
workers = 4
EOF

#Started below as service
#gunicorn -k unicorn.workers.UvicornWorker -c gunicorn_conf.py webAPI:app &

#NGINX setup
apt install nginx certbot python3-certbot-nginx -y
certbot --nginx -d wiseverses.com

cat << EOF > "/etc/nginx/sites-available/wiseverses"
server {
        server_name wiseverses.com;

        location / {
                root /home/www/wiseverses;
                index index.html;
        }
        location /api/ {
                proxy_pass http://127.0.0.1:8000;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
        }
}

server {
        listen 80;
        server_name wiseverses.com;
}
EOF

ln -s /etc/nginx/sites-available/wiseverses /etc/nginx/sites-enabled/
systemctl restart nginx

cat << EOF > "/etc/systemd/system/wiseverses.service"
[Unit]
Description=WiseVerses FastAPI web service
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/home/www/wiseverses/api
ExecStart=/home/www/wiseverses/api/wiseverses-venv/bin/gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn_conf.py webAPI:app

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable wiseverses
systemctl start wiseverses


