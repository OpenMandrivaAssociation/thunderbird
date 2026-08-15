%define _disable_lto 1


%define __libtoolize /bin/true
%define __cputoolize /bin/true

%define title Mozilla Thunderbird

%define oname thunderbird
%define thunderbird_package thunderbird
%define tb_appid \{3550f703-e582-4d05-9a08-453d09bdfdc6\}
%define tbextdir %{_libdir}/mozilla/extensions/%{tb_appid}
%define tblangdir %{_datadir}/mozilla/extensions/%{tb_appid}

%define xpi 0

%define _provides_exceptions libgtkembedmoz.so\\|libxpcom.so
%define _requires_exceptions libgtkembedmoz.so\\|libxpcom.so

# FIXME: Bug in nsExtensionManager.js prevents using x86_64 as arch
# FIXME: I tried to modify nsExtensionManager.js.in, but it
# FIXME: complained that I had modified it
%ifarch %{x86_64}
%define tbarch x86_64
%else # x86_64
%define tbarch %{_arch}
%endif # x86_64

# use bundled cbindgen
# currently enabled as updating all rust deps would take eons
%global use_bundled_cbindgen  1

# Dual toolkit by default. For faster local Qt-only iteration (abb needs one argv):
#   abb build '--define=_without_gtk 1'
#   rpmbuild -bb --without gtk …
# Same with '--define=_without_qt 1' for GTK-only.
%bcond_without gtk
%bcond_without qt

%if !%{with gtk} && !%{with qt}
%{error:Need at least one of --with gtk or --with qt}
%endif

# Toolkit builds install to separate trees (toolkit is compiled into libxul).
%define tbdir_qt  %{_libdir}/%{name}-qt-%{version}
%define tbdir_gtk %{_libdir}/%{name}-gtk-%{version}
# Default path for extension packaging (prefer Qt when both built).
%if %{with qt}
%define tbdir %{tbdir_qt}
%else
%define tbdir %{tbdir_gtk}
%endif
%define tbdistextdir %{tbdir}/distribution/extensions

%define build_py python3

# this one as well (#59759)
%define nss_libname %mklibname nss 3
%define nss_version %(pkg-config --modversion nss &>/dev/null && pkg-config --modversion nss 2>/dev/null || echo 0)

%define _enable_debug_packages %{nil}
%define debug_package %{nil}

%define xpidir http://ftp.mozilla.org/pub/thunderbird/releases/%{version}/linux-x86_64/xpi/

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
%{expand:%(for lang in %langlist; do echo "%%define locale_$lang $(echo $lang | cut -d _ -f 1) "; done)}

%if %use_dict
# myspell dicts, allows setting preferences between several providers.
%{expand:%(for lang in %langlist; do echo "%%define myspell_$lang myspell-$lang"; done)}
%define myspell_de myspell-de_DE
%define myspell_fr myspell-fr_FR
%endif

Summary:	Full-featured email, RSS, and newsgroup client
Name:		thunderbird
Version:	153.0.3
Release:	1
License:	MPL
Group:		Networking/Mail
Url:		https://www.thunderbird.net/
Source0:        https://ftp.mozilla.org/pub/thunderbird/releases/%{version}/source/thunderbird-%{version}.source.tar.xz
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
		echo "%%{expand:Source$i: %{xpidir}%%{language_$lang}.xpi}";\
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

# Fedora patches (Patch100+)
#
# (currently none required)
#
# Debian patches (Patch200+)
#
Patch201:       mozilla-thunderbird-default-mailer.patch
# Mandriva patches (Patch300+)
#Patch304:       mozilla-thunderbird-run-mozilla.patch
# OpenSuse patches (Patch400+)

# Archlinux patches (Patch500+)

# In-tree HarfBuzz: Clang 23 promotes -Wunused-template via -Wunused error pragma
Patch70:	firefox-harfbuzz-clang-unused-template.patch

