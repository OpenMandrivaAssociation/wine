%define	lib_name_orig	lib%{name}
%define	lib_major	1
%define	lib_name	%mklibname %{name} %{lib_major}
%define	lib_name_devel	%{mklibname -d wine}

Name:		wine
#(peroyvind): please do backports for new versions
Version:	1.1.30
%define pre	0
%define rel	1
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
Patch2:		wine-1.1.23-fix-str-fmt.patch
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
Patch400:       http://art.ified.ca/downloads/winepulse/winepulse-0.31-configure.ac.patch
Patch401:       http://art.ified.ca/downloads/winepulse/winepulse-0.30.patch
Patch402:	http://art.ified.ca/downloads/winepulse/winepulse-winecfg-0.6.patch

# (anssi) Wine needs GCC 4.4+ on x86_64 for MS ABI support. Note also that
# 64-bit wine cannot run 32-bit programs, so it should be named differently
# to allow co-installation. Upstream has not yet implemented this
# co-habitation, so one would need to resolve conflicts manually.
ExclusiveArch:	%{ix86}
%ifarch x86_64
BuildRequires:	gcc >= 4.4
%endif
BuildRequires:	bison flex gpm-devel perl-devel ncurses-devel sgml-tools
BuildRequires:	X11-devel freetype2-devel autoconf2.5 docbook-utils docbook-dtd-sgml
BuildRequires:	cups-devel jackit-devel imagemagick isdn4k-utils-devel xpm-devel
BuildRequires:	sane-devel glibc-static-devel esound-devel ungif-devel chrpath
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
Provides:	wine-utils = %{epoch}:%{version}-%{release} wine-full = %{epoch}:%{version}-%{release}
Provides:	%{lib_name}-capi = %{epoch}:%{version}-%{release} %{lib_name}-twain = %{epoch}:%{version}-%{release}
Obsoletes:	wine-utils wine-full %{lib_name}-capi %{lib_name}-twain
Requires:	freetype2 %{lib_name} = %{epoch}:%{version}
Requires:	xmessage
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires(post): desktop-common-data
Requires(postun): desktop-common-data
Requires(preun): rpm-helper
Requires(post):	rpm-helper
%define	_requires_exceptions	libgphoto*\\|libieee1284*\\|libjpeg*\\|libsane*\\|libusb*\\|libesd*\\|libarts*\\|libasound*\\|libaudio*
Conflicts:	wine < 1:0.9-3mdk

%description
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix.  It
consists of a program loader which loads and executes a Microsoft
Windows binary, and a library (called Winelib) that implements Windows
API calls using their Unix or X11 equivalents.  The library may also
be used for porting Win32 code into native Unix executables.

%package -n	%{lib_name}
Summary:	Libraries for %{name}
Group:		System/Libraries
Provides:	%{lib_name_orig} = %{epoch}:%{version}-%{release}
Requires(post): sed
Requires(postun): sed
Conflicts:	wine < 1:0.9-3mdk
Conflicts:	wine-utils < 1:0.9-3mdk

%description -n %{lib_name}
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix.

This package contains the library needed to run programs dynamically
linked with %{lib_name_orig}.
Wine is often updated.

%package -n	%{lib_name_devel}
Summary:	Static libraries and headers for %{name}
Group:		Development/C
Requires:	%{lib_name} = %{epoch}:%{version}
Provides:	%{lib_name_orig}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	wine-devel
Provides:	wine-devel
Obsoletes:	%{mklibname -d wine 1} < %{epoch}:%{version}

%description -n	%{lib_name_devel}
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix.

%{lib_name_devel} contains the libraries and header files needed to
develop programs which make use of wine.

Wine is often updated.

%prep
%setup -q -n %name-%o_ver
%patch1 -p0 -b .chinese
%patch2 -p0 -b .str
%patch108 -p1 -b .conf
%patch400 -p1
%patch401 -p1
%patch402 -p1
%if %mdkversion >= 200810
%endif
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
%if %{mdkversion} >= 200800
        <Name>Tools</Name>
%else
        <Name>More Applications</Name>
%endif
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
		"wineconsole cmd":Command\ Line;
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
convert programs/winemenubuilder/wine.xpm -size 16x16 %{buildroot}%{_miconsdir}/%{name}.png
convert programs/winemenubuilder/wine.xpm -size 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert programs/winemenubuilder/wine.xpm -size 48x48 %{buildroot}%{_liconsdir}/%{name}.png

chrpath -d %{buildroot}%{_bindir}/{wine,wineserver,wmc,wrc} %{buildroot}%{_libdir}/%{name}/*.so

%clean
rm -fr %{buildroot}

%preun
%_preun_service %{name}

%post
%_post_service %{name}
%if %mdkversion < 200900
%{update_desktop_database}
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_desktop_database}
%{clean_menus}
%endif

%post -n %{lib_name}
%{__sed} -i "N;s#%{_libdir}/wine\n##g" %{_sysconfdir}/ld.so.conf
%if %mdkversion < 200900
/sbin/ldconfig
%endif

%postun -n %{lib_name}
%{__sed} -i "N;s#%{_libdir}/wine\n##g" %{_sysconfdir}/ld.so.conf
%if %mdkversion < 200900
/sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc ANNOUNCE AUTHORS README
%{_initrddir}/%{name}
%{_bindir}/wine
%{_bindir}/winecfg
%{_bindir}/wineconsole*
%{_bindir}/wineserver
%{_bindir}/wineboot
%{_bindir}/function_grep.pl
%{_bindir}/wineprefixcreate
%{_bindir}/wine-preloader
%{_bindir}/msiexec
%{_bindir}/notepad
%{_bindir}/regedit
%{_bindir}/winemine
%{_bindir}/winepath
%{_bindir}/regsvr32
%{_bindir}/winefile
%{_mandir}/man1/wine.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wine.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/*
%{_mandir}/man1/wineserver.1*
%{_mandir}/man1/wineprefixcreate.1*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/generic.ppd
%{_datadir}/%{name}/%{name}.inf
%{_datadir}/applications/*.desktop
%{_sysconfdir}/xdg/menus/applications-merged/mandriva-%{name}.menu
%{_datadir}/desktop-directories/mandriva-%{name}.directory
%dir %{_datadir}/wine/fonts
%{_datadir}/wine/fonts/*
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/libwine*.so.%{lib_major}*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.cpl.so
%{_libdir}/%{name}/*.drv.so
%{_libdir}/%{name}/*.dll.so
%{_libdir}/%{name}/*.exe.so
%{_libdir}/%{name}/*.acm.so
%{_libdir}/%{name}/*.ocx.so
%{_libdir}/%{name}/*.vxd.so
%{_libdir}/%{name}/*.tlb.so
%{_libdir}/%{name}/*.ds.so
%{_libdir}/%{name}/*.sys.so
%{_libdir}/%{name}/*16
%{_libdir}/%{name}/*16.so
%{_libdir}/%{name}/fakedlls

%files -n %{lib_name_devel}
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
