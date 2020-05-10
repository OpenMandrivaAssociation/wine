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

%bcond_without staging

Name:		wine
#(peroyvind): please do backports for new versions
Version:	5.8
%if "%{beta}" != ""
Release:	0.%{beta}.1
Source0:	https://dl.winehq.org/wine/source/%(echo %version |cut -d. -f1-2)/%{name}-%{version}-%{beta}.tar.xz
Source1:	https://dl.winehq.org/wine/source/%(echo %version |cut -d. -f1-2)/%{name}-%{version}-%{beta}.tar.xz.sign
%else
Release:	2
Source0:	http://dl.winehq.org/wine/source/%(echo %version |cut -d. -f1).x/wine-%{version}.tar.xz
Source1:	http://dl.winehq.org/wine/source/%(echo %version |cut -d. -f1).x/wine-%{version}.tar.xz.sign
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
#Patch3:		wine-1.9.23-freetype-unresolved-symbol.patch
# https://bugs.winehq.org/show_bug.cgi?id=41930#c0
Patch4:		0001-Revert-gdi32-Fix-arguments-for-OSMesaMakeCurrent-whe.patch
Patch5:		wine-4.14-fix-crackling-audio.patch

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
BuildRequires:	pcap-devel
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
%ifarch %{ix86} %{x86_64}
BuildRequires:	isdn4k-utils-devel
%endif
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
BuildRequires:	libSDL2-2.0.so.1
BuildRequires:	libOpenCL.so.1
BuildRequires:	devel(libncurses)
BuildRequires:	devel(libncursesw)
BuildRequires:	libcups.so.2
BuildRequires:	libsane.so.1
BuildRequires:	libsystemd.so.0
BuildRequires:	devel(libz)
BuildRequires:	libjack.so.0
BuildRequires:	libpulse.so.0
BuildRequires:	libmpg123.so.0
BuildRequires:	libopenal.so.1
BuildRequires:	devel(libasound)
BuildRequires:	libaudiofile.so.1
BuildRequires:	libglut.so.3
BuildRequires:	libpng16.so.16
BuildRequires:	libusb-1.0.so.0
BuildRequires:	libxml2.so.2
BuildRequires:	libxslt.so.1
BuildRequires:	libcapi20.so.3
BuildRequires:	libgif.so.7
BuildRequires:	libtiff.so.5
BuildRequires:	libXpm.so.4
BuildRequires:	librsvg-2.so.2
BuildRequires:	libgphoto2.so.6
BuildRequires:	libgphoto2_port.so.12
BuildRequires:	libldap_r-2.4.so.2
BuildRequires:	liblber-2.4.so.2
BuildRequires:	libdbus-1.so.3
BuildRequires:	libgsm.so.1
BuildRequires:	libodbc.so.2
BuildRequires:	libgnutls.so.30
BuildRequires:	libintl.so.8
BuildRequires:	libd3dadapter9_1
BuildRequires:	liblcms2.so.2
BuildRequires:	libOSMesa.so.8
BuildRequires:	libGL.so.1
BuildRequires:	libGLU.so.1
BuildRequires:	libv4l2.so.0
BuildRequires:	libieee1284.so.3
BuildRequires:	libjpeg.so.8
BuildRequires:	libXcursor.so.1
BuildRequires:	libXcomposite.so.1
BuildRequires:	libXfixes.so.3
BuildRequires:	libXi.so.6
BuildRequires:	libXinerama.so.1
BuildRequires:	libXxf86vm.so.1
BuildRequires:	libXmu.so.6
BuildRequires:	libXrandr.so.2
BuildRequires:	libX11.so.6
BuildRequires:	libXrender.so.1
BuildRequires:	libXext.so.6
BuildRequires:	libSM.so.6
BUildRequires:	libvulkan-devel
BuildRequires:	libvkd3d.so.1
BuildRequires:	libfontconfig.so.1
BuildRequires:	libfreetype.so.6
BuildRequires:	libgstreamer-1.0.so.0
BuildRequires:	libgstvideo-1.0.so.0
BuildRequires:	libgstaudio-1.0.so.0
BuildRequires:	libgstbase-1.0.so.0
BuildRequires:	libva.so.2
BuildRequires:	libva-x11.so.2
BuildRequires:	libva-drm.so.2
BuildRequires:	libavcodec.so.58
BuildRequires:	libudev.so.1
BuildRequires:	libFAudio.so.0
BuildRequires:	libpcap.so.1
BuildRequires:	libkrb5.so.3
BuildRequires:	libk5crypto.so.3
BuildRequires:	libcom_err.so.2
BuildRequires:	libgcrypt.so.20
BuildRequires:	libgpg-error.so.0
BuildRequires:	libgtk-3.so.0
BuildRequires:	libgdk-3.so.0
BuildRequires:	libpangocairo-1.0.so.0
BuildRequires:	libpango-1.0.so.0
BuildRequires:	libharfbuzz.so.0
BuildRequires:	libatk-1.0.so.0
BuildRequires:	libcairo-gobject.so.2
BuildRequires:	libcairo.so.2
BuildRequires:	libgdk_pixbuf-2.0.so.0
BuildRequires:	libgio-2.0.so.0
BuildRequires:	libgobject-2.0.so.0
BuildRequires:	libglib-2.0.so.0
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
BuildRequires:	cross-i686-w64-mingw32-binutils
BuildRequires:	cross-i686-w64-mingw32-gcc-bootstrap
BuildRequires:	cross-i686-w64-mingw32-libc
%ifarch %{x86_64}
BuildRequires:	cross-x86_64-w64-mingw32-binutils
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

