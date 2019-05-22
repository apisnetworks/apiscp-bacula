Backup apnscp using Bacula, host tested and approved. It's the same solution used internally with Apis Networks since 2010.

This distribution allows for 2 simultaneous backup tasks. Servers are filed under `/etc/bacula/conf.d/servers/n`  where n is 1 or 2 (or more if more than 2 parallel backups requested).

## Installation

A complimentary migration play is included as part of the RPM. After installing bacula-apnscp.rpm, run

```bash
cd /usr/local/apnscp/resources/playbooks
ansible-playbook addins/bacula/bacula-setup.yml
```



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

Edit `/etc/bacula/conf.d/database.conf`. Set these credentials.

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
