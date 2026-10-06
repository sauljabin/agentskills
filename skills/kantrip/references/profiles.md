# Kantrip profile reference

Details for `kantrip add` and `kantrip edit` beyond the basics in `SKILL.md`.

## Contents

- [OAuth](#oauth)
- [Schema Registry](#schema-registry)
- [Editing and unsetting fields](#editing-and-unsetting-fields)
- [Importing from properties files](#importing-from-properties-files)
- [Importing Strimzi Secrets](#importing-strimzi-secrets)
- [Storage and vault](#storage-and-vault)

## OAuth

Client-credentials grant. The broker and the token endpoint each have their own
CA. Kantrip prompts for the client secret.

```bash
kantrip add prod-oauth \
  --bootstrap-server kafka.example.com:9093 \
  --ca-file ./kafka-ca.pem \
  --auth oauth \
  --oauth-token-url https://identity.example.com/oauth/token \
  --oauth-client-id kantrip-prod \
  --oauth-scope kafka.read \
  --oauth-ca-file ./identity-ca.pem
```

Repeat `--oauth-scope` for several scopes; order is kept.

## Schema Registry

A profile has at most one Registry. Kafka and the Registry never share secrets
or CA bundles.

- `--registry-url` alone means a Confluent-compatible Registry.
- Native Apicurio needs `--registry-provider apicurio` and the
  `/apis/registry/v3` endpoint.
- Apicurio's Confluent-compatible API uses `--registry-provider confluent` and
  `/apis/ccompat/v7`.
- If you need both Apicurio APIs, create two profiles with the same Kafka
  connection.
- `--registry-provider` without `--registry-url` is invalid.
- Authentication or a CA requires an `https://` URL.

```bash
kantrip add dev-apicurio \
  --bootstrap-server kafka-1:9092,kafka-2:9092 \
  --registry-provider apicurio \
  --registry-url http://registry:8080/apis/registry/v3

kantrip add registry-oauth \
  --registry-provider confluent \
  --registry-url https://registry.example.com \
  --registry-ca-file ./registry-ca.pem \
  --registry-auth oauth \
  --registry-oauth-token-url https://identity.example.com/oauth/token \
  --registry-oauth-client-id registry-client \
  --registry-oauth-scope registry.read \
  --registry-oauth-ca-file ./identity-ca.pem
```

Registry authentication types: Basic, fixed Confluent bearer token, mTLS, and
OAuth. Secrets come from no-echo prompts or private-key files.

Changing the Registry authentication type drops the old type's fields, and its
stored credentials are deleted after the commit. Changing the provider requires
a new Registry URL.

## Editing and unsetting fields

`edit` changes only the fields you pass and keeps the profile's immutable ID.
It needs at least one option.

```bash
kantrip edit dev \
  --bootstrap-server kafka-3:9092,kafka-4:9092 \
  --description 'Shared development cluster' \
  --label environment=development
```

- `--transport tls` turns on TLS with default trust.
- `--ca-file PATH` replaces the custom CA; add `--transport tls` to switch a
  plaintext profile at the same time.
- `--transport plaintext` removes the stored TLS settings.
- `--replace-secret FIELD` prompts for a new value, for example
  `kafka.auth.password`.
- `--unset FIELD` (repeatable) removes an optional field: `description`,
  `labels.KEY`, `registry`, `kafka.tls.ca`, `kafka.auth.oauth.scopes`,
  `kafka.auth.oauth.ca`, `registry.tls.ca`, `registry.auth.oauth.ca`,
  `registry.auth.oauth.scopes`, `registry.auth.oauth.logical-cluster`,
  `registry.auth.oauth.identity-pool-id`. An unknown or required field fails
  with the list of valid names.
- `--unset kafka.tls.ca` and `--ca-file` cannot be combined.

## Importing from properties files

```bash
kantrip add prod --from-properties ./client.properties
kantrip add prod --from-properties -    # stdin; PEM paths must be absolute
```

- The dialect is detected from keys: `sasl.jaas.config` or
  `ssl.truststore.location` means Java; `sasl.username` or `ssl.ca.location`
  means librdkafka. Mixing dialects fails.
- Reads `bootstrap.servers`, `security.protocol` (`PLAINTEXT`, `SSL`,
  `SASL_SSL`), the broker CA, PLAIN/SCRAM, mTLS, OAuth client credentials, and
  one Confluent or Apicurio Registry.
- Settings outside the connection (`acks`, `group.id`, ...) are ignored and
  listed on stderr.
- Fails with exit 2 (naming keys, never values) for: `SASL_PLAINTEXT`, GSSAPI,
  JKS or PKCS12 stores, custom callback classes, disabled verification,
  credentials in the Registry URL, unfilled `{{ ... }}` placeholders, repeated
  keys, or files over 1 MiB.
- Files from `confluent kafka client-config create java|python` import as is.
- Options fill gaps (for example `--bootstrap-server` if the file has none).
  Options that the file also sets must match it.
- Kantrip never changes or deletes the source file, but reminds you that it
  still holds secrets.
- Cannot be combined with `--from-strimzi`.

## Importing Strimzi Secrets

```bash
kubectl get secret app -n kafka -o yaml |
  kantrip add prod --from-strimzi - \
    --bootstrap-server kafka.example.com:9093 \
    --ca-file ./cluster-ca.pem
```

- Input must be one `v1` Secret labeled `strimzi.io/kind: KafkaUser`.
- A SCRAM Secret becomes `scram-sha-512`; a TLS Secret becomes mTLS.
- `--bootstrap-server` is required: the Secret names no brokers.
- The Secret's `ca.crt` is the clients CA and is ignored. For a listener
  signed by the Strimzi cluster CA, pass `ca.crt` from the
  `CLUSTER-cluster-ca-cert` Secret with `--ca-file`.
- Kantrip never contacts Kubernetes.

## Storage and vault

- Database lookup order: `KANTRIP_DATABASE`,
  `$XDG_DATA_HOME/kantrip/profiles.db`, `~/.local/share/kantrip/profiles.db`.
  Directory `0700`, file `0600`. Change it only through `add`, `edit`, and
  `remove`.
- macOS vault: `~/Library/Keychains/kantrip.keychain-db`. Locks after 15 idle
  minutes and on sleep. Unlock for scripts with
  `security unlock-keychain ~/Library/Keychains/kantrip.keychain-db`.
- Linux vault: GNOME Keyring collection `kantrip` or KDE Wallet `kantrip`
  (Classic, not GPG). Password windows appear on the desktop and time out
  after 60 seconds. Other Secret Service providers are refused.
- Delete credentials with `kantrip remove` or replace them with
  `kantrip edit --replace-secret`, never directly in the vault.
