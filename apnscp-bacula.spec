%global debug_package %{nil}
%define _sourcedir %(pwd)

Summary: apnscp Bacula plugin
Name: apnscp-bacula
Version: 1.0
Release: 1%{?dist}
URL: https://github.com/apisnetworks/apnscp-bacula
Vendor: Apis Networks
License: MIT
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: bacula-director
Requires: bacula-storage
Requires: bacula-client
BuildArch: noarch

%description
apnscp is a full-stack hosting platform for the modern sites.
Bacula is a backup daemon for Linux.

%prep
rm -rf %{name}-%{version}
mkdir %{name}-%{version}
cp -rf %{_sourcedir}/{README.md,LICENSE} .
cp -rf %{_sourcedir}/{conf,plays} %{name}-%{version}/
cd %{name}-%{version}
/usr/bin/chmod -Rf a+rX,u+w,g-w,o-w .

%install
cd %{name}-%{version}
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/bacula $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig
touch $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/bacula-vars
cp -dpR conf/*  $RPM_BUILD_ROOT/etc/bacula/
rm -f $RPM_BUILD_ROOT/etc/bacula/bacula-fd.conf{,.*}
rm -f $RPM_BUILD_ROOT/etc/bacula/conf.d/servers/1/*.conf
mkdir -p $RPM_BUILD_ROOT/%{apnscp_root}/addins/%{name}
cp -dpR plays/* $RPM_BUILD_ROOT/%{apnscp_root}/addins/

%post
for f in bconsole.conf bacula-sd.conf bacula-dir.conf ; do
  OLDCONFIG=/etc/bacula/$f
  [[ -f "$OLDCONFIG" ]] && mv "$OLDCONFIG" "$OLDCONFIG.apnscp-save"
done
%run_apnscp_addin bacula-setup

%postun
[[ $1 -eq 0 ]] || exit 0
for f in bconsole.conf bacula-sd.conf bacula-dir.conf ; do
  OLDCONFIG=/etc/bacula/$f
  [[ -f "$OLDCONFIG.apnscp-save" ]] && mv "$OLDCONFIG.apnscp-save" "$OLDCONFIG"
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%attr(0600, bacula, bacula) %config(noreplace) %{_sysconfdir}/sysconfig/bacula-vars
%attr(0700, bacula, bacula) %dir %{_sysconfdir}/bacula/conf.d/

%config /etc/bacula/bacula-dir-apnscp.conf
%config /etc/bacula/bacula-sd-apnscp.conf
%config /etc/bacula/bconsole-apnscp.conf
%config /etc/bacula/query-apnscp.sql

%dir %{apnscp_root}/addins/bacula-setup
%{apnscp_root}/addins/bacula-setup/defaults/main.yml
%{apnscp_root}/addins/bacula-setup/handlers/main.yml
%{apnscp_root}/addins/bacula-setup/tasks/main.yml
%{apnscp_root}/addins/bacula-setup/tasks/setup-db.yml
%{apnscp_root}/addins/bacula-setup/tasks/setup-client.yml
%{apnscp_root}/addins/bacula-setup/templates/client-template.conf.j2

%config(noreplace) %dir %{_sysconfdir}/bacula/local.d
%config(noreplace) /etc/bacula/local.d/bacula-dir-custom.conf
%config(noreplace) /etc/bacula/local.d/bacula-sd-custom.conf
%config(noreplace) /etc/bacula/local.d/bconsole-custom.conf
%attr(0755, -, -) %config(noreplace) /etc/bacula/local.d/extra.sh

%config(noreplace) %dir %{_sysconfdir}/bacula/conf.d/servers/
/etc/bacula/conf.d/bconsole.conf
/etc/bacula/conf.d/console.conf
/etc/bacula/conf.d/database.conf
/etc/bacula/conf.d/director.conf
/etc/bacula/conf.d/fileset.conf
/etc/bacula/conf.d/job.conf
/etc/bacula/conf.d/pool.conf
/etc/bacula/conf.d/schedule.conf
/etc/bacula/conf.d/sd-director.conf
/etc/bacula/conf.d/servers/base.conf
/etc/bacula/conf.d/servers/slot-base.conf
/etc/bacula/conf.d/servers/storage.conf
%attr(0755, -, -) /etc/bacula/helpers.sh
%attr(0755, -, -) /etc/bacula/conf.d/bacula-dir.sh
%attr(0755, -, -) /etc/bacula/conf.d/bacula-sd.sh
%attr(0755, -, -) /etc/bacula/conf.d/bconsole.sh
%attr(0755, -, -) /etc/bacula/conf.d/template.sh



%changelog
#* Thu Jun 13 2019 Matt Saladna <matt@apisnetworks.com> - 1.0-1.apnscp
#- Initial release
