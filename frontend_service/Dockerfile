FROM nginx:alpine

# remove default nginx page
RUN rm -rf /usr/share/nginx/html/*

# copy HTML files (templates → root)
COPY templates/ /usr/share/nginx/html/

# copy static files
COPY static/ /usr/share/nginx/html/static/

EXPOSE 80