# =============================================================================
# Qt toolkit patches (shared Gecko — port these to Firefox cairo-qt as well)
# Numbering: Patch600–614, 616–623 map to 0001–0015, 0017–0024.
# =============================================================================
Patch600:	0001-Bug-2054387-Build-system-add-cairo-qt-toolkit-option.patch
Patch601:	0002-Bug-2054387-widget-qt-add-exclusive-Qt-6-widget-back.patch
Patch602:	0003-Bug-2054387-IPC-wire-Chromium-message-pump-for-Qt.-r.patch
Patch603:	0004-Bug-2054387-gfx-Qt-platform-GL-EGL-and-WebRender-int.patch
Patch604:	0005-Bug-2054387-widget-gtk-share-DMABuf-helpers-with-Qt-.patch
Patch605:	0006-Bug-2054387-a11y-add-Qt-accessibility-backend.-r-acc.patch
# browser/ shell service (xpfe appshell Qt bits; browser/ not linked into TB)
Patch606:	0007-Bug-2054387-browser-Qt-shell-service-and-preferences.patch
Patch607:	0008-Bug-2054387-media-enable-VAAPI-DMABuf-and-WebRTC-pat.patch
Patch608:	0009-Bug-2054387-toolkit-FreeDesktop-services-and-portals.patch
Patch609:	0010-Bug-2054387-sandbox-and-misc-Qt-support-cleanups.-r-.patch
Patch610:	0011-Bug-2054387-Qt-font-options-from-fontconfig.patch
Patch611:	0012-Bug-2054387-Qt-stabilize-DPR-size-round-trip.patch
Patch612:	0013-Bug-2054387-Qt-force-overlay-scrollbars.patch
Patch613:	0014-Bug-2054387-Qt-handle-devicePixelRatio-scale-changes.patch
Patch614:	0015-Bug-2054387-sandbox-writable-user-fontconfig-cache.patch
# Keep chrome active with no-focus popups on Wayland; raise dialogs on show
Patch616:	0017-Bug-2054387-Qt-keep-chrome-active-with-nofocus-popups.patch
# Reclaim compositor stacking after no-focus popup lifecycle
Patch617:	0018-Bug-2054387-Qt-reclaim-activation-after-nofocus-popups.patch
# Reclaim after dialog/idle races
Patch618:	0019-Bug-2054387-Qt-reclaim-after-dialog-idle-activation.patch
# Stop multi-retry activate on every click (froze input / close button)
Patch619:	0020-Bug-2054387-Qt-stop-activation-reclaim-input-thrash.patch
# Never raise/requestActivate from focus handlers (Wayland input freeze loop)
Patch620:	0021-Bug-2054387-Qt-never-reclaim-activation-from-focus-handlers.patch
# Clear WindowTransparentForInput when re-enabling after modal
Patch621:	0022-Bug-2054387-Qt-clear-WindowTransparentForInput-on-Enable.patch
# Safe stacking reclaim on click/modal/popup lifecycle (not focus handlers)
Patch622:	0023-Bug-2054387-Qt-safe-stacking-reclaim-without-focus-loops.patch
# Modal/compose windows, theme/tooltips, geometry deadband, mouse buttons
Patch623:	0024-Bug-2054387-Qt-modal-compose-theme-and-geometry-stabilization.patch

# =============================================================================
# Thunderbird-only Qt patches (comm/mail — do not apply to Firefox)
# =============================================================================
# Mail shell service, themes, mailnews wiring for Qt
Patch615:	0016-Bug-2054387-Thunderbird-Qt-shell-service-and-themes.patch
# Thread-pane table/card virtual-list row height clamp (HiDPI hover jitter)
Patch624:	0025-Bug-2054387-Thunderbird-thread-pane-stable-row-heights.patch

