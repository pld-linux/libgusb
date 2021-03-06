#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
%bcond_without	vala		# Vala API

Summary:	GUsb - GObject wrapper for libusb1 library
Summary(pl.UTF-8):	GUsb - obudowanie GObject biblioteki libusb1
Name:		libgusb
Version:	0.3.7
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.xz
# Source0-md5:	62d833175b0093f83483f2ebeea6f797
BuildRequires:	gcc >= 5:3.2
BuildRequires:	glib2-devel >= 1:2.44.0
BuildRequires:	gobject-introspection-devel >= 1.29
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	libusb-devel >= 1.0.22
BuildRequires:	meson >= 0.46.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
%{?with_vala:BuildRequires:	vala >= 2:0.16}
BuildRequires:	xz
Requires:	glib2 >= 1:2.44.0
Requires:	libusb >= 1.0.22
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GUsb is a GObject wrapper for libusb1 that makes it easy to do
asynchronous control, bulk and interrupt transfers with proper
cancellation and integration into a mainloop. This makes it easy to
integrate low level USB transfers with your high-level application or
system daemon.

%description -l pl.UTF-8
GUsb to obudowanie GObject biblioteki libusb1, ułatwiające
asynchroniczne sterowanie oraz przesyłanie danych (typu bulk jak i z
użyciem przerwań) z właściwym przerywaniem i integracją w głównej
pętli. Ułatwia to integrowanie niskopoziomowego przesyłania danych po
USB w wysokopoziomowej aplikacji lub demonie systemowym.

%package devel
Summary:	Header files for GUsb library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GUsb
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.44.0
Requires:	libusb-devel >= 1.0.22

%description devel
Header files for GUsb library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GUsb.

%package static
Summary:	Static GUsb library
Summary(pl.UTF-8):	Statyczna biblioteka GUsb
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GUsb library.

%description static -l pl.UTF-8
Statyczna biblioteka GUsb.

%package apidocs
Summary:	GUsb API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki GUsb
Group:		Documentation
BuildArch:	noarch

%description apidocs
API and internal documentation for GUsb library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GUsb.

%package -n vala-libgusb
Summary:	Vala API for libgusb
Summary(pl.UTF-8):	API języka Vala do libgusb
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.16
BuildArch:	noarch

%description -n vala-libgusb
Vala API for libgusb.

%description -n vala-libgusb -l pl.UTF-8
API języka Vala do libgusb.

%prep
%setup -q

%if %{with static_libs}
%{__sed} -i -e 's/shared_library/library/' gusb/meson.build
%endif

%build
%meson build \
	-Dvapi=%{__true_false vala}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS NEWS README.md
%attr(755,root,root) %{_bindir}/gusbcmd
%attr(755,root,root) %{_libdir}/libgusb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgusb.so.2
%{_libdir}/girepository-1.0/GUsb-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgusb.so
%{_includedir}/gusb-1
%{_datadir}/gir-1.0/GUsb-1.0.gir
%{_pkgconfigdir}/gusb.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgusb.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gusb
%endif

%if %{with vala}
%files -n vala-libgusb
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gusb.deps
%{_datadir}/vala/vapi/gusb.vapi
%endif
