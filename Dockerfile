FROM tensorflow/tensorflow

LABEL maintainer="Nguyen Tien Lam <nguyentienlam@mitc.vn>"

ENV GECKODRIVER_VER v0.29.0

RUN apt-get -y update
RUN apt install nano
RUN python3 -m pip install --upgrade pip
RUN apt install -y \
    cron \
    python3-requests \
    python3-flask \
    firefox \
    && pip install uuid \
    && pip install markupsafe==2.0.1 \
    && pip install werkzeug==2.0.3 \
    && pip install selenium \
    && pip install webdriver-manager \
    && pip install Pillow \
    && pip install python-telegram-bot \
    && pip install requests \
    && pip install flask \  
    && pip install pymongo \
    && pip install python-crontab \
    && pip install pyOpenSSL

# Add geckodriver
RUN set -x \
    && curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
    && tar zxf geckodriver-*.tar.gz \
    && mv geckodriver /usr/bin/ \
    && rm geckodriver-*.tar.gz  

COPY . /opt/In0ri
ADD start.sh /start.sh
RUN chmod 755 /start.sh
EXPOSE 8080 8088
WORKDIR /opt/In0ri/FlaskApp
CMD ["/start.sh"]
