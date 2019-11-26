printf 'TELEGRAM_TOKEN="724002242:AAE26Jn1Mx5Wmp95XcJGzqzrebKZJHCSs1o"\nTELEGRAM_CHAT="263617055"' > ~/.telegram.sh && \
sudo wget https://raw.githubusercontent.com/fabianonline/telegram.sh/master/telegram -O /usr/local/bin/telegram && \
sudo chmod 777 /usr/local/bin/telegram && \
telegram "Added $(whoami)@$(hostname) client succesfully"
