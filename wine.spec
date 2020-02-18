# FIXME
# gcc -o wine64-preloader -static -nostartfiles -nodefaultlibs -Wl,-Ttext=0x7c400000 preloader.o ../libs/port/libwine_port.a -Oz -gdwarf-4 -Wstrict-aliasing=2 -pipe -Wformat -Werror=format-security  -fstack-protector --param=ssp-buffer-size=4  -fPIC -flto -Wl,-O2  -Wl,--no-undefined -flto
# /tmp/ccHA1ZYg.ltrans0.ltrans.o(.text+0x12): error: undefined reference to 'thread_data'
# /tmp/ccHA1ZYg.ltrans0.ltrans.o(.text+0x2a): error: undefined reference to 'wld_start'
%define _disable_lto 1
# OpenCL support doesn't see cl* functions even with -lCL, but works if built...
%define _disable_ld_no_undefined 1
# Build time errors with lld 9.0.0-rc1 on x86_32 only
# ld: error: can't create dynamic relocation R_386_32 against symbol: .L.str in readonly segment; recompile object files with -fPIC or pass '-Wl,-z,notext' to allow text relocations in the output
%ifarch %{ix86}
%global optflags %{optflags} -Wl,-z,notext
%global ldflags %{ldflags} -Wl,-z,notext
%endif

%ifarch %{x86_64}
%define	wine	wine64
%else
%define	wine	wine
%endif

%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%{mklibname -d wine}
%define beta	%{nil}
# Sometimes -staging patches are released late...
# And sometimes there's interim releases
%define sbeta	%{beta}
%define sver	%{version}

%bcond_without staging

# On 32-bit we have
# wine32 - those 32-bit binaries that are also used on 64-bit for 32-bit support
# wine - all other files (requires 'wine32')
# On 64-bit we have
# wine64 - all 64-bit files (suggests 'wine32')
# - Anssi 07/2010

Name:		wine
#(peroyvind): please do backports for new versions
Version:	5.2
%if "%{beta}" != ""
Release:	0.%{beta}.1
Source0:	https://dl.winehq.org/wine/source/%(echo %version |cut -d. -f1-2)/%{name}-%{version}-%{beta}.tar.xz
Source1:	https://dl.winehq.org/wine/source/%(echo %version |cut -d. -f1-2)/%{name}-%{version}-%{beta}.tar.xz.sign
%else
Release:	1
Source0:	http://dl.winehq.org/wine/source/%(echo %version |cut -d. -f1-2)/wine-%{version}.tar.xz
Source1:	http://dl.winehq.org/wine/source/%(echo %version |cut -d. -f1-2)/wine-%{version}.tar.xz.sign
%endif
%if "%{sbeta}" != ""
Source900:	https://github.com/wine-staging/wine-staging/archive/v%{sver}-%{sbeta}.tar.gz
%else
Source900:	https://github.com/wine-staging/wine-staging/archive/v%{sver}.tar.gz
%endif
Summary:	WINE Is Not An Emulator - runs MS Windows programs
License:	LGPLv2+
Group:		Emulators
URL:		http://www.winehq.com/

# RH stuff
Source2:	wine.binfmt
Source10:	wine.rpmlintrc
Source11:	http://kegel.com/wine/winetricks
Source12:	http://kegel.com/wine/wisotool
Patch0:		wine-1.0-rc3-fix-conflicts-with-openssl.patch
Patch1:		wine-1.1.7-chinese-font-substitutes.patch
Patch2:		wine-cjk.patch
Patch3:		wine-1.9.23-freetype-unresolved-symbol.patch
# https://bugs.winehq.org/show_bug.cgi?id=41930#c0
Patch4:		0001-Revert-gdi32-Fix-arguments-for-OSMesaMakeCurrent-whe.patch
Patch5:		wine-4.14-fix-crackling-audio.patch

# a: => /media/floppy
# d: => $HOME (at config_dir creation time, not refreshed if $HOME changes;
#              note that Wine also provides $HOME in My Documents)
# com4 => /dev/ttyUSB0 (replaces /dev/ttyS3)
Patch108:	wine-mdkconf.patch

# (anssi) Wine needs GCC 4.4+ on x86_64 for MS ABI support. Note also that
# 64-bit wine cannot run 32-bit programs without wine32.
ExclusiveArch:	%{ix86} %{x86_64}
%ifarch %{x86_64}
BuildRequires:	gcc >= 4.4
%endif

BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gpm-devel
BuildRequires:	perl-devel
BuildRequires:	pcap-devel
BuildRequires:	pkgconfig(OpenCL)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(libclc)
BuildRequires:	cups-devel
BuildRequires:	pkgconfig(sane-backends)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(zlib)
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
BuildRequires:	pkgconfig(audiofile)
BuildRequires:	pkgconfig(freeglut)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	isdn4k-utils-devel
BuildRequires:	glibc-static-devel
BuildRequires:	chrpath
BuildRequires:	giflib-devel
BuildRequires:	libtiff-devel
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	icoutils
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
BuildRequires:	d3d-devel >= 10.4.0-1
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(osmesa)
BuildRequires:	pkgconfig(libglvnd)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libv4l2)
BuildRequires:	ieee1284-devel
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xinerama) 
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(sm)
BUildRequires:	pkgconfig(vulkan)
BuildRequires:	pkgconfig(libvkd3d)
BuildRequires:	fontforge
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gstreamer-base-1.0)
BuildRequires:	pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:	pkgconfig(libva)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	cmake(FAudio)
BuildRequires:	prelink

%define desc Wine is a program which allows running Microsoft Windows programs \
(including DOS, Windows 3.x and Win32 executables) on Unix. It \
consists of a program loader which loads and executes a Microsoft \
Windows binary, and a library (called Winelib) that implements Windows \
API calls using their Unix or X11 equivalents.  The library may also \
be used for porting Win32 code into native Unix executables.

%ifarch %{x86_64}
%package -n	%{wine}
Summary:	WINE Is Not An Emulator - runs MS Windows programs
Group:		Emulators
Suggests:	wine32 = %{EVRD}
Suggests:	wine64-gecko
Suggests:	%{dlopen_req ncursesw}
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
Requires:	%{dlopen_req freetype}
Requires:	%{dlopen_req gnutls}
Requires:	%{dlopen_req asound}
Requires:	%{dlopen_req png}
Requires:	%{dlopen_req OSMesa}
Requires:	%{dlopen_req Xcomposite}
Requires:	%{dlopen_req Xcursor}
Requires:	%{dlopen_req Xinerama}
Requires:	%{dlopen_req Xrandr}
Requires:	%{dlopen_req Xrender}
Requires:	%{dlopen_req v4l2}
Requires(post):	desktop-file-utils
Requires(postun):	desktop-file-utils
Requires(post):	desktop-common-data
Requires(postun):	desktop-common-data
Conflicts:	%{wine} < %{EVRD}

%ifarch %{ix86}
Conflicts:	wine64
%else
Conflicts:	wine
%endif


#for winetricks
Requires:	cabextract
Requires:	unzip

Suggests:	webcore-fonts
%rename		winetricks

#remove compholio
%ifarch %{x86_64}
Obsoletes:	wine-compholio64 <= %{EVRD}
%else
Obsoletes:	wine-compholio <= %{EVRD}
%endif

%description
%desc

%ifarch %{x86_64}
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
Conflicts:	wine < %{EVRD}
Conflicts:	wine64 < %{EVRD}
Requires:	%{dlopen_req freetype}
Requires:	%{dlopen_req gnutls}
Requires:	%{dlopen_req asound}
Requires:   	%{dlopen_req png}
Requires:	%{dlopen_req OSMesa}
Requires:	%{dlopen_req Xcomposite}
Requires:	%{dlopen_req Xcursor}
Requires:	%{dlopen_req Xinerama}
Requires:	%{dlopen_req Xrandr}
Requires:	%{dlopen_req Xrender}
Requires:	%{dlopen_req v4l2}
# Make sure we have 32-bit versions of DRI drivers... Needed
# as soon as a 32-bit Windows app uses OpenGL or DirectX
Requires:	libdri-drivers
# (Anssi) If wine-gecko is not installed, wine pops up a dialog on first
# start proposing to download wine-gecko from sourceforge, while recommending
# to use distribution packages instead. Therefore suggest wine-gecko here:
Suggests:	wine-gecko
Suggests:	%{dlopen_req ncursesw}

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

#remove compholio devel
%ifarch %{x86_64}
Obsoletes:	wine-compholio64-devel <= %{EVRD}
%else
Obsoletes:	wine-compholio-devel <= %{EVRD}
%endif

%description -n	%{wine}-devel
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix.

%{wine}-devel contains the libraries and header files needed to
develop programs which make use of wine.

Wine is often updated.

