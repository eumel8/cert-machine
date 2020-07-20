cert-machine
============

generate client certs via API

prerequisites
-------------

you need your previously generated ca.key and ca.crt. The ca.key has probably a password:

```
kubectl create ns cert-machine
kubectl -n cert-machine create secret generic cert-ca --from-file=ca.key=./ca.key --from-file=ca.crt=./ca.crt
kubectl -n cert-machine create secret generic ca-key-password --from-literal=ca_key_password='xxxx'

```

installation
------------

```
kubectl -n cert-machine apply -f kubernetes/deployment.yaml
kubectl -n cert-machine apply -f kubernetes/service.yaml
```

usage
-----

```
curl http://cert-machine/client/new
```

or

```
kubectl -n cert-machine run -it busybox --image=eumel8/cert-machine:latest --restart=Never -- curl http://cert-machine/client/new
```
