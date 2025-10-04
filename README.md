# National Day 95

### In collaboration with [Abdulahk1](https://github.com/Abdulahk1)

---
# Usage

- **install required libraries `flask` and `qrcode`**

```bash
pip install flask qrcode
```

> or install it from distro official repositories
---

- **add a qr code for your local network in `static/img/qr-wifi.png`**

- **add qr code for site in `static/img/qr-site.png`**

---
> **by default, main program (national_msgs.py) is generate qr code automatically and put it in `static/img/qr-site.png`**

> **if you want to disable it, delete/hash line 24 and line 25, this lines is use `qr_gen.py` as modlue to create `site qr code` (not wifi, site only) automatically**

> **but if you want to use it (automatically), set `IP_ADDR` value to your ip address to generate qr code automatic in `static/img/qr-site.png`**
---

> **you can create qrcode manually from `gen_qr.py` tool**

> `gen_qr.py` it's saves images in `static/manual/qrcode.png`

> `python gen_qr.py '[URL]'`

---
- **by default, app is run on device only (ip '127.0.0.1')**
- **but if you want to run it as server in local network**
- **change `IP_ADDR` variable to your ip in local network**
---

- **finally, run:**

```bash
python national_msgs.py
# or in UNIX-Based
chmod +x national_msgs.py
./national_msgs.py
```
---

> `national_msgs.py` is main program
