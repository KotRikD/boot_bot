WOL Boot Bot
---
I just had to wake up my computer...</br>
Docker container: `docker.io/kotrik0/boot_bot`

# Environment values
Just check .env.example :/

# Example running
```bash
cp .env.example .env
sudo docker pull docker.io/kotrik0/boot_bot
sudo docker run --rm --network host --env-file .env docker.io/kotrik0/boot_bot
```
or `docker-compose` file
```yaml
version: '3.3'
services:
    boot_bot:
        network_mode: host
        image: docker.io/kotrik0/boot_bot
        env_file:
            - .env
```