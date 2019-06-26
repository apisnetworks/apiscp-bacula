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
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/bacula $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig
touch $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/bacula-vars
cp -dpR conf/*  $RPM_BUILD_ROOT%{_sysconfdir}/bacula/
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/bacula/bacula-fd.conf{,.*}
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/bacula/conf.d/servers/1/*.conf
mkdir -p $RPM_BUILD_ROOT/%{apnscp_root}/resources/playbooks/addins/%{name}
cp -dpR plays/* $RPM_BUILD_ROOT/%{apnscp_root}/resources/playbooks/addins/

%post
for f in bconsole.conf bacula-sd.conf bacula-dir.conf ; do
  OLDCONFIG=%{_sysconfdir}/bacula/$f
  [[ -f "$OLDCONFIG" ]] && mv "$OLDCONFIG" "$OLDCONFIG.apnscp-save"
done
%run_apnscp_addin bacula-setup

%postun
[[ $1 -eq 0 ]] || exit 0
for f in bconsole.conf bacula-sd.conf bacula-dir.conf ; do
  OLDCONFIG=%{_sysconfdir}/bacula/$f
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

%config %{_sysconfdir}/bacula/bacula-dir-apnscp.conf
%config %{_sysconfdir}/bacula/bacula-sd-apnscp.conf
%config %{_sysconfdir}/bacula/bconsole-apnscp.conf
%config %{_sysconfdir}/bacula/query-apnscp.sql

%dir %{apnscp_root}/resources/playbooks/addins/bacula-setup
%{apnscp_root}/resources/playbooks/addins/bacula-setup/defaults/main.yml
%{apnscp_root}/resources/playbooks/addins/bacula-setup/handlers/main.yml
%{apnscp_root}/resources/playbooks/addins/bacula-setup/tasks/main.yml
%{apnscp_root}/resources/playbooks/addins/bacula-setup/tasks/setup-db.yml
%{apnscp_root}/resources/playbooks/addins/bacula-setup/tasks/setup-client.yml
%{apnscp_root}/resources/playbooks/addins/bacula-setup/templates/client-template.conf.j2

%config(noreplace) %dir %{_sysconfdir}/bacula/local.d
%config(noreplace) %{_sysconfdir}/bacula/local.d/bacula-dir-custom.conf
%config(noreplace) %{_sysconfdir}/bacula/local.d/bacula-sd-custom.conf
%config(noreplace) %{_sysconfdir}/bacula/local.d/bconsole-custom.conf
%attr(0755, -, -) %config(noreplace) %{_sysconfdir}/bacula/local.d/extra.sh

%{_sysconfdir}/bacula/conf.d/bconsole.conf
%{_sysconfdir}/bacula/conf.d/console.conf
%{_sysconfdir}/bacula/conf.d/database.conf
%{_sysconfdir}/bacula/conf.d/director.conf
%{_sysconfdir}/bacula/conf.d/fileset.conf
%{_sysconfdir}/bacula/conf.d/job.conf
%{_sysconfdir}/bacula/conf.d/pool.conf
%{_sysconfdir}/bacula/conf.d/schedule.conf
%{_sysconfdir}/bacula/conf.d/sd-director.conf
%dir %{_sysconfdir}/bacula/conf.d/servers/
%{_sysconfdir}/bacula/conf.d/servers/base.conf
%{_sysconfdir}/bacula/conf.d/servers/slot-base.conf
%{_sysconfdir}/bacula/conf.d/servers/storage.conf
%attr(0755, -, -) %{_sysconfdir}/bacula/helpers.sh
%attr(0755, -, -) %{_sysconfdir}/bacula/conf.d/bacula-dir.sh
%attr(0755, -, -) %{_sysconfdir}/bacula/conf.d/bacula-sd.sh
%attr(0755, -, -) %{_sysconfdir}/bacula/conf.d/bconsole.sh
%attr(0755, -, -) %{_sysconfdir}/bacula/conf.d/template.sh



%changelog
#* Thu Jun 13 2019 Matt Saladna <matt@apisnetworks.com> - 1.0-1.apnscp
#- Initial release
