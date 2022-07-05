

[Installation](#installing)

[Quickstart](#usage)

[Documentation](#documentation)

# Installing

Open terminal in project folder.
Run:
```bash
$ git clone https://github.com/Spannnn45/frmWrk frmWrk
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

```

# Documentation

```python
# Import everything

import frmWrk
import time

# Create the webserver

website.WebServer(ip, port, directory)

# Run the server

website.start()

# Wait 10 seconds

time.sleep(10)

# Close the server
website.close()
```

frmWrk.databases should not be used.

