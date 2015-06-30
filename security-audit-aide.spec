# segfaults
%{!?_with_curl: %{!?_without_curl: %global _without_curl --without-curl}}

Summary: Intrusion detection environment
Name: security-audit-aide
Version: 0.14
Release: 3%{?dist}.3
URL: http://sourceforge.net/projects/aide
License: GPLv2+
Group: Applications/System
Source0: http://downloads.sourceforge.net/aide/aide-%{version}.tar.gz
# Customize the aide.conf man page for our database location
Patch1: aide-0.14-man.patch
Patch2: aide-0.13.1-libgrypt-init.patch
Patch3: aide-0.14-abort.patch
Patch4: aide-0.14-selinux.patch
Patch5: aide-0.14-perms.patch
Patch6: aide-0.14-other-fixes.patch

Requires: suva-client
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
BuildRequires: mktemp 
BuildRequires: prelink elfutils-libelf-devel
Buildrequires: zlib-devel
Buildrequires: libgcrypt-devel >= 1.4.5-9.el6_2.1
Buildrequires: flex bison
Buildrequires: libattr-devel libacl-devel libselinux-devel
Buildrequires: audit-libs-devel >= 1.2.8-2
%if "%{?_with_curl}x" != "x"
Buildrequires: curl-devel
%endif

%description
AIDE (Advanced Intrusion Detection Environment) is a file integrity
checker and intrusion detection program.


%prep
%setup -q -n aide-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
%configure --with-config_file=%{_sysconfdir}/aide.conf \
           --with-zlib \
           --disable-static \
           %{?_with_curl} %{?_without_curl} \
           --with-selinux --with-posix-acl --with-audit \
           --with-xattr \
           --with-prelink

make


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT bindir=%{_sbindir} install

install -m 0755 -d $RPM_BUILD_ROOT/var/lib/suvlets/SecurityAudit
mv $RPM_BUILD_ROOT%{_sbindir}/aide $RPM_BUILD_ROOT/var/lib/suvlets/SecurityAudit/aide

rm -fv $RPM_BUILD_ROOT%{_mandir}/man1/aide.1*
rm -fv $RPM_BUILD_ROOT%{_mandir}/man5/aide.conf.5*

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(0644,root,root,0755)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(4750,root,suva) /var/lib/suvlets/SecurityAudit/aide

%changelog
* Thu Jun 20 2013 ClearFoundation <developer@clearfoundation.com> - 0.14-3.3.clear
- sandboxed version for Security Audit

* Tue Apr 17 2012 Daniel Kopecek <dkopecek@redhat.com> - 0.14-3.2
- corrected z-stream versioning

* Mon Apr 16 2012 Daniel Kopecek <dkopecek@redhat.com> - 0.14-3.1
- corrected BuildRequires

* Fri Apr 13 2012 Daniel Kopecek <dkopecek@redhat.com> - 0.14-3
resolves: #811929 aide doesn't initialize its database when FIPS is enabled

* Tue May 18 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-3
resolves: #590561 aide does not detect the change of SElinux context
resolves: #590566 aide reports a changed file when it has not been changed

* Wed Apr 28 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-2
resolves: #585919 - aide: Libgcrypt warning: missing initialization
resolves: #587086 - [abrt] crash in aide-0.14-1

* Wed Mar 17 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-1
resolves: #567668 rebase to upstream release 0.14 final

* Thu Feb 25 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-0.2.rc2
resolves: #567668 rebase to new upstream release

* Wed Feb 24 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-0.1.rc1
resolves: #567668 rebase to new upstream release

* Fri Feb 19 2010 Steve Grubb <sgrubb@redhat.com> - 0.13.1-16
- Add logrotate script and spec file cleanups

* Fri Dec 11 2009 Steve Grubb <sgrubb@redhat.com> - 0.13.1-15
- Get rid of .dedosify files

* Wed Dec 09 2009 Steve Grubb <sgrubb@redhat.com> - 0.13.1-14
- Revise patch for Initialize libgcrypt correctly (#530485)

* Sat Nov 07 2009 Steve Grubb <sgrubb@redhat.com> - 0.13.1-13
- Initialize libgcrypt correctly (#530485)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.13.1-12
- rebuilt with new audit

* Wed Aug 19 2009 Steve Grubb <sgrubb@redhat.com> 0.13.1-11
- rebuild for new audit-libs
- Correct regex for root's dot files (#509370)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 08 2009 Steve Grubb <sgrubb@redhat.com> - 0.13.1-9
- Make aide smarter about prelinked files (Peter Vrabec)
- Add /lib64 to default config

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Steve Grubb <sgrubb@redhat.com> - 0.13.1-6
- enable xattr support and update config file

* Fri Sep 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.13.1-5
- fix selcon patch to apply without fuzz

* Fri Feb 15 2008 Steve Conklin <sconklin@redhat.com>
- rebuild for gcc4.3

* Tue Aug 21 2007 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Jul 22 2007 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.13.1-2
- Apply Steve Conklin's patch to increase displayed portion of
  selinux context.

* Sun Dec 17 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.13.1-1
- Update to 0.13.1 release.

* Sun Dec 10 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.13-1
- Update to 0.13 release.
- Include default aide.conf from RHEL5 as doc example file.

* Sun Oct 29 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.12-3.20061027cvs
- CAUTION! This changes the database format and results in a report of
  false inconsistencies until an old database file is updated.
- Check out CVS 20061027 which now contains Red Hat's
  acl/xattr/selinux/audit patches.
- Patches merged upstream.
- Update manual page substitutions.

* Mon Oct 23 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.12-2
- Add "memory leaks and performance updates" patch as posted
  to aide-devel by Steve Grubb.

* Sat Oct 07 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.12-1
- Update to 0.12 release.
- now offers --disable-static, so -no-static patch is obsolete
- fill last element of getopt struct array with zeroes

* Mon Oct 02 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.11-3
- rebuilt

* Mon Sep 11 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.11-2
- rebuilt

* Sun Feb 19 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.11-1
- Update to 0.11 release.
- useless-includes patch merged upstream.
- old Russian man pages not available anymore.
- disable static linking.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Fri Nov 28 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.10-0.fdr.1
- Update to 0.10 release.
- memleaks patch merged upstream.
- rootpath patch merged upstream.
- fstat patch not needed anymore.
- Updated URL.

* Thu Nov 13 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.10-0.fdr.0.2.cvs20031104
- Added buildreq m4 to work around incomplete deps of bison package.

* Tue Nov 04 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.10-0.fdr.0.1.cvs20031104
- Only tar.gz available upstream.
- byacc not needed when bison -y is available.
- Installed Russian manual pages.
- Updated with changes from CVS (2003-11-04).
- getopt patch merged upstream.
- bison-1.35 patch incorporated upstream.

* Tue Sep 09 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.9-0.fdr.0.2.20030902
- Added fixes for further memleaks.

* Sun Sep 07 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.9-0.fdr.0.1.20030902
- Initial package version.

