shitcoin_market
===============

Here to serve all your shitcoin needs.

1. Install postgresql server
On Ubuntu
$ sudo apt-get install python-psycopg2
$ sudo apt-get install libpq-dev
$ sudo apt-get install postgresql postgresql-contrib
$ sudo su - postgres
$ psql
(in postgres shell as postgres role)
CREATE ROLE halfdan;
ALTER ROLE halfdan WITH SUPERUSER;
(in postgres as halfdan role)
CREATE DATABASE shitcoin_dev;

2. Install redis server
$ sudo apt-get install redis-server

3. Install Python packages
===============
A) Create virtualenv and activate
B) $ pip install -r requirements.txt