BuildRequires:	gzip
BuildRequires:	unzip
BuildRequires:	yasm >= 1.0.1
BuildRequires:	nasm
BuildRequires:	zip
BuildRequires:	make
BuildRequires:	jpeg-devel
BuildRequires:	nss-static-devel
BuildRequires:	glibc-static-devel
BuildRequires:	icu-devel
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(hunspell)
BuildRequires:	pkgconfig(libevent) >= 1.4.7
BuildRequires:	pkgconfig(libIDL-2.0)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(nspr)
BuildRequires:	pkgconfig(nss) >= 3.125
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(vpx) >= 0.9.7
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libpng) >= 1.4.8
BuildRequires:	pkgconfig(libproxy-1.0)
BuildRequires:	rust >= 1.59.0
BuildRequires:	cargo >= 1.59.0
%if !0%{?use_bundled_cbindgen}
BuildRequires:	cbindgen >= 0.29.4
%endif
BuildRequires:	nodejs >= 10.19
BuildRequires:	clang-devel
BuildRequires:	llvm-devel
%if %{with gtk}
BuildRequires:	pkgconfig(gtk+-3.0)
%endif
%if %{with qt}
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6DBus)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(Qt6OpenGL)
BuildRequires:	pkgconfig(Qt6PrintSupport)
# System cairo for gfxFcPlatformFontList desktop font options.
BuildRequires:	pkgconfig(cairo)
%endif

Requires:	%{nss_libname} >= %{nss_version}
Requires(post,postun):	desktop-file-utils
Requires(post):	mktemp
Requires(post,postun): rpm-helper
Requires:	xdg-utils
Obsoletes:	mozilla-thunderbird < %{version}-%{release}
Obsoletes:	thunderbird-lightning < %{version}-%{release}
Obsoletes:	thunderbird-enigmail < %{version}-%{release}

Provides:	mozilla-thunderbird = %{version}-%{release}

# Need at least one toolkit binary for the neutral /usr/bin/thunderbird wrapper.
%if %{with qt} && %{with gtk}
Requires:	(%{name}-qt = %{EVRD} or %{name}-gtk = %{EVRD})
Recommends:	(%{name}-qt = %{EVRD} if %{_lib}Qt6Widgets)
Recommends:	(%{name}-gtk = %{EVRD} if %{_lib}gtk3_0)
%elif %{with qt}
Requires:	%{name}-qt = %{EVRD}
%elif %{with gtk}
Requires:	%{name}-gtk = %{EVRD}
%endif

%description
%{title} is a full-featured email, RSS and newsgroup client that
makes emailing safer, faster and easier than ever before.

This package provides the shared launcher, desktop entry and icons. The actual
application builds are in the thunderbird-qt and/or thunderbird-gtk
subpackages. The /usr/bin/thunderbird wrapper picks GTK on GNOME/MATE/Cinnamon/XFCE
and Qt on other desktops, falling back to whichever toolkit is installed.

%if %{with qt}
%package qt
Summary:	Thunderbird built with the Qt 6 toolkit
Group:		Networking/Mail
Requires:	%{name} = %{EVRD}

%description qt
Thunderbird email client built against the Qt 6 toolkit (cairo-qt). On Plasma
and other non-GTK desktops, /usr/bin/thunderbird selects this build by default.
%endif

%if %{with gtk}
%package gtk
Summary:	Thunderbird built with the GTK 3 toolkit
Group:		Networking/Mail
Requires:	%{name} = %{EVRD}
Requires:	gtk3-modules

%description gtk
Thunderbird email client built against the GTK 3 toolkit (cairo-gtk3-wayland).
On GNOME, MATE, Cinnamon and XFCE, /usr/bin/thunderbird selects this build by
default.
%endif

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
%global optflags %{optflags} -g0

%global optflags %{optflags} -Wno-error=c++11-narrowing-const-reference
%global optflags %{optflags} -Qunused-arguments -g0 -fno-lto
# botan cant detect clang with cc/c++
# Full paths: otherwise mach may prefer a broken toolchain under ~/.mozbuild
export CXX=/usr/bin/clang++
export CC=/usr/bin/clang
export AR=/usr/bin/llvm-ar
export NM=/usr/bin/llvm-nm
export RANLIB=/usr/bin/llvm-ranlib
export HOST_CC=/usr/bin/clang
export HOST_CXX=/usr/bin/clang++

%set_build_flags

if [ $(getconf _NPROCESSORS_ONLN) -le 16 ]; then
	export SMP_FLAGS="%{_smp_mflags}"
else
	export SMP_FLAGS="-j16"
fi

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
directory = "$(pwd)"
EOL

