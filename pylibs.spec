#
# spec file for pylibs
#

Name:           pylibs
Version:        0.2
Release:        1%{?dist}
Url:            https://asgardahost.ru
Summary:        A package that provides a set of simple auxiliary libs written in Python 3. 
License:        GPL
Group:          Misc

BuildArch:      noarch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-XXXXXX)

Provides:       AnsibleInventoryFormat.py,DatabaseConnector.py,ExecExternal.py,Gitlab.py,GPGBackend.py
Requires:       python3,python3-pymysql,python3-requests
Prefix:		/opt/pylibs

%description
This package provides a set of simple auxiliary libs written in Python 3.

%prep
%if %{get_src_method} == "git_clone"
    rm -fr %{builddir}
    mkdir %{builddir}
    cd %{builddir}
    git clone %{source_url} %{name}
    cd %{name}
    git checkout %{branch_or_tag}
%else
    rm -fr %{builddir}
    mkdir %{builddir}
    cd %{builddir}
    curl -o archive.tar.gz -K %{config_file} "%{source_url}/archive.tar.gz?sha=%{branch_or_tag}"
    tar -xvzf archive.tar.gz
    rm -f archive.tar.gz
    SRC_DIR=`ls`
    mv ${SRC_DIR} %{name}
    cd %{name}
%endif

%build

%install
# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

cd %{builddir}/pylibs
mkdir -p ${RPM_BUILD_ROOT}/%{prefix}

mkdir ${RPM_BUILD_ROOT}/%{prefix}/ansible
mkdir ${RPM_BUILD_ROOT}/%{prefix}/databases
mkdir ${RPM_BUILD_ROOT}/%{prefix}/execexternal
mkdir ${RPM_BUILD_ROOT}/%{prefix}/gitlab
mkdir ${RPM_BUILD_ROOT}/%{prefix}/ownvault

install -m 700 src/ansible/AnsibleInventoryFormat.py ${RPM_BUILD_ROOT}/%{prefix}/ansible/AnsibleInventoryFormat.py
install -m 700 src/databases/DatabaseConnector.py ${RPM_BUILD_ROOT}/%{prefix}/databases/DatabaseConnector.py
install -m 700 src/execexternal/ExecExternal.py ${RPM_BUILD_ROOT}/%{prefix}/execexternal/ExecExternal.py
install -m 700 src/gitlab/Gitlab.py ${RPM_BUILD_ROOT}/%{prefix}/gitlab/Gitlab.py
install -m 700 src/ownvault/GPGBackend.py ${RPM_BUILD_ROOT}/%{prefix}/ownvault/GPGBackend.py

%files
%defattr(700,gitlab-runner,gitlab-runner,700)
%{prefix}/ansible/AnsibleInventoryFormat.py
%{prefix}/databases/DatabaseConnector.py
%{prefix}/execexternal/ExecExternal.py
%{prefix}/gitlab/Gitlab.py
%{prefix}/ownvault/GPGBackend.py

%post

%clean
rm -fr ${RPM_BUILD_ROOT}
rm -fr %{builddir}

%changelog
* Tue Jul 27 2021 Roman A. Chukov <r.chukov@asgardahost.ru>
- Adding object that stores gitlab project metadata received via Gitlab API v4
- Adding some reorganization of the project structure

* Thu Jul 15 2021 Roman A. Chukov <r.chukov@asgardahost.ru>
- An initial version 0.1

