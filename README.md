# Arsenal

![](img/logo.png)

Arsenal is just a quick inventory, reminder and launcher for pentest commands.
<br>This project written by pentesters for pentesters simplify the use of all the hard-to-remember commands

![](img/arsenal.gif)

In arsenal you can search for a command, select one and it's prefilled directly in your terminal. This functionality is independent of the shell used. Indeed arsenal emulates real user input (with TTY arguments and IOCTL) so arsenal works with all shells and your commands will be in the history.

You have to enter arguments if needed, but arsenal supports global variables. <br>
For example, during a pentest we can set the variable `ip` to prefill all commands using an ip with the right one.

To do that you just have to enter the following command in arsenal:
```
>set ip=10.10.10.10
``` 

Authors: 
* Guillaume Muh
* mayfly

This project is inspired by navi (<https://github.com/denisidoro/navi>) because the original version was in bash and too hard to understand to add features


## Arsenal new features

![](img/arsenal_update.png)

- New colors
- Add tmux new pane support (with -t)
- Add default values in cheatsheets commands with `<argument|default_value>`
- Support description inside cheatsheets
- New categories and Tags
- New cheatsheets
- Add yml support (thx @0xswitch )
- Add fzf support with ctrl+t (thx @mgp25)
- Add prefix to commands generated (with -f)
- Add user config file (generated at first run in ~/.arsenal.conf)

## Install & Launch
- with pip :
```
python3 -m pip install arsenal-cli
```

- run (we also advice you to add this alias : `alias a='arsenal'`)
```
arsenal
```

- manually:
```
git clone https://github.com/Orange-Cyberdefense/arsenal.git
cd arsenal
python3 -m pip install -r requirements.txt
./run
```

Inside your .bashrc or .zshrc add the path to `run` to help you do that you could launch the addalias.sh script
```
./addalias.sh
```

- Also if you are an Arch user you can install from the AUR:
```bash
git clone https://aur.archlinux.org/arsenal.git
cd arsenal 
makepkg -si
```
- Or with an AUR helper like yay:
```bash
yay -S arsenal
```

## Launch in tmux mode

```
./run -t # if you launch arsenal in a tmux window with one pane, it will split the window and send the command to the otherpane without quitting arsenal
         # if the window is already split the command will be send to the other pane without quitting arsenal
./run -t -e # just like the -t mode but with direct execution in the other pane without quitting arsenal
```

## Launch new tmux mode

Previous mode was working only when only one session was running. Since libtmux does not provide a way to identify tmux session the code is running in.


This new mode will need a `pane_path` which pattern is `<session_name>:<window_name>:[<pane_id>]`

Regarding `pane_path` :
- session identified by `session_name` must exist.
- if windows identified by `window_name`: 
  - does not exist: it will be created then pane number is ignored if specified
  - exist and `pane_id`:
    - is not specified: command will be sent to all panes in the window
    - does not exist: a new pane will be created (similar to previous mode)
    - exist: guess what

Note: within tmux session `prefix-q` willdisplay panes number

```
# will send command to all pane in arsenal-windows (windows creation needed) 
./run --tmux-new tmux-pentest:arsenal-windows:

# will send command to a new pane
./run --tmux-new tmux-pentest:arsenal-windows:99

# will send command to pane 3
./run --tmux-new tmux-pentest:arsenal-windows:3
```

## Add external cheatsheets

You could add your own cheatsheets by referencing them in your `.arsenal.conf`

If in `.arsenal.conf` you set `use_builtin_cheats` to `yes` your cheats will  will be mered with cheats defined in `<arsenal_home>/data/cheats`

arsenal reads `.md` (MarkDown) and `.rst` (RestructuredText).

Cheatsheets examples are in `<arsenal_home>/cheats`: `README.md` and `README.rst`

## Add a prefix commands generated

In order to prefix commands generated by arsenal you need to set the `arsenal_prefix_cmd` global variable. 

For example if you need your commands to be prefixed with `proxychains -q`:
```
>set arsenal_prefix_cmd=proxychains -q
```

then you can start run arsenal with the prefix option:
```bash
arsenal -f
```

## Troubleshooting

If you got on error on color init try : 
```
export TERM='xterm-256color'
```

--

If you have the following exception when running Arsenal:
```
ImportError: cannot import name 'FullLoader'
```
First, check that requirements are installed:
```
pip install -r requirements.txt
```
If the exception is still there:
```
pip install -U PyYAML
```

--

If you encounter an exception similar to the following (contains TIOCSTI in strace) when running Arsenal:
```
[...]
    fcntl.ioctl(stdin, termios.TIOCSTI, c)
OSError: [Errno 5] Input/output error
```
Then you may need to re-enable TIOCSTI. Please run the following commands as root to fix this issue on the current session :
```
sysctl -w dev.tty.legacy_tiocsti=1
```
If you want this workaround to survive a reboot, add the following configuration to sysctl.conf file and reboot :
```
echo "dev.tty.legacy_tiocsti=1" >> /etc/sysctl.conf
```
More information is available in the issue [https://github.com/Orange-Cyberdefense/arsenal/issues/77](https://github.com/Orange-Cyberdefense/arsenal/issues/77)


## Mindmap
- Active directory mindmap
  - Due to csp on github when you open the svg, we moved the AD mindmap and the source to this repository : [https://github.com/Orange-Cyberdefense/ocd-mindmaps](https://github.com/Orange-Cyberdefense/ocd-mindmaps)

[https://orange-cyberdefense.github.io/ocd-mindmaps/img/pentest_ad_dark_2022_11.svg](https://orange-cyberdefense.github.io/ocd-mindmaps/img/pentest_ad_dark_2022_11.svg)

- AD mindmap black version
![](./mindmap/pentest_ad_black.png)

- Exchange Mindmap (thx to @snovvcrash)
![](./mindmap/Pentesting_MS_Exchange_Server_on_the_Perimeter.png)

- Active directory ACE mindmap
![](./mindmap/ACEs_xmind.png)

## TODO cheatsheets 

### reverse shell
- [X] msfvenom
- [X] php
- [X] python
- [X] perl
- [X] powershell
- [X] java
- [X] ruby

### whitebox analysis grep regex
- [X] php
- [X] nodejs
- [X] hash

### Tools

#### smb
- [X] enum4linux 
- [X] smbmap
- [ ] smbget     
- [X] rpcclient
- [ ] rpcinfo
- [X] nbtscan
- [X] impacket

#### kerberos & AD
- [X] impacket
- [X] bloodhound
- [X] rubeus
- [ ] powerview
- [ ] shadow credentials attack
- [ ] samaccountname attack

#### MITM
- [X] mitm6
- [X] responder

#### Unserialize
- [X] ysoserial
- [ ] ysoserial.net

### bruteforce & pass cracking
- [X] hydra
- [X] hashcat
- [X] john

#### scan
- [X] nmap
- [X] eyewitness
- [X] gowitness

#### fuzz    
- [X] gobuster
- [X] ffuf
- [X] wfuzz

#### DNS
- [X] dig
- [X] dnsrecon
- [X] dnsenum
- [X] sublist3r

#### rpc
- [ ] rpcbind

#### netbios-ssn
- [X] snmpwalk
- [X] snmp-check
- [X] onesixtyone

#### sql
- [X] sqlmap 

#### oracle
- [ ] oscanner
- [ ] sqlplus
- [ ] tnscmd10g

#### mysql
- [X] mysql

#### nfs
- [X] showmount

#### rdp
- [X] xfreerdp
- [X] rdesktop
- [ ] ncrack

#### mssql
- [X] sqsh

#### winrm
- [X] evilwinrm

#### redis
- [ ] redis-cli

#### postgres
- [X] psql
- [ ] pgdump

#### vnc
- [X] vncviewer

#### x11
- [X] xspy
- [X] xwd
- [X] xwininfo

#### ldap
- [X] ldapsearch

#### https
- [ ] sslscan

#### web 
- [ ] burp
- [X] nikto
- [ ] tplmap

#### app web
- [X] drupwn
- [X] wpscan
- [ ] nuclei
