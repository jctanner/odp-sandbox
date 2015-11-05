````shell
[root@sandbox log]# curl -u admin:admin http://$(hostname -f):8080/api/v1/clusters
{
  "href" : "http://sandbox.odp.com:8080/api/v1/clusters",
  "items" : [
    {
      "href" : "http://sandbox.odp.com:8080/api/v1/clusters/ODP_Sandbox",
      "Clusters" : {
        "cluster_name" : "ODP_Sandbox",
        "version" : "ODP-0.9"
      }
    }
  ]
}
````


