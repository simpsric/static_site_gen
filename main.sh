python3 src/main.py
if [ $? -eq 0 ]; then
    cd public && python3 -m http.server 8888
fi