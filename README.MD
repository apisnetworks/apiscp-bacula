Backup apnscp using Bacula, host tested and approved. It's the same solution used internally with Apis Networks since 2010.

This distribution allows for 2 simultaneous backup tasks. Servers are filed under `/etc/bacula/conf.d/servers/n`  where n is 1 or 2 (or more if more than 2 parallel backups requested). 

Bacula requires 1 server designated as the director (bacula-dir), which initiates backups and stores data on the server (bacula-sd); this path is /home/bacula. The director/storage daemon does not have to run apnscp. Skip down to [Manual installation](#Manual-installation) for free-form configration. 

Each server that is to be backed up must run a file daemon (bacula-fd). A unique password should be generated for each server and stored in *servers/n/server-name.conf* on the director. Firewall permissions must be extended to permit access by the director.

Backups can be of two types,

| FileSet      | Description                                                  |
| ------------ | ------------------------------------------------------------ |
| Client-Layer | Minimum viable backup, client data under /home/virtual/siteXX |
| Server       | All data under / and /home except for logs and FST           |




## Installation

A complimentary migration play is included as part of the RPM. After installing bacula-apnscp.rpm, run

```bash
cd /usr/local/apnscp/resources/playbooks
ansible-playbook addin.yml --extra-vars=play=bacula-setup
```
This will configure the director.


### Manual installation

```bash
yum install -y bacula-director bacula-storage bacula-console
systemctl enable bacula-sd bacula-dir
```

Link MySQL driver to baccats,

```bash
alternatives --set libbaccats.so /usr/lib64/libbaccats-mysql.so
```

Create a database to store backup metadata,

```bash
# Create database + grants
echo "CREATE DATABASE bacula; CREATE USER bacula@localhost IDENTIFIED BY 'somepassword';" | mysql
# Populate database
env db_name=bacula /usr/libexec/bacula/make_bacula_tables mysql 
```

Create a file that stores environment variables for Bacula components,

```bash
touch /etc/sysconfig/bacula-vars
chown bacula:bacula /etc/sysconfig/bacula-vars
chmod 600 /etc/sysconfig/bacula-vars
```

Edit `/etc/sysconfig/bacula-vars`. Set the following credentials:

| Variable         | Purpose                                              |
| ---------------- | ---------------------------------------------------- |
| DB_HOSTNAME      | Database hostname (usually "localhost")              |
| DB_USER          | Database username (usually "bacula")                 |
| DB_PASSWORD      | Database password as set above (do not use "bacula") |
| DB_NAME          | Database name (usually "bacula")                     |
| SD_HOSTNAME      | Storage daemon hostname (usually "localhost")        |
| SD_PASSWORD      | Storage daemon password (do not use "bacula")        |
| MONITOR_PASSWORD | Monitoring via "bat" app (do not use "bacula")       |
| DIR_PASSWORD     | Unrestricted director password (do not use "bacula") |
| CONSOLE_PASSWORD | Console password via bconsole (do not use "bacula")  |

All credentials will be automatically set for both the directory and storage daemon

Add a new machine,

Start Bacula services.

```bash
systemctl enable bacula-sd bacula-dir
```

#### Backup devices
For each device, install client + whitelist firewall.
```bash
yum install -y bacula-client
```
