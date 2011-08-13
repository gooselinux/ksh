%define       releasedate   2010-06-21

Name:         ksh
Summary:      The Original ATT Korn Shell
URL:          http://www.kornshell.com/
Group:        System Environment/Shells
#zlib is used for INIT.2010-02-02.tgz/src/cmd/INIT/ratz.c - used only for build tool
#CPL everywhere else (for KSH itself)
License:      CPL
Version:      20100621
Release:      2%{?dist}
Source0:      http://www.research.att.com/~gsf/download/tgz/ast-ksh.%{releasedate}.tgz
Source1:      http://www.research.att.com/~gsf/download/tgz/INIT.%{releasedate}.tgz
Source3:      kshrc.rhs
Source4:      dotkshrc

#documentation of important changes not mentioned in RELEASE file
Source5:      ChangeLog

#don't use not wanted/needed builtins - Fedora/RHEL specific
Patch1:       ksh-20070328-builtins.patch

#send upstream
Patch2:       ksh-20100621-memleak.patch

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Conflicts:    pdksh
Requires: coreutils, glibc-common, diffutils
BuildRequires: bison
Requires(post): grep, coreutils
Requires(preun): grep, coreutils

%description
KSH-93 is the most recent version of the KornShell by David Korn of
AT&T Bell Laboratories.
KornShell is a shell programming language, which is upward compatible
with "sh" (the Bourne Shell).

%prep
%setup -q -c
%setup -q -T -D -a 1
%patch1 -p1 -b .builtins
%patch2 -p1 -b .memleak

cp %{SOURCE5} .

#/dev/fd test does not work because of mock
sed -i 's|ls /dev/fd|ls /proc/self/fd|' src/cmd/ksh93/features/options

%build
./bin/package "read" ||:
export CCFLAGS="$RPM_OPT_FLAGS"
export CC=gcc
./bin/package "make"

#missing in 2010-06-21, chech later if added back
#cp lib/package/LICENSES/ast LICENSE

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{/bin,%{_bindir},%{_mandir}/man1}
install -c -m 755 arch/*/bin/ksh $RPM_BUILD_ROOT/bin/ksh
install -c -m 644 arch/*/man/man1/sh.1 $RPM_BUILD_ROOT%{_mandir}/man1/ksh.1
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/skel
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/skel/.kshrc
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/kshrc

%post
if [ ! -f /etc/shells ]; then
        echo "/bin/ksh" > /etc/shells
else
        if ! grep -q '^/bin/ksh$' /etc/shells ; then
                echo "/bin/ksh" >> /etc/shells
        fi
fi

%postun
if [ ! -f /bin/ksh ]; then
	sed -i '/^\/bin\/ksh$/ d' /etc/shells
fi

%verifyscript
echo -n "Looking for ksh in /etc/shells... "
if ! grep '^/bin/ksh$' /etc/shells > /dev/null; then
    echo "missing"
    echo "ksh missing from /etc/shells" >&2
else
    echo "found"
fi

