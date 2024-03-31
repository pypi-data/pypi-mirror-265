# afxdl

Download audio from <https://aphextwin.warp.net>

## Install

```bash
pip install afxdl
```

OR:

```bash
pipx install afxdl
```

## Run

```shellsession
$ afxdl ~/Music/AphexTwin
[-] Fetching album information...
[+] Found: 'Blackbox Life Recorder 21f / in a room7 F760' (9 tracks)
[-] Downloading albums...
[+] Done!
...
[-] Fetching album information...
[+] All Finished!
```

## Help

```shellsession
$ afxdl -h
usage: afxdl [-h] [-o] [-V] [save_dir]

download audio from <aphextwin.warp.net>

positional arguments:
  save_dir         directory to save albums (default: ./AphexTwin/)

options:
  -h, --help       show this help message and exit
  -o, --overwrite  overwrite saved albums (default: False)
  -V, --version    show program's version number and exit
```
