#!/bin/bash

systemctl stop assistance-bot.servie
git pull
systemctl start assistance-bot.service