env CARGO_HOME=.cargo cargo install cbindgen
export PATH=$(pwd)/.cargo/bin:$PATH
cd -
%endif

# https://bugzilla.mozilla.org/show_bug.cgi?id=2041134
sed -i 's/log\.warn(/log.warning(/' \
	comm/build/moz.configure/gecko_source.configure

export MOZCONFIG=$(pwd)/.mozconfig
cat > $MOZCONFIG << EOF
mk_add_options MOZILLA_OFFICIAL=1
mk_add_options BUILD_OFFICIAL=1
mk_add_options MOZ_MAKE_FLAGS="$SMP_FLAGS"
ac_add_options --enable-application=comm/mail
ac_add_options --prefix="%{_prefix}"
ac_add_options --libdir="%{_libdir}"
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-jpeg
ac_add_options --with-system-zlib
ac_add_options --with-system-libevent
ac_add_options --with-system-png
ac_add_options --disable-tests
ac_add_options --disable-debug
ac_add_options --disable-updater
ac_add_options --disable-crashreporter
ac_add_options --disable-strip
ac_add_options --disable-elf-hack
ac_add_options --enable-strip
ac_add_options --enable-update-channel=release
ac_add_options --enable-official-branding
ac_add_options --enable-optimize="-O2"
ac_add_options --without-wasm-sandboxed-libraries
ac_add_options --enable-linker=lld
ac_add_options --disable-lto
# Distro builds use system toolchains and libraries, not mach bootstrap
# sysroots (which reject --with-system-nspr/nss among others).
ac_add_options --disable-bootstrap
# Use libproxy instead of GSettings-based unixproxy (GSettings lives under
# widget/gtk and is not built for cairo-qt).
ac_add_options --enable-libproxy
# We don't care about binary compatibility with prehistoric libstdc++.
unset MOZ_STDCXX_COMPAT
EOF

%if %{with qt}
cp -a $MOZCONFIG $MOZCONFIG-qt
echo 'mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-qt' >>$MOZCONFIG-qt
echo 'ac_add_options --enable-default-toolkit=cairo-qt' >>$MOZCONFIG-qt
%endif
%if %{with gtk}
cp -a $MOZCONFIG $MOZCONFIG-gtk
echo 'mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-gtk' >>$MOZCONFIG-gtk
echo 'ac_add_options --enable-default-toolkit=cairo-gtk3-wayland' >>$MOZCONFIG-gtk
%endif

MC=$(pwd)/.mozconfig
MOZCONFIGS=""
%if %{with gtk}
MOZCONFIGS="$MOZCONFIGS $MC-gtk"
%endif
%if %{with qt}
MOZCONFIGS="$MOZCONFIGS $MC-qt"
%endif

export LDFLAGS="${LDFLAGS:+$LDFLAGS }-Wl,--no-keep-memory"
export RUSTFLAGS="-Cdebuginfo=0"
export MOZ_NOSPAM=1
export MACH_USE_SYSTEM_PYTHON=1
export MACH_NO_WRITE_TIMES=1
# (tpg) re-use already existing user profile
export MOZ_ALLOW_DOWNGRADE=1
export MOZ_LEGACY_PROFILES=1

for MOZCONFIG in $MOZCONFIGS; do
	export MOZCONFIG
	cat $MOZCONFIG
	%build_py ./mach build
done

#===============================================================================

%install

export MACH_USE_SYSTEM_PYTHON=1

