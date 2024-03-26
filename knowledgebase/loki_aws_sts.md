# Preparing file
```
cluster_name=$(oc get infrastructures.config.openshift.io cluster -ojsonpath={.status.infrastructureName})
lokistack_name="logging-loki-$cluster_name"
oidc_provider=$(oc get authentication cluster -o json | jq -r '.spec.serviceAccountIssuer' | sed 's~http[s]*://~~g')
lokistack_ns="openshift-logging"

aws_account_id=$(aws sts get-caller-identity --query 'Account' --output text)
region=$(oc get infrastructures.config.openshift.io cluster -ojsonpath={.status.platformStatus.aws.region})
cluster_id=$(oc get clusterversion -o jsonpath='{.items[].spec.clusterID}{"\n"}')

trust_rel_file="/tmp/$cluster_id-trust.json"
role_name="$lokistack_ns-$lokistack_name"

cat > "$trust_rel_file" <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Effect": "Allow",
     "Principal": {
       "Federated": "arn:aws:iam::${aws_account_id}:oidc-provider/${oidc_provider}"
     },
     "Action": "sts:AssumeRoleWithWebIdentity",
     "Condition": {
       "StringEquals": {
         "${oidc_provider}:sub": [
           "system:serviceaccount:${lokistack_ns}:${lokistack_name}",
           "system:serviceaccount:${lokistack_ns}:${lokistack_name}-ruler"
         ]
       }
     }
   }
 ]
}
EOF
```

# Creating IAM role
```
role_arn=$(aws iam create-role \
             --role-name "$role_name" \
             --assume-role-policy-document "file://$trust_rel_file" \
             --query Role.Arn \
             --output text)
echo $role_arn
```

# Attaching role policy 'AmazonS3FullAccess' to role
```
aws iam attach-role-policy \
  --role-name "$role_name" \
  --policy-arn "arn:aws:iam::aws:policy/AmazonS3FullAccess"
```

# Create Bucket
```
BUCKETNAME="logging-loki-qitang"
SECRETNAME="logging-storage-secret"
STORAGECLASS=$(oc get sc -ojsonpath={.items[?(@.metadata.annotations.storageclass\\.kubernetes\\.io/is-default-class == \"true\")].metadata.name})

aws s3api create-bucket --bucket ${BUCKETNAME} --region us-east-2 --create-bucket-configuration LocationConstraint=us-east-2
```

# Create Secret
```
oc -n ${lokistack_ns} create secret generic ${SECRETNAME} \
  --from-literal=bucketnames="${BUCKETNAME}" \
  --from-literal=role_arn="${role_arn}" \
  --from-literal=region="us-east-2"
```

# Deploy Lokistack
```
cat << EOF | oc apply -f -
apiVersion: loki.grafana.com/v1
kind: LokiStack
metadata:
  name: ${lokistack_name}
  namespace: openshift-logging
spec:
  managementState: Managed
  size: 1x.demo
  storage:
    secret:
      name: ${SECRETNAME}
      type: s3
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

# Cleanup Resources
```
aws iam detach-role-policy --role-name "${role_name}" --policy-arn "arn:aws:iam::aws:policy/AmazonS3FullAccess"
aws iam delete-role --role-name "${role_name}"
```
