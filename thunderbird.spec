%define __libtoolize /bin/true
%define __cputoolize /bin/true

%define official_branding 1

%if %mandriva_branch == Cooker
# Cooker
%define release 1
%else
# Old distros
%define subrel 1
%define release %mkrel 0
%endif

%if %mdkversion >= 201200
# rpmlint just sucks!!!
%define _build_pkgcheck_set %{nil}
%define _build_pkgcheck_srpm %{nil}
%endif

%if %{official_branding}
%define title Mozilla Thunderbird
%else
%define title Mail/News
%endif

%define oname thunderbird
%define tb_appid \{3550f703-e582-4d05-9a08-453d09bdfdc6\}
%define tbdir %{_libdir}/%{oname}-%{version}
%define tbextdir %{_libdir}/mozilla/extensions/%{tb_appid}

%define xpi 0
%define enigmail_version 1.4.1
%define enigmail_short_version 1.4
%define enigmail_id \{847b3a00-7ab1-11d4-8f02-006008948af5\}

%define _provides_exceptions libgtkembedmoz.so\\|libxpcom.so
%define _requires_exceptions libgtkembedmoz.so\\|libxpcom.so

# FIXME: Bug in nsExtensionManager.js prevents using x86_64 as arch
# FIXME: I tried to modify nsExtensionManager.js.in, but it
# FIXME: complained that I had modified it
%ifarch %{ix86}
%define tbarch x86
%else # ix86
%ifarch x86_64
%define tbarch %{_arch}
%else # x86_64
%define tbarch %{_arch}
%endif # x86_64
%endif # ix86

# this seems fragile, so require the exact version or later (#58754)
%define sqlite3_version %(pkg-config --modversion sqlite3 &>/dev/null && pkg-config --modversion sqlite3 2>/dev/null || echo 0)
# this one as well (#59759)
%define nss_libname %mklibname nss 3
%define nss_version %(pkg-config --modversion nss &>/dev/null && pkg-config --modversion nss 2>/dev/null || echo 0)

Name:		thunderbird
Version:	12.0.1
Release:	%{release}
Summary:	Full-featured email, RSS, and newsgroup client
License:	MPL
Group:		Networking/Mail
URL:		http://www.mozillamessaging.com/
Source0:        http://ftp.mozilla.org/pub/mozilla.org/thunderbird/releases/%{version}/source/thunderbird-%{version}.source.tar.bz2
Source1:        http://ftp.mozilla.org/pub/mozilla.org/thunderbird/releases/%{version}/source/thunderbird-%{version}.source.tar.bz2.asc
Source12:       mozilla-thunderbird-mandriva-default-prefs.js
Source30:       mozilla-thunderbird-open-browser.sh
Source31:       mozilla-thunderbird-open-browser-xdg.sh
# Mandriva sources (Source300+)
Source300:      http://www.mozilla-enigmail.org/download/source/enigmail-%{enigmail_version}.tar.gz
Source301:      http://www.mozilla-enigmail.org/download/source/enigmail-%{enigmail_version}.tar.gz.asc
Source302:      %{name}-icons.tar.gz
Source303:	thunderbird.desktop
# Language package template
Source400:	mozilla-thunderbird-enigmail-l10n-template.in
# Build patches
Patch2:         mozilla-firefox-1.0-prdtoa.patch
# Debian patches (Patch200+)
#
Patch201:       mozilla-thunderbird-default-mailer.patch
Patch212:       mozilla-thunderbird-enigmail-ui-content-contents-rdf.patch
Patch213:       mozilla-thunderbird-enigmail-build-package-contents-rdf.patch
Patch215:	mozilla-thunderbird-enigmail-visibility.patch
# Mandriva patches (Patch300+)
Patch300:       mozilla-thunderbird-0.8-progname.patch
Patch301:       mozilla-thunderbird-enigmail-package.patch
Patch304:       mozilla-thunderbird-run-mozilla.patch
# OpenSuse patches (Patch400+)
Patch400:	thunderbird-appname.patch
Patch401:	mozilla-thunderbird-10.0.1-no_optimization_override.diff

# https://bugzilla.mozilla.org/show_bug.cgi?id=722975
Patch500: firefox_add_ifdefs_to_gfx_thebes_gfxPlatform.cpp.patch

