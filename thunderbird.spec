%define _disable_lto 1

%define __libtoolize /bin/true
%define __cputoolize /bin/true

%define title Mozilla Thunderbird

%define oname thunderbird
%define thunderbird_package thunderbird
%define tb_appid \{3550f703-e582-4d05-9a08-453d09bdfdc6\}
%define tbdir %{_libdir}/%{oname}-%{version}
%define tbextdir %{_libdir}/mozilla/extensions/%{tb_appid}
%define tblangdir %{_datadir}/mozilla/extensions/%{tb_appid}


%define objdir objdir

%define xpi 0
%define enigmail_version 1.9.6.1
%define enigmail_short_version %(echo %{version}| cut -d. -f1,2)
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
%define sqlite3_libname %{mklibname sqlite3_ 0}
%define sqlite3_version %(pkg-config --modversion sqlite3 &>/dev/null && pkg-config --modversion sqlite3 2>/dev/null || echo 0)
# this one as well (#59759)
%define nss_libname %mklibname nss 3
%define nss_version %(pkg-config --modversion nss &>/dev/null && pkg-config --modversion nss 2>/dev/null || echo 0)

%define xpidir http://ftp.mozilla.org/pub/mozilla.org/thunderbird/releases/%{version}/linux-i686/xpi/

# Supported l10n language lists
%define langlist  ar ast be bg bn_BD br ca cs da de el en_GB en_US es_AR es_ES et eu fi fr fy ga gd gl he hr hu hy id is it ja ko lt nb_NO nl nn_NO pa_IN pl pt_BR pt_PT ro ru si sk sl sq sr sv_SE ta_LK tr uk vi zh_CN zh_TW

# Disabled l10n languages, for any reason
%define disabled_langlist gu_IN mk sr af rm

# Disabled myspell dicts, for any reason
%define disabled_dict_langlist	ar be br_FR es_AR eu fi fy ga gu_IN he ja ko mk pa_IN rm tr zh_CN zh_TW

%define use_dict 0

# Language descriptions
%define language_af af
%define langname_af Afrikaans
%define language_ar ar
%define langname_ar Arabic
%define language_ast ast
%define langname_ast Asturian
%define language_be be
%define langname_be Belarusian
%define language_bg bg
%define langname_bg Bulgarian
%define language_bn_BD bn-BD
%define langname_bn_BD Bengali (Bangla)
%define language_br br
%define langname_br Breton
%define language_ca ca
%define langname_ca Catalan
%define language_cs cs
%define langname_cs Czech
%define language_da da
%define langname_da Dansk
%define language_de de
%define langname_de German
%define language_el el
%define langname_el Greek
%define language_en_GB en-GB
%define langname_en_GB British English
%define language_en_US en-US
%define langname_en_US American English
%define language_es_AR es-AR
%define langname_es_AR Spanish (Argentina)
%define language_es_ES es-ES
%define langname_es_ES Spanish
%define language_et_EE et-EE
%define langname_et_EE Estonian (Magento)
%define language_et et
%define langname_et Estonian
%define language_eu eu
%define langname_eu Basque
%define language_fi fi
%define langname_fi Finnish
%define language_fr fr
%define langname_fr French
%define language_fy fy-NL
%define langname_fy Frisian
%define language_ga ga-IE
%define langname_ga Irish
%define language_gd gd
%define langname_gd Scottish Gaelic
%define language_gl gl
%define langname_gl Galician
%define language_gu_IN gu-IN
%define langname_gu_IN Gujarati
%define language_he he
%define langname_he Hebrew
%define language_hr hr
%define langname_hr Croatian
%define language_hu hu
%define langname_hu Hungarian
%define language_hy hy-AM
%define langname_hy Armenian
%define language_id id
%define langname_id Indonesian
%define language_is is
%define langname_is Icelandic
%define language_it it
%define langname_it Italian
%define language_ja ja
%define langname_ja Japanese
%define language_ka ka
%define langname_ka Georgian
%define language_ko ko
%define langname_ko Korean
%define language_lt lt
%define langname_lt Lithuanian
%define language_mk mk
%define langname_mk Macedonian
%define language_nb_NO nb-NO
%define langname_nb_NO Norwegian Bokmaal
%define language_nl nl
%define langname_nl Dutch
%define language_nn_NO nn-NO
%define langname_nn_NO Norwegian Nynorsk
%define language_pa_IN pa-IN
%define langname_pa_IN Punjabi (gurmukhi)
%define language_pl pl
%define langname_pl Polish
%define language_pt_BR pt-BR
%define langname_pt_BR Brazilian portuguese
%define language_pt_PT pt-PT
%define langname_pt_PT Portuguese
%define language_rm rm
%define langname_rm Romansh
%define language_ro ro
%define langname_ro Romanian
%define language_ru ru
%define langname_ru Russian
%define language_si si
%define langname_si Sinhala
%define language_sk sk
%define langname_sk Slovak
%define language_sl sl
%define langname_sl Slovenian
%define language_sq sq
%define langname_sq Albanian
%define language_sr sr
%define langname_sr Serbian
%define language_sv_SE sv-SE
%define langname_sv_SE Swedish
%define language_ta_LK ta-LK
%define langname_ta_LK Tamil (Sri-Lanka)
%define language_tr tr
%define langname_tr Turkish
%define language_uk uk
%define langname_uk Ukrainian
%define language_vi vi
%define langname_vi Vietnamese
%define language_zh_CN zh-CN
%define langname_zh_CN Simplified Chinese
%define language_zh_TW zh-TW
%define langname_zh_TW Traditional Chinese

