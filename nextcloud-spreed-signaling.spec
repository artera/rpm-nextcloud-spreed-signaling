%define _sysusersdir %{_prefix}/lib/sysusers.d

Name:          nextcloud-spreed-signaling
Version:       0.5.0
Release:       1%{?dist}
Summary:       Standalone signaling server for Nextcloud Talk
License:       GPLv2+
URL:           https://github.com/strukturag/nextcloud-spreed-signaling
Source0:       https://github.com/strukturag/nextcloud-spreed-signaling/releases/download/v%{version}/%{name}-v%{version}.tar.gz
Source1:       signaling.user
BuildRequires: git
BuildRequires: golang
BuildRequires: make
BuildRequires: systemd-rpm-macros

%description
Standalone signaling server for Nextcloud Talk.

%prep
export GOFLAGS="-buildmode=pie -trimpath -ldflags=-linkmode=external -mod=readonly -modcacherw"
%autosetup -n %{name}-v%{version} -p1
%make_build build
# %make_build client

%install
# install -Dm0755 bin/client %{buildroot}%{_bindir}/signaling-client
install -Dm0755 bin/signaling %{buildroot}%{_bindir}/signaling
install -Dm0755 bin/proxy %{buildroot}%{_bindir}/signaling-proxy
install -Dm0644 server.conf.in %{buildroot}%{_sysconfdir}/signaling/server.conf
install -Dm0644 proxy.conf.in %{buildroot}%{_sysconfdir}/signaling/proxy.conf
install -Dm0644 dist/init/systemd/signaling.service %{buildroot}%{_unitdir}/signaling.service
install -Dm0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/signaling.conf

%files
%{_bindir}/signaling*
%{_unitdir}/*.service
%{_sysusersdir}/*.conf
%config(noreplace) %{_sysconfdir}/signaling/*.conf

%post
/usr/bin/systemd-sysusers signaling.conf
%systemd_post signaling.service

%preun
%systemd_preun signaling.service

%postun
%systemd_postun_with_restart signaling.service

%changelog
