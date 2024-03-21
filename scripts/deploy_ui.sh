cd ~/dev/project/capstone/ui
git pull
npm ci
npm run build
sudo rm -rf /var/www/html
sudo mkdir /var/www/html
sudo cp build/* /var/www/html -r