# --- Danger line ---

# Defaults (all languages enabled by default)
# l10n
%{expand:%(for lang in %langlist; do echo "%%define with_$lang 1"; done)}
%{expand:%(for lang in %disabled_langlist; do echo "%%define with_$lang 0"; done)}
# dicts
%{expand:%(for lang in %langlist; do echo "%%define with_dict_$lang %{use_dict}"; done)}
%{expand:%(for lang in %disabled_dict_langlist; do echo "%%define with_dict_$lang 0"; done)}

# Locales
%{expand:%(for lang in %langlist; do echo "%%define locale_$lang `echo $lang | cut -d _ -f 1` "; done)}

%if %use_dict
# myspell dicts, allows setting preferences between several providers.
%{expand:%(for lang in %langlist; do echo "%%define myspell_$lang myspell-$lang"; done)}
%define myspell_de myspell-de_DE
%define myspell_fr myspell-fr_FR
%endif

Summary:	Full-featured email, RSS, and newsgroup client
Name:		thunderbird
Version:	52.0
Release:	0.1
License:	MPL
Group:		Networking/Mail
Url:		http://www.mozillamessaging.com/
Source0:        http://ftp.mozilla.org/pub/mozilla.org/thunderbird/releases/%{version}/source/thunderbird-%{version}.source.tar.xz
Source12:       mozilla-thunderbird-mandriva-default-prefs.js
Source30:       mozilla-thunderbird-open-browser.sh
Source31:       mozilla-thunderbird-open-browser-xdg.sh
Source100:	thunderbird.rpmlintrc
# Mandriva sources (Source300+)
Source300:      http://www.mozilla-enigmail.org/download/source/enigmail-%{enigmail_version}.tar.gz
Source301:      http://www.mozilla-enigmail.org/download/source/enigmail-%{enigmail_version}.tar.gz.asc
Source302:      %{name}-icons.tar.gz
Source303:	thunderbird.desktop
# Language package template
Source400:	mozilla-thunderbird-enigmail-l10n-template.in
Source401:	thunderbird-l10n-template.in
# l10n sources
%{expand:%(\
	i=500;\
	for lang in %langlist; do\
		echo "%%{expand:Source$i: %{xpidir}/%%{language_$lang}.xpi}";\
		i=$[i+1];\
	done\
	)
}
%if %use_dict
%{expand:%(\
	disabled="%{disabled_dict_langlist}";\
	for lang in %langlist; do\
		echo "$disabled" | grep -q "\<$lang\>" || \
			echo "BuildRequires: %%{myspell_$lang}";\
	done\
	)
}
%endif
# Build patches
Patch2:         mozilla-firefox-1.0-prdtoa.patch
#
# Fedora patches (Patch100+)
#
Patch100:	 thunderbird-objdir.patch
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

