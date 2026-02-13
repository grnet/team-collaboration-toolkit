.. _guide_nextcloud:

==================
Guide to Nextcloud
==================

.. contents::
   :local:
   :depth: 1

Requirements
============

Short version
-------------

For 50 users:

 * 4 CPUs
 * 8 GB RAM
 * As much disk space as the users' files plus 30 GB.

But please read also the long version.

Long version
------------

In GRNET, where Nextcloud is being used, as of 2026, by about 50 users,
we have it installed on VMs with very slow disks, which are the
bottleneck. In order to work around this, we've put MySQL on a separate
VM, and that latter VM has two disks: one for the redo logs and one for
the data files. Thus we effectively use three disks in parallel. However
on a server with modern disks (let alone one with SSD), it is unlikely
this will be necessary.

Our Nextcloud server has 16 CPUs and 32 GB RAM, however the CPUs are
mostly idle, and there are 20 GB RAM free and 9 GB used for buffers and
cache. On our MySQL server it's hard to talk about RAM because MySQL
always consumes the entire available RAM, however its 8 CPUs are mostly
idle. Our feeling from what we see is that if the disk was faster, a
single server as described in the short version above would suffice.

However the machine load also depends on what these 50 users are doing,
and every organization is different. In GRNET about half are
developers/devops who use Nextcloud very little. For your organization
we don't know, but it's likely you won't know either before you see the
system in action.

Regarding disk space, we see that the installed system and the MySQL
data are slightly over 10 GB, but MySQL grows slowly. Therefore the 30
GB that we propose is approximately twice as much as is needed and will
result in about 50% usage, not including users' files.

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
