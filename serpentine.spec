#
# Conditional build:
%bcond_with	muine		# build muine plugin
#
Summary:	CD-Audio recording application
Summary(pl.UTF-8):	Aplikacja do nagrywania płyt CD-Audio
Name:		serpentine
Version:	0.9
Release:	4
License:	GPL v2
Group:		X11/Applications
Source0:	http://download.berlios.de/serpentine/%{name}-%{version}.tar.bz2
# Source0-md5:	12e548494eed087c999cca47247ebbed
Patch0:		%{name}-python.patch
URL:		http://s1x.homelinux.net/projects/serpentine/
BuildRequires:	GConf2-devel
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1.7
BuildRequires:	gettext-tools
BuildRequires:	intltool
%if %{with muine}
BuildRequires:	mono-csharp
BuildRequires:	muine
%endif
BuildRequires:	pkgconfig
BuildRequires:	python-pygtk-devel >= 2:2.8.0
BuildRequires:	rpm-pythonprov
%pyrequires_eq	python-modules
%pyrequires_eq	python
Requires(post,postun):	desktop-file-utils
Requires:	python-PyXML
Requires:	python-dbus
Requires:	python-gnome-desktop-nautilus-cd-burner >= 2.12.0
Requires:	python-gnome-desktop-totem >= 2.12.0
Requires:	python-gnome-gconf >= 2.12.0
Requires:	python-gnome-ui >= 2.12.0
Requires:	python-gnome-vfs >= 2.12.0
Requires:	python-gstreamer >= 0.8.2
Requires:	python-libxml2 >= 1:2.6.22
Requires:	python-pygtk-glade >= 2:2.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Serpentine is a simple to use and very powerful CD-Audio recording
application.

%description -l pl.UTF-8
Serpentine to prosta w użyciu i potężna aplikacja do nagrywania płyt
CD-Audio.

%package -n muine-plugin-serpentine
Summary:	Serpentine plugins for Muine
Summary(pl.UTF-8):	Wtyczka Serpentine dla Muine
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	muine

%description -n muine-plugin-serpentine
Serpentine plugin for Muine.

%description -n muine-plugin-serpentine -l pl.UTF-8
Wtyczka Serpentine dla Muine.

%prep
%setup -q
%patch0 -p1

%build
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-muine=%{?with_muine:yes}%{!?with_muine:no}
%{__make}

%{py_comp} serpentine
%{py_ocomp} serpentine

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# remove not needed *.py files
rm -f $RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}/*.py
rm -f $RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}/plugins/*.py

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_desktopdir}/*.desktop
%{py_sitescriptdir}/%{name}

%if %{with muine}
%files -n muine-plugin-serpentine
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/muine/*
%endif