%if %{official_branding}
BuildRequires:	imagemagick
%endif
BuildRequires:	autoconf2.1
BuildRequires:	gzip
BuildRequires:	python
BuildRequires:	unzip
BuildRequires:	yasm >= 1.0.1
BuildRequires:	zip
BuildRequires:	jpeg-devel
BuildRequires:	libiw-devel
BuildRequires:	nss-static-devel >= 2:3.13.2
BuildRequires:	python-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(hunspell)
BuildRequires:	pkgconfig(libevent) >= 1.4.7
BuildRequires:	pkgconfig(libgnomeui-2.0)
BuildRequires:	pkgconfig(libIDL-2.0)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(nspr)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(sqlite3) >= 3.7.1.1
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(vpx) >= 0.9.7
BuildRequires:	pkgconfig(zlib)
%if %mdkversion >= 201100
BuildRequires:	pkgconfig(cairo) >= 1.10
BuildRequires:	pkgconfig(libpng) >= 1.4.8
%endif

Requires:	%{mklibname sqlite3_ 0} >= %{sqlite3_version}
Requires:	%{nss_libname} >= 2:%{nss_version}
Requires(post,postun):	desktop-file-utils
Requires(post):	mktemp
Requires(post,postun): rpm-helper
Requires: xdg-utils
Obsoletes: mozilla-thunderbird < %{version}-%{release}
Provides: mozilla-thunderbird = %{version}-%{release}

%description
%{title} is a full-featured email, RSS and newsgroup client that
makes emailing safer, faster and easier than ever before.

#===============================================================================
# enigmail-l10n
# Supported l10n language lists
%define l10n_langlist	ar ca cs de el es fi fr it ja ko nb nl pl pt pt_BR ru sl sv tr vi zh_CN zh_TW

# Disabled l10n languages, for any reason
# nl sk es_AR do not support 0.95.0 yet
%define disabled_l10n_langlist	hu
# define disabled_l10n_langlist %{nil}

# Language descriptions
%define language_ar ar
%define langname_ar Arabic
%define language_ca ca
%define langname_ca Catalan
%define language_cs cs-CZ
%define langname_cs Czech
%define language_de de
%define langname_de German
%define language_el el
%define langname_el Greek
%define language_es_AR es-AR
%define langname_es_AR Spanish (Argentina)
%define language_es es-ES
%define langname_es Spanish
%define language_fi fi-FI
%define langname_fi Finnish
%define language_fr fr
%define langname_fr French
%define language_hu hu-HU
%define langname_hu Hungarian
%define language_it it-IT
%define langname_it Italian
%define language_ja ja-JP
%define langname_ja Japanese
%define language_ko ko-KR
%define langname_ko Korean
%define language_nb nb-NO
%define langname_nb Norwegian Bokmaal
%define langname_nl Dutch
%define language_nl nl
%define language_pl pl
%define langname_pl Polish
%define langname_pt Portuguese
%define language_pt pt-PT
%define language_pt_BR pt-BR
%define langname_pt_BR Brazilian portuguese
%define language_ro ro-RO
%define langname_ro Romanian
%define language_ru ru-RU
%define langname_ru Russian
%define language_sk sk
%define langname_sk Slovak
%define language_sl sl-SI
%define langname_sl Slovenian
%define language_sv sv-SE
%define langname_sv Swedish
%define language_tr tr
%define langname_tr Turkish
%define language_vi vi
%define langname_vi Vietnamese
%define language_zh_CN zh-CN
%define langname_zh_CN Simplified Chinese
%define language_zh_TW zh-TW
%define langname_zh_TW Traditional Chinese

# --- Danger line ---

# All langs
%{expand:%%define langlist %(for lang in %l10n_langlist; do echo "$lang"; done | sort -u | sed ':a;$!N;s/\n/ /;ta')}

# Defaults (all languages enabled by default)
# l10n
%{expand:%(for lang in %l10n_langlist; do echo "%%define l10n_$lang 1"; done)}
%{expand:%(for lang in %disabled_l10n_langlist; do echo "%%define l10n_$lang 0"; done)}

# Params
%{expand:%(for lang in %langlist; do echo "%%bcond_without $lang"; done)}

# Locales
%{expand:%(for lang in %l10n_langlist; do echo "%%define locale_$lang `echo $lang | cut -d _ -f 1` "; done)}

# Expand all languages packages.
%{expand:%(\
	for lang in %langlist; do\
		echo "%%{expand:%%(sed "s!__LANG__!$lang!g" %{_sourcedir}/mozilla-thunderbird-enigmail-l10n-template.in 2> /dev/null)}";\
	done\
	)
}

