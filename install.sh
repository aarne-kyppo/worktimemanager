#!/bin/bash
user="$SUDO_USER"
echo $user
if [ -f "/usr/share/worktime/worktime.py" ]
then
rm  /usr/share/worktime/worktime.py
mkdir /usr/share/worktime/src
elif  [ -d "/usr/share/worktime/src"]
then
rm /usr/share/worktime/src/*
else
mkdir /usr/share/worktime/src
fi
cp worktime/* /usr/share/worktime/src
chown -R "$user" /usr/share/worktime
if [ -f "/usr/bin/worktimemanager" ]
then
rm /usr/bin/worktimemanager
fi
cp worktimemanager /usr/bin
chmod a+x /usr/bin/worktimemanager
echo "Installation is finished. You can start program from terminal with command:\"worktimemanager\""
