
# Installing

Open terminal in project folder.
Run:
```bash
git clone https://github.com/Spannnn45/frmWrk frmWrk
```

Done. Look at usage for quickstart.

# Usage

```python
# Example for website

import frmWrk.website as frw

website = frw.WebServer("127.0.0.1", 80, "./")
website.start()

try:
    input()
    website.close()
except KeyboardInterrupt:
    website.close()
    print("\nServer closed")
    exit(0)

import frmWrk.website as frw

webSite = frw.WebServer()
```


