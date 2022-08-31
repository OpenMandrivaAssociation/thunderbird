%define _disable_lto 1

%define __libtoolize /bin/true
%define __cputoolize /bin/true

%define title Mozilla Thunderbird

%define oname thunderbird
%define thunderbird_package thunderbird
%define tb_appid \{3550f703-e582-4d05-9a08-453d09bdfdc6\}
%define tbdir %{_libdir}/%{oname}
%define tbextdir %{_libdir}/mozilla/extensions/%{tb_appid}
%define tbdistextdir %{tbdir}/distribution/extensions
%define tblangdir %{_datadir}/mozilla/extensions/%{tb_appid}


%define objdir obj

%define xpi 0

%define _provides_exceptions libgtkembedmoz.so\\|libxpcom.so
%define _requires_exceptions libgtkembedmoz.so\\|libxpcom.so

# FIXME: Bug in nsExtensionManager.js prevents using x86_64 as arch
# FIXME: I tried to modify nsExtensionManager.js.in, but it
# FIXME: complained that I had modified it
%ifarch %{ix86}
%define tbarch x86
%else # ix86
%ifarch %{x86_64}
%define tbarch x86_64
%else # x86_64
%define tbarch %{_arch}
%endif # x86_64
%endif # ix86

# use bundled cbindgen
# currently enabled as updating all rust deps would take eons
%global use_bundled_cbindgen  1

%define build_py python3

# this seems fragile, so require the exact version or later (#58754)
%define sqlite3_libname %{mklibname sqlite3_ 0}
%define sqlite3_version %(pkg-config --modversion sqlite3 &>/dev/null && pkg-config --modversion sqlite3 2>/dev/null || echo 0)
# this one as well (#59759)
%define nss_libname %mklibname nss 3
%define nss_version %(pkg-config --modversion nss &>/dev/null && pkg-config --modversion nss 2>/dev/null || echo 0)

%define _enable_debug_packages %{nil}
%define debug_package %{nil}

%define xpidir http://ftp.mozilla.org/pub/mozilla.org/thunderbird/releases/%{version}/linux-x86_64/xpi/

# Supported l10n language lists
%define langlist  ar ast be bg br ca cs da de el en_GB en_US es_AR es_ES et eu fi fr fy ga gd gl he hr hu hy id is it ja ko lt nb_NO nl nn_NO pl pt_BR pt_PT ro ru sk sl sq sr sv_SE tr uk vi zh_CN zh_TW

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
Version:	102.2.0
Release:	1
License:	MPL
Group:		Networking/Mail
Url:		http://www.mozillamessaging.com/
Source0:        http://ftp.mozilla.org/pub/mozilla.org/thunderbird/releases/%{version}/source/thunderbird-%{version}.source.tar.xz
%if 0%{?use_bundled_cbindgen}
Source2:        cbindgen-vendor.tar.xz
%endif
Source12:       mozilla-thunderbird-omv-default-prefs.js
Source30:       mozilla-thunderbird-open-browser.sh
Source31:       mozilla-thunderbird-open-browser-xdg.sh
Source100:	thunderbird.rpmlintrc
Source303:	thunderbird.desktop
# Language package template
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
#
Patch10:	firefox-98.0-python-3.11.patch
Patch11:	build-python-3.11.patch
# Fedora patches (Patch100+)
#
# (currently none required)

#
# Debian patches (Patch200+)
#
Patch201:       mozilla-thunderbird-default-mailer.patch
# Mandriva patches (Patch300+)
Patch304:       mozilla-thunderbird-run-mozilla.patch
# OpenSuse patches (Patch400+)

BuildRequires:	gzip
BuildRequires:	unzip
BuildRequires:	yasm >= 1.0.1
BuildRequires:	nasm
BuildRequires:	zip
BuildRequires:	jpeg-devel
BuildRequires:	nss-static-devel
BuildRequires:	glibc-static-devel
BuildRequires:	icu-devel
BuildRequires:  pkgconfig(python3)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gl)
BuildRequires:  pkgconfig(gtk+-3.0)
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
BuildRequires:	pkgconfig(libpng) >= 1.4.8
BuildRequires:  rust >= 1.59.0
BuildRequires:  cargo >= 1.59.0
%if !0%{?use_bundled_cbindgen}
BuildRequires:  cbindgen >= 0.23.0
%endif
BuildRequires:  nodejs >= 10.19
BuildRequires:	clang-devel
BuildRequires:	llvm-devel

Requires:	%{sqlite3_libname} >= %{sqlite3_version}
Requires:	%{nss_libname} >= %{nss_version}
Requires(post,postun):	desktop-file-utils
Requires(post):	mktemp
Requires(post,postun): rpm-helper
Requires: xdg-utils
Requires:       gtk3-modules
Obsoletes: mozilla-thunderbird < %{version}-%{release}
Obsoletes: thunderbird-lightning < %{version}-%{release}
Obsoletes: thunderbird-enigmail < %{version}-%{release}

Provides: mozilla-thunderbird = %{version}-%{release}

%description
%{title} is a full-featured email, RSS and newsgroup client that
makes emailing safer, faster and easier than ever before.

#===============================================================================
# l10n

# Expand all languages packages.
%{expand:%(\
        for lang in %langlist; do\

                echo "%%{expand:%%(sed "s!__LANG__!$lang!g" %{SOURCE401} 2> /dev/null)}";\
        done\
        )
}

#===============================================================================

%prep

%autosetup -p1

#===============================================================================
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

