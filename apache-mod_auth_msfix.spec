#Module-Specific definitions
%define mod_name mod_auth_msfix
%define mod_conf A24_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	A module that fix MS XP WebDAV client problem
Name:		apache-%{mod_name}
Version:	0.2.1
Release:	17
Group:		System/Servers
License:	GPL
URL:		https://www.luluware.com/mod_auth_msfix.html
Source0:	%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}
Patch0:		mod_auth_msfix-0.2.1-apache220.diff
Requires:	apache-mod_dav
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:  apache-devel >= 2.2.0
BuildRequires:	file
Epoch:		1

%description
When MS XP Clients connect to WebDAV, they may have a problem
sending the user's name to Apache. They send domaine\username
or username@domaine, which break most of the authentification
module of Apache. 

This mod can fix the user's name by rewriting it.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0

cp %{SOURCE1} %{mod_conf}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
%{_bindir}/apxs -c %{mod_name}.c

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc CHANGES INSTALL README mod_auth_msfix.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-16mdv2012.0
+ Revision: 772561
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-15
+ Revision: 678262
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-14mdv2011.0
+ Revision: 587920
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-13mdv2010.1
+ Revision: 516046
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-12mdv2010.0
+ Revision: 406533
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-11mdv2009.1
+ Revision: 325543
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-10mdv2009.0
+ Revision: 234659
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-9mdv2009.0
+ Revision: 215532
- fix rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-8mdv2008.1
+ Revision: 181668
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-7mdv2008.0
+ Revision: 82520
- rebuild

* Sat Aug 18 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-6mdv2008.0
+ Revision: 65622
- rebuild


* Sun Mar 11 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2.1-5mdv2007.1
+ Revision: 141273
- rebuild
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-3mdv2007.1
+ Revision: 79324
- Import apache-mod_auth_msfix

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-3mdv2007.0
- rebuild

* Thu Dec 15 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-2mdk
- rebuilt against apache-2.2.0
- fix the config

* Mon Nov 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-1mdk
- fix versioning

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.2.1-2mdk
- fix deps

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.2.1-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.2.1-5mdk
- use the %1

* Mon Feb 28 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.2.1-4mdk
- fix %%post and %%postun to prevent double restarts

* Fri Feb 25 2005 Stefan van der Eijk <stefan@eijk.nu> 2.0.53_0.2.1-3mdk
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.2.1-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.2.1-1mdk
- rebuilt for apache 2.0.53

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_0.2.1-1mdk
- built for apache 2.0.52

* Fri Sep 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.51_0.2.1-1mdk
- built for apache 2.0.51

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_0.2.1-1mdk
- built for apache 2.0.50
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.49_0.2.1-1mdk
- 0.2.1
- built for apache 2.0.49

* Tue Mar 30 2004 Michael Scherer <misc@mandrake.org> 2.0.48_0.2.0-2mdk 
- Enhance description

