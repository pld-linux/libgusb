#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	GUsb - GObject wrapper for libusb1 library
Summary(pl.UTF-8):	GUsb - obudowanie GObject biblioteki libusb1
Name:		libgusb
Version:	0.1.2
Release:	2
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.xz
# Source0-md5:	9eaf4e27aa533cbe3789f8af305cdf4a
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	glib2-devel >= 1:2.28.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libusb-devel >= 1.0.0
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-glib-devel
BuildRequires:	xz
Requires:	glib2 >= 1:2.28.0
Requires:	libusb >= 1.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GUsb is a GObject wrapper for libusb1 that makes it easy to do
asynchronous control, bulk and interrupt transfers with proper
cancellation and integration into a mainloop. This makes it easy to
integrate low level USB transfers with your high-level application or
system daemon.

%description -l pl.UTF-8
GUsb to obudowanie GObject biblioteki libusb1, ułatwiające
asynchroniczne sterowanie oraz przesyłanie danych (typu bulk jak i
z użyciem przerwań) z właściwym przerywaniem i integracją w głównej
pętli. Ułatwia to integrowanie niskopoziomowego przesyłania danych po
USB w wysokopoziomowej aplikacji lub demonie systemowym.

%package devel
Summary:	Header files for GUsb library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GUsb
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.28.0
Requires:	libusb-devel >= 1.0.0
Requires:	udev-glib-devel

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

%description apidocs
API and internal documentation for GUsb library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GUsb.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgusb.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS NEWS README TODO
%attr(755,root,root) %{_libdir}/libgusb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgusb.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgusb.so
%{_includedir}/gusb-1
%{_pkgconfigdir}/gusb.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgusb.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gusb
%endif
