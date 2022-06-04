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
%global optflags %{optflags} -Wl,-z,notext -fuse-ld=lld
%global ldflags %{ldflags} -Wl,-z,notext -fuse-ld=lld
%endif

%define _fortify_cflags %{nil}
%define _ssp_cflags %{nil}

%ifarch %{x86_64}
%bcond_without wow64
%else
%bcond_with wow64
%endif

%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%{mklibname -d wine}
%define beta	%{nil}
# Sometimes -staging patches are released late...
# And sometimes there's interim releases
%define sbeta	%{beta}
%define sver	%{version}
#define smaster 1

%bcond_without staging

Name:		wine
#(peroyvind): please do backports for new versions
Version:	7.10
%if "%{beta}" != ""
Release:	0.%{beta}.1
Source0:	https://dl.winehq.org/wine/source/%(echo %version |cut -d. -f1-2)/%{name}-%{version}-%{beta}.tar.xz
Source1:	https://dl.winehq.org/wine/source/%(echo %version |cut -d. -f1-2)/%{name}-%{version}-%{beta}.tar.xz.sign
%else
Release:	1
Source0:	http://dl.winehq.org/wine/source/%(echo %version |cut -d. -f1).x/wine-%{version}.tar.xz
Source1:	http://dl.winehq.org/wine/source/%(echo %version |cut -d. -f1).x/wine-%{version}.tar.xz.sign
%endif
%if "%{sbeta}" != ""
Source900:	https://github.com/wine-staging/wine-staging/archive/v%{sver}-%{sbeta}.tar.gz
%else
Source900:	https://github.com/wine-staging/wine-staging/archive/%{?smaster:master}%{!?smaster:v%{sver}}.tar.gz
%endif
Summary:	WINE Is Not An Emulator - runs MS Windows programs
License:	LGPLv2+
Group:		Emulators
URL:		http://www.winehq.com/

Source2:	wine.binfmt
Source10:	wine.rpmlintrc
Source11:	https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks
Source12:	http://kegel.com/wine/wisotool
Patch0:		wine-1.0-rc3-fix-conflicts-with-openssl.patch
Patch1:		wine-1.1.7-chinese-font-substitutes.patch
Patch2:		wine-cjk.patch
Patch3:		wine-7.0-aarch64-compile.patch
# https://bugs.winehq.org/show_bug.cgi?id=41930#c0
Patch4:		0001-Revert-gdi32-Fix-arguments-for-OSMesaMakeCurrent-whe.patch
Patch5:		wine-4.14-fix-crackling-audio.patch
Patch6:		wine-5.11-llvm-libunwind.patch
Patch7:		wine-winnt.h-clang.patch

# a: => /media/floppy
# d: => $HOME (at config_dir creation time, not refreshed if $HOME changes;
#              note that Wine also provides $HOME in My Documents)
# com4 => /dev/ttyUSB0 (replaces /dev/ttyS3)
Patch108:	wine-mdkconf.patch
%ifarch %{x86_64}
# Wine needs GCC 4.4+ on x86_64 for MS ABI support.
BuildRequires:	gcc >= 4.4
%endif

BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gpm-devel
BuildRequires:	perl-devel
BuildRequires:	pkgconfig(libpcap)
BuildRequires:	pkgconfig(OpenCL)
BuildRequires:	pkgconfig(ncurses)
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
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(gpg-error)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(capi20)
BuildRequires:	pkgconfig(netapi)
BuildRequires:	glibc-static-devel
BuildRequires:	chrpath
BuildRequires:	giflib-devel
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
BuildRequires:	jxrlib-devel
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
BuildRequires:	pkgconfig(krb5)
BuildRequires:	pkgconfig(com_err)
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

