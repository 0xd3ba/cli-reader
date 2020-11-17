# cliReader

![banner_clireader.png](https://github.com/0xd3ba/cli-reader/blob/main/img/banner.png?raw=true)

An interactive reader for reading light novels online, right from the *terminal* !<br/>
**Note**: This is not a downloader, crawlers for downloading already exist; 
For example, [lightnovel-crawler](https://github.com/dipu-bd/lightnovel-crawler).


### Websites Supported
The following websites are currently supported (with their corresponding IDs that's used in the reader):

| ID   |      Website      |
|----------|:-------------|
| `wuxiaworld` |  https://www.wuxiaworld.com |
| `lnworld` |    https://www.lightnovelworld.com  |

(Support for other websites will be added in future)

### Commands List
The reader comes with a minimal set of easy to remember (and use) commands that you
can use to interact with the in-built shell for searching novels, reading...etc.

| Command   |      Description      |
|----------|:-------------|
| `help` |  Displays the description and usage of a command |
| `listwebs` |    Lists the websites that are currently supported by the reader |
| `read` |   Read the given novel from the specified chapter (default is `Chapter 1`)  |
| `settheme` | Set the theme of the reader (Lists all the themes if no theme is specified)     |
| `setweb` | Switch to another website with the given website ID  |
| `search` | Searches for novel in the corresponding website and lists the search results    |
| `quit` | Quits the application    |
<br/>

## Installation Instructions

Make sure you have `Python3 (v3.7+)` installed on your system. If not installed, it will
not work.

#### 1. (Optional) Setting up a virtual environment - Highly recommended
- Make sure Python's virtual environment module is installed. If not, install it using `pip3` or `pip`
depending on your system:
```
$ pip3 install virtualenv
```
Alternatively, on Linux-based systems you can do
```
$ sudo apt install python3-venv
```
- Once installed, change to a directory where you'll like the virtual environment to be created.
Then create the virtual environment using `python3` or `python` and then activate it
```
$ python3 -m venv clireader_venv        # You can use any other name for this
$ source clireader_venv/bin/activate    # Activate the virtual environment
(clireader_venv) $ ...                  # Now activated
```

#### 2. Installing the dependencies
- Clone the repository and change to the repository's root directory
```
(clireader_venv) $ git clone https://github.com/0xd3ba/cli-reader
(clireader_venv) $ cd cli-reader
```

- Install the dependencies (a small and minimal set) by using `pip3` or `pip` (virtual environment is highly
recommended for this, or else this step may mess things up)
```
(clireader_venv) $ pip3 install -r requirement.txt
```

#### 3. Starting the application
- Once all the steps above are completed, you can start the application by simply doing
```
(clireader_venv) $ python3 clireader.py
```
<br/>

## Contributors
- [`0xd3ba`](https://github.com/0xd3ba) (Debasish Das)
- [`dasarnab`](https://github.com/dasarnab) (Arnab Das)
- [`dreedxerniitb`](https://github.com/dreedxerniitb) (Harsh Raj)
- [`imsagartyagi`](https://github.com/imsagartyagi) (Sagar Tyagi)

<br/>

## Disclaimer
This was written as a course project for `CS699: Software Lab` @IIT-Bombay, solely for the sake of educational purposes. 
Under any circumstances, we are not responsible for any consequences
(not like there's any, but still) that you might face due to using this.