BuildRequires:	imagemagick
BuildRequires:	autoconf2.1
BuildRequires:	gzip
BuildRequires:	python
BuildRequires:	unzip
BuildRequires:	yasm >= 1.0.1
BuildRequires:	zip
BuildRequires:	jpeg-devel
BuildRequires:	libiw-devel
BuildRequires:	nss-static-devel >= 2:3.13.2
BuildRequires:	icu-devel
BuildRequires:	python-devel
BuildRequires:	python-virtualenv
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gl)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:	pkgconfig(gtk+-2.0)
%if %mdvver >= 201500
BuildRequires:  pkgconfig(gtk+-3.0)
%endif
BuildRequires:	pkgconfig(hunspell)
BuildRequires:	pkgconfig(libevent) >= 1.4.7
BuildRequires:	pkgconfig(libIDL-2.0)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(nspr)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(sqlite3) >= 3.7.1.1
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(vpx) >= 0.9.7
BuildRequires:	pkgconfig(zlib)
%if %mdkversion >= 201500
BuildRequires:	pkgconfig(libpng) >= 1.4.8
%endif

Requires:	%{sqlite3_libname} >= %{sqlite3_version}
Requires:	%{nss_libname} >= 2:%{nss_version}
Requires(post,postun):	desktop-file-utils
Requires(post):	mktemp
Requires(post,postun): rpm-helper
Requires: xdg-utils
%if %mdvver >= 201500
Requires:       gtk3-modules
%endif
Obsoletes: mozilla-thunderbird < %{version}-%{release}
Provides: mozilla-thunderbird = %{version}-%{release}

%description
%{title} is a full-featured email, RSS and newsgroup client that
makes emailing safer, faster and easier than ever before.

#===============================================================================
# enigmail-l10n
# Supported l10n language lists
%define em_l10n_langlist	ar ca cs de el es fi fr it ja ko nb nl pl pt pt_BR ru sl sv tr vi zh_CN zh_TW

# Disabled l10n languages, for any reason
# nl sk es_AR do not support 0.95.0 yet
%define em_disabled_l10n_langlist	hu
# define disabled_l10n_langlist %{nil}

# Language descriptions
%define em_language_ar ar
%define em_langname_ar Arabic
%define em_language_ca ca
%define em_langname_ca Catalan
%define em_language_cs cs
%define em_langname_cs Czech
%define em_language_de de
%define em_langname_de German
%define em_language_el el
%define em_langname_el Greek
%define em_language_es_AR es-AR
%define em_langname_es_AR Spanish (Argentina)
%define em_language_es es-ES
%define em_langname_es Spanish
%define em_language_fi fi
%define em_langname_fi Finnish
%define em_language_fr fr
%define em_langname_fr French
%define em_language_hu hu
%define em_langname_hu Hungarian
%define em_language_it it
%define em_langname_it Italian
%define em_language_ja ja
%define em_langname_ja Japanese
%define em_language_ko ko
%define em_langname_ko Korean
%define em_language_nb nb-NO
%define em_langname_nb Norwegian Bokmaal
%define em_langname_nl Dutch
%define em_language_nl nl
%define em_language_pl pl
%define em_langname_pl Polish
%define em_langname_pt Portuguese
%define em_language_pt pt-PT
%define em_language_pt_BR pt-BR
%define em_langname_pt_BR Brazilian portuguese
%define em_language_ru ru
%define em_langname_ru Russian
%define em_language_sk sk
%define em_langname_sk Slovak
%define em_language_sl sl
%define em_langname_sl Slovenian
%define em_language_sv sv-SE
%define em_langname_sv Swedish
%define em_language_tr tr
%define em_langname_tr Turkish
%define em_language_vi vi
%define em_langname_vi Vietnamese
%define em_language_zh_CN zh-CN
%define em_langname_zh_CN Simplified Chinese
%define em_language_zh_TW zh-TW
%define em_langname_zh_TW Traditional Chinese

# Expand all languages packages.
%{expand:%(\
        for lang in %langlist; do\

                echo "%%{expand:%%(sed "s!__LANG__!$lang!g" %{SOURCE401} 2> /dev/null)}";\
        done\
        )
}

# --- Danger line ---

# All langs
%{expand:%%define em_langlist %(for lang in %em_l10n_langlist; do echo "$lang"; done | sort -u | sed ':a;$!N;s/\n/ /;ta')}

# Locales
%{expand:%(for lang in %em_l10n_langlist; do echo "%%define em_locale_$lang `echo $lang | cut -d _ -f 1` "; done)}