#===============================================================================

%package enigmail
Summary:        Access the authentication and encryption features provided by GnuPG
Group:          Networking/Mail
Requires:       %{name} >= %{version}
Requires:       gnupg
Requires(post,preun): %{name} >= %{version}
Requires(post,postun):	mktemp
# Bug #35180
Suggests:	pinentry-gtk
Obsoletes:	mozilla-thunderbird-enigmail < %{version}-%{release}
Provides:	mozilla-thunderbird-enigmail = %{version}-%{release}
%(for lang in %l10n_langlist %disabled_l10n_langlist; do
    echo "Obsoletes: mozilla-thunderbird-enigmail-$lang < %{version}-%{release}"
    echo "Obsoletes: mozilla-thunderbird-enigmail-l10n-$lang < %{version}-%{release}"
done)

%description enigmail
Enigmail is an extension to the mail client of %{title}
which allows users to access the authentication and encryption
features provided by GnuPG.

Main Features

    * Encrypt/sign mail when sending, decrypt/authenticate received
      mail
    * Support for inline-PGP (RFC 2440) and PGP/MIME (RFC 3156)
    * Per-Account based encryption and signing defaults
    * Per-Recipient rules for automated key selection, and
      enabling/disabling encryption and signing
    * OpenPGP key management interface

#===============================================================================

%package -n nsinstall
Summary:        Netscape portable install command
Group:          Development/Other

%description -n nsinstall
Netscape portable install command.

#===============================================================================
%package lightning
Summary:	Calendar extension for Thunderbird
Group:		Networking/Mail
URL:		http://www.mozilla.org/projects/calendar/lightning/
Requires:	%{name} >= %{version}
Obsoletes:	mozilla-thunderbird-lightning < %{version}-%{release}
Provides:	mozilla-thunderbird-lightning = %{version}-%{release}

%description lightning
Calendar extension for Thunderbird.


#===============================================================================

%prep
%setup -q -c -n %{name}-%{version}

#===================
# Thunderbird itself
%setup -q -T -D -n %{name}-%{version}/comm-release

%patch2 -p0

%patch201 -p2 -b .default_mail

%patch300 -p0 -b .progname
%patch301 -p1 -b .enigmailpackage
%patch304 -p0 -b .run-mozilla

%patch400 -p1 -b .appname
%patch401 -p0 -b .no_optimization_override
%patch500 -p1

#===============================================================================
# Enigmail
%setup -q -T -D -n %{name}-%{version}/comm-release/mozilla/extensions -a300
%if 0
%patch212 -p2 -b .enigmail-ui-content-contents-rdf
%patch213 -p2 -b .enigmail-build-package-contents-rdf
%endif

%if !%{official_branding}
%setup -q -T -D -n %{name}-%{version}/comm-release -a302
%endif

%setup -q -T -D -n %{name}-%{version}/comm-release

#===============================================================================

%build
export MOZCONFIG=`pwd`/.mozconfig
cat > $MOZCONFIG << EOF
mk_add_options MOZILLA_OFFICIAL=1
mk_add_options BUILD_OFFICIAL=1
#mk_add_options MOZ_MAKE_FLAGS="%{_smp_mflags}"
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@
ac_add_options --prefix="%{_prefix}"
ac_add_options --libdir="%{_libdir}"
ac_add_options --sysconfdir="%{_sysconfdir}"
ac_add_options --mandir="%{_mandir}"
ac_add_options --includedir="%{_includedir}"
ac_add_options --datadir="%{_datadir}"
ac_add_options --enable-application=mail
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-jpeg
ac_add_options --with-system-zlib
ac_add_options --with-system-libevent
ac_add_options --with-system-libvpx
%if %mdkversion >= 201100
ac_add_options --with-system-png
ac_add_options --enable-system-cairo
%else
ac_add_options --disable-system-png
ac_add_options --disable-system-cairo
%endif
ac_add_options --with-system-bz2
ac_add_options --enable-system-sqlite
ac_add_options --enable-system-hunspell
ac_add_options --with-pthreads
ac_add_options --disable-tests
ac_add_options --disable-debug
ac_add_options --disable-installer
ac_add_options --disable-updater
ac_add_options --enable-xinerama
ac_add_options --disable-crashreporter
ac_add_options --enable-default-toolkit=cairo-gtk2
ac_add_options --disable-xprint
ac_add_options --disable-strip
ac_add_options --enable-pango
ac_add_options --enable-startup-notification
ac_add_options --enable-svg
ac_add_options --enable-canvas
ac_add_options --enable-crypto
ac_add_options --enable-mathml
ac_add_options --disable-gnomevfs
ac_add_options --enable-gio
ac_add_options --enable-calendar
ac_add_options --enable-strip
ac_add_options --enable-official-branding
ac_add_options --with-distribution-id=com.mandriva
ac_add_options --enable-optimize
ac_add_options --enable-startup-notification
ac_add_options --disable-cpp-exceptions
EOF

# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
#
# Disable C++ exceptions since Mozilla code is not exception-safe
#
MOZ_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS" | sed -e 's/-Wall//' -e 's/-fexceptions/-fno-exceptions/g')
export CFLAGS="$MOZ_OPT_FLAGS"
export CXXFLAGS="$MOZ_OPT_FLAGS"
export PREFIX="%{_prefix}"
export LIBDIR="%{_libdir}"

MOZ_SMP_FLAGS=-j1
# On x86 architectures, Mozilla can build up to 4 jobs at once in parallel,
# however builds tend to fail on other arches when building in parallel.
%ifarch %{ix86} x86_64
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 2 ] && MOZ_SMP_FLAGS=-j2
[ "$RPM_BUILD_NCPUS" -ge 4 ] && MOZ_SMP_FLAGS=-j4
%endif

export LDFLAGS="%{ldflags}"
make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS"

#===============================================================================

pushd mozilla/extensions/enigmail
for i in `find . -type f -name Makefile.in`; do
    if [ -f $i.bak ]; then
        cp $i.bak $i
    else
        cp $i $i.bak
    fi
#    %{__perl} -pi -e 's|^(DEPTH.*= )../|\1|;' $i
done
./makemake -r
popd

pushd mozilla/extensions/enigmail
%make

(cd lang
 %{__perl} -pi -e 's|es-AR/enigmail.properties|es-ES/enigmail.properties|' jar.mn
 echo 'zh-TW' >> current-languages.txt
 make
 for i in `cat current-languages.txt`; do
   ./make-lang.sh $i %{enigmail_short_version}
 done
)

%make xpi
popd

#===============================================================================

%install
mkdir -p %{buildroot}{%{_libdir},%{_bindir},%{_datadir}/applications}
mkdir -p %buildroot%tbdir

rm -f extensions/spellcheck/locales/en-US/hunspell/en-US.{dic,aff}

%makeinstall_std STRIP=/bin/true

rm -rf %buildroot%tbdir/dictionaries
ln -s /usr/share/dict/mozilla %buildroot%tbdir/dictionaries

%if %{official_branding}
install -p -D %{buildroot}/%{tbdir}/chrome/icons/default/default256.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
%else
install -p -D %{SOURCE302} %{buildroot}%{_datadir}/pixmaps/%{name}.png
%endif

%{__install} -p -D %{SOURCE303} %{buildroot}/%{_datadir}/applications/mandriva-%{name}.desktop

# set up the thunderbird start script
(cd %{buildroot}%{_bindir} && %{__ln_s} thunderbird %{name})

%{__perl} -pi -e 's|^moz_libdir=.*|moz_libdir=%{tbdir}|' %{buildroot}%{_bindir}/thunderbird
%{__perl} -pi -e 's|^MRE_HOME=.*|MRE_HOME=%{tbdir}|' %{buildroot}%{_bindir}/thunderbird

# For backwards compatibility with old profiles. Bug #37528
install -m 755 %{SOURCE31} %{buildroot}%{tbdir}/open-browser.sh
# For new profiles
%define COMMAND /usr/bin/xdg-open

%{__cat} %{SOURCE12} | %{__perl} -p -e 's,THUNDERBIRD_RPM_VR,%{version}-%{release},g;' \
                                    -e 's,THUNDERBIRD_VENDOR_COMMENT,%{mandriva_release},g;' \
  > %{buildroot}/mdv-default-prefs
cp -a %{buildroot}/mdv-default-prefs %{buildroot}%{tbdir}/defaults/pref/all-mandriva.js
rm -f %{buildroot}/mdv-default-prefs

#===============================================================================

