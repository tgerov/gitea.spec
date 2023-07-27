%global debug_package %{nil}

Name:           gitea
Version:        1.20.1
Release:        1%{?dist}
Summary:        Gitea is a painless self-hosted Git service.

License:        MIT
URL:            https://gitea.io
Source0:        https://github.com/go-gitea/gitea/archive/refs/tags/v%{version}.tar.gz
Source1:        gitea.service

BuildRequires:  golang
BuildRequires:  nodejs >= 16.0.0
BuildRequires:  npm
BuildRequires:  make
BuildRequires:  git
BuildRequires:  systemd-units
BuildRequires:  pam-devel

Requires:       git

%description
Gitea is a painless self-hosted Git service. It is similar to GitHub, Bitbucket, and GitLab. 

%prep
%autosetup


%build
%undefine _auto_set_build_flags
export TAGS="bindata sqlite sqlite_unlock_notify pam"
make

%install
install -d -p %{buildroot}%{_bindir}
install -d -p %{buildroot}%{_unitdir}
install -d -m 0770 %{buildroot}%{_sharedstatedir}/%{name}
install -d -m 0770 %{buildroot}%{_sysconfdir}/%{name}
install -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -m 640 custom/conf/app.example.ini %{buildroot}%{_sysconfdir}/%{name}/app.ini
install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /bin/bash \
    -c "Gitea Service Account" %{name}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%{_bindir}/%{name}
%dir %attr(0750,gitea,gitea) %{_sharedstatedir}/%{name}
%dir %attr(0750,gitea,gitea) %{_sysconfdir}/%{name}
%config(noreplace) %attr(0640,gitea,gitea) %{_sysconfdir}/%{name}/app.ini
%{_unitdir}/%{name}.service
%license LICENSE

%changelog
* Thu Jul 27 2023 Tsvetan Gerov <tsvetan@gerov.eu> 1.20.1-1
- Bump version to 1.20.1
* Thu Sep 29 2022 Tsvetan Gerov <tsvetan@gerov.eu> 1.17.2-1
- Bump version to 1.17.2
* Sat Jul 16 2022 Tsvetan Gerov <tsvetan@gerov.eu> 1.16.9-1
- Bump version to 1.16.9
* Thu Jul 14 2022 Tsvetan Gerov <tsvetan@gerov.eu> 1.16.8-2
- Bugfix: Set gitea local user shell to bash
* Thu Jul 14 2022 Tsvetan Gerov <tsvetan@gerov.eu> 1.16.8-1
- Initial Build
 
