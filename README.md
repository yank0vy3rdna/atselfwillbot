# atselfwillbot
Telegram bot filling at self will expulsion from ITMO University application @atselfwillbot
## dependencies
- telebot
- texliveonfly with all texlive to compile atselfwill.tex
## hosting
Hosted with Ubuntu 18 VDS and supervisord
/etc/supervisor/conf.d/atselfwill.conf
```
[program:atselfwill]
command=atselfwillbotdirectorypath/wd.sh
autostart=true
autorestart=true
stderr_logfile=/var/log/atselfwill.err.log
directory=atselfwillbotdirectorypath
user=username
environment=HOME=homepath
```