%prep
%if "%{beta}" != ""
%setup -qn %{name}-%{version}-%{beta}
%else
%setup -q
%endif
%patch1 -p0 -b .chinese~
%patch2 -p1 -b .cjk~
%patch108 -p1 -b .conf~

%if %{with staging}
# wine-staging
tar --strip-components=1 -zxf "%{SOURCE900}"
WINEDIR="$(pwd)"
cd patches
./patchinstall.sh --all DESTDIR="$WINEDIR"
cd ..

%patch3 -p1 -b .dlopenLazy~
%endif
%patch4 -p1 -b .civ3~
%patch5 -p1 -b .pulseaudiosucks~

autoreconf

%build
# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
%undefine _fortify_cflags
%ifarch %{ix86}
# (Anssi 04/2008) bug #39604
# Some protection systems complain "debugger detected" with our
# -fomit-frame-pointer flag, so disable it.
export CFLAGS="%{optflags} -fno-omit-frame-pointer"
%endif

# Clang doesn't support M$ ABI on 64bit
#export CC=gcc
#export CXX=g++

%configure	--with-pulse \
		--without-hal \
		--without-nas \
    		--with-xattr \
		--with-gstreamer \
%ifarch %{x86_64}
		--enable-win64
%endif

%make depend
%make

%install
%makeinstall_std LDCONFIG=/bin/true

install -m 0755 %{SOURCE11} %{buildroot}%{_bindir}/
install -m 0755 %{SOURCE12} %{buildroot}%{_bindir}/

# Danny: dirty:
# install -m755 tools/fnt2bdf -D %{buildroot}%{_bindir}/fnt2bdf

# Allow users to launch Windows programs by just clicking on the .exe file...
install -m755 %{SOURCE2} -D %{buildroot}%{_binfmtdir}/wine.conf

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

%ifarch %{x86_64}
# fix the binary name
sed -i 's,Exec=wine ,Exec=wine64 ,' %{buildroot}%{_datadir}/applications/wine.desktop
%endif

install -d %{buildroot}{%{_liconsdir},%{_iconsdir},%{_miconsdir}}

# winecfg icon
convert dlls/user32/resources/oic_winlogo.ico[5] %{buildroot}%{_miconsdir}/%{name}.png
convert dlls/user32/resources/oic_winlogo.ico[0] %{buildroot}%{_iconsdir}/%{name}.png
convert dlls/user32/resources/oic_winlogo.ico[1] %{buildroot}%{_liconsdir}/%{name}.png

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

%ifarch %{x86_64}
chrpath -d %{buildroot}%{_bindir}/{wine64,wineserver,wmc,wrc} %{buildroot}%{_libdir}/%{name}/*.so
%else
chrpath -d %{buildroot}%{_bindir}/{wine,wineserver,wmc,wrc} %{buildroot}%{_libdir}/%{name}/*.so
%endif

%ifarch %{x86_64}
cat > README.install.urpmi <<EOF
This is the Win64 version of Wine. This version can only be used to run
64-bit Windows applications as is. For running 32-bit Windows applications,
you need to also install the 'wine32' package from the 32-bit repository.
EOF
%endif

%files -n %{wine}
%doc ANNOUNCE AUTHORS README
%ifarch %{x86_64}
%doc README.install.urpmi
%{_bindir}/wine64
%{_bindir}/wine64-preloader
%endif
%config %{_binfmtdir}/wine.conf
%{_bindir}/winecfg
%{_bindir}/wineconsole*
%{_bindir}/wineserver
%{_bindir}/wineboot
%{_bindir}/function_grep.pl
#%{_bindir}/wineprefixcreate
%{_bindir}/msidb
%{_bindir}/msiexec
%{_bindir}/notepad
%{_bindir}/regedit
%{_bindir}/winemine
%{_bindir}/winepath
%{_bindir}/regsvr32
%{_bindir}/winefile
%{_bindir}/winetricks
%{_bindir}/wisotool
%ifarch %{ix86}
%optional %{_mandir}/man1/wine.1*
%optional %lang(de) %{_mandir}/de.UTF-8/man1/wine.1*
%optional %lang(pl) %{_mandir}/pl.UTF-8/man1/wine.1*
%endif
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
%{_datadir}/%{name}/%{name}.inf
%{_datadir}/%{name}/winebus.inf
%{_datadir}/%{name}/winehid.inf
%{_datadir}/%{name}/nls/l_intl.nls
%{_datadir}/%{name}/nls/c_*
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
%{_libdir}/%{name}/*.com.so
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
