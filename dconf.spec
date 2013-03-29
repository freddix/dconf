Summary:	Low-level configuration system
Name:		dconf
Version:	0.16.0
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/dconf/0.16/%{name}-%{version}.tar.xz
# Source0-md5:	a266b3f75edabaf15ffcbe9e21130f7e
URL:		http://live.gnome.org/dconf
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk+3-devel
BuildRequires:	gtk-doc
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	vala
Requires(post,postun):	glib-gio
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
dconf is a low-level configuration system. Its main purpose is to
provide a backend to GSettings on platforms that don't already have
configuration storage systems.

%package libs
Summary:	dconf library
Group:		Libraries

%description libs
dconf library.

%package devel
Summary:	Header files for dconf library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for dconf library.

%package editor
Summary:	Configuration editor for dconf
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	hicolor-icon-theme


%description editor
dconf-editor allows you to browse and modify dconf database.

%package apidocs
Summary:	dconf API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
API documentation for dconf library.

%prep
%setup -q

%build
%{__libtoolize}
%{__gtkdocize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules	\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/dconf/{db,profile}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
gio-querymodules %{_libdir}/gio/modules ||:

%postun
umask 022
gio-querymodules %{_libdir}/gio/modules ||:

%post editor
%update_icon_cache hicolor
%update_gsettings_cache

%postun editor
%update_icon_cache hicolor
%update_gsettings_cache

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS
%dir %{_sysconfdir}/dconf
%dir %{_sysconfdir}/dconf/db
%dir %{_sysconfdir}/dconf/profile
%dir %{_libexecdir}
%attr(755,root,root) %{_bindir}/dconf
%attr(755,root,root) %{_libdir}/gio/modules/libdconfsettings.so
%attr(755,root,root) %{_libexecdir}/dconf-service
%{_datadir}/dbus-1/services/ca.desrt.dconf.service
%{_mandir}/man1/dconf-service.1*
%{_mandir}/man1/dconf.1*

%files editor
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dconf-editor
%{_datadir}/dconf-editor
%{_datadir}/glib-2.0/schemas/ca.desrt.dconf-editor.gschema.xml
%{_desktopdir}/dconf-editor.desktop
%{_iconsdir}/hicolor/*/apps/dconf-editor.*
%{_mandir}/man1/dconf-editor.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libdconf-dbus-1.so.?
%attr(755,root,root) %ghost %{_libdir}/libdconf.so.?
%attr(755,root,root) %{_libdir}/libdconf-dbus-1.so.*.*.*
%attr(755,root,root) %{_libdir}/libdconf.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdconf.so
%attr(755,root,root) %{_libdir}/libdconf-dbus-1.so
%{_includedir}/dconf
%{_includedir}/dconf-dbus-1
%{_pkgconfigdir}/*.pc
%{_datadir}/vala/vapi/dconf.*
%{_mandir}/man7/dconf.7*

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/dconf

