#!/bin/bash
user="$SUDO_USER"
echo $user
if [ -d "/usr/share/worktime" ]
then
rm  /usr/share/worktime/worktime.py
else
mkdir /usr/share/worktime
fi
cp worktime/* /usr/share/worktime
chown -R "$user" /usr/share/worktime
if [ -f "/usr/bin/worktimemanager" ]
then
rm /usr/bin/worktimemanager
fi
cp worktimemanager /usr/bin
chmod a+x /usr/bin/worktimemanager
echo "Installation is finished. You can start program from terminal with command:\"worktimemanager\""