%if %{with wow64}
# This is ugly, but it has to be until and unless we fix multiarch support
# in general.
# We need to pull in 32-bit libraries, but can't install the corresponding
# -devel packages because the headers would conflict with the 64bit headers.
# Given the headers are the same anyway, we can just create fake devel
# environments by symlinking .so files and reusing system (64bit) includes.
BuildRequires:	devel(libSDL2-2.0)
BuildRequires:	devel(libOpenCL)
BuildRequires:	devel(libncurses)
BuildRequires:	devel(libncursesw)
BuildRequires:	devel(libcups)
BuildRequires:	devel(libsane)
BuildRequires:	devel(libsystemd)
BuildRequires:	devel(libz)
BuildRequires:	devel(libbz2)
BuildRequires:	devel(libjack)
BuildRequires:	devel(libpulse)
BuildRequires:	devel(libmpg123)
BuildRequires:	devel(libopenal)
BuildRequires:	devel(libasound)
BuildRequires:	devel(libaudiofile)
BuildRequires:	devel(libglut)
BuildRequires:	devel(libpng16)
BuildRequires:	devel(libusb-1.0)
BuildRequires:	devel(libxml2)
BuildRequires:	devel(libxslt)
BuildRequires:	devel(libcapi20)
BuildRequires:	devel(libgif)
BuildRequires:	devel(libtiff)
BuildRequires:	devel(libXpm)
BuildRequires:	devel(librsvg-2)
BuildRequires:	devel(libgphoto2)
BuildRequires:	devel(libgphoto2_port)
BuildRequires:	devel(libldap_r-2.4)
BuildRequires:	devel(liblber-2.4)
BuildRequires:	devel(libdbus-1)
BuildRequires:	devel(libgsm)
BuildRequires:	devel(libodbc)
BuildRequires:	devel(libgnutls)
BuildRequires:	devel(libintl)
BuildRequires:	libd3dadapter9-devel
BuildRequires:	devel(liblcms2)
BuildRequires:	devel(libOSMesa)
BuildRequires:	devel(libGL)
BuildRequires:	devel(libGLU)
BuildRequires:	devel(libv4l2)
BuildRequires:	devel(libieee1284)
BuildRequires:	devel(libjpeg)
BuildRequires:	devel(libjpegxr)
BuildRequires:	devel(libXcursor)
BuildRequires:	devel(libXcomposite)
BuildRequires:	devel(libXfixes)
BuildRequires:	devel(libXi)
BuildRequires:	devel(libXinerama)
BuildRequires:	devel(libXxf86vm)
BuildRequires:	devel(libXmu)
BuildRequires:	devel(libXrandr)
BuildRequires:	devel(libX11)
BuildRequires:	devel(libXrender)
BuildRequires:	devel(libXext)
BuildRequires:	devel(libSM)
BuildRequires:	libvulkan-devel
BuildRequires:	devel(libvkd3d)
BuildRequires:	devel(libfontconfig)
BuildRequires:	devel(libfreetype)
BuildRequires:	devel(libgstreamer-1.0)
BuildRequires:	devel(libgstvideo-1.0)
BuildRequires:	devel(libgstaudio-1.0)
BuildRequires:	devel(libgstbase-1.0)
BuildRequires:	devel(libva)
BuildRequires:	devel(libva-x11)
BuildRequires:	devel(libva-drm)
BuildRequires:	devel(libavcodec)
BuildRequires:	devel(libudev)
BuildRequires:	devel(libFAudio)
BuildRequires:	devel(libpcap)
BuildRequires:	devel(libkrb5)
BuildRequires:	devel(libk5crypto)
BuildRequires:	devel(libcom_err)
BuildRequires:	devel(libgcrypt)
BuildRequires:	devel(libgpg-error)
BuildRequires:	devel(libgtk-3)
BuildRequires:	devel(libgdk-3)
BuildRequires:	devel(libpangocairo-1.0)
BuildRequires:	devel(libpango-1.0)
BuildRequires:	devel(libharfbuzz)
BuildRequires:	devel(libatk-1.0)
BuildRequires:	devel(libatk-bridge-2.0)
BuildRequires:	devel(libatspi)
BuildRequires:	devel(libcairo-gobject)
BuildRequires:	devel(libcairo)
BuildRequires:	devel(libgdk_pixbuf-2.0)
BuildRequires:	devel(libgio-2.0)
BuildRequires:	devel(libgobject-2.0)
BuildRequires:	devel(libglib-2.0)
BuildRequires:	devel(liborc-0.4)
BuildRequires:	libunwind-nongnu-devel
BuildRequires:	devel(libelf)
BuildRequires:	devel(libdw)
BuildRequires:	devel(liblzma)
BuildRequires:	devel(libpcre)
BuildRequires:	devel(libffi)
BuildRequires:	devel(libepoxy)
BuildRequires:	devel(libfribidi)
BuildRequires:	devel(libpangoft2-1.0)
BuildRequires:	devel(libuuid)
BuildRequires:	devel(libblkid)
BuildRequires:	devel(libmount)
BuildRequires:	devel(libpixman-1)
BuildRequires:	devel(libexpat)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libXft)
BuildRequires:	devel(libxcb-render)
BuildRequires:	devel(libxcb-shm)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
BuildRequires:	devel(libXdamage)
%endif
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
#for winetricks
Requires:	cabextract
Requires:	unzip
Suggests:	webcore-fonts
%rename		winetricks
%ifarch %{x86_64}
# Make sure we have 32-bit versions of DRI drivers... Needed
# as soon as a 32-bit Windows app uses OpenGL or DirectX
Requires:	libdri-drivers
%endif
# (Anssi) If wine-gecko is not installed, wine pops up a dialog on first
# start proposing to download wine-gecko from sourceforge, while recommending
# to use distribution packages instead. Therefore suggest wine-gecko here:
Suggests:	wine-gecko
Suggests:	%{dlopen_req ncursesw}
%if %{with wow64}
%rename		wine32
%rename		wine64
%endif
%ifarch %{ix86} %{x86_64}
BuildRequires:	cross-i686-w64-mingw32-binutils >= 2.38-2
BuildRequires:	cross-i686-w64-mingw32-gcc-bootstrap
BuildRequires:	cross-i686-w64-mingw32-libc
%ifarch %{x86_64}
BuildRequires:	cross-x86_64-w64-mingw32-binutils >= 2.38-2
BuildRequires:	cross-x86_64-w64-mingw32-gcc-bootstrap
BuildRequires:	cross-x86_64-w64-mingw32-libc
%endif
%endif