# Install one toolkit build into its libdir and apply shared distro customizations.
# Prefer packaging from the objdir (like Firefox) so dual-toolkit installs do not
# clobber each other under a shared DESTDIR path.
install_toolkit() {
	local toolkit="$1"
	local libdir="$2"
	local obj="obj-${toolkit}"

	export MOZCONFIG=$(pwd)/.mozconfig-${toolkit}

	mkdir -p %{buildroot}${libdir}

	# Stage package into ${obj}/dist via the mail installer (no DESTDIR).
	if [ -d ${obj}/comm/mail/installer ]; then
		make -C ${obj}/comm/mail/installer STRIP=/bin/true MOZ_PKG_FATAL_WARNINGS=0
	elif [ -d ${obj}/mail/installer ]; then
		make -C ${obj}/mail/installer STRIP=/bin/true MOZ_PKG_FATAL_WARNINGS=0
	else
		echo "install_toolkit: no mail installer in ${obj}" >&2
		return 1
	fi

	if [ -d ${obj}/dist/thunderbird ]; then
		cp -a ${obj}/dist/thunderbird/. %{buildroot}${libdir}/
	elif [ -d ${obj}/dist/bin ]; then
		cp -a ${obj}/dist/bin/. %{buildroot}${libdir}/
	else
		echo "install_toolkit: staged tree missing under ${obj}/dist" >&2
		ls -la ${obj}/dist 2>/dev/null || true
		return 1
	fi

	rm -rf %{buildroot}${libdir}/dictionaries
	ln -s %{_datadir}/dict/mozilla %{buildroot}${libdir}/dictionaries

	# For backwards compatibility with old profiles. Bug #37528
	install -m 755 %{SOURCE31} %{buildroot}${libdir}/open-browser.sh

	mkdir -p %{buildroot}${libdir}/defaults/pref
	sed -e 's,THUNDERBIRD_RPM_VR,%{version}-%{release},g;' \
		-e 's,THUNDERBIRD_VENDOR_COMMENT,%{distro_release},g;' \
		%{SOURCE12} > %{buildroot}${libdir}/defaults/pref/all-omv.js

	# Drop SDK/devel bits if present
	rm -rf %{buildroot}%{_datadir}/idl/%{oname}-%{version}
	rm -rf %{buildroot}%{_includedir}/%{oname}-%{version}
	rm -rf %{buildroot}%{_libdir}/%{oname}-devel-%{version}
	# Ensure neutral bindir is ours (wrappers installed below)
	rm -f %{buildroot}%{_bindir}/thunderbird
}

mkdir -p %{buildroot}{%{_libdir},%{_bindir},%{_datadir}/applications}

%if %{with qt}
install_toolkit qt %{tbdir_qt}
%endif
%if %{with gtk}
install_toolkit gtk %{tbdir_gtk}
%endif

# Toolkit-specific launchers
%if %{with qt}
cat > %{buildroot}%{_bindir}/thunderbird-qt << EOF
#!/bin/sh
export MOZ_LEGACY_PROFILES=1
exec %{tbdir_qt}/thunderbird "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/thunderbird-qt
%endif

%if %{with gtk}
cat > %{buildroot}%{_bindir}/thunderbird-gtk << EOF
#!/bin/sh
export MOZ_LEGACY_PROFILES=1
if [ "\${XDG_SESSION_TYPE:-}" = wayland ]; then
	export MOZ_ENABLE_WAYLAND=1
	unset MOZ_DISABLE_WAYLAND
else
	export MOZ_DISABLE_WAYLAND=1
	unset MOZ_ENABLE_WAYLAND
fi
exec %{tbdir_gtk}/thunderbird "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/thunderbird-gtk
%endif

# Neutral dispatcher: GTK on GNOME/MATE/Cinnamon/XFCE, Qt elsewhere;
# fall back to whichever toolkit is installed.
cat > %{buildroot}%{_bindir}/thunderbird << EOF
#!/bin/sh
export MOZ_LEGACY_PROFILES=1

GTK_BIN="%{tbdir_gtk}/thunderbird"
QT_BIN="%{tbdir_qt}/thunderbird"

prefer=qt
# XDG_CURRENT_DESKTOP is often colon-separated, e.g. ubuntu:GNOME
desktop=\$(printf '%s' "\${XDG_CURRENT_DESKTOP:-}" | tr '[:upper:]' '[:lower:]')
oifs=\$IFS
IFS=:
for d in \$desktop; do
	case "\$d" in
	gnome|gnome-classic|gnome-flashback|unity|mate|cinnamon|x-cinnamon|xfce)
		prefer=gtk
		break
		;;
	esac
done
IFS=\$oifs

