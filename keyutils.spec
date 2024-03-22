Summary:	Linux Key Management Utilities
Summary(pl.UTF-8):	Narzędzia do linuksowego zarządzania kluczami
Name:		keyutils
Version:	1.6.3
Release:	1
License:	LGPL v2+ (library), GPL v2+ (utility)
Group:		Base
Source0:	https://git.kernel.org/pub/scm/linux/kernel/git/dhowells/keyutils.git/snapshot/%{name}-%{version}.tar.gz
# Source0-md5:	6b70b2b381c1b6d9adfaf66d5d3e7c00
Patch0:		helpers.patch
Patch1:		%{name}-pkgconfigdir.patch
URL:		https://git.kernel.org/pub/scm/linux/kernel/git/dhowells/keyutils.git
BuildRequires:	rpmbuild(macros) >= 1.402
BuildRequires:	glibc-devel >= 6:2.4
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Utilities to control the kernel key management facility and to provide
a mechanism by which the kernel call back to userspace to get a key
instantiated.

%description -l pl.UTF-8
Narzędzia sterujące zarządzaniem kluczami w jądrze i dostarczające
mechanizm, przez który jądro odwołuje się do przestrzeni użytkownika w
celu pobrania instancji klucza.

%package libs
Summary:	Key utilities library
Summary(pl.UTF-8):	Biblioteka narzędzi do zarządzania kluczami
License:	LGPL v2+
Group:		Libraries
Requires:	glibc >= 6:2.4

%description libs
This package provides a wrapper library for the key management
facility system calls.

%description libs -l pl.UTF-8
Ten pakiet zawiera bibliotekę obudowującą wywołania systemowe do
zarządzania kluczami.

%package devel
Summary:	Development package for building Linux key management utilities
Summary(pl.UTF-8):	Pakiet programistyczny do tworzenia narzędzi zarządzających linuksowymi kluczami
License:	LGPL v2+
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package provides the header files for building key utilities.

%description devel -l pl.UTF-8
Ten pakiet udostępnia pliki nagłówkowe do tworzenia narzędzi
zarządzających kluczami.

%package static
Summary:	Static Linux key management library
Summary(pl.UTF-8):	Statyczna biblioteka do zarządzania linuksowymi kluczami
License:	LGPL v2+
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static linux key management library.

%description static -l pl.UTF-8
Statyczna biblioteka do zarządzania linuksowymi kluczami.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} -j1 \
	CC="%{__cc}" \
	LIBDIR=/%{_lib} \
	USRLIBDIR=%{_libdir} \
	CFLAGS="-Wall %{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR=/%{_lib} \
	USRLIBDIR=%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) /bin/keyctl
%attr(755,root,root) /sbin/key.dns_resolver
%attr(755,root,root) /sbin/request-key
%dir %{_datadir}/keyutils
%attr(755,root,root) %{_datadir}/keyutils/*.sh
%{_mandir}/man1/keyctl.1*
%{_mandir}/man5/request-key.conf.5*
%{_mandir}/man5/key.dns_resolver.conf.5*
%{_mandir}/man8/key.dns_resolver.8*
%{_mandir}/man8/request-key.8*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/request-key.conf

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libkeyutils.so.*.*
%attr(755,root,root) %ghost /%{_lib}/libkeyutils.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkeyutils.so
%{_includedir}/keyutils.h
%{_pkgconfigdir}/libkeyutils.pc
%{_mandir}/man3/keyctl.3*
%{_mandir}/man3/keyctl_*.3*
%{_mandir}/man3/find_key_by_type_and_name.3*
%{_mandir}/man3/recursive_key_scan.3*
%{_mandir}/man3/recursive_session_key_scan.3*
%{_mandir}/man7/asymmetric-key.7*
%{_mandir}/man7/keyutils.7*

%files static
%defattr(644,root,root,755)
%{_libdir}/libkeyutils.a
