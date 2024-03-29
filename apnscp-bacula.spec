%global debug_package %{nil}
%define _sourcedir %(pwd)

Summary: apnscp Bacula plugin
Name: apnscp-bacula
Version: 1.0
Release: 9%{?dist}
URL: https://github.com/apisnetworks/apnscp-bacula
Vendor: Apis Networks
License: MIT
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: bacula-director
Requires: bacula-storage
Requires: bacula-client
Requires: bacula-console
Requires: mailx
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
%{apnscp_root}/resources/playbooks/addins/bacula-setup/files/mysql-tables
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
%ghost %{_sysconfdir}/my.cnf.d/bacula.conf


%changelog
* Thu Jan 04 2024 Matt Saladna <matt@apisnetworks.com> - 1.0-9.apnscp
- Quiet locale errors on non-US systems

* Thu Jan 07 2021 Matt Saladna <matt@apisnetworks.com> - 1.0-8.apnscp
- Additional backup locations

* Sun Jan 03 2021 Matt Saladna <matt@apisnetworks.com> - 1.0-7.apnscp
- MariaDB 10.5 compatibility

* Sun Dec 20 2020 Matt Saladna <matt@apisnetworks.com> - 1.0-6.apnscp
- Raise concurrent director jobs to 4
- Set maximal Full pool retention to ensure jobs are proprerly expired from catalog

* Thu Sep 10 2020 Matt Saladna <matt@apisnetworks.com> - 1.0-5.apnscp
- Regex error

* Sun Sep 06 2020 Matt Saladna <matt@apisnetworks.com> - 1.0-4.apnscp
- Reset max_join_size to system default

* Wed Jul 24 2019 Matt Saladna <matt@apisnetworks.com> - 1.0-3.apnscp
- Switch bsmtp with mailx, add deps

* Wed Jul 10 2019 Matt Saladna <matt@apisnetworks.com> - 1.0-2.apnscp
- Ignore /home/bacula from Server profile
- Default FileSet Client-Layer

* Wed Jun 26 2019 Matt Saladna <matt@apisnetworks.com> - 1.0-1.apnscp
- Initial release
