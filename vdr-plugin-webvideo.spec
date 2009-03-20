
%define plugin	webvideo
%define name	vdr-plugin-%plugin
%define version	0.1.2
%define rel	2

Summary:	VDR plugin: Download video files from the web
Name:		%name
Version:	%version
Release:	%mkrel %rel
Group:		Video
License:	GPLv3+
URL:		http://users.tkk.fi/~aajanki/vdr/webvideo/
Source:		http://users.tkk.fi/~aajanki/vdr/webvideo/vdr-%plugin-%version.tgz
Source1:	webvid.init
Source2:	webvid.sysconfig
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	vdr-devel >= 1.6.0
BuildRequires:	libxml2-devel
BuildRequires:	python-devel
Requires:	vdr-abi = %vdr_abi
Suggests:	webvid

%description
Webvideo plugin is a tool for browsing and downloading videos from
popular video sharing websites, such as YouTube and Google video,
using VDR menu interface or a command line client. With the help of
xineliboutput plugin the videos can be played directly without
downloading them first. Mplayer plugin is also supported.

The package consists of three components: VDR plugin, a daemon that
transforms webpages into a format understood by the plugin, and a
command line client webvi that can do everything the plugin does but
works without VDR.

%package -n webvid
Summary:	Web video downloader daemon
Group:		Video
Requires:	python-curl
Requires:	python-libxslt
Requires:	python-libxml2
Requires:	python-ctypes
# used via ctypes:
Requires:	%{_lib}mms0

%description -n webvid
webvid is a server that downloads web pages from certain media sharing
websites, such as YouTube or Google Video, and transforms them into an
XML-based menu format.

The server listens for client (VDR plugin or webvi, the command line
client) connections in port 2357. The client asks for a menu page or
media file using a reference its has received from the server earlier.
The server connects to upstream web site, downloads a web page, and
transforms it into a simple XML format.The client then shows the menu
to the user who may choose to follow another link.

%package -n webvi
Summary:	Command line web video downloader
Group:		Video
Suggests:	webvid
Requires:	python-libxml2

%description -n webvi
webvi is a command line tool for downloading video and audio files
from certain media sharing websites, such as YouTube or Google Video.

The program communicates with webvid daemon, which must be running in
the background.

%prep
%setup -q -n %plugin-%version
cd vdr-plugin
%vdr_plugin_prep
%vdr_plugin_params_begin %plugin
# save downloaded files to dir
var=DOWNLOAD_DIR
param="-d DOWNLOADDIR"
# connect to server
var=SERVER
param="-s SERVER"
# connect to port
var=PORT
param="-p PORT"
%vdr_plugin_params_end

%build
python setup.py build
cd vdr-plugin
export VDR_PLUGIN_FLAGS="%vdr_plugin_flags $(pkg-config --cflags libxml-2.0)"
%vdr_plugin_build 

%install
rm -rf %{buildroot}
python setup.py install --root=%{buildroot}
%make install-data PLUGINCONFIGDIR=%{buildroot}%{_vdr_plugin_cfgdir}/%{plugin}

install -d -m755 %{buildroot}%{_initrddir}
install -m755 %{SOURCE1} %{buildroot}%{_initrddir}/webvid
install -d -m755 %{buildroot}%{_sysconfdir}/sysconfig
install -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/webvid

cd vdr-plugin
%vdr_plugin_install

%clean
rm -rf %{buildroot}

%post
%vdr_plugin_post %plugin

%postun
%vdr_plugin_postun %plugin

%post -n webvid
%_post_service webvid

%preun -n webvid
%_preun_service webvid

%files -f vdr-plugin/%plugin.vdr
%defattr(-,root,root)
%doc README HISTORY TODO
%dir %{_vdr_plugin_cfgdir}/%plugin
%config(noreplace) %{_vdr_plugin_cfgdir}/%plugin/mime.types

%files -n webvid
%defattr(-,root,root)
%doc README.daemon
%config(noreplace) %{_sysconfdir}/sysconfig/webvid
%{_initrddir}/webvid
%{_bindir}/webvid
%{python_sitelib}/webvid*
%{_datadir}/webvid

%files -n webvi
%defattr(-,root,root)
%doc README.webvi
%{_bindir}/webvi
