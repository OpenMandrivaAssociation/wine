%ifarch x86_64
%define	wine	wine64
%define	mark64	()(64bit)
%else
%define	wine	wine
%define	mark64	%{nil}
%endif
%define	lib_name_orig	lib%{name}
%define	lib_major	1
%define	lib_name	%mklibname %{name} %{lib_major}
%define	lib_name_devel	%{mklibname -d wine}

# On 32-bit we have
# wine32 - those 32-bit binaries that are also used on 64-bit for 32-bit support
# wine - all other files (requires 'wine32')
# On 64-bit we have
# wine64 - all 64-bit files (suggests 'wine32')
# - Anssi 07/2010

Name:		wine
#(peroyvind): please do backports for new versions
Version:	1.3.9
%define pre	0
%define rel	2
%if %pre
Release:	%mkrel 0.%pre.%rel
%define o_ver	%version-%pre
%else
Release:	%mkrel %rel
%define o_ver	%version
%endif
Epoch:		1
Summary:	WINE Is Not An Emulator - runs MS Windows programs
License:	LGPLv2+
Group:		Emulators
URL:		http://www.winehq.com/
BuildRoot:      %_tmppath/%{name}-%{version}-%{release}-buildroot
Source0:	http://ibiblio.org/pub/linux/system/emulators/wine/%{name}-%{o_ver}.tar.bz2
Source1:	http://ibiblio.org/pub/linux/system/emulators/wine/%{name}-%{o_ver}.tar.bz2.sign

# RH stuff
Source2:        wine.init
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

#(eandry) add a pulseaudio sound driver (from http://art.ified.ca/downloads/ )
# Patch400:	http://art.ified.ca/downloads/winepulse/winepulse-0.39-configure.ac.patch
#
# Rediff configure.ac patch manually until winepulse upstream fixes it
Patch400:	wine-1.3.9-winepulse-configure.ac.patch
Patch401:	http://art.ified.ca/downloads/winepulse/winepulse-0.39.patch
Patch402:	http://art.ified.ca/downloads/winepulse/winepulse-0.38-winecfg.patch

# (anssi) Wine needs GCC 4.4+ on x86_64 for MS ABI support. Note also that
# 64-bit wine cannot run 32-bit programs, so it should be named differently
# to allow co-installation. Upstream has not yet implemented this
# co-habitation, so one would need to resolve conflicts manually.
ExclusiveArch:	%{ix86}
%if %mdkversion >= 201010
ExclusiveArch:	x86_64
%endif
%ifarch x86_64
BuildRequires:	gcc >= 4.4
%endif
BuildRequires:	bison flex gpm-devel perl-devel ncurses-devel sgml-tools
BuildRequires:	X11-devel freetype2-devel autoconf2.5 docbook-utils docbook-dtd-sgml
BuildRequires:	cups-devel jackit-devel imagemagick isdn4k-utils-devel xpm-devel
BuildRequires:	sane-devel glibc-static-devel ungif-devel chrpath
BuildRequires:	desktop-file-utils libalsa-devel openldap-devel lcms-devel
BuildRequires:	libxslt-devel dbus-devel hal-devel
BuildRequires:	valgrind librsvg pulseaudio-devel
BuildRequires:	gsm-devel
BuildRequires:	mesaglu-devel
BuildRequires:	fontforge
BuildRequires:	gphoto2-devel
BuildRequires:	unixODBC-devel
BuildRequires:	libmpg123-devel
BuildRequires:	openal-devel
BuildRequires:	gnutls-devel tiff-devel libv4l-devel
BuildRequires:	gstreamer0.10-devel libgstreamer0.10-plugins-base-devel
%if %mdvver >= 201100
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
Suggests:	wine32 = %{epoch}:%{version}-%{release}
%else
# on 32-bit we always want wine32 package
Requires:	wine32 = %{epoch}:%{version}-%{release}
%endif

Provides:	%{wine}-utils = %{epoch}:%{version}-%{release} %{wine}-full = %{epoch}:%{version}-%{release}
Provides:	%{lib_name}-capi = %{epoch}:%{version}-%{release} %{lib_name}-twain = %{epoch}:%{version}-%{release}
Provides:	%{lib_name} = %{epoch}:%{version}-%{release}
Provides:	wine-bin = %{epoch}:%{version}-%{release}
Obsoletes:	%{wine}-utils %{wine}-full %{lib_name}-capi %{lib_name}-twain
Obsoletes:	%{lib_name} <= %{epoch}:%{version}-%{release}
Requires:	xmessage
Suggests:	sane-frontends
# wine dlopen's these, so let's add the dependencies ourself
Requires:	libfreetype.so.6%{mark64} libasound.so.2%{mark64}
Requires:	libXrender.so.1%{mark64} libpng.so.3%{mark64}
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires(post): desktop-common-data
Requires(postun): desktop-common-data
Requires(preun): rpm-helper
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

%ifarch %ix86
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

%description -n	wine32
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix.

This package contains the files needed to support 32-bit Windows
programs.
%endif

%package -n	%{wine}-devel
Summary:	Static libraries and headers for %{name}
Group:		Development/C
Requires:	%{wine} = %{epoch}:%{version}
Provides:	%{lib_name_devel} = %{epoch}:%{version}-%{release}
Provides:	%{lib_name_orig}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	%{lib_name_devel} <= %{epoch}:%{version}-%{release}
Obsoletes:	%{mklibname -d wine 1} < %{epoch}:%{version}
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
%setup -q -n %name-%o_ver
%patch1 -p0 -b .chinese
%patch108 -p1 -b .conf
%patch400 -p1
%patch401 -p1
%patch402 -p1
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
%configure2_5x	--with-x \
		--with-pulse \
		--without-nas \
		--without-esd \
%ifarch x86_64
		--enable-win64
%endif

%make depend
%make

%install
rm -rf %{buildroot}
%makeinstall_std LDCONFIG=/bin/true 

# Danny: dirty:
install -m755 tools/fnt2bdf -D %{buildroot}%{_bindir}/fnt2bdf

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

%clean
rm -fr %{buildroot}

%preun -n %{wine}
%_preun_service %{name}

%post -n %{wine}
%_post_service %{name}

%files -n %{wine}
%defattr(-,root,root)
%doc ANNOUNCE AUTHORS README
%ifarch x86_64
%doc README.install.urpmi
%{_bindir}/wine64
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
%defattr(-,root,root)
%{_bindir}/wine
%{_bindir}/wine-preloader
%endif

%{_libdir}/libwine*.so.%{lib_major}*
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
%defattr(-,root,root)
%{_libdir}/%{name}/*.a
%{_libdir}/libwine*.so
%{_libdir}/%{name}/*.def
%{_includedir}/*
%{_bindir}/fnt2bdf
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
