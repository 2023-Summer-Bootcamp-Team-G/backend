FROM nginx:latest 

RUN apt-get update && apt-get install -y inotify-tools

COPY inotify_script.sh /usr/local/bin/inotify_script.sh
RUN chmod +x /usr/local/bin/inotify_script.sh

COPY dist/ /usr/share/nginx/html

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

CMD ["/usr/local/bin/inotify_script.sh"]
