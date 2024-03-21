# 
cd ~/dev/project/capstone/ui
git pull
npm ci
npm run build
sudo rm -rf /var/www/html
mkdir /var/www/html
cp build/. /var/www/html