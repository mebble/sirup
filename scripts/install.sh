# Resources:
# https://unix.stackexchange.com/questions/8656/usr-bin-vs-usr-local-bin-on-linux

APP_PATH="$HOME/.local/share/sirup/"
EXE_PATH="$HOME/.local/bin/sirup"

echo "Downloading sirup"
if [ ! -d $APP_PATH ]
then
    mkdir -p $APP_PATH
    git clone https://github.com/mebble/sirup.git $APP_PATH
    ln -s "$APP_PATH/sirup" $EXE_PATH
else
    cd $APP_PATH
    git pull --rebase
fi

cat <<EOF
Successfully installed!
For usage instructions, run:
sirup help
EOF
