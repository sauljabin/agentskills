# Kantrip client reference

What each supported client gets from Kantrip, what it rejects, and where it
stops. Other programs (for example `kafkactl`) have no adapter but can still
run under `kantrip exec` and read the `KAFKA_*_CONFIG_FILE` variables.

## Minimum versions

| Client | Minimum | Also checked |
| --- | --- | --- |
| Apache Kafka Java CLIs (`*.sh`) | Kafka 2.6 | 2.7 for custom CA or mTLS; 4.1 for OAuth |
| Confluent Platform Java CLIs | CP 6.0 | 6.1 for custom CA or mTLS; 8.1 for OAuth |
| Schema Registry consoles | CP 5.5 | As for Confluent Platform |
| `kcat` / `kafkacat` | 1.7.0 | librdkafka 2.11.0 for OAuth with a custom token CA |
| `kaskade` | 5.0.1 | None |
| `kaf` | 0.2.14 | None |
| `kcl` | 0.20.0 | None |

Kantrip checks the version before every launch and names the release to
install when it is too old. `kantrip doctor` shows the same result.

## kcat

- Gets `KCAT_CONFIG` pointing at a private librdkafka file.
- `-s avro`, `-s key=avro`, `-s value=avro` get the Registry URL through `-r`.
- Avro works only with a Confluent-compatible Registry **without**
  authentication. Not with native Apicurio.
- Rejects `-F`, `-r`, and `-X schema.registry.url=...`.

```bash
kantrip exec prod -- kcat -L
kantrip exec prod -- kcat -C -t orders
kantrip exec prod -- kcat -C -t avro-orders -s value=avro
```

## Apache Kafka and Confluent Java CLIs

- Seven shared commands: `kafka-topics`, `kafka-console-producer`,
  `kafka-console-consumer`, `kafka-consumer-groups`, `kafka-configs`,
  `kafka-acls`, `kafka-broker-api-versions`. Use `.sh` names with Apache
  archives and unsuffixed names with Confluent Platform.
- Get `--bootstrap-server` plus `--consumer.config`, `--producer.config`, or
  `--command-config`. These cannot be overridden.

```bash
kantrip exec prod -- kafka-topics --list
kantrip exec prod -- kafka-consumer-groups --list
kantrip exec prod -- kafka-configs --describe --entity-type topics --entity-name orders
```

## Confluent Schema Registry consoles

- `kafka-avro-console-*`, `kafka-json-schema-console-*`,
  `kafka-protobuf-console-*` (producer and consumer).
- Need a Registry with the Confluent provider. Any authentication type works.
- Fail before starting without a Registry or with native Apicurio.

```bash
kantrip exec prod -- kafka-avro-console-consumer --topic orders --from-beginning
```

## Kaskade

- `admin` and `consumer` get a private INI through `--config-file`.
- `-k registry` or `-v registry` switches to an INI with a `[registry]`
  section for the profile's provider.
- Decodes Avro, JSON Schema, and Protobuf with **both** Confluent and native
  Apicurio. The only client that decodes native Apicurio.
- A Registry with a fixed token fails before launch for Registry decoding.
- Rejects `-b/--bootstrap-servers`, `--config-file`, `--registry`, and
  `--kafka` except `group.id` and `broker.address.family`.

```bash
kantrip exec prod -- kaskade admin
kantrip exec prod -- kaskade consumer --topic orders
kantrip exec prod -- kaskade consumer --topic avro-orders --earliest -v registry
```

## kaf

- Gets a private config with one cluster named `kantrip`, via `--config`.
  Runs with `HOME=/dev/null` so it can never save credentials.
- Kafka OAuth profiles fail before launch.
- Registry: Confluent-compatible, no auth or Basic, system-trusted CA only.
  Any other Registry setup makes every kaf command fail.
- Rejects `--config`, `-b/--brokers`, `-c/--cluster`, `--schema-registry`,
  and every `kaf config` command.

```bash
kantrip exec prod -- kaf topics
kantrip exec prod -- kaf consume orders --offset oldest
echo '{"id":"42"}' | kantrip exec prod -- kaf produce orders --avro-schema-id 7
```

## kcl

- Gets a private TOML config through `KCL_CONFIG_PATH`. `KCL_*` variables are
  removed.
- Kafka OAuth profiles fail before launch.
- Registry: Confluent-compatible with no auth, Basic, fixed token, or mTLS.
  OAuth and native Apicurio fail.
- Rejects `-B`, `-R`, `-C/--profile`, `--config-path`, `--no-config-file`,
  `--config-env-prefix`, every `kcl profile` command, and `-X` keys other
  than `broker_timeout`, `dial_timeout`, `retry_timeout`, `help`, `list`.

```bash
kantrip exec prod -- kcl topic list
kantrip exec prod -- kcl consume orders --decode=value
```

## Choosing a client by profile type

| Profile has | Works | Does not work |
| --- | --- | --- |
| Kafka OAuth | Java CLIs (version permitting), consoles, kcat, Kaskade | kaf, kcl |
| Native Apicurio Registry | Kaskade | kcat Avro, consoles, kaf, kcl Registry |
| Confluent Registry with auth | Consoles, Kaskade (not fixed token), kcl (not OAuth) | kcat Avro, kaf (except Basic) |
| Confluent Registry, no auth | All Registry-capable clients | None |
