=========
Collabora
=========

Overview
========

Installs Collabora Office with an Apache reverse proxy on port 443, so
that it can be used from nextcloud.

Parameters
==========

``nextcloud_fqdn``
  The domain name for Nextcloud.

``collabora_fqdn``
  The domain name for Collabora Office.

``collabora_allowed_languages``
  The languages allowed for spell checking, as a space-separated string.
  The default is ``en_US``.  Avoid specifying too many as it is said to
  affect startup performance.
