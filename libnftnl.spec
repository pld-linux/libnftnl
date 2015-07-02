#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
%bcond_without	jansson		# JSON parsing support (via jansson)
%bcond_without	mxml		# XML parsing support (via mxml)

Summary:	Netfilter nf_tables infrastructure library
Summary(pl.UTF-8):	Biblioteka infrastruktury nf_tables netfiltra
Name:		libnftnl
Version:	1.0.3
Release:	2
License:	GPL v2+
Group:		Libraries
Source0:	http://www.netfilter.org/projects/libnftnl/files/%{name}-%{version}.tar.bz2
# Source0-md5:	203701a73cc3c51ca751d7cb2e176250
URL:		http://www.netfilter.org/projects/libnftnl/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1.6
%{?with_apidocs:BuildRequires:	doxygen}
%{?with_jansson:BuildRequires:	jansson-devel >= 2.3}
BuildRequires:	libmnl-devel >= 1.0.0
BuildRequires:	libtool >= 2:2
BuildRequires:	linux-libc-headers >= 7:3.14
%{?with_mxml:BuildRequires:	mxml-devel >= 2.6}
%{?with_jansson:Requires:	jansson >= 2.3}
Requires:	libmnl >= 1.0.0
%{?with_mxml:Requires:	mxml >= 2.6}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libnftnl is a userspace library providing a low-level netlink
programming interface (API) to the in-kernel nf_tables subsystem. The
library libnftnl has been previously known as libnftables. This
library is currently used by nftables.

%description -l pl.UTF-8
libnftnl to biblioteka przestrzeni użytkownika udostępniająca
niskopoziomowy interfejs programistyczny (API) netlink do podsystemu
nf_tables w jądrze. Wcześniej biblioteka nazywała się libnftables.
Jest obecnie używana przez narzędzie nftables.

%package devel
Summary:	Header files for libnftnl library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libnftnl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libmnl-devel >= 1.0.0

%description devel
Header files for libnftnl library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libnftnl.

%package static
Summary:	Static libnftnl library
Summary(pl.UTF-8):	Statyczna biblioteka libnftnl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libnftnl library.

%description static -l pl.UTF-8
Statyczna biblioteka libnftnl.

%package apidocs
Summary:	libnftnl API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libnftnl
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API and internal documentation for libnftnl library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libnftnl.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	%{?with_jansson:--with-json-parsing} \
	%{?with_mxml:--with-xml-parsing}

%{__make}

%{?with_apidocs:doxygen doxygen.cfg}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnftnl.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnftnl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnftnl.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnftnl.so
%{_includedir}/libnftnl
%{_pkgconfigdir}/libnftnl.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libnftnl.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doxygen/html/*
%endif