if [ -z "\${XDG_CURRENT_DESKTOP:-}" ]; then
	case "\$(printf '%s' "\${DESKTOP_SESSION:-}" | tr '[:upper:]' '[:lower:]')" in
	gnome*|mate*|cinnamon*|xfce*)
		prefer=gtk
		;;
	esac
fi

run_gtk() {
	if [ "\${XDG_SESSION_TYPE:-}" = wayland ]; then
		export MOZ_ENABLE_WAYLAND=1
		unset MOZ_DISABLE_WAYLAND
	else
		export MOZ_DISABLE_WAYLAND=1
		unset MOZ_ENABLE_WAYLAND
	fi
	exec "\$GTK_BIN" "\$@"
}

run_qt() {
	unset MOZ_ENABLE_WAYLAND
	unset MOZ_DISABLE_WAYLAND
	exec "\$QT_BIN" "\$@"
}

if [ "\$prefer" = gtk ]; then
	if [ -x "\$GTK_BIN" ]; then
		run_gtk "\$@"
	elif [ -x "\$QT_BIN" ]; then
		run_qt "\$@"
	fi
else
	if [ -x "\$QT_BIN" ]; then
		run_qt "\$@"
	elif [ -x "\$GTK_BIN" ]; then
		run_gtk "\$@"
	fi
fi

echo "thunderbird: no toolkit binary found (install thunderbird-qt and/or thunderbird-gtk)" >&2
exit 1
EOF
chmod +x %{buildroot}%{_bindir}/thunderbird

%{__install} -p -D %{SOURCE303} %{buildroot}%{_datadir}/applications/%{name}.desktop

# Icons live in the main package so either toolkit can be removed independently.
# Official branding icons live in the source tree (package-manifest may not
# stage chrome/icons/default for all layouts).
BRAND_ICONS=comm/mail/branding/thunderbird
mkdir -p %{buildroot}{%{_liconsdir},%{_iconsdir},%{_miconsdir}}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{16x16,22x22,24x24,32x32,48x48,64x64,128x128,256x256}/apps
install -m 644 ${BRAND_ICONS}/default48.png %{buildroot}%{_liconsdir}/%{name}.png
install -m 644 ${BRAND_ICONS}/default32.png %{buildroot}%{_iconsdir}/%{name}.png
install -m 644 ${BRAND_ICONS}/default16.png %{buildroot}%{_miconsdir}/%{name}.png
for i in 16 22 24 32 48 64 128 256; do
	if [ -f ${BRAND_ICONS}/default$i.png ]; then
		install -m 644 ${BRAND_ICONS}/default$i.png \
			%{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
	fi
done

# Convert rpm macros to bash variables
%{expand:%(for lang in %langlist; do echo "language_$lang=%%{language_$lang}"; done)}
%{expand:%(for lang in %langlist; do echo "with_$lang=%%{with_$lang}"; done)}
%{expand:%(for lang in %langlist; do echo "dict_$lang=%%{with_dict_$lang}"; done)}

# Install all languages (shared, not toolkit-specific)
for lang in %langlist; do
	with="with_$lang"
	with=${!with}
	[ $with -eq 0 ] && continue

	language="language_$lang"
	language=${!language}

	cd $language
	mkdir -p %{buildroot}%{tblangdir}/langpack-${language}@thunderbird.mozilla.org/
	cp -f -r * %{buildroot}%{tblangdir}/langpack-${language}@thunderbird.mozilla.org/
	cd ..
done

%if %{with qt}
%pre qt
if [ -d %{tbdir_qt}/dictionaries ]; then
	rm -rf %{tbdir_qt}/dictionaries
fi
%endif

%if %{with gtk}
%pre gtk
if [ -d %{tbdir_gtk}/dictionaries ]; then
	rm -rf %{tbdir_gtk}/dictionaries
fi
%endif

%post
%{_bindir}/update-desktop-database %{_datadir}/applications
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

%if %{with qt}
%files qt
%{_bindir}/thunderbird-qt
%{tbdir_qt}/
%endif

%if %{with gtk}
%files gtk
%{_bindir}/thunderbird-gtk
%{tbdir_gtk}/
%endif
