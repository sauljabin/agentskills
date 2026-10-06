# Kaskade connection reference

## Contents

- [Confluent Cloud](#confluent-cloud)
- [Amazon MSK with IAM](#amazon-msk-with-iam)
- [Kafka ACLs](#kafka-acls)
- [OAuth Schema Registry](#oauth-schema-registry)
- [Native Apicurio with OAuth](#native-apicurio-with-oauth)
- [Operation timeouts](#operation-timeouts)

## Confluent Cloud

Prefer an INI file so API secrets stay off the command line:

```ini
[kafka]
bootstrap.servers = pkc-xxxxx.us-east-1.aws.confluent.cloud:9092
security.protocol = SASL_SSL
sasl.mechanism = PLAIN
sasl.username = replace-with-cluster-api-key
sasl.password = replace-with-cluster-api-secret

[registry]
url = https://psrc-xxxxx.us-east-1.aws.confluent.cloud
basic.auth.user.info = replace-with-sr-key:replace-with-sr-secret
```

```bash
kaskade admin --config-file cloud.ini
kaskade consumer --config-file cloud.ini -t orders -k string -v registry
```

## Amazon MSK with IAM

```bash
kaskade admin -b "$AWS_MSK_BOOTSTRAP_SERVERS" --aws region=us-east-1
kaskade consumer -b "$AWS_MSK_BOOTSTRAP_SERVERS" -t orders --aws region=us-east-1
```

Kaskade sets `SASL_SSL`, `OAUTHBEARER`, and token refresh. Credentials come
from the standard AWS provider chain (environment, `AWS_PROFILE`, IAM roles).
Never put AWS credentials in the INI.

Required `kafka-cluster` actions:

| Mode | Actions |
| --- | --- |
| Admin, read only | `Connect`, `DescribeTopic`, `DescribeTopicDynamicConfiguration`, `DescribeGroup` |
| Admin, full | Read-only plus `CreateTopic`, `AlterTopic`, `DeleteTopic`, `AlterTopicDynamicConfiguration` |
| Consumer | `Connect`, `DescribeTopic`, `ReadData`, `DescribeGroup`, `AlterGroup` |

Example policies live in the Kaskade repository under `examples/aws-msk-iam-*.json`.
Cross-account access also needs a resource-based cluster policy.

## Kafka ACLs

For SASL/SCRAM and mTLS principals (`User:<name>` or `User:CN=...`):

| Mode | Topic ACLs | Group ACLs |
| --- | --- | --- |
| Admin, read only | `Describe`, `DescribeConfigs` | `Describe` on groups to show |
| Admin, full | Read-only plus `Create`, `Alter`, `Delete`, `AlterConfigs` | `Describe` on groups to show |
| Consumer | `Read`, `Describe` on the topic | `Read`, `Describe` on `group.id` or the `kaskade-` prefix |

Consumer access to one topic plus Kaskade's ephemeral groups:

```bash
kafka-acls.sh --bootstrap-server "$BOOTSTRAP" \
  --command-config admin-client.properties \
  --add --allow-principal "User:<principal>" \
  --operation Read --operation Describe --topic '<topic>'

kafka-acls.sh --bootstrap-server "$BOOTSTRAP" \
  --command-config admin-client.properties \
  --add --allow-principal "User:<principal>" \
  --operation Read --operation Describe \
  --group kaskade- --resource-pattern-type prefixed
```

`--earliest` and `--partition` use direct assignment and ignore committed
offsets.

## OAuth Schema Registry

Confluent client-credentials flow. Put these in `[registry]` rather than on
the command line when they hold secrets:

```ini
[registry]
url = https://registry.example.com
bearer.auth.credentials.source = OAUTHBEARER
bearer.auth.issuer.endpoint.url = https://idp.example.com/token
bearer.auth.client.id = registry-reader
bearer.auth.client.secret = replace-with-client-secret
bearer.auth.scope = registry.read
bearer.auth.logical.cluster = lsrc-xxxxx
bearer.auth.identity.pool.id = pool-xxxxx
```

Logical cluster and identity pool are deployment-specific. Kaskade passes
every other `--registry` property to the Confluent client unchanged.

## Native Apicurio with OAuth

```ini
[registry]
provider = apicurio
apicurio.registry.url = https://registry.example.com/apis/registry/v3
apicurio.registry.tls.certificates = /private/registry-and-idp-ca.pem
apicurio.registry.auth.service.token.endpoint = https://idp.example.com/token
apicurio.registry.auth.client.id = registry-reader
apicurio.registry.auth.client.secret = replace-with-client-secret
apicurio.registry.auth.client.scope = registry.read
```

- `apicurio.registry.tls.certificates` is the CA bundle for both the Registry
  and the token endpoint; include both chains when they differ.
- Basic auth and unencrypted PEM mTLS are also supported.
- Not supported: JKS/PKCS12, header-based IDs, custom ID handlers, legacy
  8-byte framing, and serializer-only properties.

## Operation timeouts

Seconds, decimals allowed, greater than zero. Set in `[timeouts]` or with
repeatable `--timeout property=seconds`.

| Property | Default | Controls |
| --- | ---: | --- |
| `consumer.poll` | 0.5 | Each fetch poll |
| `consumer.idle` | 2.5 | Stop a page load after empty polls |
| `consumer.assignment` | 15 | Initial assignment or rebalance |
| `consumer.request` | 10 | Metadata and watermark requests |
| `admin.read` | 10 | Metadata, offsets, configs, groups |
| `admin.write` | 60 | Create, edit, delete, partition changes |

Native librdkafka timeouts (`socket.timeout.ms`, `session.timeout.ms`) stay in
`[kafka]` or `--kafka`.
