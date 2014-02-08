%ifarch x86_64
%define	wine	wine64
%else
%define	wine	wine
%endif
%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%{mklibname -d wine}
%define beta %nil

# On 32-bit we have
# wine32 - those 32-bit binaries that are also used on 64-bit for 32-bit support
# wine - all other files (requires 'wine32')
# On 64-bit we have
# wine64 - all 64-bit files (suggests 'wine32')
# - Anssi 07/2010

Name:		wine
#(peroyvind): please do backports for new versions
Version:	1.6
%if "%beta" != ""
Release:	0.%beta.1
Source0:	http://mirrors.ibiblio.org/wine/source/%(echo %version |cut -d. -f1-2)/%{name}-%{version}-%beta.tar.bz2
Source1:	http://mirrors.ibiblio.org/wine/source/%(echo %version |cut -d. -f1-2)/%{name}-%{version}-%beta.tar.bz2.sign
%else
Release:	2
Source0:	http://mirrors.ibiblio.org/wine/source/%(echo %version |cut -d. -f1-2)/%{name}-%{version}.tar.bz2
Source1:	http://mirrors.ibiblio.org/wine/source/%(echo %version |cut -d. -f1-2)/%{name}-%{version}.tar.bz2.sign
%endif
Epoch:		2
Summary:	WINE Is Not An Emulator - runs MS Windows programs
License:	LGPLv2+
Group:		Emulators
URL:		http://www.winehq.com/

# RH stuff
Source2:	wine.init
Source10:	wine.rpmlintrc
Patch0:		wine-1.0-rc3-fix-conflicts-with-openssl.patch
Patch1:		wine-1.1.7-chinese-font-substitutes.patch
# (Anssi 05/2008) Adds:
# a: => /media/floppy (/mnt/floppy on 2007.1 and older)
# d: => $HOME (at config_dir creation time, not refreshed if $HOME changes;
#              note that Wine also provides $HOME in My Documents)
# only on 2008.0: e: => /media/cdrom (does not exist on 2008.1+)
# only on 2007.1 and older: e: => /mnt/cdrom
# com4 => /dev/ttyUSB0 (replaces /dev/ttyS3)
# have to substitute @MDKVERSION@ in dlls/ntdll/server.c
Patch108:	wine-mdkconf.patch
Patch200:	wine-1.3.24-64bit-tools.patch
#(eandry) add a pulseaudio sound driver (from http://art.ified.ca/downloads/ )

# Rediff configure.ac patch manually until winepulse upstream fixes it

# (anssi) Wine needs GCC 4.4+ on x86_64 for MS ABI support. Note also that
# 64-bit wine cannot run 32-bit programs without wine32.
ExclusiveArch:	%{ix86}
%if %{mdkversion} >= 201010
ExclusiveArch:	x86_64
%endif
%ifarch x86_64
BuildRequires:	gcc >= 4.4
%endif

BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gpm-devel
BuildRequires:	perl-devel
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	cups-devel
BuildRequires:	pkgconfig(sane-backends)
BuildRequires:	pkgconfig(lcms)
BuildRequires:	autoconf
BuildRequires:	docbook-utils
BuildRequires:	docbook-dtd-sgml
BuildRequires:	docbook-utils
BuildRequires:	docbook-dtd-sgml
BuildRequires:	sgml-tools
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libmpg123)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(gstreamer-0.10)
BuildRequires:	pkgconfig(gstreamer-plugins-base-0.10)
BuildRequires:	isdn4k-utils-devel
BuildRequires:	glibc-static-devel
BuildRequires:	chrpath
BuildRequires:	ungif-devel
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(libgphoto2)
BuildRequires:	desktop-file-utils
BuildRequires:	openldap-devel
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	valgrind
BuildRequires:	gsm-devel
BuildRequires:	unixODBC-devel
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libv4l2)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xinerama) 
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(sm)
BuildRequires:	fontforge
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
%if "%{distepoch}" >= "2011.0"
BuildRequires:	prelink
%endif

%define desc Wine is a program which allows running Microsoft Windows programs \
(including DOS, Windows 3.x and Win32 executables) on Unix. It \
consists of a program loader which loads and executes a Microsoft \
Windows binary, and a library (called Winelib) that implements Windows \
API calls using their Unix or X11 equivalents.  The library may also \
be used for porting Win32 code into native Unix executables.

%ifarch x86_64
%package -n	%{wine}
Summary:	WINE Is Not An Emulator - runs MS Windows programs
Group:		Emulators
Suggests:	wine32 = %{EVRD}
Suggests:	wine64-gecko
Suggests:	libncursesw.so.5%{_arch_tag_suffix}
Suggests:	libncurses.so.5%{_arch_tag_suffix}
%else
# on 32-bit we always want wine32 package
Requires:	wine32 = %{EVRD}
%endif

%rename		%{wine}-utils
%rename		%{wine}-full
%rename		%{libname}-capi
%rename		%{libname}-twain
%rename		%{libname}
Provides:	wine-bin = %{EVRD}
Requires:	xmessage
Suggests:	sane-frontends
# wine dlopen's these, so let's add the dependencies ourself
Requires:	libfreetype.so.6%{_arch_tag_suffix}
Requires:	libasound.so.2%{_arch_tag_suffix}
Requires:	libXrender.so.1%{_arch_tag_suffix}
%if "%{distepoch}" >= "2012.0"
Requires:      libpng15.so.15%{_arch_tag_suffix}
%else
Requires:      libpng12.so.0%{_arch_tag_suffix}
%endif
Requires(post):	desktop-file-utils
Requires(postun):	desktop-file-utils
Requires(post):	desktop-common-data
Requires(postun):	desktop-common-data
Requires(preun):	rpm-helper
Requires(post):	rpm-helper
Conflicts:	%{wine} < 1:0.9-3mdk
%ifarch %{ix86}
Conflicts:	wine64
%else
Conflicts:	wine
%endif

%description
%desc

%ifarch x86_64
%description -n	%{wine}
%desc

This package contains the Win64 version of Wine. You need the wine32
package from the 32-bit repository to be able to run 32-bit applications.
%endif

%ifarch %{ix86}
%package -n	wine32
Summary:	32-bit support for Wine
Group:		Emulators
# This is not an EVR-specific requirement, as otherwise on x86_64 urpmi could
# resolve the dependency to wine64 even on upgrades, and therefore replace
# wine+wine32 installation with a wine32+wine64 installation. - Anssi
Requires:	wine-bin
Conflicts:	wine < 1:1.2-0.rc7.1
Conflicts:	wine64 < 1:1.2-0.rc7.1
# (Anssi) If wine-gecko is not installed, wine pops up a dialog on first
# start proposing to download wine-gecko from sourceforge, while recommending
# to use distribution packages instead. Therefore suggest wine-gecko here:
Suggests:	wine-gecko
Suggests:	libncursesw.so.5
Suggests:	libncurses.so.5

%description -n	wine32
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix.

This package contains the files needed to support 32-bit Windows
programs.
%endif

%package -n	%{wine}-devel
Summary:	Static libraries and headers for %{name}
Group:		Development/C
Requires:	%{wine} = %{EVRD}
%rename		%{devname}
Obsoletes:	%{mklibname -d wine 1} < %{EVRD}
%ifarch %{ix86}
Conflicts:	wine64-devel
%else
Conflicts:	wine-devel
%endif

%description -n	%{wine}-devel
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix.

%{wine}-devel contains the libraries and header files needed to
develop programs which make use of wine.

Wine is often updated.

%prep
%if "%beta" != ""
%setup -q -n %name-%version-%beta
%else
%setup -q
%endif
%patch1 -p0 -b .chinese
%patch108 -p1 -b .conf
%patch200 -p1
sed -i 's,@MDKVERSION@,%{mdkversion},' dlls/ntdll/server.c