#patch3 -p1 -b .dlopenLazy~
%endif
%patch4 -p1 -b .civ3~
%patch5 -p1 -b .pulseaudiosucks~

autoreconf
aclocal
autoconf

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

# FIXME Continuing workarounds for lack of proper multiarch support
export LD_LIBRARY_PATH=`pwd`/lib32
export CFLAGS="`echo $CFLAGS |sed -e 's,-m64,,g'` -L`pwd`/lib32 -I%{_includedir}/freetype2 -m32"
export LDFLAGS="%{ldflags} -L`pwd`/lib32 -m32"
export PKG_CONFIG_PATH="`pwd`/lib32/pkgconfig":%{_datadir}/pkgconfig
mkdir -p lib32/pkgconfig
for i in OpenCL sane-backends zlib jack libpulse \
	libmpg123 openal alsa audiofile freeglut libpng libusb-1.0 libxml-2.0 \
	libxslt xpm libtiff-4 librsvg-2.0 libgphoto2 libxslt gnutls \
	lcms2 osmesa libglvnd glu libv4l2 libjpeg xcursor xcomposite xi \
	xinerama xxf86vm xmu xrandr x11 xrender xext sm vulkan libvkd3d \
	fontconfig freetype2 gstreamer-1.0 gstreamer-base-1.0 \
	gstreamer-plugins-base-1.0 libva libavcodec libudev sdl2 gtk+-3.0; do
	sed -e 's,64,,g' %{_libdir}/pkgconfig/$i.pc >lib32/pkgconfig/$i.pc
done
# ****ing glib SUCKS, why can't they just use stdint.h like the rest
# of the world?
sed -e "s,lib64,lib,g;s,-I\\\${libdir}/glib-2.0/include,-I`pwd`/lib32,g" %{_libdir}/pkgconfig/glib-2.0.pc >lib32/pkgconfig/glib-2.0.pc
sed -e 's,typedef signed long gint64,typedef int64_t gint64,g;s,typedef unsigned long guint64,typedef uint64_t guint64,g' %{_libdir}/glib-2.0/include/glibconfig.h >lib32/glibconfig.h
sed -i -e '/limits.h/i#include <stdint.h>' lib32/glibconfig.h
# Same for dbus and other libraries that prefer compatibility with
# the 1960s over sanity
mkdir lib32/dbus
sed -e "s,64,,g;s,-I\\\${libdir}/dbus-1.0/include,-I`pwd`/lib32,g" %{_libdir}/pkgconfig/dbus-1.pc >lib32/pkgconfig/dbus-1.pc
sed -e 's,typedef signed long gint64,typedef int64_t gint64,g;s,typedef unsigned long guint64,typedef uint64_t guint64,g' %{_libdir}/dbus-1.0/include/dbus/dbus-arch-deps.h >lib32/dbus/dbus-arch-deps.h