# icons
mkdir -p %{buildroot}{%{_liconsdir},%{_iconsdir},%{_miconsdir}}
%if %{official_branding}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{16x16,22x22,24x24,32x32,48x48,256x256}/apps
install -m 644 %{buildroot}/%{tbdir}/chrome/icons/default/default48.png %{buildroot}%{_liconsdir}/%{name}.png
install -m 644 %{buildroot}/%{tbdir}/chrome/icons/default/default32.png %{buildroot}%{_iconsdir}/%{name}.png
install -m 644 %{buildroot}/%{tbdir}/chrome/icons/default/default16.png %{buildroot}%{_miconsdir}/%{name}.png
install -m 644 %{buildroot}/%{tbdir}/chrome/icons/default/default16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
install -m 644 %{buildroot}/%{tbdir}/chrome/icons/default/default22.png %{buildroot}%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
install -m 644 %{buildroot}/%{tbdir}/chrome/icons/default/default24.png %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
install -m 644 %{buildroot}/%{tbdir}/chrome/icons/default/default32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -m 644 %{buildroot}/%{tbdir}/chrome/icons/default/default48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
install -m 644 %{buildroot}/%{tbdir}/chrome/icons/default/default256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%else
#mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{64x64,128x128}/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{16x16,22x22,24x24,32x32,48x48,64x64,128x128}/apps
install -m 644 %{name}-48.png %{buildroot}%{_liconsdir}/%{name}.png
install -m 644 %{name}-32.png %{buildroot}%{_iconsdir}/%{name}.png
install -m 644 %{name}-16.png %{buildroot}%{_miconsdir}/%{name}.png
# Converting up, but not a big issue now that we have official branding
install -m 644 %{name}-16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
install -m 644 %{name}-22.png %{buildroot}%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
install -m 644 %{name}-24.png %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
install -m 644 %{name}-32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -m 644 %{name}-48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
install -m 644 %{name}-64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
install -m 644 %{name}-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%endif

#===============================================================================

mkdir -p %{buildroot}%{tbextdir}/%{enigmail_id}
%if !%{xpi}
# MD this is odd, the short version here is 1.5 but the rest of the files still contain 1.4
#{_bindir}/unzip -q mozilla/dist/bin/enigmail-%{enigmail_short_version}*.xpi -d %{buildroot}%{tbextdir}/%{enigmail_id}
%{_bindir}/unzip -q mozilla/dist/bin/enigmail-*.xpi -d %{buildroot}%{tbextdir}/%{enigmail_id}
%{__chmod} 644 %{buildroot}%{tbextdir}/%{enigmail_id}/chrome.manifest
%else
cp -aL mozilla/dist/bin/enigmail-%{enigmail_short_version}*.xpi %{buildroot}%{tbextdir}/%{enigmail_id}/%{enigmail_id}.xpi
%endif

#==============================================================================
#enigmail lang package
# Convert rpm macros to bash variables
%{expand:%(for lang in %langlist; do echo "language_$lang=%%{language_$lang}"; done)}
%{expand:%(for lang in %langlist; do echo "with_$lang=%%{with $lang}"; done)}
%{expand:%(for lang in %l10n_langlist; do echo "l10n_$lang=%%{l10n_$lang}"; done)}
pushd mozilla/extensions/enigmail/lang
 for lang in %langlist; do
    mkdir -p %{buildroot}%{_datadir}/mozilla/extensions/%{tb_appid}/enigmail-$lang@enigmail.mozdev.org
    language="language_$lang"
    language=${!language}
    %{_bindir}/unzip -q enigmail-${language}-%{enigmail_short_version}.xpi -d %{buildroot}%{_datadir}/mozilla/extensions/%{tb_appid}/enigmail-$lang@enigmail.mozdev.org/
 done
popd

#===============================================================================
# lightning ext here
pushd mozilla/dist/xpi-stage/
  for ext in {calendar-timezones,gdata-provider,lightning}; do
    hash="$(sed -n '/^    <em:id>\(.*\)<\/em:id>.*/{s//\1/p;q}' $ext/install.rdf)"
    mkdir -p %buildroot%{tbextdir}/$hash
    %{_bindir}/unzip -q $ext.xpi -d %buildroot%{tbextdir}/$hash/
  done
popd

#===============================================================================

cp -aL mozilla/dist/bin/nsinstall %{buildroot}%{_bindir}

