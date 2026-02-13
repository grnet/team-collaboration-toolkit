.. _guide_nextcloud:

==================
Guide to Nextcloud
==================

.. contents::
   :local:
   :depth: 1

Usage
=====

The collection has an :file:`examples` directory. Use it like this:

1. Ensure you have a valid domain name on which to install Nextcloud
   (it's hard to use an invalid domain name because certbot will not
   work properly).
2. Ensure the collection is installed as explained in the "Installation"
   section above.
3. Copy :file:`examples/nextcloud-deploy` elsewhere and go there to make
   changes.
4. Find all instances of ``example.com`` and modify them as needed.
5. Run the playbook: ``ansible-playbook site.yml``.

For more information, check the role reference.

FAQ
===

The ``mysql`` Ansible module is missing
---------------------------------------

Ansible versions older than 2.10 are not supported by Ansible. Please
upgrade Ansible to a supported version.

An error occurs while executing the reboot task
-----------------------------------------------

This occurs when the target machine is localhost, that is, when the
Ansible controller is the same machine as the Nextcloud server. This is
not supported.

Why ferm?
---------

Short answer: It's simpler and better.

Longer answer: ``iptables`` is hard to use and many users prefer
``ufw``. While it is often sufficient, ``ufw`` is too simple. It can
work well for years but at some point you will need something it doesn't
do. For example, you may want to deny access to a given IP address; this
rule must be among the first checked, and with ``ufw`` it's hard to
define the order of rules (at least with Ansible).

With ``ferm``, all firewall configuration is in files in
:file:`/etc/ferm`. Entering ``service ferm reload`` replaces all
iptables with those specified in :file:`/etc/ferm`. ``service ferm
stop`` deactivates the firewall. The syntax of these files is simple and
intuitive, resulting in ``ferm`` being easier, although this also
depends on your experience.

``ferm`` is also preferred by others, such as the debops project.

For more information on how we use ``ferm`` with Ansible, read the
`Firewall section of the "common" role`_.

.. _firewall section of the "common" role: https://aptikogeneral.readthedocs.io/en/latest/common.html#firewall
