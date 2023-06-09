# Check credentialsMode

```
oc get cloudcredentials cluster -o=jsonpath={.spec.credentialsMode}
```

```
oc get secret $secret_name -n kube-system -o jsonpath --template '{ .metadata.annotations }'
```
where `secret_name` is `aws-creds` for AWS or `gcp-credentials` for GCP.

AWS or GCP clusters that use `manual` mode only: To determine whether the cluster is configured to create and manage cloud credentials from outside of the cluster, run the following command:
```
oc get authentication cluster -o jsonpath --template='{ .spec.serviceAccountIssuer }'
```

Ref: https://docs.openshift.com/container-platform/4.13/authentication/managing_cloud_provider_credentials/about-cloud-credential-operator.html

# Create CredentialsRequest

When the cluster uses `mint` or `passthrough` mode, users can get cloud credentials with specific permissions by creating a `CredentialsRequest` CR. For example:
```
apiVersion: cloudcredential.openshift.io/v1
kind: CredentialsRequest
metadata:
  annotations:
    capability.openshift.io/name: Logging
    include.release.openshift.io/self-managed-high-availability: "true"
    include.release.openshift.io/single-node-developer: "true"
  name: cluster-logging-operator
  namespace: openshift-cloud-credential-operator
spec:
  providerSpec:
    apiVersion: cloudcredential.openshift.io/v1
    kind: AWSProviderSpec
    statementEntries:
    - action:
      - s3:*
      effect: Allow
      resource: "arn:aws:s3:::*"
  secretRef:
    name: aws-s3-credentials
    namespace: openshift-logging
  serviceAccountNames:
  - cluster-logging-operator
  - logcollector
```
With above file, there will be a `secret/aws-s3-credentials` created in `openshift-logging` project, and the secret contains the `aws_access_key_id` and `aws_secret_access_key` which can be used to manage s3 buckets. More actions can be found here: https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-with-s3-actions.html.


Below CredentialsRequest contains all the requested permissions for s3 bucket:
```
$ oc get credentialsrequests.cloudcredential.openshift.io -n openshift-cloud-credential-operator   openshift-image-registry   -oyaml
apiVersion: cloudcredential.openshift.io/v1
kind: CredentialsRequest
metadata:
  annotations:
    include.release.openshift.io/ibm-cloud-managed: "true"
    include.release.openshift.io/self-managed-high-availability: "true"
    include.release.openshift.io/single-node-developer: "true"
  labels:
    controller-tools.k8s.io: "1.0"
  name: $name
  namespace: openshift-cloud-credential-operator
spec:
  providerSpec:
    apiVersion: cloudcredential.openshift.io/v1
    kind: AWSProviderSpec
    statementEntries:
    - action:
      - s3:CreateBucket
      - s3:DeleteBucket
      - s3:PutBucketTagging
      - s3:GetBucketTagging
      - s3:PutBucketPublicAccessBlock
      - s3:GetBucketPublicAccessBlock
      - s3:PutEncryptionConfiguration
      - s3:GetEncryptionConfiguration
      - s3:PutLifecycleConfiguration
      - s3:GetLifecycleConfiguration
      - s3:GetBucketLocation
      - s3:ListBucket
      - s3:GetObject
      - s3:PutObject
      - s3:DeleteObject
      - s3:ListBucketMultipartUploads
      - s3:AbortMultipartUpload
      - s3:ListMultipartUploadParts
      effect: Allow
      resource: '*'
  secretRef:
    name: $secret-name
    namespace: $namespace
  serviceAccountNames:
  - $serviceaccount
```