#==============================================================================
#exclude devel files
rm -rf %{buildroot}%{_datadir}/idl/%{oname}-%{version}
rm -rf %{buildroot}%{_includedir}/%{oname}-%{version}
rm -rf %{buildroot}%{_libdir}/%{oname}-devel-%{version}

#===============================================================================

%pre
if [ $1 == 2 ]; then
  if [ -d %{tbdir}/dictionaries ]; then
    # Otherelse rpm can't switch this into a symlink :(
    rm -rf %{tbdir}/dictionaries
  fi
fi

%post
%{_bindir}/update-desktop-database %{_datadir}/applications

mktemp="/bin/mktemp -d -q -p /tmp -t %{name}.XXXXXXXXXX"

TMPDIR= TB_TMPDIR=`$mktemp` && {
    HOME="$TB_TMPDIR" LD_LIBRARY_PATH="%{tbdir}" %{tbdir}/thunderbird-bin -nox -register
    test -d "$TB_TMPDIR" && rm -rf -- "$TB_TMPDIR"
}

if [ -x %{_bindir}/gtk-update-icon-cache ]; then
 %{_bindir}/gtk-update-icon-cache --force --quiet %{_datadir}/icons/hicolor
fi


%postun
%{_bindir}/update-desktop-database %{_datadir}/applications
if [ "$1" = "0" -a -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --force --quiet %{_datadir}/icons/hicolor
fi


#===============================================================================

%post enigmail
if [ -f %{tbdir}/components/compreg.dat ]; then
    rm -f %{tbdir}/components/compreg.dat
fi

if [ -f %{tbdir}/components/xpti.dat ]; then
    rm -f %{tbdir}/components/xpti.dat
fi

mktemp="/bin/mktemp -d -q -p /tmp -t %{name}.XXXXXXXXXX"

TMPDIR= TB_TMPDIR=`$mktemp` && {
%if %{xpi}
    HOME="$TB_TMPDIR" LD_LIBRARY_PATH="%{tbdir}" %{tbdir}/thunderbird-bin -nox -install-global-extension %{tbextdir}/enigmail-%{enigmail_version}-linux-*.xpi
%endif
    HOME="$TB_TMPDIR" LD_LIBRARY_PATH="%{tbdir}" %{tbdir}/thunderbird-bin -nox -register
    test -d "$TB_TMPDIR" && rm -rf -- "$TB_TMPDIR"
}

%preun enigmail
if [ -f %{tbdir}/components/compreg.dat ]; then
    rm -f %{tbdir}/components/compreg.dat
fi

if [ -f %{tbdir}/components/xpti.dat ]; then
    rm -f %{tbdir}/components/xpti.dat
fi

if [ -x %{tbdir}/thunderbird-bin ]; then 
mktemp="/bin/mktemp -d -q -p /tmp -t %{name}.XXXXXXXXXX"

  TMPDIR= TB_TMPDIR=`$mktemp` && {
  %if %{xpi}
      HOME="$TB_TMPDIR" LD_LIBRARY_PATH="%{tbdir}" %{tbdir}/thunderbird-bin -nox -install-global-extension %{tbextdir}/enigmail-%{enigmail_version}-linux-*.xpi
  %endif
      HOME="$TB_TMPDIR" LD_LIBRARY_PATH="%{tbdir}" %{tbdir}/thunderbird-bin -nox -register
      test -d "$TB_TMPDIR" && rm -rf -- "$TB_TMPDIR"
  }
fi

#===============================================================================

%files
%doc mozilla/LEGAL
%attr(755,root,root) %{_bindir}/mozilla-thunderbird
%attr(755,root,root) %{_bindir}/thunderbird
%attr(644,root,root) %{_datadir}/applications/*.desktop
%attr(644,root,root) %{_datadir}/pixmaps/%{name}.png
%{tbdir}
%if %{xpi}
%dir %{tbextdir}
%endif
# Mandriva menu
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
# other icons
%if %{official_branding}
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%else
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%endif
# enigmail
%exclude %{tbextdir}/%{enigmail_id}

%files enigmail
%{tbextdir}/%{enigmail_id}

%files -n nsinstall
%{_bindir}/nsinstall

%files lightning
%{tbextdir}/calendar-timezones@mozilla.org
%{tbextdir}/{a62ef8ec-5fdc-40c2-873c-223b8a6925cc}
%{tbextdir}/{e2fda1a4-762b-4020-b5ad-a41df1933103}