%description
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix. It
consists of a program loader which loads and executes a Microsoft
Windows binary, and a library (called Winelib) that implements Windows
API calls using their Unix or X11 equivalents.  The library may also
be used for porting Win32 code into native Unix executables.

%package devel
Summary:	Static libraries and headers for %{name}
Group:		Development/C
Requires:	%{name} = %{EVRD}
%rename		%{devname}
Obsoletes:	%{mklibname -d wine 1} < %{EVRD}
%rename wine64-devel

%description devel
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix.

%{name}-devel contains the libraries and header files needed to
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
%endif

%ifarch %{armx}
%patch3 -p1 -b .aarch64~
%endif
%patch4 -p1 -b .civ3~
%patch5 -p1 -b .pulseaudiosucks~
%patch6 -p1 -b .unwind~

autoreconf
aclocal
autoconf

%build
# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
%undefine _fortify_cflags
export CFLAGS="`echo %{optflags} |sed -e 's,-m64,,g;s,-mx32,,g'`"
export CXXFLAGS="`echo %{optflags} |sed -e 's,-m64,,g;s,-mx32,,g'`"
export LDFLAGS="`echo %{build_ldflags} |sed -e 's,-m64,,g;s,-mx32,,g'`"
%ifarch %{ix86}
# (Anssi 04/2008) bug #39604
# Some protection systems complain "debugger detected" with our
# -fomit-frame-pointer flag, so disable it.
export CFLAGS="${CFLAGS} -fno-omit-frame-pointer"
%endif

%ifarch %{x86_64}
# As of wine 5.6, clang 10.0:
# winecfg in 64bit mode crashes on startup if built with
# clang. Probably clang doesn't get the M$ ABI right
export CC=gcc
export CXX=g++
%endif

export CONFIGURE_TOP=`pwd`
mkdir build
cd build
%configure	--with-pulse \
		--without-hal \
    		--with-xattr \
		--with-gstreamer \
%ifarch %{x86_64}
		--enable-win64
%endif

if cat config.log |grep "won't be supported" |grep -q -vE '(OSSv4)'; then
	echo "Full config.log:"
	cat config.log
	echo "******************************"
	echo "Missing dependencies detected:"
	echo "(Only missing OSSv4 is OK):"
	echo "******************************"
	cat config.log |grep "won't be supported"
	exit 1
fi

%make_build depend
%make_build

%if %{with wow64}
cd ..

mkdir build32
cd build32
if ! PKG_CONFIG_LIBDIR="%{_prefix}/lib/pkgconfig:%{_datadir}/pkgconfig" \
PKG_CONFIG_PATH="%{_prefix}/lib/pkgconfig:%{_datadir}/pkgconfig" \
../configure \
		--prefix=%{_prefix} \
		--with-pulse \
		--without-hal \
    		--with-xattr \
		--with-gstreamer \
		--with-wine64=../build; then
	echo "32-bit configure failed. Full config.log:"
	cat config.log
fi
if cat config.log |grep "won't be supported" |grep -q -vE '(OSSv4|netapi)'; then
	echo "Full config.log:"
	cat config.log
	echo "***************************************"
	echo "Missing 32-bit dependencies detected:"
	echo "(Only missing OSSv4 and netapi are OK):"
	echo "***************************************"
	cat config.log |grep "won't be supported"
	exit 1
fi
%make_build depend
%make_build
%endif


%install
%if %{with wow64}
cd build32
%make_install LDCONFIG=/bin/true
cd ..
%endif

