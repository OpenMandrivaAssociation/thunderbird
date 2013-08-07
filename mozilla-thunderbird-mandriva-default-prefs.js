pref("general.useragent.vendor", "Mandriva");
pref("general.useragent.vendorSub", "THUNDERBIRD_RPM_VR");
pref("general.useragent.vendorComment", "THUNDERBIRD_VENDOR_COMMENT");

# Follow system locale
pref("intl.locale.matchOS", true);

# extensions.autoDisableScopes is a new preference added in firefox 8
# it defines "scopes" where newly installed addons are disabled by default
# this is an additive bit field, and the value defaults to 15 (1+2+4+8)
# we need to remove system scope (8) from it so language packs and other addons
# which are installed systemwide won't get marked as 3rd party and disabled
# documentation: http://kb.mozillazine.org/About:config_entries#Extensions.
# or in toolkit/mozapps/extensions/AddonManager.jsm
# we also need to disable the "disable addon selection dialog"
pref("extensions.autoDisableScopes", 0);
pref("extensions.shownSelectionUI", true);
