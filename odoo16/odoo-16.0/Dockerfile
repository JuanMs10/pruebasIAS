FROM ubuntu:22.04

LABEL maintainer="IAS Software & Angel Guadarrama"

# Generate locale C.UTF-8 for postgres and general locale data
ENV LANG C.UTF-8

# Set timezone
ENV TZ=America/Bogota
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/time

# Install some deps
RUN set -x; \
        apt update \
        && apt install -y --no-install-recommends \
            ca-certificates \
            curl \
            dirmngr \
            fonts-noto-cjk build-essential \
            gnupg \
            node-less \
            python3-pip \
            python3-pyldap \
            python3-qrcode \
            python3-renderpm \
            python3-setuptools \
            python3-vobject \
            python3-watchdog \
            python3-dev \
            libffi-dev wkhtmltopdf

# Install postgresql-client-12
RUN curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt jammy-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN apt update
RUN apt -y install postgresql-client-12

# Copy local requirements
RUN pip3 install --upgrade pip
COPY ./requirements.txt /
RUN pip3 install -r /requirements.txt

# Install Odoo
ENV ODOO_VERSION 16.0
ARG ODOO_RELEASE=latest
RUN set -x; \
        curl -o odoo.deb -sSL http://nightly.odoo.com/${ODOO_VERSION}/nightly/deb/odoo_${ODOO_VERSION}.${ODOO_RELEASE}_all.deb \
        && dpkg --force-depends -i odoo.deb \
        && apt-get update \
        && apt-get -y install -f --no-install-recommends \
        && rm -rf /var/lib/apt/lists/* odoo.deb

# Copy entrypoint script and Odoo configuration file
COPY ./entrypoint.sh /
COPY ./config/odoo.conf /etc/odoo/
RUN chown odoo -Rf /etc/odoo/*

# Mount /var/lib/odoo to allow restoring filestore and /mnt/extra-addons for users addons
RUN mkdir -p /mnt/extra-addons \
        && chown -R odoo /mnt/extra-addons
VOLUME ["/var/lib/odoo", "/mnt/extra-addons"]

# Add debugpy to odoo-bin
RUN pip3 install debugpy
COPY ./debugpy.txt /
RUN cd / && cat debugpy.txt >> /usr/bin/odoo

# Expose Odoo services
EXPOSE 9006 19006 8886

# Set the default config file
ENV ODOO_RC /etc/odoo/odoo.conf

COPY wait-for-psql.py /usr/local/bin/wait-for-psql.py

# Set default user when running the container
USER odoo

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]
