Name:           imperva-backup
Version:        v0.1
Release:        1%{?dist}
Summary:        Imperva Backup Script and Systemd Service
Vendor:         Zachary Kennedy

License:        GPLv2
URL:            https://github.com/grimsbygeek/imperva_backup
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

%description
This package installs the Imperva backup script and sets up a systemd service to run it daily.

%prep
%setup -q

%install
mkdir -p %{buildroot}/usr/local/bin
cp -a usr/local/bin/imperva_backup.py %{buildroot}/usr/local/bin/

mkdir -p %{buildroot}/etc/systemd/system
cp -a etc/systemd/system/imperva_backup.service %{buildroot}/etc/systemd/system/
cp -a etc/systemd/system/imperva_backup.timer %{buildroot}/etc/systemd/system/

%files
/usr/local/bin/imperva_backup.py
/etc/systemd/system/imperva_backup.service
/etc/systemd/system/imperva_backup.timer

%post
systemctl daemon-reload
systemctl enable imperva_backup.timer
systemctl start imperva_backup.timer

%preun
if [ $1 -eq 0 ]; then
    systemctl stop imperva_backup.timer
    systemctl disable imperva_backup.timer
fi

%postun
systemctl daemon-reload
