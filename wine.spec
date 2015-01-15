%ifarch x86_64
%define	wine	wine64
%define	mark64	()(64bit)
%else
%define	wine	wine
%define	mark64	%{nil}
%endif

%define major 1
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

# On 32-bit we have
# wine32 - those 32-bit binaries that are also used on 64-bit for 32-bit support
# wine - all other files (requires 'wine32')
# On 64-bit we have
# wine64 - all 64-bit files (suggests 'wine32')
# - Anssi 07/2010

Summary:	WINE Is Not An Emulator - runs MS Windows programs
Name:		wine
Version:	1.7.34
Release:	4
Epoch:		2
License:	LGPLv2+
Group:		Emulators
Url:		http://www.winehq.com/
Source0:	http://mirrors.ibiblio.org/wine/source/%(echo %{version} |cut -d. -f1-2)/%{name}-%{version}.tar.bz2
Source1:	http://mirrors.ibiblio.org/wine/source/%(echo %{version} |cut -d. -f1-2)/%{name}-%{version}.tar.bz2.sign
# RH stuff
Source2:	wine.init
# Wine-Compholio, from github by tag
# https://github.com/compholio/wine-compholio/archive/v%{version}.tar.gz
Source3:	wine-staging-%{version}.tar.gz
Source10:	wine.rpmlintrc
Source11:	http://kegel.com/wine/winetricks
Source12:	http://kegel.com/wine/wisotool

# (Anssi 05/2008) Adds:
# a: => /media/floppy (/mnt/floppy on 2007.1 and older)
# d: => $HOME (at config_dir creation time, not refreshed if $HOME changes;
#              note that Wine also provides $HOME in My Documents)
# only on 2008.0: e: => /media/cdrom (does not exist on 2008.1+)
# com4 => /dev/ttyUSB0 (replaces /dev/ttyS3)
# have to substitute @MDKVERSION@ in dlls/ntdll/server.c
Patch0:		wine-mdkconf.patch
Patch1:		wine-1.3.24-64bit-tools.patch


BuildRequires:	bison
BuildRequires:	chrpath
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd-sgml
BuildRequires:	docbook-utils
BuildRequires:	flex
BuildRequires:	fontforge
BuildRequires:	imagemagick
BuildRequires:	prelink
BuildRequires:	sgml-tools
BuildRequires:	valgrind
BuildRequires:	cups-devel
BuildRequires:	gettext-devel
BuildRequires:	glibc-static-devel
BuildRequires:	gpm-devel
BuildRequires:	gsm-devel
BuildRequires:	isdn4k-utils-devel
BuildRequires:	openldap-devel
BuildRequires:	perl-devel
BuildRequires:	ungif-devel
BuildRequires:	unixODBC-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(gstreamer-0.10)
BuildRequires:	pkgconfig(gstreamer-plugins-base-0.10)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(lcms)
BuildRequires:	pkgconfig(libgphoto2)
BuildRequires:	pkgconfig(libmpg123)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libv4l2)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(sane-backends)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xrender)

ExclusiveArch:	%{ix86}
ExclusiveArch:	x86_64

#----------------------------------------------------------------------------

%ifarch x86_64
%package -n %{wine}
Summary:	WINE Is Not An Emulator - runs MS Windows programs
Group:		Emulators
Suggests:	wine32 = %{EVRD}
Suggests:	wine64-gecko
Suggests:	libncursesw.so.5%{mark64}
Suggests:	libncurses.so.5%{mark64}
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
Requires:	libfreetype.so.6%{mark64}
Requires:	libasound.so.2%{mark64}
Requires:	libXrender.so.1%{mark64}
Requires:	libpng15.so.15%{mark64}
Requires(post,postun):	desktop-common-data
Requires(post,preun):	rpm-helper

# for winetricks:
Requires:	cabextract
Requires:	unzip

Suggests:	webcore-fonts
%rename		winetricks

%ifarch %{ix86}
Conflicts:	wine64
Conflicts:	wine-compholio64
Conflicts:	wine-compholio
%else
Conflicts:	wine-compholio64
Conflicts:	wine-compholio
%endif

%description
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix. It
consists of a program loader which loads and executes a Microsoft
Windows binary, and a library (called Winelib) that implements Windows
API calls using their Unix or X11 equivalents.  The library may also
be used for porting Win32 code into native Unix executables.

%ifarch x86_64
%description -n %{wine}
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix. It
consists of a program loader which loads and executes a Microsoft
Windows binary, and a library (called Winelib) that implements Windows
API calls using their Unix or X11 equivalents.  The library may also
be used for porting Win32 code into native Unix executables.

This package contains the Win64 version of Wine. You need the wine32
package from the 32-bit repository to be able to run 32-bit applications.
%endif

#----------------------------------------------------------------------------

%ifarch %{ix86}
%package -n wine32
Summary:	32-bit support for Wine
Group:		Emulators
# This is not an EVR-specific requirement, as otherwise on x86_64 urpmi could
# resolve the dependency to wine64 even on upgrades, and therefore replace
# wine+wine32 installation with a wine32+wine64 installation. - Anssi
Requires:	wine-bin
# (Anssi) If wine-gecko is not installed, wine pops up a dialog on first
# start proposing to download wine-gecko from sourceforge, while recommending
# to use distribution packages instead. Therefore suggest wine-gecko here:
Suggests:	wine-gecko
Suggests:	libncursesw.so.5
Suggests:	libncurses.so.5

%description -n wine32
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix.

This package contains the files needed to support 32-bit Windows
programs.
%endif

#----------------------------------------------------------------------------

%package -n %{wine}-devel
Summary:	Static libraries and headers for %{name}
Group:		Development/C
Requires:	%{wine} = %{EVRD}
%rename		%{devname}
%ifarch %{ix86}
Conflicts:	wine64-devel
%else
Conflicts:	wine-devel
%endif

%description -n %{wine}-devel
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix.

%{wine}-devel contains the libraries and header files needed to
develop programs which make use of wine.

Wine is often updated.

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

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1 -b .conf
%patch1 -p1

# Wine-Compholio
gzip -dc "%{SOURCE3}" | /bin/tar -xf - --strip-components=1
make -C "patches" DESTDIR="%{_builddir}/wine-%{version}" install

sed -i 's,@MDKVERSION@,%{mdkversion},' dlls/ntdll/server.c

%build
%ifarch %{ix86}
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

make depend
make

%install
%makeinstall_std LDCONFIG=/bin/true

install -m 0755 %{SOURCE11} %{buildroot}%{_bindir}/
install -m 0755 %{SOURCE12} %{buildroot}%{_bindir}/

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
%{_bindir}/winetricks
%{_bindir}/wisotool
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
#{_datadir}/%{name}/generic.ppd
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