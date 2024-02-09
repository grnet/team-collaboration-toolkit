============
Installation
============

For the time being it is not possible to install the collections using
``ansible-galaxy``. You need to clone the repository like this::

  git clone https:://github.com/grnet/team-collaboration-toolkit.git

You also need to add the working directory to
ANSIBLE_COLLECTIONS_PATH_, for example::

  export ANSIBLE_COLLECTIONS_PATH=$ANSIBLE_COLLECTIONS_PATH:\
  /home/user/team-collaboration-toolkit

.. _ansible_collections_path: https://docs.ansible.com/ansible/latest/reference_appendices/config.html#envvar-ANSIBLE_COLLECTIONS_PATH
