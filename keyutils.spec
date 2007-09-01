Summary:	Linux Key Management Utilities
Summary(pl.UTF-8):	Narzędzia do linuksowego zarządzania kluczami
Name:		keyutils
Version:	1.2
Release:	1
License:	LGPL v2+ (library), GPL v2+ (utility)
Group:		Base
Source0:	http://people.redhat.com/~dhowells/keyutils/%{name}-%{version}.tar.bz2
# Source0-md5:	227086776abccc3ee34599591db563f0
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
Summary(pl.UTF-8):	Statyczna biblioetka do zarządzania linuksowymi kluczami
License:	LGPL v2+
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static linux key management libraries.

%description static -l pl.UTF-8
Statyczna biblioetka do zarządzania linuksowymi kluczami.

%prep
%setup -q

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

rm -f $RPM_BUILD_ROOT%{_mandir}/man3/keyctl_assume_authority.3
echo ".so keyctl_instantiate.3" > $RPM_BUILD_ROOT%{_mandir}/man3/keyctl_assume_authority.3

rm -f $RPM_BUILD_ROOT%{_mandir}/man3/keyctl_describe_alloc.3
echo ".so keyctl_describe.3" > $RPM_BUILD_ROOT%{_mandir}/man3/keyctl_describe_alloc.3

rm -f $RPM_BUILD_ROOT%{_mandir}/man3/keyctl_negate.3
echo ".so keyctl_instantiate.3" > $RPM_BUILD_ROOT%{_mandir}/man3/keyctl_negate.3

rm -f $RPM_BUILD_ROOT%{_mandir}/man3/keyctl_read_alloc.3
echo ".so keyctl_read.3" > $RPM_BUILD_ROOT%{_mandir}/man3/keyctl_read_alloc.3

rm -f $RPM_BUILD_ROOT%{_mandir}/man3/keyctl_unlink.3
echo ".so keyctl_link.3" > $RPM_BUILD_ROOT%{_mandir}/man3/keyctl_unlink.3

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) /bin/keyctl
%attr(755,root,root) /sbin/request-key
%dir %{_datadir}/keyutils
%attr(755,root,root) %{_datadir}/keyutils/*.sh
%{_mandir}/man1/keyctl.1*
%{_mandir}/man5/request-key.conf.5*
%{_mandir}/man8/request-key.8*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/request-key.conf

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libkeyutils-*.so
%attr(755,root,root) %ghost /%{_lib}/libkeyutils.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkeyutils.so
%{_includedir}/keyutils.h
%{_mandir}/man3/keyctl_*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libkeyutils.a
