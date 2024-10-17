
%define plugin	webvideo
%define name	vdr-plugin-%plugin
%define version	0.3.2
%define rel	5

%define major	0
%define libname	%mklibname webvi %{major}
%define devname %mklibname webvi -d

Summary:	VDR plugin: Download video files from the web
Name:		%name
Version:	%version
Release:	%mkrel %rel
Group:		Video
License:	GPLv3+
URL:		https://users.tkk.fi/~aajanki/vdr/webvideo/
Source:		http://users.tkk.fi/~aajanki/vdr/webvideo/vdr-%plugin-%version.tgz
Patch0:		webvideo-lib64.patch
Patch1:		webvideo-ldflags.patch
# remove stuff that is already handled by us from Makefile:
Patch2:		webvideo-makefile-skip.patch
Patch3:		webvideo-sysconfdir.patch
Patch4:		webvideo-no-ldconfig.patch
Patch5:		webvideo-default-template-path.patch
BuildRequires:	vdr-devel >= 1.6.0-7
BuildRequires:	libxml2-devel
BuildRequires:	python-devel
Requires:	vdr-abi = %vdr_abi

%description
Webvideo plugin is a tool for browsing and downloading videos from
popular video sharing websites, such as YouTube and Google video,
using VDR menu interface or a command line client. With the help of
xineliboutput plugin the videos can be played directly without
downloading them first. Mplayer plugin is also supported.

This package is the VDR plugin. A standalone command line client is
available in package webvi.

%package -n python-webvi
Summary:	Python module for web video download and playback
Group:		System/Libraries
Requires:	python-curl
Requires:	python-libxslt
Requires:	python-libxml2
Requires:	python-mimms
Suggests:	rtmpdump
Suggests:	rtmpdump-yle
Obsoletes:	webvid < 0.3.2
%py_requires

%description -n python-webvi
webvi is a tool for downloading and playing videos from popular video
sharing webvites such as YouTube.

This package contains the python module.

%package -n %libname
Summary:	Shared library for using webvi
Group:		System/Libraries
Requires:	python-webvi >= %{version}

%description -n %{libname}
webvi is a tool for downloading and playing videos from popular video
sharing webvites such as YouTube.

This package contains the C library for using the webvi python
module.

%package -n %devname
Summary:	Development files for webvi C bindings
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	webvi-devel = %{version}-%{release}

%description -n %{devname}
webvi is a tool for downloading and playing videos from popular video
sharing webvites such as YouTube.

This package contains the C bindings for the webvi python module.

%package -n webvi
Summary:	Command line web video downloader
Group:		Video
Requires:	python-libxml2
Requires:	python-webvi >= %{version}
%py_requires

%description -n webvi
webvi is a command line tool for downloading video and audio files
from certain media sharing websites, such as YouTube or Google Video.

%prep
%setup -q -n %plugin-%version
%autopatch -p1
cd src/vdr-plugin
%vdr_plugin_prep
%vdr_plugin_params_begin %plugin
# save downloaded files to dir
var=DOWNLOAD_DIR
param="-d DOWNLOAD_DIR"
# read video site templates from DIR instead of default
var=TEMPLATE_DIR
param="-t TEMPLATE_DIR"
# read another config file instead of default
var=CONFIG_FILE
param="-c CONFIG_FILE"
# execute a command after downloading a file
var=POSTPROCESS_CMD
param="-p POSTPROCESS_CMD"
%vdr_plugin_params_end

%build
%make CXXFLAGS="%{optflags}" CFLAGS="%{optflags}" LDFLAGS="%{ldflags}" PREFIX="%{_prefix}"
cd src/vdr-plugin
%vdr_plugin_build 

%install
python setup.py install --root=%{buildroot}
%make install \
	VDRPLUGINCONFDIR=%{buildroot}%{vdr_plugin_cfgdir} \
	PREFIX=%{buildroot}%{_prefix} \
	SYSCONFDIR="%{buildroot}%{_sysconfdir}" \
	LIBDIR="%{buildroot}%{_libdir}"

install -d -m755 %{buildroot}%{_includedir}
install -m644 src/libwebvi/libwebvi.h %{buildroot}%{_includedir}

cd src/vdr-plugin
%vdr_plugin_install

%files -f src/vdr-plugin/%plugin.vdr
%defattr(-,root,root)
%doc README README.vdrplugin HISTORY TODO
%dir %{vdr_plugin_cfgdir}/%plugin
%config(noreplace) %{vdr_plugin_cfgdir}/%plugin/mime.types
%config(noreplace) %{vdr_plugin_cfgdir}/%plugin/webvi.plugin.conf

%files -n python-webvi
%defattr(-,root,root)
%{python_sitelib}/webvi
%{python_sitelib}/libwebvi-*.egg-info
%{_datadir}/webvi

%files -n %libname
%defattr(-,root,root)
%{_libdir}/libwebvi.so.%{major}*

%files -n %devname
%defattr(-,root,root)
%doc README TODO HISTORY doc/developers.txt
%{_includedir}/libwebvi.h
%{_libdir}/libwebvi.so

%files -n webvi
%defattr(-,root,root)
%doc README README.webvi TODO HISTORY
%{_sysconfdir}/webvi.conf
%{_bindir}/webvi
%{python_sitelib}/webvicli



%changelog
* Sat Nov 06 2010 Funda Wang <fwang@mandriva.org> 0.3.2-3mdv2011.0
+ Revision: 594033
- rebuld for py2.7

* Tue Nov 02 2010 Michael Scherer <misc@mandriva.org> 0.3.2-2mdv2011.0
+ Revision: 592365
- rebuild for python 2.7

* Sat Sep 04 2010 Anssi Hannula <anssi@mandriva.org> 0.3.2-1mdv2011.0
+ Revision: 575894
- new version
- drop webvid subpackage, no daemon is needed anymore
- add makefile patches:
  o fix libdir on lib64 (lib64.patch)
  o use ldflags (ldflags.patch)
  o skip manually installed files (makefile-skip.patch)
  o use proper sysconfdir (sysconfdir.patch)
  o do not run ldconfig (no-ldconfig.patch)
- fix default template path for our prefix (default-template-path.patch)
- add python-webvi package for the new main python module that replaces
  webvid
- add libwebvi0 and libwebvi-devel for the C bindings
- update vdr plugin sysconfig file to match current options
- remove now unneeded extra plugin flags

* Sun Sep 27 2009 Anssi Hannula <anssi@mandriva.org> 0.1.6-1mdv2011.0
+ Revision: 449955
- new version
- drop gcc4.4.patch, applied upstream

* Tue Jul 28 2009 Anssi Hannula <anssi@mandriva.org> 0.1.5-2mdv2010.0
+ Revision: 401088
- rebuild for new VDR
- adapt for vdr compilation flags handling changes, bump buildrequires

* Wed Jul 15 2009 Anssi Hannula <anssi@mandriva.org> 0.1.5-1mdv2010.0
+ Revision: 396169
- new version
- update sysconfig file
- fix build with gcc4.4 (gcc4.4.patch)

* Fri Mar 20 2009 Anssi Hannula <anssi@mandriva.org> 0.1.2-2mdv2009.1
+ Revision: 359385
- rebuild for new vdr

* Sat Mar 07 2009 Anssi Hannula <anssi@mandriva.org> 0.1.2-1mdv2009.1
+ Revision: 352557
- initial Mandriva release

