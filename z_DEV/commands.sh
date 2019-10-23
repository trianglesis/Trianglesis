#!/usr/bin/env bash


CREATE USER 'root'@'localhost' IDENTIFIED BY 'PASSWD';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;


## MYSQL DUMP:
mysqldump core_db > core_db_DUMP_ALL.sql -u root


## VENV

C:\Python368\Scripts\pip.exe install virtualenv
C:\Python368\Scripts\virtualenv.exe core
C:\Python368\Scripts\virtualenv.exe venv

C:\Python368>python.exe -m venv "D:\..\projects\PycharmProjects\triangle\core"
D:\..\projects\PycharmProjects\triangle\core
C:\Python368>D:\..\projects\PycharmProjects\triangle\core\Scripts\activate.bat

pip install -r "/var/www/triangle/req373.txt"
pip install -r "D:\Projects\PycharmProjects\triangle\req368.txt"