for i in libSDL2-2.0.so.1 libOpenCL.so.1 libcups.so.2 \
	libsane.so.1 libsystemd.so.0 libjack.so.0 libpulse.so.0 \
	libmpg123.so.0 libopenal.so.1 libaudiofile.so.1 \
	libglut.so.3 libpng16.so.16 libusb-1.0.so.0 libxml2.so.2 \
	libxslt.so.1 libcapi20.so.3 libgif.so.7	libtiff.so.5 libXpm.so.4 \
	librsvg-2.so.2 libgphoto2.so.6 libgphoto2_port.so.12 \
	libldap_r-2.4.so.2 liblber-2.4.so.2 libdbus-1.so.3 \
	libgsm.so.1 libodbc.so.2 libgnutls.so.30 libintl.so.8 \
	liblcms2.so.2 libOSMesa.so.8 libGL.so.1 \
	libGLU.so.1 libv4l2.so.0 libieee1284.so.3 libjpeg.so.8 \
	libXcursor.so.1 libXcomposite.so.1 libXi.so.6 libXinerama.so.1 \
	libXfixes.so.3 \
	libXxf86vm.so.1 libXmu.so.6 libXrandr.so.2 libX11.so.6 \
	libXrender.so.1 libXext.so.6 libSM.so.6 \
	libvkd3d.so.1 libfontconfig.so.1 libfreetype.so.6 \
	libgstreamer-1.0.so.0 libgstvideo-1.0.so.0 \
	libgstaudio-1.0.so.0 libgstbase-1.0.so.0 \
	libva.so.2 libva-x11.so.2 libva-drm.so.2 \
	libavcodec.so.58 libpcap.so.1 libkrb5.so.3 libk5crypto.so.3 \
	libudev.so.1 libFAudio.so.0 libcom_err.so.2 libgcrypt.so.20 libgpg-error.so.0 \
	libgtk-3.so.0 libgdk-3.so.0 libpangocairo-1.0.so.0 libpango-1.0.so.0 \
	libharfbuzz.so.0 libatk-1.0.so.0 libcairo-gobject.so.2 libcairo.so.2 \
	libgdk_pixbuf-2.0.so.0 libgio-2.0.so.0 libgobject-2.0.so.0 libglib-2.0.so.0 \
	; do
	if [ -e /usr/lib/$i ]; then 
		ln -s /usr/lib/$i lib32/`echo $i |sed -e 's,\.so\..*,.so,'`
	else
		ln -s /lib/$i lib32/`echo $i |sed -e 's,\.so\..*,.so,'`
	fi