cd build
%make_install LDCONFIG=/bin/true
cd ..

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

for i in %{buildroot}%{_bindir}/* %{buildroot}%{_libdir}/%{name}/*.so %{buildroot}%{_prefix}/lib/%{name}/*.so; do
	chrpath -d $i || :
done

%files
%doc ANNOUNCE AUTHORS README
%ifarch %{x86_64}
%{_bindir}/wine64
%{_bindir}/wine64-preloader
%if %{with wow64}
%{_bindir}/wine
%{_bindir}/wine-preloader
%endif
%else
%{_bindir}/wine
%{_bindir}/wine-preloader
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
%{_mandir}/man1/wine.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wine.1*
%lang(de) %{_mandir}/de.UTF-8/man1/winemaker.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wineserver.1*
%lang(pl) %{_mandir}/pl.UTF-8/man1/wine.1*
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
%{_datadir}/%{name}/nls/l_intl.nls
%{_datadir}/%{name}/nls/locale.nls
%{_datadir}/%{name}/nls/c_*
%{_datadir}/%{name}/nls/normidna.nls
%{_datadir}/%{name}/nls/normnfc.nls
%{_datadir}/%{name}/nls/normnfd.nls
%{_datadir}/%{name}/nls/normnfkc.nls
%{_datadir}/%{name}/nls/normnfkd.nls
%{_datadir}/%{name}/nls/sortdefault.nls
%{_datadir}/applications/*.desktop
%{_sysconfdir}/xdg/menus/applications-merged/mandriva-%{name}.menu
%{_datadir}/desktop-directories/mandriva-%{name}.directory
%dir %{_datadir}/wine/fonts
%{_datadir}/wine/fonts/*
%{_miconsdir}/*.png
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%dir %{_libdir}/%{name}
%ifarch %{x86_64}
%dir %{_libdir}/%{name}/x86_64-unix
%dir %{_libdir}/%{name}/x86_64-windows
%{_libdir}/%{name}/x86_64-unix/libwine.so.1*
%endif
%ifarch %{aarch64}
%dir %{_libdir}/%{name}/aarch64-unix
%dir %{_libdir}/%{name}/aarch64-windows
%{_libdir}/%{name}/aarch64-unix/libwine.so.1*
%endif
%{_libdir}/%{name}/*/*.so
%{_libdir}/%{name}/*/*.acm
%{_libdir}/%{name}/*/*.ax
%{_libdir}/%{name}/*/*.com
%{_libdir}/%{name}/*/*.cpl
%{_libdir}/%{name}/*/*.dll
%{_libdir}/%{name}/*/*.drv
%{_libdir}/%{name}/*/*.ds
%{_libdir}/%{name}/*/*.exe
%{_libdir}/%{name}/*/*.ocx
%{_libdir}/%{name}/*/*.sys
%{_libdir}/%{name}/*/*.tlb
%{_libdir}/%{name}/*/*.msstyles
%{_libdir}/%{name}/*/windows.networking.connectivity
%if %{with wow64}
%dir %{_prefix}/lib/%{name}
%dir %{_prefix}/lib/%{name}/i386-unix
%dir %{_prefix}/lib/%{name}/i386-windows
%{_prefix}/lib/%{name}/i386-unix/libwine.so.1*
%{_prefix}/lib/%{name}/*/*.so
%{_prefix}/lib/%{name}/*/*.acm
%{_prefix}/lib/%{name}/*/*.ax
%{_prefix}/lib/%{name}/*/*.com
%{_prefix}/lib/%{name}/*/*.cpl
%{_prefix}/lib/%{name}/*/*.dll
%{_prefix}/lib/%{name}/*/*.drv
%{_prefix}/lib/%{name}/*/*.ds
%{_prefix}/lib/%{name}/*/*.exe
%{_prefix}/lib/%{name}/*/*.msstyles
%{_prefix}/lib/%{name}/*/*.ocx
%{_prefix}/lib/%{name}/*/*.sys
%{_prefix}/lib/%{name}/*/*.tlb
%{_prefix}/lib/%{name}/*/*.vxd
%{_prefix}/lib/%{name}/*/*.dll16
%{_prefix}/lib/%{name}/*/*.exe16
%{_prefix}/lib/%{name}/*/*.drv16
%{_prefix}/lib/%{name}/*/*.mod16
%{_prefix}/lib/%{name}/*/windows.networking.connectivity
%endif

%files devel
%{_libdir}/%{name}/*/*.a
%ifarch %{x86_64}
%{_prefix}/lib/%{name}/*/*.a
%endif
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
