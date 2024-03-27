# Use the official Apache image as the base image
FROM httpd:latest

# Install mod_wsgi module
RUN apt-get update \
    && apt-get install -y libapache2-mod-wsgi-py3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy your custom Apache configuration file into the container
COPY config.conf /usr/local/apache2/conf/httpd.conf

# Specify the command to start Apache when the container starts
CMD ["httpd-foreground"]
