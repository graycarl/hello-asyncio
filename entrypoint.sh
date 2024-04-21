#!/bin/bash

# Run all the python script in the /app folder which with the filename starts with number.

for file in /app/[0-9][0-9]*.py; do
    python3 $file &
    port="80$(basename $file | cut -c 1-2)"
    # write nginx location block for each python script
cat << EOF > /etc/nginx/snippets/perf-$(basename $file | cut -c 1-2)
location /$(basename $file | cut -c 1-2) {
    proxy_pass http://127.0.0.1:$port;
}
EOF
done
cat <<EOF > /etc/nginx/sites-enabled/default
server {
    listen 80;
    include /etc/nginx/snippets/perf-*;
}
EOF

# Start nginx
exec nginx -g 'daemon off;'
