

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

With a index.html in the working directory this will make host a website at 127.0.0.1

```python
# Example for website

import frmWrk.website as frw

# Start the server on 127.0.0.1:80
website = frw.WebServer("127.0.0.1", 80, "./")
website.start()

# Close the server when we get input
input()
website.close()

```

# Documentation

```python
# Import everything

import frmWrk
import time

# Create the webserver. Directory is where the server should look for files
website = frmWrk.website.WebServer(ip, port, directory)

# Run the server
website.start()

# Wait 10 seconds and close the server
time.sleep(10)

website.close()
```


frmWrk.databases should not be used.
It Can be used but please dont use it.

