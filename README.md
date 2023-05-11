# DetectDefaceWeb


nano docker-detect-deface-web.yml
version: "3.5"
services:

  flask:
    #change to mongo dung chung
    image: mrlam2605/detect-deface-web
    user: root
    container_name: flask_app_detect_deface_web
    restart: unless-stopped
    environment:
      MONGODB_USERNAME: root
      MONGODB_PASSWORD: abc123-
      MONGODB_HOSTNAME: 192.168.10.50
      API_URL: http://192.168.10.50:4000/notification/add
    ports:
        - "9080:8080"
        - "9088:8088"
    #depends_on:
    #  - mongodb
    networks:
      - app-network
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - /etc/timezone:/etc/timezone:ro
      - ./Alert:/opt/In0ri/Alert

networks:
  app-network:
    driver: bridge



git clone https://github.com/nguyentienlamhp/DetectDefaceWeb
    docker-compose -f docker-detect-deface-web.yml down
    cd DetectDefaceWeb
    ls
    docker image ls
    docker image rm e51d2e19b679
    docker build -t mrlam2605/detect-deface-web .
    cd .. && docker-compose -f docker-detect-deface-web.yml up -d
    docker exec -it flask_app_detect_deface_web bash
    docker logs flask_app_detect_deface_web -f
    docker exec -it flask_app_detect_deface_web bash
