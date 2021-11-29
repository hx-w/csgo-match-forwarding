sudo docker-compose down
sudo docker image rm csgo-match-forwarding_match-nonebot
sudo docker-compose up -d
sudo docker logs -f match-gocq
