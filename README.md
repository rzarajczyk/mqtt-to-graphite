## Requirements
### Python dependencies
```shell
pip install paho-mqtt
```

## Supervisor installation:
```shell
sudo apt install supervisor
sudo cp ~/capybara/supervisor/capybara.conf /etc/supervisor/conf.d/
sudo supervisorctl reread
sudo supervisorctl update
```