# Expand all languages packages.
%{expand:%(\
	for lang in %em_langlist; do\
		echo "%%{expand:%%(sed "s!__LANG__!$lang!g" %{SOURCE400} 2> /dev/null)}";\
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
Suggests:	pinentry-gtk2
Obsoletes:	mozilla-thunderbird-enigmail < %{version}-%{release}
Provides:	mozilla-thunderbird-enigmail = %{version}-%{release}
%(for lang in %em_l10n_langlist %em_disabled_l10n_langlist; do
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

%setup -q -n %{name}-%{version}

%patch2 -p0

%patch100 -p2 -b .objdir
%patch201 -p2 -b .default_mail

%patch300 -p0 -b .progname
%patch301 -p1 -b .enigmailpackage
%patch304 -p0 -b .run-mozilla

%patch400 -p1 -b .appname
#===============================================================================
# Enigmail
%setup -q -T -D -n %{name}-%{version}/mozilla/extensions -a300
%if 0
%patch212 -p2 -b .enigmail-ui-content-contents-rdf
%patch213 -p2 -b .enigmail-build-package-contents-rdf
%endif

%setup -q -T -D -n %{name}-%{version}

#===============================================================================
# l10n
# Convert rpm macros to bash variables
%{expand:%(for lang in %langlist; do echo "language_$lang=%%{language_$lang}"; done)}
%{expand:%(for lang in %langlist; do echo "locale_$lang=%%{locale_$lang}"; done)}
%{expand:%(for lang in %langlist; do echo "with_$lang=%%{with_$lang}"; done)}
%{expand:%(for lang in %langlist; do echo "dict_$lang=%%{with_dict_$lang}"; done)}

# Unpack all languages
for lang in %langlist; do
	with="with_$lang"
	with=${!with}
	[ $with -eq 0 ] && continue

	language="language_$lang"
	language=${!language}

	locale="locale_$lang"
	locale=${!locale}

	# l10n
	mkdir ${language}
	cd ${language}
	unzip -qq %{_sourcedir}/${language}.xpi
	cd ..

	# dict
	dict="dict_$lang"
	dict=${!dict}
	[ $dict -eq 0 ] && continue

done

%build
%if %mdvver >= 201500

# fix build with freetype 2.6
sed -i '/^ftglyph.h/ i ftfntfmt.h' mozilla/config/system-headers

%ifarch %arm
# arm still requires gcc
export CXX=g++
export CC=gcc
%else
# (tpg) clang works, just export it to be sure it is used
export CXX=g++
export CC=gcc
%global optflags %optflags -Wno-error -Wno-null-conversion -Wno-inconsistent-missing-override
%endif 
%endif

export MOZCONFIG=`pwd`/.mozconfig
cat > $MOZCONFIG << EOF
mk_add_options MOZILLA_OFFICIAL=1
mk_add_options BUILD_OFFICIAL=1
#mk_add_options MOZ_MAKE_FLAGS="%{_smp_mflags}"
ac_add_options --prefix="%{_prefix}"
ac_add_options --libdir="%{_libdir}"
ac_add_options --enable-application=mail
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-jpeg
ac_add_options --with-system-zlib
ac_add_options --with-system-libevent
%if %mdvver > 3000000
ac_add_options --with-system-icu
%endif
%if %mdvver >= 201500
ac_add_options --with-system-libvpx
ac_add_options --with-system-png
ac_add_options --enable-system-sqlite
%else
ac_add_options --disable-system-png
%endif
ac_add_options --disable-system-cairo
ac_add_options --with-system-bz2
ac_add_options --enable-system-hunspell
ac_add_options --with-pthreads
ac_add_options --disable-tests
ac_add_options --disable-debug
ac_add_options --disable-updater
ac_add_options --disable-crashreporter
%if %mdvver >= 201500
ac_add_options --enable-default-toolkit=cairo-gtk3
%else
ac_add_options --enable-default-toolkit=cairo-gtk2
%endif
ac_add_options --disable-strip
ac_add_options --enable-startup-notification
ac_add_options --disable-gconf
ac_add_options --enable-gio
ac_add_options --enable-calendar
ac_add_options --enable-strip
ac_add_options --enable-official-branding
ac_add_options --enable-optimize
ac_add_options --enable-startup-notification
EOF

# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
#
MOZ_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS" | sed -e 's/-Wall//')
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fno-delete-null-pointer-checks"
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
make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS" MOZ_PKG_FATAL_WARNINGS=0

#===============================================================================

pushd mozilla/extensions/enigmail
%configure
make PYTHON=python2
popd


pushd mozilla/extensions/enigmail
(cd lang
 chmod 0755 ./make-lang.sh
 for i in `cat current-languages.txt`; do
   ./make-lang.sh $i %{enigmail_short_version}
 done
)

popd

#===============================================================================

%install
mkdir -p %{buildroot}{%{_libdir},%{_bindir},%{_datadir}/applications}
mkdir -p %buildroot%tbdir

rm -f extensions/spellcheck/locales/en-US/hunspell/en-US.{dic,aff}

%makeinstall_std -f client.mk STRIP=/bin/true MOZ_PKG_FATAL_WARNINGS=0

rm -rf %buildroot%tbdir/dictionaries
ln -s /usr/share/dict/mozilla %buildroot%tbdir/dictionaries

install -p -D %{buildroot}/%{tbdir}/chrome/icons/default/default256.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

%{__install} -p -D %{SOURCE303} %{buildroot}/%{_datadir}/applications/mandriva-%{name}.desktop

# set up the thunderbird start script
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

#===============================================================================

mkdir -p %{buildroot}%{tbextdir}/%{enigmail_id}
%if !%{xpi}
%{_bindir}/unzip -q mozilla/extensions/enigmail/build/enigmail-*.xpi -d %{buildroot}%{tbextdir}/%{enigmail_id}
%{__chmod} 644 %{buildroot}%{tbextdir}/%{enigmail_id}/chrome.manifest
%else
cp -aL mozilla/extensions/enigmail/build/enigmail-%{enigmail_short_version}*.xpi %{buildroot}%{tbextdir}/%{enigmail_id}/%{enigmail_id}.xpi
%endif

#==============================================================================
#enigmail lang package
# Convert rpm macros to bash variables
%{expand:%(for lang in %em_langlist; do echo "language_$lang=%%{em_language_$lang}"; done)}
pushd mozilla/extensions/enigmail/lang
 for lang in %em_langlist; do
    mkdir -p %{buildroot}%{_datadir}/mozilla/extensions/%{tb_appid}/enigmail-$lang@enigmail.mozdev.org
    language="language_$lang"
    language=${!language}
    %{_bindir}/unzip -q enigmail-${language}-%{enigmail_short_version}.xpi -d %{buildroot}%{_datadir}/mozilla/extensions/%{tb_appid}/enigmail-$lang@enigmail.mozdev.org/
 done
popd

#===============================================================================
# lightning ext here
pushd %{objdir}/dist/xpi-stage/
  for ext in {gdata-provider,lightning}; do
    hash="$(sed -n '/^    <em:id>\(.*\)<\/em:id>.*/{s//\1/p;q}' $ext/install.rdf)"
    mkdir -p %buildroot%{tbextdir}/$hash
    %{_bindir}/unzip -q $ext-*.xpi -d %buildroot%{tbextdir}/$hash/
  done
popd

#===============================================================================

cp -aL %{objdir}/dist/bin/nsinstall %{buildroot}%{_bindir}

#==============================================================================
#exclude devel files
rm -rf %{buildroot}%{_datadir}/idl/%{oname}-%{version}
rm -rf %{buildroot}%{_includedir}/%{oname}-%{version}
rm -rf %{buildroot}%{_libdir}/%{oname}-devel-%{version}

#===============================================================================

# Convert rpm macros to bash variables
%{expand:%(for lang in %langlist; do echo "language_$lang=%%{language_$lang}"; done)}
%{expand:%(for lang in %langlist; do echo "with_$lang=%%{with_$lang}"; done)}
%{expand:%(for lang in %langlist; do echo "dict_$lang=%%{with_dict_$lang}"; done)}

# Create dicts dir
%if %use_dict
mkdir -p %{buildroot}%{mozillalibdir}/dictionaries
%endif

# Install all languages
for lang in %langlist; do
	with="with_$lang"
	with=${!with}
	[ $with -eq 0 ] && continue

	language="language_$lang"
	language=${!language}

	# l10n
	cd $language
	mkdir -p %{buildroot}%{tblangdir}/langpack-${language}@thunderbird.mozilla.org/
	cp -f -r * %{buildroot}%{tblangdir}/langpack-${language}@thunderbird.mozilla.org/
	cd ..

done

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
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
# enigmail
%exclude %{tbextdir}/%{enigmail_id}

%files enigmail
%{tbextdir}/%{enigmail_id}

%files -n nsinstall
%{_bindir}/nsinstall

%files lightning
%{tbextdir}/{a62ef8ec-5fdc-40c2-873c-223b8a6925cc}
%{tbextdir}/{e2fda1a4-762b-4020-b5ad-a41df1933103}
