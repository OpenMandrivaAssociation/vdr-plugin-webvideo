
%define plugin	webvideo
%define name	vdr-plugin-%plugin
%define version	0.3.2
%define rel	1

%define major	0
%define libname	%mklibname webvi %{major}
%define devname %mklibname webvi -d

Summary:	VDR plugin: Download video files from the web
Name:		%name
Version:	%version
Release:	%mkrel %rel
Group:		Video
License:	GPLv3+
URL:		http://users.tkk.fi/~aajanki/vdr/webvideo/
Source:		http://users.tkk.fi/~aajanki/vdr/webvideo/vdr-%plugin-%version.tgz
Patch0:		webvideo-lib64.patch
Patch1:		webvideo-ldflags.patch
# remove stuff that is already handled by us from Makefile:
Patch2:		webvideo-makefile-skip.patch
Patch3:		webvideo-sysconfdir.patch
Patch4:		webvideo-no-ldconfig.patch
Patch5:		webvideo-default-template-path.patch
BuildRoot:	%{_tmppath}/%{name}-buildroot
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
%apply_patches
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
rm -rf %{buildroot}
python setup.py install --root=%{buildroot}
%make install \
	VDRPLUGINCONFDIR=%{buildroot}%{_vdr_plugin_cfgdir} \
	PREFIX=%{buildroot}%{_prefix} \
	SYSCONFDIR="%{buildroot}%{_sysconfdir}" \
	LIBDIR="%{buildroot}%{_libdir}"

install -d -m755 %{buildroot}%{_includedir}
install -m644 src/libwebvi/libwebvi.h %{buildroot}%{_includedir}

cd src/vdr-plugin
%vdr_plugin_install

%clean
rm -rf %{buildroot}

%post
%vdr_plugin_post %plugin

%postun
%vdr_plugin_postun %plugin

%files -f src/vdr-plugin/%plugin.vdr
%defattr(-,root,root)
%doc README README.vdrplugin HISTORY TODO
%dir %{_vdr_plugin_cfgdir}/%plugin
%config(noreplace) %{_vdr_plugin_cfgdir}/%plugin/mime.types
%config(noreplace) %{_vdr_plugin_cfgdir}/%plugin/webvi.plugin.conf

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

