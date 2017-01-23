%if 0%{?fedora}
%global with_python3 1
%endif

%global srcname olefile
%global _description \
olefile is a Python package to parse, read and write Microsoft OLE2 files\
(also called Structured Storage, Compound File Binary Format or Compound\
Document File Format), such as Microsoft Office 97-2003 documents,\
vbaProject.bin in MS Office 2007+ files, Image Composer and FlashPix files,\
Outlook messages, StickyNotes, several Microscopy file formats, McAfee\
antivirus quarantine files, etc.

Name:           python-%{srcname}
Version:        0.44
Release:        1%{?dist}
Summary:        Python package to parse, read and write Microsoft OLE2 files

License:        BSD
URL:            https://pypi.python.org/pypi/olefile/
Source0:        https://files.pythonhosted.org/packages/source/o/%{srcname}/%{srcname}-%{version}.zip
# Don't install docs (they are installed through %%doc)
Patch0:         olefile_skip-doc.patch

BuildArch:      noarch


%description %{_description}


%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  python2-sphinx
BuildRequires:  python-sphinx_rtd_theme
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname} %{_description}

Python2 version.


%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %{_description}

Python3 version.
%endif


%prep
%autosetup -p1 -n %{srcname}-%{version}


%build
%py2_build
## FIXME: Fix doc build on EL7
%if 0%{?rhel}
make -C doc html BUILDDIR=_build_py2
%else
make -C doc html BUILDDIR=_build_py2 SPHINXBUILD=sphinx-build-%python2_version
%endif

%if 0%{?with_python3}
%py3_build
make -C doc html BUILDDIR=_build_py3 SPHINXBUILD=sphinx-build-%python3_version
%endif


%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif


%check
# Tests got left out in the 0.44 source archive
# https://github.com/decalage2/olefile/issues/56
# PYTHONPATH=%%{buildroot}%%{python2_sitelib} %%{__python2} tests/test_olefile.py
# PYTHONPATH=%%{buildroot}%%{python3_sitelib} %%{__python3} tests/test_olefile.py


%files -n python2-%{srcname}
%doc README.md doc/_build_py2/html
%license doc/License.rst
%{python2_sitelib}/OleFileIO_PL.py*
%{python2_sitelib}/olefile-*.egg-info
%{python2_sitelib}/olefile/


%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc README.md doc/_build_py3/html
%license doc/License.rst
%{python3_sitelib}/OleFileIO_PL.py*
%{python3_sitelib}/__pycache__/OleFileIO_PL.*
%{python3_sitelib}/olefile-*.egg-info
%{python3_sitelib}/olefile/
%endif


%changelog
* Thu Jan 12 2017 Sandro Mani <manisandro@gmail.com> - 0.44-1
- Update to 0.44

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
