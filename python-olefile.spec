%global srcname olefile
%global commit bc9d196b02e9be2d179c5b75c696a8e041232254
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global _description \
olefile is a Python package to parse, read and write Microsoft OLE2 files\
(also called Structured Storage, Compound File Binary Format or Compound\
Document File Format), such as Microsoft Office 97-2003 documents,\
vbaProject.bin in MS Office 2007+ files, Image Composer and FlashPix files,\
Outlook messages, StickyNotes, several Microscopy file formats, McAfee\
antivirus quarantine files, etc.

Name:           python-%{srcname}
Version:        0.44
Release:        0.4%{?commit:.git%shortcommit}%{?dist}
Summary:        Python package to parse, read and write Microsoft OLE2 files

License:        BSD
URL:            https://github.com/decalage2/olefile/
%if %{defined commit}
Source0:        %{url}/archive/%{commit}/%{srcname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz
%endif
# Don't install docs (they are installed through %%doc)
Patch0:         olefile_skip-doc.patch
# Remove reference to olefile2 (a pre python2.6 compatibility version)
Patch1:         olefile_no-olefile2.patch

BuildArch:      noarch


%description %{_description}


%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname} %{_description}

Python2 version.


%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %{_description}

Python3 version.


%prep
%if %{defined commit}
%autosetup -p1 -n %{srcname}-%{commit}
%else
%autosetup -p1 -n %{srcname}-%{version}
%endif

# olefile2 is a pre python2.6 compatibility version
rm -f olefile/olefile2.*
# Remove shebang from non-executable scripts
sed -i -e '1{\@^#!/usr/local/bin/python@d}' OleFileIO_PL.py
sed -i -e '1{\@^#!/usr/local/bin/python@d}' olefile/__init__.py
sed -i -e '1{\@^#!/usr/bin/env python@d}' olefile/olefile.py
# Fix incorrect line endings
sed -i -e "s/\r//" olefile/doc/*.md
sed -i -e "s/\r//" OleFileIO_PL.py


%build
%py2_build
%py3_build


%install
%py2_install
%py3_install


%check
PYTHONPATH=%{buildroot}%{python2_sitelib} %{__python2} tests/test_olefile.py
PYTHONPATH=%{buildroot}%{python3_sitelib} %{__python3} tests/test_olefile.py


%files -n python2-%{srcname}
%doc README.md olefile/doc/*
%license olefile/doc/License.*
%{python2_sitelib}/OleFileIO_PL.py*
%{python2_sitelib}/olefile-*.egg-info
%{python2_sitelib}/olefile/

%files -n python3-%{srcname}
%doc README.md olefile/doc/*
%license olefile/doc/License.*
%{python3_sitelib}/OleFileIO_PL.py*
%{python3_sitelib}/__pycache__/OleFileIO_PL.*
%{python3_sitelib}/olefile-*.egg-info
%{python3_sitelib}/olefile/


%changelog
* Mon Jan 02 2017 Sandro Mani <manisandro@gmail.com> - 0.44-0.4.gitbc9d196
- Fix incorrect line endings
- Remove shebang from non-executable scripts

* Mon Jan 02 2017 Sandro Mani <manisandro@gmail.com> - 0.44-0.3.gitbc9d196
- Further reduce duplicate text
- Add python_provides

* Mon Jan 02 2017 Sandro Mani <manisandro@gmail.com> - 0.44-0.2.gitbc9d196
- Use %%py_build and %%py_install macros
- Use %%summary, %%url to reduce duplicate text
- Add %%check
- Move BR to subpackages

* Mon Jan 02 2017 Sandro Mani <manisandro@gmail.com> - 0.44-0.1.gitbc9d196
- Initial package
