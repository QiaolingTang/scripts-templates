# Create CredentialsRequest

With below file, there will be a `secret/aws-s3-credentials` created in `openshift-logging` project, and the secret contains the `aws_access_key_id` and `aws_secret_access_key` which can be used to manage s3 buckets. More actions can be found here: https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-with-s3-actions.html .
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