done
ln -s libSDL2-2.0.so lib32/libSDL2.so
ln -s libldap_r-2.4.so lib32/libldap_r.so
ln -s liblber-2.4.so lib32/liblber.so
ln -s /usr/lib/libpng16.so.16 lib32/libpng.so
mkdir build32
cd build32
../configure \
		--prefix=%{_prefix} \
		--with-pulse \
		--without-hal \
    		--with-xattr \
		--with-gstreamer \
		--with-wine64=../build
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
%{_datadir}/%{name}/winebus.inf
%{_datadir}/%{name}/winehid.inf
%{_datadir}/%{name}/wineusb.inf
%{_datadir}/%{name}/nls/l_intl.nls
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
%{_libdir}/libwine*.so.%{major}*
%dir %{_libdir}/%{name}
# *.cpl, *.com and friends get built if there
# is a working Windoze crosscompiler
# (x86_64)
%optional %{_libdir}/%{name}/*.cpl
%optional %{_libdir}/%{name}/*.com
%optional %{_libdir}/%{name}/*.ocx
%optional %{_libdir}/%{name}/*.tlb
%optional %{_libdir}/%{name}/*.drv
%optional %{_libdir}/%{name}/*.dll
%optional %{_libdir}/%{name}/*.exe
%optional %{_libdir}/%{name}/*.acm
%optional %{_libdir}/%{name}/*.ds
%optional %{_libdir}/%{name}/*.sys
%{_libdir}/%{name}/*.ax
# If there isn't, they get built as *.cpl.so,
# *.com.so etc. instead
# (e.g. arches that don't have native
# Windoze versions)
# Some stuff gets built as *.*.so all
# the time.
%optional %{_libdir}/%{name}/*.cpl.so
%optional %{_libdir}/%{name}/*.com.so
%optional %{_libdir}/%{name}/*.ocx.so
%optional %{_libdir}/%{name}/*.tlb.so
%{_libdir}/%{name}/*.drv.so
%{_libdir}/%{name}/*.dll.so
%{_libdir}/%{name}/*.exe.so
%{_libdir}/%{name}/*.acm.so
%{_libdir}/%{name}/*.ds.so
%{_libdir}/%{name}/*.sys.so
%ifarch %{ix86}
%{_libdir}/%{name}/*16.so
%{_libdir}/%{name}/*.vxd.so
%endif
%{_libdir}/%{name}/fakedlls
%if %{with wow64}
%{_prefix}/lib/libwine*.so.%{major}*
%dir %{_prefix}/lib/%{name}
%optional %{_prefix}/lib/%{name}/*.cpl.so
%optional %{_prefix}/lib/%{name}/*.com.so
%optional %{_prefix}/lib/%{name}/*.drv.so
%optional %{_prefix}/lib/%{name}/*.dll.so
%optional %{_prefix}/lib/%{name}/*.exe.so
%optional %{_prefix}/lib/%{name}/*.acm.so
%optional %{_prefix}/lib/%{name}/*.ocx.so
%optional %{_prefix}/lib/%{name}/*.vxd.so
%optional %{_prefix}/lib/%{name}/*16.so
%optional %{_prefix}/lib/%{name}/*.tlb.so
%optional %{_prefix}/lib/%{name}/*.ds.so
%optional %{_prefix}/lib/%{name}/*.sys.so
%optional %{_prefix}/lib/%{name}/*.cpl
%optional %{_prefix}/lib/%{name}/*.com
%optional %{_prefix}/lib/%{name}/*.drv
%optional %{_prefix}/lib/%{name}/*.dll
%optional %{_prefix}/lib/%{name}/*.exe
%optional %{_prefix}/lib/%{name}/*.acm
%optional %{_prefix}/lib/%{name}/*.ocx
%optional %{_prefix}/lib/%{name}/*.vxd
%optional %{_prefix}/lib/%{name}/*.tlb
%optional %{_prefix}/lib/%{name}/*.ds
%optional %{_prefix}/lib/%{name}/*.sys
%{_prefix}/lib/%{name}/*.dll16
%{_prefix}/lib/%{name}/*.exe16
%{_prefix}/lib/%{name}/*.drv16
%{_prefix}/lib/%{name}/*.mod16
%{_prefix}/lib/%{name}/*.ax
%{_prefix}/lib/%{name}/fakedlls
%endif

%files devel
%{_libdir}/%{name}/*.a
%{_libdir}/libwine*.so
%{_libdir}/%{name}/*.def
%ifarch %{x86_64}
%{_prefix}/lib/%{name}/*.a
%{_prefix}/lib/libwine*.so
%{_prefix}/lib/%{name}/*.def
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
