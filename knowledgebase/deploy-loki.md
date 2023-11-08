# Set env vars
```
BUCKETNAME="logging-loki-qitang"
SECRETNAME="logging-storage-secret"
NAMESPACE="openshift-logging"
STORAGECLASS=$(oc get sc -ojsonpath={.items[?(@.metadata.annotations.storageclass\\.kubernetes\\.io/is-default-class == \"true\")].metadata.name})
LOKISTACK_NAME="logging-loki"
```

# Create bucket
### AWS
```
STORAGETYPE="s3"

aws s3api create-bucket --bucket ${BUCKETNAME} --region us-east-2 --create-bucket-configuration LocationConstraint=us-east-2

oc extract secret/aws-creds -n kube-system --confirm

oc -n ${NAMESPACE} create secret generic ${SECRETNAME} --from-file=access_key_id=aws_access_key_id --from-file=access_key_secret=aws_secret_access_key --from-literal=region=us-east-2 --from-literal=bucketnames="${BUCKETNAME}" --from-literal=endpoint=https://s3.us-east-2.amazonaws.com
```

### GCP
```
STORAGETYPE="gcs"

gcloud alpha storage buckets create gs://${BUCKETNAME}
oc extract secret/gcp-credentials -n kube-system --confirm
oc -n ${NAMESPACE} delete secret ${SECRETNAME} || :
oc -n ${NAMESPACE} create secret generic ${SECRETNAME} --from-literal=bucketname="${BUCKETNAME}" --from-file="key.json"="service_account.json"
```

# Create lokistack
```
cat << EOF | oc apply -f -
apiVersion: loki.grafana.com/v1
kind: LokiStack
metadata:
  name: ${LOKISTACK_NAME}
  namespace: openshift-logging
spec:
  managementState: Managed
  size: 1x.extra-small
  storage:
    secret:
      name: ${SECRETNAME}
      type: ${STORAGETYPE}
  storageClassName: ${STORAGECLASS}
  tenants:
    mode: openshift-logging
  rules:
    enabled: true
    selector:
      matchLabels:
        openshift.io/cluster-monitoring: "true"
    namespaceSelector:
      matchLabels:
        openshift.io/cluster-monitoring: "true"
EOF
```

```
cat << EOF | oc apply -f -
apiVersion: loki.grafana.com/v1
kind: LokiStack
metadata:
  name: ${LOKISTACK_NAME}
  namespace: openshift-logging
spec:
  managementState: Managed
  size: 1x.demo
  storage:
    secret:
      name: ${SECRETNAME}
      type: ${STORAGETYPE}
  storageClassName: ${STORAGECLASS}
  tenants:
    mode: openshift-logging
  rules:
    enabled: true
    selector:
      matchLabels:
        openshift.io/cluster-monitoring: "true"
    namespaceSelector:
      matchLabels:
        openshift.io/cluster-monitoring: "true"
EOF
```

# Create clusterlogging
```
cat << EOF | oc create -f -
apiVersion: logging.openshift.io/v1
kind: ClusterLogging
metadata:
  name: instance
  namespace: openshift-logging
spec:
  collection:
    type: vector
  logStore:
    lokistack:
      name: ${LOKISTACK_NAME}
    type: lokistack
  managementState: Managed
  visualization:
    type: ocp-console
EOF
```

```
cat << EOF | oc create -f -
apiVersion: logging.openshift.io/v1
kind: ClusterLogging
metadata:
  name: instance
  namespace: openshift-logging
spec:
  collection:
    type: vector
  logStore:
    lokistack:
      name: ${LOKISTACK_NAME}
    type: lokistack
  managementState: Managed
EOF
```
