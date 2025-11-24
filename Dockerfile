FROM lscr.io/linuxserver/webtop:latest

# It seems like git and curl are not installed by default
# RUN apt-get update && apt-get install -y git curl && apt-get clean

WORKDIR /opt/cache

ENV REPO_PATH=/opt/cache/MenuPizze
ENV ENTRYPOINT_SCRIPT=/usr/local/bin/update-repo.sh

RUN git clone https://github.com/Norby99/MenuPizze "$REPO_PATH"

RUN cat << 'EOF' > $ENTRYPOINT_SCRIPT
#!/bin/sh
set -e
REPO_DIR="${REPO_PATH:-/opt/cache/MenuPizze}"

if curl -s --head --request GET https://github.com --max-time 2 >/dev/null; then
    echo ">> Internet OK. Aggiorno la repo..."
    cd "$REPO_DIR" && git pull || true
else
    echo ">> Offline. Uso la copia cache."
fi

exec /init
EOF

# Remove windows CR
RUN sed -i 's/\r$//' $ENTRYPOINT_SCRIPT
RUN chmod +x $ENTRYPOINT_SCRIPT

# Execute my script in background
#TODO
#python3 /opt/cache/MenuPizze/myscript.py &

ENTRYPOINT ["/bin/sh", "-c", "$ENTRYPOINT_SCRIPT"]
