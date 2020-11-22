FROM debian:latest

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y imagemagick libreoffice diffutils
RUN sed -i 's/<policy domain="coder" rights="none" pattern="PDF" \/>/<policy domain="coder" rights="read \| write" pattern="PDF" \/>/g' /etc/ImageMagick-6/policy.xml