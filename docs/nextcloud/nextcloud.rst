.. _nextcloud:

=========
nextcloud
=========

Overview
========

Installs and configures Nextcloud. Use like this::

  - role: grnet.nextcloud.nextcloud
    nextcloud_fqdn: nextcloud.example.com
    default_phone_region: GR
    mail_from_address: noreply
    mail_domain: example.com

You may need to perform additional configuration using Nextcloud's web
interface. See section :ref:`nextcloud_limitations` for that.

Parameters
==========

``nextcloud_fqdn``
  The domain name for Nextcloud.

``nextcloud_admin_user``
  The username for the Nextcloud administrator. The default is
  ``admin``.

``nextcloud_admin_user_password``
  The Nextcloud administrator password. This will usually be in the
  vault.

``nextcloud_download_url``
  By default, the latest version of Nextcloud Community will be
  installed. To install another version, specify a different URL, such
  as
  ``https://download.nextcloud.com/server/releases/nextcloud-24.0.11.zip``.
  It must point to a zip file.

  Unless when an upgrade is specifically requested, this role downloads
  and installs Nextcloud only if it is not already installed; if already
  installed, the role does not upgrade it and ``nextcloud_download_url``
  is irrelevant. To upgrade Nextcloud, see :ref:`upgrading_nextcloud`.

``php_memory_limit``
  Default 512M.

``opcache_interned_strings_buffer``
  The default for this PHP setting is 8. However in some installations
  it might need to be set to 16, and sometimes to 32. It seems to depend
  on the installed apps. See the `related support forum discussion`_ for
  more information.

  .. _related support forum discussion: https://help.nextcloud.com/t/nextcloud-23-02-opcache-interned-strings-buffer/134007/4

``default_phone_region``
  A country code like "GR". There is no default. This is used for
  Nextcloud's ``default_phone_region`` configuration parameter.

``mail_from_address``, ``mail_domain``
  The email address from which email notifications from Nextcloud appear
  to be sent. For example, to use ``noreply@example.com``, specify
  ``mail_from_address=noreply`` and ``mail_domain=example.com``.

  These settings are those that can be set in the web interface, under
  Basic settings, Email server. This role will overwrite these settings
  whenever Ansible is run.

  It will always use localhost port 25 as the smarthost, without
  authentication and without encryption. For this to work, use Ansible
  role mail_satellite_.

  .. _mail_satellite: https://aptikogeneral.readthedocs.io/en/latest/mail_satellite.html

``mysql_client_key``, ``mysql_client_cert``, ``mysql_ca_cert``
  By default, these parameters are empty. In this case, Nextcloud
  connects to MySQL without TLS. If they have values, they must be
  pathnames (in the Ansible controller) from which the keys and
  certificates are taken and installed in the Nextcloud server. In this
  case, Nextcloud is configured to connect to MySQL with TLS.

  Either all three must be empty, or all three must have a value.

``nextcloud_cron_schedule``
  How often to run Nextcloud's ``cron.php`` (which, e.g., sends
  notifications to users). It must be in the format accepted by
  ``cron``. The default is ``*/5 * * * *``.

``nextcloud_maintenance_window_start``
  The start time, as an integer hour, in UTC, when cron is allowed to
  perform non-time-critical tasks. (The end time is four hours later.)
  The default is 1, i.e. 01:00 UTC.

.. _upgrading_nextcloud:

Upgrading Nextcloud
===================

The role has the option of upgrading Nextcloud to a newer version.
This will cause some downtime and it is important to understand how it
works before trying it. Apart from some checks, this is what it does:

* It moves :file:`/etc/cron.d/nextcloud` to :file:`/tmp/nextcloud.cron`.
* It downloads and unzips the new Nextcloud version to
  :file:`/tmp/nextcloud`.
* It copies the existing Nextcloud installation's :file:`config.php` to
  :file:`/tmp/nextcloud/config`.
* It stops the php-fpm service.
* It moves the existing Nextcloud installation directory to
  :file:`/tmp/nextcloud.old`, then moves the data directory to
  :file:`/tmp/nextcloud/data`, then moves :file:`/tmp/nextcloud` to the
  correct directory (:file:`/var/www/.../nextcloud`). These should
  happen instantly, because these moves are in the same filesystem. In
  fact, the playbook verifies that this is the case before running.
* It starts the php-fpm service. So far the downtime is minimal.
* It executes the ``php occ upgrade`` command. This takes several
  minutes during which Nextcloud is out of service (it shows a related
  message to users).
* It copies :file:`/tmp/nextcloud.old/translationfiles` to the correct
  location (this contains updated Greek translations).
* It moves :file:`/tmp/nextcloud.cron` back to its correct location.

You can upgrade Nextcloud by specifying the ``upgrade_nextcloud`` tag.
In that case, you also need to specify ``nextcloud_download_url`` to
point to the version you want to upgrade to. **This should not be more
than one major release ahead of what is already installed** (this is not
checked), otherwise the upgrade will fail.

Here is an example of how to upgrade::

    ansible-playbook site.yml --tags upgrade_nextcloud \
        -e nextcloud_download_url=https://download.nextcloud.com/server/releases/nextcloud-23.0.0.zip

If all goes well, at the end of the upgrade the directory
:file:`/tmp/nextcloud.old` still contains the old installation (but
without the `data` directory). You need to remove it or move it
elsewhere in order to attempt another upgrade.

If anything goes wrong, you have to cleanup yourself (restore
:file:`/etc/cron.d/nextcloud` and :file:`/var/www/.../nextcloud`). This
is why it is important to understand the process clearly.

Sometimes after major upgrades the theme might break; for example, icons
or logos may be missing from the main toolbar or from other toolbars
(such as the toolbar of the markdown editor). In this case, this
typically fixes the problems::

    cd /var/www/.../nextcloud
    sudo -u www-data php occ maintenance:repair

.. _nextcloud_limitations:

Limitations
===========

Server setup
------------

Many things are hardwired. The current assumption is that Nextcloud,
Redis and Apache are all going to be in the same machine.

Setting up theming
------------------

It seems to be nontrivial to setup theming through the command line,
particularly to setup logo, background and favicon. Therefore, the role
does not touch theming; use the web interface to setup theming after
Ansible is run.

Setting up the Mail app
-----------------------

It doesn't seem to be possible to setup the Mail app through the command
line or Ansible. You need to go to the web interface, logon as admin,
and go to Settings, Administration, Groupware.
