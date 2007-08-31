Summary:	Linux Key Management Utilities
Name:		keyutils
Version:	1.2
Release:	1
License:	GPL/LGPL
Group:		Base
Source0:	http://people.redhat.com/~dhowells/keyutils/%{name}-%{version}.tar.bz2
# Source0-md5:	227086776abccc3ee34599591db563f0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Utilities to control the kernel key management facility and to provide
a mechanism by which the kernel call back to userspace to get a key
instantiated.

%package libs
Summary:	Key utilities library
Group:		Base

%description libs
This package provides a wrapper library for the key management
facility system calls.

%package devel
Summary:	Development package for building linux key management utilities
Group:		Development/Libraries

%description devel
This package provides headers and libraries for building key
utilities.

%package static
Summary:	Static linux key management libraries
Group:		Development/Libraries

%description static
Static linux key management libraries.

%prep
%setup -q

%build
%{__make} -j1 \
	CC="%{__cc}" \
	LIBDIR=/%{_lib} \
	USRLIBDIR=%{_libdir} \
	NO_GLIBC_KEYERR=1 \
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

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README LICENCE.GPL
%attr(755,root,root) /sbin/*
%attr(755,root,root) /bin/*
%dir %{_datadir}/keyutils
%attr(755,root,root) %{_datadir}/keyutils/*.sh
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf

%files libs
%defattr(644,root,root,755)
%doc LICENCE.LGPL
%attr(755,root,root) /%{_lib}/libkeyutils-*.so
%attr(755,root,root) /%{_lib}/libkeyutils.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*.h
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