%ifarch %ix86
%global optflags %{optflags} -g0 -fno-exceptions -Wno-format-security
%global ldflags %{ldflags} -Wl,--no-keep-memory -Wl,--reduce-memory-overheads
# still requires gcc
export CXX=g++
export CC=gcc
# avoid oom with rust
export RUSTFLAGS="-Cdebuginfo=0"
%else
%global optflags %{optflags} -Qunused-arguments
%endif

%setup_compile_flags

export PATH=$(pwd)/.cargo/bin:$PATH

%if 0%{?use_bundled_cbindgen}
mkdir -p my_rust_vendor
cd my_rust_vendor
%{__tar} xf %{SOURCE2}
mkdir -p .cargo
cat > .cargo/config <<EOL
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "`pwd`"
EOL

env CARGO_HOME=.cargo cargo install cbindgen
export PATH=`pwd`/.cargo/bin:$PATH
cd -
%endif


export MOZCONFIG=`pwd`/.mozconfig
cat > $MOZCONFIG << EOF
mk_add_options MOZILLA_OFFICIAL=1
mk_add_options BUILD_OFFICIAL=1
#mk_add_options MOZ_MAKE_FLAGS="%{_smp_mflags}"
mk_add_options MOZ_OBJDIR=`pwd`/%{objdir}
ac_add_options --enable-application=comm/mail
ac_add_options --prefix="%{_prefix}"
ac_add_options --libdir="%{_libdir}"
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-jpeg
ac_add_options --with-system-zlib
%if %mdvver > 3000000
ac_add_options --with-system-libevent
#ac_add_options --with-system-icu
%endif
%if %mdvver <= 3000000
ac_add_options --with-system-libvpx
%endif
ac_add_options --with-system-png
ac_add_options --disable-tests
ac_add_options --disable-debug
ac_add_options --disable-updater
ac_add_options --disable-crashreporter
ac_add_options --enable-default-toolkit=cairo-gtk3
ac_add_options --disable-strip
%ifnarch aarch64
ac_add_options --disable-elf-hack
%endif
ac_add_options --enable-strip
ac_add_options --enable-update-channel=release
ac_add_options --enable-official-branding
%ifarch %{ix86}
ac_add_options --enable-linker=bfd
ac_add_options --disable-optimize
%else
ac_add_options --enable-optimize="-O2"
%endif
%ifarch x86_64 aarch64
# ERROR: --enable-rust-simd does not work with Rust 1.33 or later. 
# See https://bugzilla.mozilla.org/show_bug.cgi?id=1521249 .
# ac_add_options --enable-rust-simd

%endif
ac_add_options --without-wasm-sandboxed-libraries
EOF

export MACH_USE_SYSTEM_PYTHON=1
export MACH_NO_WRITE_TIMES=1

%build_py ./mach build

#===============================================================================

%install

export MACH_USE_SYSTEM_PYTHON=1

mkdir -p %{buildroot}{%{_libdir},%{_bindir},%{_datadir}/applications}
mkdir -p %buildroot%tbdir

#rm -f extensions/spellcheck/locales/en-US/hunspell/en-US.{dic,aff}

DESTDIR=%buildroot STRIP=/bin/true MOZ_PKG_FATAL_WARNINGS=0 %build_py ./mach install

rm -rf %buildroot%tbdir/dictionaries
ln -s /usr/share/dict/mozilla %buildroot%tbdir/dictionaries

%{__install} -p -D %{SOURCE303} %{buildroot}/%{_datadir}/applications/mandriva-%{name}.desktop

# set up the thunderbird start script
# For backwards compatibility with old profiles. Bug #37528
install -m 755 %{SOURCE31} %{buildroot}%{tbdir}/open-browser.sh
# For new profiles
%define COMMAND /usr/bin/xdg-open

sed -e 's,THUNDERBIRD_RPM_VR,%{version}-%{release},g;' \
    -e 's,THUNDERBIRD_VENDOR_COMMENT,%{mandriva_release},g;' \
  %{SOURCE12} > %{buildroot}%{tbdir}/defaults/pref/all-omv.js

#===============================================================================

# icons
mkdir -p %{buildroot}{%{_liconsdir},%{_iconsdir},%{_miconsdir}}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{16x16,22x22,24x24,32x32,48x48,64x64,128x128,256x256}/apps
install -m 644 %{buildroot}/%{tbdir}/chrome/icons/default/default48.png %{buildroot}%{_liconsdir}/%{name}.png
install -m 644 %{buildroot}/%{tbdir}/chrome/icons/default/default32.png %{buildroot}%{_iconsdir}/%{name}.png
install -m 644 %{buildroot}/%{tbdir}/chrome/icons/default/default16.png %{buildroot}%{_miconsdir}/%{name}.png
install -m 644 %{buildroot}/%{tbdir}/chrome/icons/default/default16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
install -m 644 %{buildroot}/%{tbdir}/chrome/icons/default/default22.png %{buildroot}%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
install -m 644 %{buildroot}/%{tbdir}/chrome/icons/default/default24.png %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
install -m 644 %{buildroot}/%{tbdir}/chrome/icons/default/default32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -m 644 %{buildroot}/%{tbdir}/chrome/icons/default/default48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
install -m 644 %{buildroot}/%{tbdir}/chrome/icons/default/default64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
install -m 644 %{buildroot}/%{tbdir}/chrome/icons/default/default128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
install -m 644 %{buildroot}/%{tbdir}/chrome/icons/default/default256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

#===============================================================================

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

%files
%{_bindir}/thunderbird
%{_datadir}/applications/*.desktop
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
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png