%build
%ifarch %ix86
# (Anssi 04/2008) bug #39604
# Some protection systems complain "debugger detected" with our
# -fomit-frame-pointer flag, so disable it.
export CFLAGS="%{optflags} -fno-omit-frame-pointer"
%endif

# (Anssi 04/2008)
# If icotool is present, it is used to rebuild icon files. It is in contrib
# so we do not do that; this is here to ensure that installed icoutils does
# not change build behaviour.
export ICOTOOL=false

autoreconf
%configure2_5x	--with-pulse \
		--without-nas \
%ifarch x86_64
		--enable-win64
%endif

%make depend
%make

%install
rm -rf %{buildroot}
%makeinstall_std LDCONFIG=/bin/true

# Danny: dirty:
# install -m755 tools/fnt2bdf -D %{buildroot}%{_bindir}/fnt2bdf

# Allow users to launch Windows programs by just clicking on the .exe file...
install -m755 %{SOURCE2} -D %{buildroot}%{_initrddir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/xdg/menus/applications-merged
cat > %{buildroot}%{_sysconfdir}/xdg/menus/applications-merged/mandriva-%{name}.menu <<EOF
<!DOCTYPE Menu PUBLIC "-//freedesktop//DTD Menu 1.0//EN"
"http://www.freedesktop.org/standards/menu-spec/menu-1.0.dtd">
<Menu>
    <Name>Applications</Name>
    <Menu>
        <Name>Tools</Name>
        <Menu>
            <Name>Emulators</Name>
            <Menu>
                <Name>Wine</Name>
                <Directory>mandriva-%{name}.directory</Directory>
                <Include>
                    <Category>X-MandrivaLinux-MoreApplications-Emulators-Wine</Category>
                </Include>
            </Menu>
        </Menu>
    </Menu>
</Menu>
EOF

mkdir -p %{buildroot}%{_datadir}/desktop-directories
cat > %{buildroot}%{_datadir}/desktop-directories/mandriva-%{name}.directory <<EOF
[Desktop Entry]
Name=Wine
Icon=%{name}
Type=Directory
EOF

mkdir -p %{buildroot}%{_datadir}/applications/
for i in	winecfg:Configurator \
		notepad:Notepad \
		winefile:File\ Manager \
		regedit:Registry\ Editor \
		winemine:Minesweeper \
		wineboot:Reboot \
		"wineconsole cmd":Command\ Line \
		"wine uninstaller:Wine Software Uninstaller";
do cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-`echo $i|cut -d: -f1`.desktop << EOF
[Desktop Entry]
Name=`echo $i|cut -d: -f2`
Comment=`echo $i|cut -d: -f2`
Exec=`echo $i|cut -d: -f1`
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Emulators-Wine;
EOF
done

# Categories=Emulator does nothing and is added as a workaround to kde #27700
desktop-file-install	--vendor="" \
			--add-mime-type=application/x-zip-compressed \
			--remove-mime-type=application/x-zip-compressed \
			--add-category=Emulator \
			--dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/wine.desktop

%ifarch x86_64
# fix the binary name
sed -i 's,Exec=wine ,Exec=wine64 ,' %{buildroot}%{_datadir}/applications/wine.desktop
%endif

install -d %{buildroot}{%{_liconsdir},%{_iconsdir},%{_miconsdir}}

# winecfg icon
convert dlls/user32/resources/oic_winlogo.ico[8] %{buildroot}%{_miconsdir}/%{name}.png
convert dlls/user32/resources/oic_winlogo.ico[7] %{buildroot}%{_iconsdir}/%{name}.png
convert dlls/user32/resources/oic_winlogo.ico[6] %{buildroot}%{_liconsdir}/%{name}.png

# notepad icon
convert programs/notepad/notepad.ico[2] %{buildroot}%{_miconsdir}/notepad.png
convert programs/notepad/notepad.ico[7] %{buildroot}%{_iconsdir}/notepad.png
convert programs/notepad/notepad.ico[8] %{buildroot}%{_liconsdir}/notepad.png
# winefile icon
convert programs/winefile/winefile.ico[2] %{buildroot}%{_miconsdir}/winefile.png
convert programs/winefile/winefile.ico[8] %{buildroot}%{_iconsdir}/winefile.png
convert programs/winefile/winefile.ico[7] %{buildroot}%{_liconsdir}/winefile.png
# regedit icon
convert programs/regedit/regedit.ico[2] %{buildroot}%{_miconsdir}/regedit.png
convert programs/regedit/regedit.ico[8] %{buildroot}%{_iconsdir}/regedit.png
convert programs/regedit/regedit.ico[7] %{buildroot}%{_liconsdir}/regedit.png
# winemine icon
convert programs/winemine/winemine.ico[2] %{buildroot}%{_miconsdir}/winemine.png
convert programs/winemine/winemine.ico[8] %{buildroot}%{_iconsdir}/winemine.png
convert programs/winemine/winemine.ico[7] %{buildroot}%{_liconsdir}/winemine.png

# wine uninstaller icon:
convert programs/msiexec/msiexec.ico[2] %{buildroot}%{_miconsdir}/msiexec.png
convert programs/msiexec/msiexec.ico[8] %{buildroot}%{_iconsdir}/msiexec.png
convert programs/msiexec/msiexec.ico[7] %{buildroot}%{_liconsdir}/msiexec.png

# change the icons in the respective .desktop files, in order:
sed -i 's,Icon=%{name},Icon=notepad,' %{buildroot}%{_datadir}/applications/mandriva-wine-notepad.desktop
sed -i 's,Icon=%{name},Icon=winefile,' %{buildroot}%{_datadir}/applications/mandriva-wine-winefile.desktop
sed -i 's,Icon=%{name},Icon=regedit,' %{buildroot}%{_datadir}/applications/mandriva-wine-regedit.desktop
sed -i 's,Icon=%{name},Icon=winemine,' %{buildroot}%{_datadir}/applications/mandriva-wine-winemine.desktop
sed -i 's,Icon=%{name},Icon=msiexec,' "%{buildroot}%{_datadir}/applications/mandriva-wine-wine uninstaller.desktop"

%ifarch x86_64
chrpath -d %{buildroot}%{_bindir}/{wine64,wineserver,wmc,wrc} %{buildroot}%{_libdir}/%{name}/*.so
%else
chrpath -d %{buildroot}%{_bindir}/{wine,wineserver,wmc,wrc} %{buildroot}%{_libdir}/%{name}/*.so
%endif

%ifarch x86_64
cat > README.install.urpmi <<EOF
This is the Win64 version of Wine. This version can only be used to run
64-bit Windows applications as is. For running 32-bit Windows applications,
you need to also install the 'wine32' package from the 32-bit repository.
EOF
%endif

%preun -n %{wine}
%_preun_service %{name}

%post -n %{wine}
%_post_service %{name}

%files -n %{wine}
%doc ANNOUNCE AUTHORS README
%ifarch x86_64
%doc README.install.urpmi
%{_bindir}/wine64
%{_bindir}/wine64-preloader
%endif
%{_initrddir}/%{name}
%{_bindir}/winecfg
%{_bindir}/wineconsole*
%{_bindir}/wineserver
%{_bindir}/wineboot
%{_bindir}/function_grep.pl
#%{_bindir}/wineprefixcreate
%{_bindir}/msiexec
%{_bindir}/notepad
%{_bindir}/regedit
%{_bindir}/winemine
%{_bindir}/winepath
%{_bindir}/regsvr32
%{_bindir}/winefile
%{_mandir}/man1/wine.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wine.1*
%lang(de) %{_mandir}/de.UTF-8/man1/winemaker.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wineserver.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/*
%{_mandir}/man1/wineserver.1*
%{_mandir}/man1/msiexec.1*
%{_mandir}/man1/notepad.1*
%{_mandir}/man1/regedit.1*
%{_mandir}/man1/regsvr32.1*
%{_mandir}/man1/wineboot.1*
%{_mandir}/man1/winecfg.1*
%{_mandir}/man1/wineconsole.1*
%{_mandir}/man1/winecpp.1*
%{_mandir}/man1/winefile.1*
%{_mandir}/man1/winemine.1*
%{_mandir}/man1/winepath.1*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/generic.ppd
%{_datadir}/%{name}/%{name}.inf
%{_datadir}/%{name}/l_intl.nls
%{_datadir}/applications/*.desktop
%{_sysconfdir}/xdg/menus/applications-merged/mandriva-%{name}.menu
%{_datadir}/desktop-directories/mandriva-%{name}.directory
%dir %{_datadir}/wine/fonts
%{_datadir}/wine/fonts/*
%{_miconsdir}/*.png
%{_iconsdir}/*.png
%{_liconsdir}/*.png

%ifarch %{ix86}
%files -n wine32
%{_bindir}/wine
%{_bindir}/wine-preloader
%endif

%{_libdir}/libwine*.so.%{major}*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.cpl.so
%{_libdir}/%{name}/*.drv.so
%{_libdir}/%{name}/*.dll.so
%{_libdir}/%{name}/*.exe.so
%{_libdir}/%{name}/*.acm.so
%{_libdir}/%{name}/*.ocx.so
%ifarch %{ix86}
%{_libdir}/%{name}/*.vxd.so
%{_libdir}/%{name}/*16.so
%endif
%{_libdir}/%{name}/*.tlb.so
%{_libdir}/%{name}/*.ds.so
%{_libdir}/%{name}/*.sys.so
%{_libdir}/%{name}/fakedlls

%files -n %{wine}-devel
%{_libdir}/%{name}/*.a
%{_libdir}/libwine*.so
%{_libdir}/%{name}/*.def
%{_includedir}/*
# %{_bindir}/fnt2bdf
%{_bindir}/wmc
%{_bindir}/wrc
%{_bindir}/winebuild
%{_bindir}/winegcc
%{_bindir}/wineg++
%{_bindir}/winecpp
%{_bindir}/widl
%{_bindir}/winedbg
%{_bindir}/winemaker
%{_bindir}/winedump
%{_mandir}/man1/wmc.1*
%{_mandir}/man1/wrc.1*
%{_mandir}/man1/winebuild.1*
%{_mandir}/man1/winemaker.1*
%{_mandir}/man1/winedump.1*
%{_mandir}/man1/widl.1*
%{_mandir}/man1/winedbg.1*
%{_mandir}/man1/wineg++.1*
%{_mandir}/man1/winegcc.1*
%{_mandir}/pl.UTF-8/man1/wine.1*

%changelog
* Sat Sep 01 2012 Zombie Ryushu <ryushu@mandriva.org> 1:1.5.12-1mdv2012.0
+ Revision: 816157
- Upgrade to 1.5.12

* Tue Aug 28 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 1:1.5.11-1.2
+ Revision: 815962
- correct buildrequires on libgphoto-devel
- spec file clean

  + Zombie Ryushu <ryushu@mandriva.org>
    - Why is the cluster rejecting this?

* Tue Aug 21 2012 Zombie Ryushu <ryushu@mandriva.org> 1:1.5.11-1
+ Revision: 815544
- Upgrade to 1.5.11

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - add suggests on libncurses & libncursesw

* Thu Aug 02 2012 Zombie Ryushu <ryushu@mandriva.org> 1:1.5.10-1
+ Revision: 811627
- Upgrade to 1.5.10

* Thu Jul 19 2012 Zombie Ryushu <ryushu@mandriva.org> 1:1.5.9-1
+ Revision: 810145
- Upgrade to 1.5.9

* Thu Jul 05 2012 Zombie Ryushu <ryushu@mandriva.org> 1:1.5.8-1
+ Revision: 808157
- Upgrade to 1.5.8

* Sat Jun 30 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1:1.5.7-1
+ Revision: 807634
- new version
- update download url

* Sat Jun 09 2012 Zombie Ryushu <ryushu@mandriva.org> 1:1.5.6-1
+ Revision: 804099
- Upgrade to 1.5.6

* Tue May 29 2012 Zombie Ryushu <ryushu@mandriva.org> 1:1.5.5-1
+ Revision: 801175
- fnt2bdf
- Upgrade to 1.5.5

* Mon May 14 2012 Zombie Ryushu <ryushu@mandriva.org> 1:1.5.4-1
+ Revision: 798763
- Upgrade to 1.5.4

* Sat Apr 28 2012 Zombie Ryushu <ryushu@mandriva.org> 1:1.5.3-1
+ Revision: 794200
- Upgrade to 1.5.3

* Fri Apr 20 2012 Zombie Ryushu <ryushu@mandriva.org> 1:1.5.2-1
+ Revision: 792410
- remove oname
- Upgrade to 1.5.2
- setup stage directory

* Mon Apr 02 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1:1.5.1-1
+ Revision: 788714
- Update to 1.5.1

* Thu Mar 08 2012 Zombie Ryushu <ryushu@mandriva.org> 1:1.4-1
+ Revision: 783218
- Remove Pre-Release flahs
- Upgrade to 1.4
- Upgrade to 1.4

* Sun Mar 04 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1:1.4-0.rc6.1
+ Revision: 782089
- Update to rc6

  + Dmitry Mikhirev <dmikhirev@mandriva.org>
    - use %%mark64 for requires

* Tue Feb 28 2012 Zombie Ryushu <ryushu@mandriva.org> 1:1.4-0.rc5.1
+ Revision: 781187
- Upgrade to rc5

* Mon Feb 20 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1:1.4-0.rc4.2
+ Revision: 778115
- use canonical soname dependency on libpng

* Fri Feb 17 2012 Zombie Ryushu <ryushu@mandriva.org> 1:1.4-0.rc4.1
+ Revision: 776309
- Upgrade to rc4

* Thu Feb 16 2012 Zombie Ryushu <ryushu@mandriva.org> 1:1.4-0.rc3.1
+ Revision: 775112
- Upgrade to rc3

* Sat Feb 04 2012 Zombie Ryushu <ryushu@mandriva.org> 1:1.4-0.rc2.1
+ Revision: 771074
- Upgrade to rc2

* Tue Jan 31 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1:1.4-0.rc1.1
+ Revision: 770033
- Require the correct version of libpng (1.5, not 1.2)
- Update to 1.4-rc1
- Fix build with current rpmlint rules

* Sat Jan 14 2012 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.37-1
+ Revision: 760871
- Upgrade to 1.3.37

* Sun Jan 01 2012 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.36-1
+ Revision: 748543
- Upgrade to 1.3.36
- Upgrade to 1.3.36

* Sat Dec 17 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.35-1
+ Revision: 743210
- Upgrade to 1.3.35

* Fri Dec 09 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.34-1
+ Revision: 739290
- Upgrade to 1.3.34

* Sat Nov 19 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.33-1
+ Revision: 731770
- Upgrade to 1.3.33

* Sat Nov 05 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.32-1
+ Revision: 719043
- Upgrade to 1.3.32

* Sat Oct 22 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.31-1
+ Revision: 705643
- Upgrade to 1.3.31

* Tue Oct 11 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.30-1
+ Revision: 704325
- Upgrade to 1.1.30
- upgrade to 1.3.29

* Sat Sep 10 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 1:1.3.28-1
+ Revision: 699297
- new version
- haul out some trash
- use %%{EVRD} & %%rename macros

* Tue Sep 06 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.27-1
+ Revision: 698389
- Fix missing backslash
- Upgrade to 1.3.27 and deprecated un-needed Winepulse patches

* Sat Aug 06 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.26-1
+ Revision: 693381
- Upgrade to 1.3.26

* Thu Aug 04 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.25-1
+ Revision: 693162
- Deprecate Winepulse
- Upgrade to 1.3.25

* Sat Jul 09 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.24-1
+ Revision: 689372
- Upgrade to 1.3.24

* Sat Jun 25 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.23-1
+ Revision: 687173
- Upgrade to 1.3.23

* Sun Jun 12 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.22-2.2
+ Revision: 684354
- Update Build deps because some were missing
- Fix man page

* Fri Jun 10 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.22-2
+ Revision: 684188
- Fix man page
- Fix man page
- Upgrade to 1.3.22

* Sat May 28 2011 Funda Wang <fwang@mandriva.org> 1:1.3.21-1
+ Revision: 680398
- update to new version 1.3.21

* Sat May 14 2011 Funda Wang <fwang@mandriva.org> 1:1.3.20-2
+ Revision: 674586
- rediff winepulse configure.ac patch

  + Zombie Ryushu <ryushu@mandriva.org>
    - Upgrade 1.3.20

* Mon May 09 2011 Anssi Hannula <anssi@mandriva.org> 1:1.3.19-2
+ Revision: 673040
- add suggests on wine64-gecko in wine64
- update old comment in .spec

* Sun May 01 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.19-1
+ Revision: 661378
- Fix Winepulse
- Fix Winepulse
- Upgrade to 1.3.19

* Thu Apr 21 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.18-1
+ Revision: 656561
- Upgrade to wine 1.3.18

* Sat Apr 09 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.17-2
+ Revision: 652133
- Fix missing build deps

* Sat Apr 09 2011 Funda Wang <fwang@mandriva.org> 1:1.3.17-1
+ Revision: 652086
- X11-devel is not needed
- new version 1.3.17
- rediff winpusle configure patch

  + Zombie Ryushu <ryushu@mandriva.org>
    - Reset Releaseflag
    - Upgrade to 1.3.16
    - add X11-devel
    - compile with gstreamer
    - Add gettext-devel

* Sun Mar 13 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.15-2
+ Revision: 644144
- Upgrade to 1.3.15 and restore Winepulse patch

* Sat Feb 26 2011 Funda Wang <fwang@mandriva.org> 1:1.3.14-2
+ Revision: 639995
- rebuild

* Fri Feb 18 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.14-1
+ Revision: 638605
- Update to 1.3.14

* Sat Feb 05 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.13-1
+ Revision: 636021
- Update to 1.3.13

* Wed Jan 26 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.3.12-1
+ Revision: 633001
- remove deprecated patch preventing building
- Upgrade to 1.3.12

* Fri Jan 07 2011 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.3.11-1mdv2011.0
+ Revision: 629667
- update to 1.3.11

  + Funda Wang <fwang@mandriva.org>
    - tighten BR

* Fri Dec 24 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.3.10-1mdv2011.0
+ Revision: 624675
- update to 1.3.10
- rediff the winepulse-configure.ac patch
- update the file list

* Fri Dec 17 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.3.9-2mdv2011.0
+ Revision: 622434
- make the prelink BR condintional, so that the package can be backported

* Fri Dec 10 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.3.9-1mdv2011.0
+ Revision: 620457
- update to 1.3.9
- rediff winepulse-configure.ac patch
- add gstreamer*-devel as BR for gstreamer support
- add BR prelink

* Wed Dec 01 2010 Funda Wang <fwang@mandriva.org> 1:1.3.8-2mdv2011.0
+ Revision: 604301
- update file list
- new verison 1.3.8

* Sat Nov 13 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.3.7-1mdv2011.0
+ Revision: 597055
- Update to 1.3.7

* Sat Oct 30 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.3.6-1mdv2011.0
+ Revision: 590647
- update to wine-1.3.6
- rediff winepulse-configure.ac manually for now
- update str-fmt patch

* Sat Oct 16 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.3.5-1mdv2011.0
+ Revision: 585933
- update to 1.3.5

* Sat Oct 02 2010 Anssi Hannula <anssi@mandriva.org> 1:1.3.4-2mdv2011.0
+ Revision: 582531
- remove version-specific dependency on wine-bin from wine32 to avoid
  possible upgrade problems on x86_64 (32-bit installations were replaced
  with 32+64-bit installations)

* Sat Oct 02 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.3.4-1mdv2011.0
+ Revision: 582416
- update to 1.3.4
- update two of pulseaudio patches (winepulse and winepulse-configure.ac) to 0.39

* Sat Sep 18 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.3.3-1mdv2011.0
+ Revision: 579758
- new version, 1.3.3
- update to 1.3.2

* Fri Aug 20 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.3.1-1mdv2011.0
+ Revision: 571519
- update to 1.3.1

* Fri Jul 30 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.3.0-1mdv2011.0
+ Revision: 563794
- update to 1.3.0

* Wed Jul 21 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.2-3mdv2011.0
+ Revision: 556588
- provide a .desktop file for 'wine uninstaller'

* Sat Jul 17 2010 Thierry Vignaud <tv@mandriva.org> 1:1.2-2mdv2011.0
+ Revision: 554460
- BuildRequires: gnutls-devel tiff-devel libv4l-devel according to annouce

* Fri Jul 16 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.2-1mdv2011.0
+ Revision: 554424
- update to 1.2 final
- use the icons of notepad,winefile,regedit,winemine for their respective .desktop files

* Sat Jul 10 2010 Anssi Hannula <anssi@mandriva.org> 1:1.2-0.rc7.1mdv2011.0
+ Revision: 549898
- split 32-bit package to 'wine' and 'wine32'
  o 'wine32' contains only the files needed for 32-bit support on 64-bit
  o 'wine' contains all the other files
  o one can now install both 'wine64' and 'wine32' on x86_64 and run both
    64-bit and 32-bit applications
  o on 32-bit systems both 'wine' and 'wine32' are needed
- fix .desktop file of wine64

  + Ahmad Samir <ahmadsamir@mandriva.org>
    - new release, 1.2-rc7
    - update all winepulse patches to 0.38

* Mon Jun 21 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.2-0.rc4.1mdv2010.1
+ Revision: 548353
- new upstream release, 1.2-rc4

* Sat Jun 12 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.2-0.rc3.1mdv2010.1
+ Revision: 547953
- new upstream release 1.2-rc3
- update winepulse-0.36-winecfg to 0.37

* Mon May 31 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.2-0.rc2.2mdv2010.1
+ Revision: 546774
- add requires on libpng3 as it's dlopened fixes winemenubuilder crash
  (mdv #59578)

* Sat May 29 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.2-0.rc2.1mdv2010.1
+ Revision: 546574
- new upstream release 1.2-rc2

* Sun May 09 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.1.44-1mdv2010.1
+ Revision: 544287
- update to 1.1.44
- update to winepulse-0.36-winecfg.patch
- stay with manually rediffed winepulse-configure.ac.patch as upstream's still
  doesn't work

* Thu May 06 2010 Anssi Hannula <anssi@mandriva.org> 1:1.1.43-2mdv2010.1
+ Revision: 542937
- require dlopened libxrender1 (fixes at least Spotify issues, reported
  by Mikko Kuivaniemi)

* Fri Apr 16 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.1.43-1mdv2010.1
+ Revision: 535640
- new upstream release 1.1.43
- fix file list

* Fri Apr 02 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.1.42-1mdv2010.1
+ Revision: 530790
- new upstream release 1.1.42
- remove the winepule makefile sed hack, fixed upstream
- update winepulse patch to 0.36
- update winepule-winecfg patch to 0.34
- rediff winepulse-configure.ac patch manually until winepulse upstream updates it

* Sat Mar 20 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.1.41-1mdv2010.1
+ Revision: 525418
- add a hack to make it build with winepulse
- parallel make works again
- disable esd, it's old, and pulseaudio (via winepulse) can do esd

  + Funda Wang <fwang@mandriva.org>
    - new version 1.1.41

* Sat Mar 13 2010 Funda Wang <fwang@mandriva.org> 1:1.1.40-1mdv2010.1
+ Revision: 518737
- build non-parallelly
- new version 1.1.40

* Sat Feb 20 2010 Emmanuel Andry <eandry@mandriva.org> 1:1.1.39-1mdv2010.1
+ Revision: 508703
- drop obsolete esound-devel BR
- New version 1.1.39

* Sat Feb 06 2010 Funda Wang <fwang@mandriva.org> 1:1.1.38-1mdv2010.1
+ Revision: 501310
- update winepulse patches
- New version 1.1.38

  + Anssi Hannula <anssi@mandriva.org>
    - add notices to the description and README.install.urpmi of x86_64
      wine64 packages that explain that it cannot be used to run 32-bit
      Windows applications

* Fri Jan 22 2010 Frederik Himpe <fhimpe@mandriva.org> 1:1.1.37-1mdv2010.1
+ Revision: 495081
- update to new version 1.1.37

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - add suggests on sane-frontends (#57193)

* Tue Jan 12 2010 Anssi Hannula <anssi@mandriva.org> 1:1.1.36-3mdv2010.1
+ Revision: 490060
- move main description block below tags (fixes tags and description in
  32-bit build)

* Mon Jan 11 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 1:1.1.36-2mdv2010.1
+ Revision: 489885
- add conflicts on wine64 for wine package and vice versa
- suggest wine-gecko only for 32 bit wine
- drop library package as library isn't of much use without binary...
- fix so that dependencies, obsoletes etc. gets in place for wine64 package
- do 64 bit build again (with some improvements, still not parallel installable
  with 32 bit build though..)
- remove backwards compatibility for ancient menu structure
- add back service scriptlets that got accidentally removed earlier...

* Sat Jan 09 2010 Funda Wang <fwang@mandriva.org> 1:1.1.36-1mdv2010.1
+ Revision: 488104
- update file list again
- update file list
- New version 1.1.36

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - disable 64 bit build for now..
    - make 32 bit library dependencies specific to %%{ix86} only
    - ditch requires_exceptions, wine dlopen()'s all libraries anyways..
    - get rid of some pre/post requires that were required in dead scriptlets
    - get rid of obsolete scriptlets
    - add initial support for wine64...
    - enable pulseaudio patches that I for some reason accidentally disabled previously..

* Sat Dec 19 2009 Funda Wang <fwang@mandriva.org> 1:1.1.35-1mdv2010.1
+ Revision: 480043
- new version 1.1.35

  + Anssi Hannula <anssi@mandriva.org>
    - add suggests on wine-gecko

* Mon Dec 07 2009 Emmanuel Andry <eandry@mandriva.org> 1:1.1.34-3mdv2010.1
+ Revision: 474373
- update P401

* Sun Dec 06 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 1:1.1.34-2mdv2010.1
+ Revision: 474268
- add library dependencies for alsa & freetype
- ditch nonsense explicit dependency on library package

* Sat Dec 05 2009 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.1.34-1mdv2010.1
+ Revision: 473851
- Update to 1.1.34

* Sat Nov 14 2009 Funda Wang <fwang@mandriva.org> 1:1.1.33-1mdv2010.1
+ Revision: 465944
- new version 1.1.33

* Sat Oct 24 2009 Frederic Crozat <fcrozat@mandriva.com> 1:1.1.32-1mdv2010.0
+ Revision: 459155
- Release 1.1.32

* Mon Oct 19 2009 Emmanuel Andry <eandry@mandriva.org> 1:1.1.31-2mdv2010.0
+ Revision: 458259
- reenable and update P400

* Sat Oct 10 2009 Zombie Ryushu <ryushu@mandriva.org> 1:1.1.31-1mdv2010.0
+ Revision: 456511
- Remove Deprecated Pulse patch
- Upgrade to version 1.1.31

* Sat Sep 26 2009 Emmanuel Andry <eandry@mandriva.org> 1:1.1.30-1mdv2010.0
+ Revision: 449458
- New version 1.1.30
- update P400 and P402
- BR openal-devel

  + Anssi Hannula <anssi@mandriva.org>
    - add missing buildrequires on gphoto2-devel unixODBC-devel

* Mon Sep 07 2009 Emmanuel Andry <eandry@mandriva.org> 1:1.1.29-1mdv2010.0
+ Revision: 432638
- New version 1.1.29
- update P402
- BR libmpg123-devel

* Sat Aug 22 2009 Funda Wang <fwang@mandriva.org> 1:1.1.28-1mdv2010.0
+ Revision: 419578
- fix file list
- New version 1.1.28

* Wed Aug 19 2009 Emmanuel Andry <eandry@mandriva.org> 1:1.1.27-3mdv2010.0
+ Revision: 418119
- update winepulse patches
- add menu entries for wineboot and wineconsole

* Mon Aug 10 2009 Emmanuel Andry <eandry@mandriva.org> 1:1.1.27-2mdv2010.0
+ Revision: 414323
- BR gsm-devel
- drop old 2007.0 conditionnals

* Sat Aug 08 2009 Funda Wang <fwang@mandriva.org> 1:1.1.27-1mdv2010.0
+ Revision: 411565
- rediff pulseaudio patch
- new version 1.1.27

* Sat Jul 25 2009 Emmanuel Andry <eandry@mandriva.org> 1:1.1.26-2mdv2010.0
+ Revision: 399779
- update winepulse to 0.29

* Sat Jul 18 2009 Funda Wang <fwang@mandriva.org> 1:1.1.26-1mdv2010.0
+ Revision: 396970
- update wine patch
- new version 1.1.26

* Sun Jul 05 2009 Funda Wang <fwang@mandriva.org> 1:1.1.25-1mdv2010.0
+ Revision: 392574
- New version 1.1.25

* Sun Jun 07 2009 Funda Wang <fwang@mandriva.org> 1:1.1.23-1mdv2010.0
+ Revision: 383427
- fix str fmt
- New version 1.1.23

* Sat May 23 2009 Funda Wang <fwang@mandriva.org> 1:1.1.22-1mdv2010.0
+ Revision: 378877
- New version 1.1.22

* Sat May 09 2009 Funda Wang <fwang@mandriva.org> 1:1.1.21-1mdv2010.0
+ Revision: 373696
- New version 1.1.21

* Wed Apr 29 2009 Emmanuel Andry <eandry@mandriva.org> 1:1.1.20-1mdv2010.0
+ Revision: 369137
- New version 1.1.20

* Tue Apr 14 2009 Emmanuel Andry <eandry@mandriva.org> 1:1.1.19-1mdv2009.1
+ Revision: 366908
- New version 1.1.19
- update winepulse driver

* Wed Mar 18 2009 Emmanuel Andry <eandry@mandriva.org> 1:1.1.17-2mdv2009.1
+ Revision: 357306
- disable nas (#48843)

* Sat Mar 14 2009 Emmanuel Andry <eandry@mandriva.org> 1:1.1.17-1mdv2009.1
+ Revision: 355121
- fix chrpath arguments
- update files list
- add winepulse sound driver (fedora)
- New version 1.1.17
- drop patch 109 (merged upstream)

  + Anssi Hannula <anssi@mandriva.org>
    - add back 64-bit comments that were erroneously removed in r355000

* Sat Feb 28 2009 Funda Wang <fwang@mandriva.org> 1:1.1.16-1mdv2009.1
+ Revision: 346000
- fix file list
- New version 1.1.16

* Fri Feb 13 2009 Emmanuel Andry <eandry@mandriva.org> 1:1.1.15-1mdv2009.1
+ Revision: 340139
- New version 1.1.15
- drop P110, fixed diffently upstream

  + Anssi Hannula <anssi@mandriva.org>
    - update comments in spec about wine64 according to recent developments

* Fri Jan 30 2009 Funda Wang <fwang@mandriva.org> 1:1.1.14-1mdv2009.1
+ Revision: 335650
- new version 1.1.14

* Sun Jan 18 2009 Funda Wang <fwang@mandriva.org> 1:1.1.13-1mdv2009.1
+ Revision: 330836
- New version 1.1.13

* Sat Jan 03 2009 Funda Wang <fwang@mandriva.org> 1:1.1.12-1mdv2009.1
+ Revision: 323571
- New version 1.1.12

* Sun Dec 21 2008 Funda Wang <fwang@mandriva.org> 1:1.1.11-1mdv2009.1
+ Revision: 316867
- new version 1.1.11

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Sat Dec 06 2008 Funda Wang <fwang@mandriva.org> 1:1.1.10-1mdv2009.1
+ Revision: 310958
- New version 1.1.10

* Sat Nov 22 2008 Funda Wang <fwang@mandriva.org> 1:1.1.9-1mdv2009.1
+ Revision: 305697
- wineshelllink is merged into winemenubuilder

  + Emmanuel Andry <eandry@mandriva.org>
    - New version

* Sat Nov 08 2008 Funda Wang <fwang@mandriva.org> 1:1.1.8-2mdv2009.1
+ Revision: 300925
- New version 1.1.8

* Wed Oct 29 2008 Funda Wang <fwang@mandriva.org> 1:1.1.7-2mdv2009.1
+ Revision: 298147
- better chinese font substitute list

* Tue Oct 28 2008 Funda Wang <fwang@mandriva.org> 1:1.1.7-1mdv2009.1
+ Revision: 297804
- New version 1.1.7

* Sat Oct 11 2008 Funda Wang <fwang@mandriva.org> 1:1.1.6-1mdv2009.1
+ Revision: 291790
- New version 1.1.6

* Sat Sep 06 2008 Funda Wang <fwang@mandriva.org> 1:1.1.4-1mdv2009.0
+ Revision: 281787
- New version 1.1.4

* Sat Aug 23 2008 Funda Wang <fwang@mandriva.org> 1:1.1.3-1mdv2009.0
+ Revision: 275341
- New version 1.1.3

* Fri Jul 25 2008 Funda Wang <fwang@mandriva.org> 1:1.1.2-1mdv2009.0
+ Revision: 249803
- add cpl.so
- New version 1.1.2

  + Emmanuel Andry <eandry@mandriva.org>
    - New version

* Sat Jun 28 2008 Funda Wang <fwang@mandriva.org> 1:1.1.0-1mdv2009.0
+ Revision: 229612
- New version 1.1.0

* Tue Jun 17 2008 Anssi Hannula <anssi@mandriva.org> 1:1.0-1mdv2009.0
+ Revision: 222989
- final 1.0

* Sat Jun 14 2008 Funda Wang <fwang@mandriva.org> 1:1.0-0.rc5.1mdv2009.0
+ Revision: 219112
- New version 1.0 rc5

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sat Jun 07 2008 Funda Wang <fwang@mandriva.org> 1:1.0-0.rc4.1mdv2009.0
+ Revision: 216649
- New version 1.0 rc4
- disable patch0, it seems there is a better solution upstream

* Mon Jun 02 2008 Funda Wang <fwang@mandriva.org> 1:1.0-0.rc3.1mdv2009.0
+ Revision: 214176
- fix for newer openssl
- New version 1.0 rc3

* Fri May 23 2008 Anssi Hannula <anssi@mandriva.org> 1:1.0-0.rc2.1mdv2009.0
+ Revision: 210752
- new version
- update file list

* Tue May 13 2008 Anssi Hannula <anssi@mandriva.org> 1:1.0-0.rc1.2mdv2009.0
+ Revision: 206812
- make d: $HOME again
- make e: cdrom on 2008.0 and older, not on 2008.1 as /media/cdrom does
  not exist by default
- use /mnt instead of /media on 2007.1 and earlier

* Sun May 11 2008 Anssi Hannula <anssi@mandriva.org> 1:1.0-0.rc1.1mdv2009.0
+ Revision: 205445
- new version
- adapt mdkconf.patch for rewritten dosdevices creation
- change dos device mappings (will affect newly created wine prefixes
  only):
  o reintroduce D: => /media/cdrom mapping, it is not handled
    automatically
  o change home dir from D: to E:
  o drop E: => ~/tmp mapping
  o replace COM4 => /dev/modem with COM4 => /dev/ttyUSB0
  o drop explicit COM1-3 and LPT1 mappings, they are handled
    automatically by wine (it maps them to /dev/ttySX and /dev/lpX)
- drop "My Documents" directory from Windows directory, it was
  apparently inadvertently added on an earlier rediffing of mdkconf.patch
- drop duplicate buildroot entry
- drop now unneeded CVS file cleaning
- drop unsupported option --enable-opengl (it is enabled by default)
- use parallel make for make depend
- drop unneeded additional make and make install calls in programs/
  subdirectory

* Tue Apr 22 2008 Anssi Hannula <anssi@mandriva.org> 1:0.9.60-1mdv2009.0
+ Revision: 196630
- new version
- rediff mdkconf patch
- update file list

* Sun Apr 13 2008 Anssi Hannula <anssi@mandriva.org> 1:0.9.59-1mdv2009.0
+ Revision: 192650
- do not buildrequire icoutils for now
- new version
- rediff fontforge-symbol-font.patch and add comments
- buildrequires valgrind icoutils librsvg
- fix "debugger detected" errors with some protection systems (#39604)
  by disabling -fomit-frame-pointer

* Sun Mar 30 2008 Anssi Hannula <anssi@mandriva.org> 1:0.9.58-2mdv2008.1
+ Revision: 191173
- revert commit 191172 (Emmanuel Aundry), there is no --disable-debug
  option (debugging is still enabled)

  + Emmanuel Andry <eandry@mandriva.org>
    - disable debug to please cd protections
    - add patch from ubuntu to fix some font rendering (#39552)

* Mon Mar 24 2008 Anssi Hannula <anssi@mandriva.org> 1:0.9.58-1mdv2008.1
+ Revision: 189764
- move wine backport branch as the main branch
- new version
- rediff mdkconf patch
- prepare branch for backporting wine during 2008.1 freeze

* Thu Mar 20 2008 Per Øyvind Karlsen <peroyvind@mandriva.org> 1:0.9.56-2mdv2008.1
+ Revision: 189141
- sorta ressurect esd patch since there's still issues (remaining issues seems to lie
  with pulseaudio and not wine), but only use esd if alsa fails (ie. in case of
  pulseaudio occupying sound device). This way you'll only get wine wine sound latency
  in cases where you otherwise wouldn't have any sound at all. (P109)

* Sun Feb 24 2008 Funda Wang <fwang@mandriva.org> 1:0.9.56-1mdv2008.1
+ Revision: 174204
- New version 0.9.56

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1:0.9.55-4mdv2008.1
+ Revision: 171173
- rebuild

* Thu Feb 14 2008 Per Øyvind Karlsen <peroyvind@mandriva.org> 1:0.9.55-3mdv2008.1
+ Revision: 167747
- drop bogus patch for #37259 as it's not only wrong, but also broken
- drop symlink for /media/cdrom as it's handled by HAL (#37362)

* Wed Feb 13 2008 Frederic Crozat <fcrozat@mandriva.com> 1:0.9.55-2mdv2008.1
+ Revision: 167078
- Patch109: try esd before Alsa for PulseAudio (only on 2008.1 and later) (Mdv bug #37259)

  + Funda Wang <fwang@mandriva.org>
    - New devel package policy

* Sat Feb 09 2008 Funda Wang <fwang@mandriva.org> 1:0.9.55-1mdv2008.1
+ Revision: 164391
- New version 0.9.55

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - fix inccorect link to cdrom  & floppy in wineprefixcreate (fixes #37362)

* Sat Jan 26 2008 Funda Wang <fwang@mandriva.org> 1:0.9.54-1mdv2008.1
+ Revision: 158296
- New version 0.9.54

* Sat Jan 12 2008 Funda Wang <fwang@mandriva.org> 1:0.9.53-1mdv2008.1
+ Revision: 149704
- New version 0.9.53
- restore buildroot

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat Dec 29 2007 Funda Wang <fwang@mandriva.org> 1:0.9.52-1mdv2008.1
+ Revision: 139050
- New version 0.9.52

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Dec 15 2007 Funda Wang <fwang@mandriva.org> 1:0.9.51-1mdv2008.1
+ Revision: 120291
- add de man page
- New version 0.9.51

* Sat Dec 01 2007 Funda Wang <fwang@mandriva.org> 1:0.9.50-1mdv2008.1
+ Revision: 114240
- New version 0.9.50

* Sat Nov 10 2007 Funda Wang <fwang@mandriva.org> 1:0.9.49-1mdv2008.1
+ Revision: 107403
- New version 0.9.49

* Tue Nov 06 2007 Funda Wang <fwang@mandriva.org> 1:0.9.48-2mdv2008.1
+ Revision: 106463
- rebuild for new lzma

* Sun Oct 28 2007 Funda Wang <fwang@mandriva.org> 1:0.9.48-1mdv2008.1
+ Revision: 102744
- New version 0.9.48

* Sat Oct 13 2007 Funda Wang <fwang@mandriva.org> 1:0.9.47-1mdv2008.1
+ Revision: 97817
- New version 0.9.47

* Tue Oct 09 2007 Funda Wang <fwang@mandriva.org> 1:0.9.46-1mdv2008.1
+ Revision: 96063
- New version 0.9.46
- drop old menu

* Fri Aug 31 2007 Anssi Hannula <anssi@mandriva.org> 1:0.9.44-2mdv2008.0
+ Revision: 76970
- adapt wine submenu to the new menu structure

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Sat Aug 25 2007 Funda Wang <fwang@mandriva.org> 1:0.9.44-1mdv2008.0
+ Revision: 71334
- rediff prefix patch
- New version 0.9.44

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 1:0.9.43-2mdv2008.0
+ Revision: 69712
- kill ldconfig require as requested by pixel

* Sun Aug 12 2007 Funda Wang <fwang@mandriva.org> 1:0.9.43-1mdv2008.0
+ Revision: 62172
- New version 0.9.43

* Fri Aug 03 2007 Anssi Hannula <anssi@mandriva.org> 1:0.9.42-1mdv2008.0
+ Revision: 58393
- 0.9.42

* Sat Jul 14 2007 Funda Wang <fwang@mandriva.org> 1:0.9.41-1mdv2008.0
+ Revision: 52009
- New version

* Sat Jun 30 2007 Funda Wang <fwang@mandriva.org> 1:0.9.40-1mdv2008.0
+ Revision: 45993
- New version

* Wed Jun 27 2007 Andreas Hasenack <andreas@mandriva.com> 1:0.9.39-2mdv2008.0
+ Revision: 44945
- rebuild with new rpm-mandriva-setup (-fstack-protector)

* Sat Jun 16 2007 Funda Wang <fwang@mandriva.org> 1:0.9.39-1mdv2008.0
+ Revision: 40325
- New version

* Fri Jun 01 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 1:0.9.38-1mdv2008.0
+ Revision: 34387
- new release: 0.9.38

* Sat May 12 2007 David Walluck <walluck@mandriva.org> 1:0.9.37-1mdv2008.0
+ Revision: 26415
- 0.9.37

* Fri Apr 27 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 1:0.9.36-1mdv2008.0
+ Revision: 18750
- oops, forgot signature
- new release: 0.9.36

* Thu Apr 19 2007 David Walluck <walluck@mandriva.org> 1:0.9.35-1mdv2008.0
+ Revision: 14962
- 0.9.35
- 0.9.34


* Sun Mar 18 2007 David Walluck <walluck@mandriva.org>
+ 2007-03-18 19:40:25 (146189)
- 0.9.33

* Sun Mar 04 2007 Anssi Hannula <anssi@mandriva.org> 0.9.32-1mdv2007.1
+ 2007-03-04 02:48:54 (131975)
- remove source1 from spec too (SILENT)
- from Per Øyvind Karlsen <pkarlsen@mandriva.com>
    - new release: 0.9.32

* Fri Feb 16 2007 David Walluck <walluck@mandriva.org> 0.9.31-1mdv2007.1
+ 2007-02-16 23:17:01 (122042)
- 0.9.31
  bunzip2 patches
  wine.init should not be mode 755 in SRPM

* Sun Jan 28 2007 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.30-1mdv2007.1
+ 2007-01-28 13:16:56 (114488)
- new release: 0.9.30
  drop P112 (fixed upstream)

* Thu Jan 11 2007 Anssi Hannula <anssi@mandriva.org> 0.9.29-1mdv2007.1
+ 2007-01-11 22:01:12 (107674)
- 0.9.29

* Fri Dec 22 2006 Anssi Hannula <anssi@mandriva.org> 0.9.28-1mdv2007.1
+ 2006-12-22 20:01:19 (101655)
- 0.9.28

* Sat Dec 16 2006 Anssi Hannula <anssi@mandriva.org> 0.9.27-2mdv2007.1
+ 2006-12-16 03:46:22 (98021)
- add a workaround for kde .exe association (#27700)

* Sat Dec 16 2006 Anssi Hannula <anssi@mandriva.org> 0.9.27-1mdv2007.1
+ 2006-12-16 01:46:11 (98013)
- 0.9.27
  o requires Mandriva 2007.0 or newer for start menu entry creation
- clean already removed patches from spec
- drop non-working patch107, start menu and desktop entries now as upstream
- add xdg wine submenu
- remove rpath from wmc and wrc too

* Fri Dec 01 2006 Anssi Hannula <anssi@mandriva.org> 0.9.26-1mdv2007.1
+ 2006-12-01 15:47:08 (89701)
- 0.9.26

* Sat Nov 11 2006 Anssi Hannula <anssi@mandriva.org> 0.9.25-1mdv2007.1
+ 2006-11-11 23:02:35 (83226)
- 0.9.25

* Sat Nov 04 2006 Anssi Hannula <anssi@mandriva.org> 0.9.24-1mdv2007.1
+ 2006-11-04 22:11:49 (76646)
- update filelist
- 0.9.24
- disable x86_64 as it does not build correctly yet
- Import wine

* Sat Sep 16 2006 Anssi Hannula <anssi@mandriva.org> 0.9.20-5mdv2007.0
- rebuild to fix binary rpm upload

* Tue Sep 12 2006 Anssi Hannula <anssi@mandriva.org> 0.9.20-4mdv2007.0
- fix buildrequires

* Sun Sep 10 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.20-3mdv2007.0
- fix install of fnt2bdf

* Sat Aug 26 2006 Götz Waschk <waschk@mandriva.org> 0.9.20-2mdv2007.0
- fix buildrequires

* Fri Aug 25 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.20-1mdv2007.0
- New release 0.9.20

* Fri Aug 11 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1:0.9.19-1mdv2007.0
- New release 0.9.19

* Thu Aug 03 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.18-2mdv2007.0
- initscript fixes:
	o do a check before trying to enable wine registration
	o fix formatting of success/failure output
	o use gprintf in stead of echo to make it translatable

* Tue Aug 01 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.18-1mdv2007.0
- 0.9.18

* Sun Jul 16 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1:0.9.17-1mdv2007.0
- New release 0.9.17
- new xdg menu (that might be broken:p)
- fix macro-in-%%changelog

* Fri Jun 23 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.16-1mdv2007.0
- New release 0.9.16
- fix backport for 2006.0
- don't build on sparc

* Wed Jun 14 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.15-1mdv2007.0
- 0.9.15

* Fri May 26 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.14-1mdk
- New release 0.9.14

* Sat May 20 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.9.13-3mdk
- fix requires for xorg7 (s/X11R6-contrib/xmessage/)
- fix buildrequires

* Sat May 13 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.13-2mdk
- fix path in menu P207 (fixes #21842)

* Fri May 12 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1:0.9.13-1mdk
- New release 0.9.13
- get rid of rpath

* Thu Apr 20 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.12-1mdk
- New release 0.9.12

* Sat Apr 01 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.11-1mdk
- New release 0.9.11

* Sat Apr 01 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.10-2mdk
- Rebuild

* Thu Mar 16 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.10-1mdk
- New release 0.9.10

* Fri Mar 03 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.9-1mdk
- New release 0.9.9

* Mon Feb 20 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.8-1mdk
- New release 0.9.8
- drop destdir patch (P1) as it's finally fixed upstream!

* Thu Feb 02 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.7-1mdk
- 0.9.7
- requires(bla,bla) -> requires(bla) requires(bla)

* Thu Jan 19 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.6-1mdk
- New release 0.9.6
- drop P115 (fixed upstream)

* Thu Jan 12 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.5-3mdk
- fix WMF vulnerability (P115, from Ubuntu)

* Mon Jan 09 2006 Olivier Blin <oblin@mandriva.com> 0.9.5-2mdk
- convert parallel init to LSB

* Fri Jan 06 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.5-1mdk
- New release 0.9.5

* Tue Jan 03 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.4-3mdk
- parallel init support

* Sat Dec 31 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.4-2mdk
- force dependency on current library version (fixes #19522)

* Fri Dec 23 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.4-1mdk
- New release 0.9.4

* Mon Dec 12 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.3-1mdk
- New release 0.9.3
- drop P113

* Thu Nov 24 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.2-1mdk
- New release 0.9.2

* Tue Nov 15 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.9.1-1mdk
- new release

* Fri Oct 28 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9-3mdk
- gah, fix conflicts

* Thu Oct 27 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9-2mdk
- merge back in twain and capi libraries and rather exclude them from depencies
  as they're softlinked and the availability will be automatically detected
- remove autoreq on sound daemon libraries for the same reason
- update url for source

* Wed Oct 26 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9-1mdk
- 0.9 (first beta after 12 years! :o)
- add epoch due to new versioning
- don't build on ppc (by spturtle's request, doesn't build)

* Sat Oct 01 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 20050930-1mdk
- 20050930
- regenerate wineprefix patch (P108)
- drop esd patch (P109, merged upstream)
- drop fontforge patch (P114, fixed upstream)

* Wed Aug 31 2005 Buchan Milne <bgmilne@linux-mandrake.com> 20050725-6mdk
- Rebuild for new libldap-2.2

* Tue Aug 30 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 20050725-5mdk
- fix problem with conflicts by adding version to provides (fixes #17927)

* Thu Aug 25 2005 Laurent MONTEL <lmontel@mandriva.com> 20050725-4
- Fix upgrade from 10.1

* Tue Aug 23 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 20050725-3mdk
- fix initscript (rewrote S2, fixes #17676)
- fix upgrade by adding conflicts (fixes #17737)
- fix build with new fontforge (P114 from wine cvs)

* Sat Aug 06 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 20050725-2mdk
- fix so that esd support is automatically detected by winecfg and also added
  to the driver list (added to P109)
- try to detect oss after other sound drivers, otherwise it will be detected
  first even if there are other drivers (added to to P113)
- fix requires(pre,postun,preun)
- fix requires-on-release
- nuke wine-utils and wine-full packages and rather just move the user
  utils to main wine package and the devel utils to the devel package
- drop mdk 8.2 specific stuff
- don't add library dir to /etc/ld.so.conf anymore, remove the old line
- clean out old junk!!

* Fri Aug 05 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 20050725-1mdk
- 20050725
- add back esd support (P109)
- drop wine wrapper script as it's no longer needed (drop S104, modifies P108,
  should also fix #9350)

* Sun Jul 10 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 20050628-3mdk
- move winecfg to main package as it's now usable and the only way to configure wine
- fix dangling-relative-symlink by moving symlink for twain to twain package

* Sat Jul 09 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 20050628-2mdk
- arg, by an accident last release got shipped with an old version of wine-launcher.sh,
  ship new one again

* Fri Jul 08 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 20050628-1mdk
- 20050628
- all configs have been moved to registry, therefore remove those configs (S200 & P100)
- don't build documentation

* Fri Jun 10 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 20050524-1mdk
- 20050524
- fix build with newer alsa (P112 from gentoo)
- add missing buildrequires (fixes #16062)

* Sat Apr 30 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 20050419-2mdk
- don't build on x86_64
- fix build on older releases where fontforge isn't available (which 
  also makes it easier to rebuild package for the club:o)

* Fri Apr 29 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 20050419-1mdk
- 20050419
- regenerate P100
- drop directx9 patch (P111, merged upstream:)

* Sun Apr 17 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 20050310-1mdk
- 20050310
- add directx9 patch (P111)
- update shellink patch (P107)
- %%mkrel
- fix executable-marked-as-config-file

* Wed Feb 16 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 20050211-2mdk
- fix buildrequires

* Sun Feb 13 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 20050211-1mdk
- 20050211

* Fri Jan 14 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 20050111-1mdk
- 20040111
- drop apploader patch (P105) as it breaks current scripts
- drop P110 (fixed upstream)

* Wed Dec 01 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 20041201-1mdk
- 20041201
- fix problem with preloader (P110, fixes #12438)
- regenerate P100

* Mon Nov 08 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 20041019-1mdk
- 20041019
- regenerate P107
- wineclipsrv is no more, remove from %%files
- initial attempt on building win64 emulator on x64_64 (probably needs more work)

* Thu Aug 26 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 20040813-2mdk
- fix temp path in config file and remove some directories in path (P100)
- update launcher script (upstream changes) (S104)
- drop S103 & S105

* Wed Aug 18 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 20040813-1mdk
- 20040813
- regenerate P100
- drop P109 (added upstream)

* Fri Jul 23 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 20040716-2mdk
- add support for esd (P109)
- update wine-launcher.sh script (S104) to no longer use soundwrappers as we now
  have support for both arts and esd in wine

* Thu Jul 22 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 20040716-1mdk
- 20040716
- regenerate P100
- drop P106

* Wed Jun 30 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 20040615-2mdk
- fix buildrequires
- clean out old stuff from spec

* Sat Jun 19 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 20040615-1mdk
- 20040615
- adapt wineprefixcreate for mdk (P108, fixes #10074):
	o trash wine-config (S103 & S105)
	o no longer make a windows system i /var/lib/wine as we rather use a local
	  per user (trash S100)
	o update wine-launcher.sh (S104) to use wineprefixcreate
- regenerate P100
- add new files to %%files list
- do not build on sparc64

* Thu Jun 17 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 20040505-4mdk
- quick and dirty replacement for wine-config.pl (S105) for making drives in
  wine with symlinks (feedback wanted!)
- spec fixes

* Sat Jun 05 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 20040505-3mdk
- rebuild

* Thu May 13 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 20040505-2mdk
- 20040505
- drop P2
- regenerate P100

* Wed May 05 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 20040408-2mdk
- fix problem with $WINEPREFIX being overridden (fixes #9511 Frank <fwallingford@hotmail.com>)

* Thu Apr 15 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 20040408-1mdk
- 20040408
- regenerate P2 & P100

* Fri Apr 02 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 20040309-1mdk
- 20040309
- regenerate P100
- make a separate .wine-native directory for native windowsdir (from Danny, see #8823)
- update %%files list, files changed upstream

* Sun Mar 21 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 20040213-3mdk
- fix problems with arguments when none is specified (fixes #9100)

