.. _jitsi_statistics:

====================================
Getting statistics about Jitsi usage
====================================

Company administrators often want to see some statistics about what
conferences happened and what the attendance was. We have a Prometheus
exporter that can provide this information to a Prometheus server. The
exporter is installed if prometheus_server_ips_ has a value.

To enable the exporter, follow these steps:

 * Ensure prometheus_server_ips_ has a valid value.
 * Optionally set :ref:`jitsi_prometheus_exporter_port
   <jitsi_reference>`; the default is 9102.
 * Add an appropriate item to prometheus_scrape_configs_; for example::

    prometheus_scrape_configs:
      - job_name: jitsi
        static_configs:
          - targets:
              - jitsi.example.com:9102

To create a graph of the data in a Grafana dashboard:

 * Go to the dashboard and select Add, Visualization.
 * In the right panel, visualization, select "Time series", and in the
   Panel options below it, specify a title such as "Jitsi conference
   participants".
 * In the bottom panel, in the query builder, select Code (instead of
   "Builder) and type the PromQL query ``label_replace(jitsi_room_participants, "room", "$1", "room", "(.*)@.*")``.
 * Switch to Builder Label filters select ``room !=
   __active_rooms_exist__``.
 * In the query builder, under Options, select Legend = ``{{room}}``.

.. _prometheus_server_ips: https://aptikogeneral.readthedocs.io/en/latest/prometheus.html#parameters
.. _prometheus_scrape_configs: https://aptikogeneral.readthedocs.io/en/latest/prometheus.html#parameters