%files 
%defattr(-, root, root,-)
#%doc README LICENSE src/cmd/ksh93/COMPATIBILITY src/cmd/ksh93/RELEASE ChangeLog
%doc README src/cmd/ksh93/COMPATIBILITY src/cmd/ksh93/RELEASE ChangeLog
/bin/ksh
%{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/skel/.kshrc
%config(noreplace) %{_sysconfdir}/kshrc

%clean
    rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Jun 29 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100621-2
- fix memory leak (second part is not upstream yet) (#586923)

* Tue Jun 29 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100621-1
- updated to 2010-06-21

* Tue May 31 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100202-9
- add pathmunge to /etc/kshrc

* Tue May 25 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100202-8
- fix rare cd builtin crash

* Tue May 04 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100202-7
- fix memory leak (#588710)

* Mon May 03 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100202-6
- fix infinite loop when whence builtin is used with -q option (#587127)
- fix stdin for double command substitution (#584704)

* Mon Mar 29 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100202-5
- fix typo in last patch

* Fri Mar 26 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100202-4
- restore tty settings after timed out read for utf-8 locale

* Fri Feb 19 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100202-3
- add zlib to license

* Wed Feb 10 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100202-2
- add COMPATIBILITY, RELEASE and ChangeLog to docs

* Tue Feb 09 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100202-1
- updated to stable version 2010-02-02

* Tue Jan 05 2010 Michal Hlavinka <mhlavink@redhat.com> - 20091224-1
- updated to 2009-12-24

* Fri Dec 07 2009 Michal Hlavinka <mhlavink@redhat.com> - 20091206-1
- updated to 2009-12-06

* Fri Dec 04 2009 Michal Hlavinka <mhlavink@redhat.com> - 20091130-1
- updated to 2009-11-30

* Wed Nov 18 2009 Michal Hlavinka <mhlavink@redhat.com> - 20091021-1
- updated to 2009-10-21

* Thu Aug 27 2009 Michal Hlavinka <mhlavink@redhat.com> - 20090630-1
- updated to 2009-06-30

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090505-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 11 2009 Michal Hlavinka <mhalvink@redhat.com> - 20090505-1
- updated to 2009-05-05

* Tue May 05 2009 Michal Hlavinka <mhalvink@redhat.com> - 20090501-1
- updated to 2009-05-01

* Tue Mar 10 2009 Michal Hlavinka <mhlavink@redhat.com> - 20081104-3
- fix typos in spec file

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081104-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 21 2009 Michal Hlavinka <mhlavink@redhat.com> 20081104-1
- update to 2008-11-04
- ast-ksh-locales are not useable remove them

* Tue Oct 21 2008 Michal Hlavinka <mhlavink@redhat.com> 20080725-4
- fix #467025 - Ksh fails to initialise environment when login from graphic console

* Wed Aug 06 2008 Tomas Smetana <tsmetana@redhat.com> 20080725-3
- fix BuildRequires, rebuild

* Tue Aug  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 20080725-2
- fix license tag

* Mon Jul 28 2008 Tomas Smetana <tsmetana@redhat.com> 20080725-1
- new upstream version

* Thu Jun 26 2008 Tomas Smetana <tsmetana@redhat.com> 20080624-1
- new upstream version

* Mon Feb 11 2008 Tomas Smetana <tsmetana@redhat.com> 20080202-1
- new upstream version

* Wed Jan 30 2008 Tomas Smetana <tsmetana@redhat.com> 20071105-3
- fix #430602 - ksh segfaults after unsetting OPTIND

* Mon Jan 07 2008 Tomas Smetana <tsmetana@redhat.com> 20071105-2
- fix #405381 - ksh will not handle $(xxx) when typeset -r IFS
- fix #386501 - bad group in spec file

* Wed Nov 07 2007 Tomas Smetana <tsmetana@redhat.com> 20071105-1
- new upstream version

* Wed Aug 22 2007 Tomas Smetana <tsmetana@redhat.com> 20070628-1.1
- rebuild

* Thu Jul 12 2007 Tomas Smetana <tsmetana@redhat.com> 20070628-1
- new upstream version
- fix unaligned access messages (Related: #219420)

* Tue May 22 2007 Tomas Smetana <tsmetana@redhat.com> 20070328-2
- fix wrong exit status of spawned process after SIGSTOP
- fix building of debuginfo package, add %%{?dist} to release
- fix handling of SIGTTOU in non-interactive shell
- remove useless builtins

* Thu Apr 19 2007 Tomas Smetana <tsmetana@redhat.com> 20070328-1
- new upstream source
- fix login shell invocation (#182397)
- fix memory leak

* Wed Feb 21 2007 Karsten Hopp <karsten@redhat.com> 20070111-1
- new upstream version
- fix invalid write in uname function

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 20060214-1.1
- rebuild

* Thu Jun 01 2006 Karsten Hopp <karsten@redhat.de> 20060214-1
- new upstream source

* Mon Feb 27 2006 Karsten Hopp <karsten@redhat.de> 20060124-3
- PreReq grep, coreutils (#182835)

* Tue Feb 14 2006 Karsten Hopp <karsten@redhat.de> 20060124-2
- make it build in chroots (#180561)

* Mon Feb 13 2006 Karsten Hopp <karsten@redhat.de> 20060124-1
- version 20060124

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 20050202-5.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Karsten Hopp <karsten@redhat.de> 20050202-5
- rebuild

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 20050202-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 02 2006 Karsten Hopp <karsten@redhat.de> 20050202-4
- fix uname -i output
- fix loop (*-path.patch)
- conflict pdksh instead of obsoleting it

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com> 20050202-3.1
- rebuilt for new gcj

* Tue May 10 2005 Karsten Hopp <karsten@redhat.de> 20050202-3
- enable debuginfo

* Tue Mar 15 2005 Karsten Hopp <karsten@redhat.de> 20050202-2
- add /usr/bin/ksh link for compatibility with pdksh scripts (#151134)

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 20050202-1 
- update and rebuild with gcc-4

* Tue Mar 01 2005 Karsten Hopp <karsten@redhat.de> 20041225-2 
- fix gcc4 build 

* Fri Jan 21 2005 Karsten Hopp <karsten@redhat.de> 20041225-1
- rebuild with new ksh tarball (license change)

* Tue Nov 02 2004 Karsten Hopp <karsten@redhat.de> 20040229-11
- disable ia64 for now

* Fri Oct 15 2004 Karsten Hopp <karsten@redhat.de> 20040229-9 
- rebuild

* Thu Sep 02 2004 Nalin Dahyabhai <nalin@redhat.com> 20040229-8
- remove '&' from summary

* Thu Sep 02 2004 Bill Nottingham <notting@redhat.com> 20040229-7
- obsolete pdksh (#131303)

* Mon Aug 02 2004 Karsten Hopp <karsten@redhat.de> 20040229-6
- obsolete ksh93, provide ksh93

* Mon Jul 05 2004 Karsten Hopp <karsten@redhat.de> 20040229-3 
- add /bin/ksh to /etc/shells

* Wed Jun 16 2004 Karsten Hopp <karsten@redhat.de> 20040229-2 
- add ppc64 patch to avoid ppc64 dot symbol problem

* Fri May 28 2004 Karsten Hopp <karsten@redhat.de> 20040229-1 
- initial version

