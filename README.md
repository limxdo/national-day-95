# National Day 95

### In collaboration with [Abdulahk1](https://github.com/Abdulahk1)

# Usage

- **install required libraries `flask` and `qrcode`**

```bash
pip install flask qrcode
```

> or install it from distro official repositories

- **add a qr code for your local network in `static/img/qr-wifi.png`**

- **add qr code for site in `static/img/qr-site.png`**

> **you can create qrcode from `gen_qr.py` tool**

> `gen_qr.py` it's saves images in `static/manual/qrcode.png`

> `python gen_qr.py '[URL]'`

- **you must set your ip in `IP_ADDR` varible or set ip manual from flask**

- **by default, app is run on device (ip '127.0.0.1')**

- **but if you want to run it as server in local network**

- **change 'IP_ADDR' variable to your ip in local network**

- **finally, run:**

```bash
python national_msgs.py
# or in UNIX-Based
chmod +x national_msgs.py
./national_msgs.py
```

> `national_msgs.py` is main program
