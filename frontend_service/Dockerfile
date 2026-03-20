FROM nginx:alpine

# remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# clean default html
RUN rm -rf /usr/share/nginx/html/*

# copy templates (HTML files)
COPY templates/ /usr/share/nginx/html/

# copy static files
COPY static/ /usr/share/nginx/html/static/

EXPOSE 80