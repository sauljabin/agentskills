---
name: kaskade
description: >-
  Uses Kaskade, a terminal UI for Apache Kafka with two modes: `kaskade admin`
  to browse and manage topics, partitions, and consumer groups, and `kaskade
  consumer` to read records and decode them as JSON, Avro, Protobuf, or
  through Confluent Schema Registry or native Apicurio Registry. Builds the
  right command line, `client.ini`, and `settings.yaml` for TLS, SASL,
  Confluent Cloud, Amazon MSK IAM, offsets, framing, themes, and keybindings.
  Use when the user wants to browse Kafka topics or consumer groups in a
  terminal, consume or decode Kafka records interactively, connect Kaskade to
  a cluster, set up Registry decoding, customize Kaskade themes or shortcuts,
  grant Kaskade ACLs or IAM permissions, or fix a Kaskade error. Also use when
  the user mentions `kaskade` or `kas`.
license: CC-BY-4.0
compatibility: Requires kaskade on Linux or macOS (brew install kaskade or pipx install kaskade) and an interactive terminal to run the TUI.
metadata:
  author: sauljabin
  version: "1.0"
---

# Kaskade

Kaskade is a keyboard-driven terminal UI for Kafka.

- `kaskade admin` shows topics, partitions, and consumer groups, and creates,
  edits, and deletes topics.
- `kaskade consumer` reads records from one topic and decodes keys and values.

Project: https://github.com/sauljabin/kaskade

## Install

```bash
brew install kaskade
# or
pipx install kaskade
kaskade --version
```

## How an agent should use it

Kaskade is a full-screen TUI. It needs a real terminal and a person at the
keyboard. Your job is usually to:

1. Work out the connection, topic, offsets, and decoding the user needs.
2. Build the exact command line, and a `client.ini` when secrets are involved.
3. Hand the command to the user to run in their terminal.
4. Explain what they will see and which keys to press.

Do not try to drive the TUI from a non-interactive shell. `kaskade admin --help`
and `kaskade consumer --help` list every option without opening the TUI. The
consumer connects before the TUI opens, so connection errors print to the
terminal first.

## Quick start

```bash
kaskade admin -b localhost:9092
kaskade admin -b kafka-1:9092,kafka-2:9092
kaskade consumer -b localhost:9092 -t orders
kaskade consumer -b localhost:9092 -t orders -k string -v json --earliest
```

## Consumer options

**Deserializers** for `-k/--key` and `-v/--value`: `bytes`, `boolean`,
`string`, `long`, `integer`, `double`, `float`, `json`, `avro`, `protobuf`,
`registry`.

**Starting position:**

```bash
kaskade consumer -b kafka:9092 -t orders --earliest
kaskade consumer -b kafka:9092 -t orders \
  --partition 1:10 --partition 2:earliest --partition 3
```

`--partition PARTITION[:OFFSET|earliest]` is repeatable. A number, including
`0`, is an absolute offset. No offset means latest. `--earliest` and
`--partition` cannot be combined.

**Schema Registry** (Avro, JSON Schema, and Protobuf detected per record):

```bash
# Confluent (default provider)
kaskade consumer -b kafka:9092 -t orders -k registry -v registry \
  --registry url=http://registry:8081

# Native Apicurio v3
kaskade consumer -b kafka:9092 -t orders -k registry -v registry \
  --registry provider=apicurio \
  --registry apicurio.registry.url=http://registry:8080/apis/registry/v3

# Apicurio through its Confluent-compatible API
kaskade consumer -b kafka:9092 -t orders -v registry \
  --registry url=http://registry:8080/apis/ccompat/v7
```

**Local schemas** use `raw` framing by default. Framing is never guessed from
the bytes; set it explicitly with `framing`, `key.framing`, or `value.framing`
as `raw`, `confluent`, or `apicurio`:

```bash
kaskade consumer -b kafka:9092 -t orders -v json --json value.framing=confluent
kaskade consumer -b kafka:9092 -t orders -v avro --avro value=order.avsc
kaskade consumer -b kafka:9092 -t orders -v protobuf \
  --protobuf descriptor=order.desc --protobuf value=shop.Order \
  --protobuf value.framing=confluent
```

Protobuf needs a descriptor set:
`protoc --include_imports --descriptor_set_out=order.desc --proto_path=protos protos/order.proto`.

**Bytes display:** `--bytes encoding=hex` (or `key.encoding`,
`value.encoding`) with `base64`, `hex`, `byte-array`, `escaped`. Failed
decodes fall back to bytes; set that with `--fallback encoding=hex`.

## Connections

Kafka properties are `confluent-kafka` (librdkafka) names passed with
repeatable `--kafka property=value`:

```bash
kaskade admin -b kafka:9093 --kafka security.protocol=SSL
kaskade admin -b "$BOOTSTRAP" --aws region=us-east-1     # Amazon MSK IAM
```

**Keep secrets out of the command line.** Put them in a private INI file and
pass it with `--config-file`. Sections: `[kafka]`, `[registry]`, `[aws]`,
`[timeouts]`; all optional.

```ini
[kafka]
bootstrap.servers = kafka.example.com:9092
security.protocol = SASL_SSL
sasl.mechanism = PLAIN
sasl.username = replace-with-api-key
sasl.password = replace-with-api-secret

[registry]
url = https://registry.example.com
basic.auth.user.info = replace-with-key:replace-with-secret
```

```bash
chmod 600 prod.ini
kaskade admin --config-file prod.ini
kaskade consumer --config-file prod.ini -t orders -v registry
```

Precedence, lowest to highest: INI sections, then repeated `--kafka`,
`--registry`, `--aws`, `--timeout` options, then `-b`, then AWS IAM settings,
then `--earliest`. A non-empty `bootstrap.servers` is required from some
source.

If the user already has Kantrip profiles, prefer
`kantrip exec PROFILE -- kaskade admin`. Kantrip writes the INI for them and
keeps secrets in its vault.

Confluent Cloud, MSK IAM permissions, Kafka ACLs, OAuth Registry, and timeout
tuning are in [references/connections.md](references/connections.md).

## Keys inside the TUI

| Action | Keys |
| --- | --- |
| Move | arrows or `h` `j` `k` `l` |
| First or last | `g` or `G` |
| Select | `Enter` |
| Back or clear filter | `Esc` |
| Help | `?` or `F1` |
| Command palette (themes, actions) | `:` or `Ctrl+P` |
| Quit | `Ctrl+C` |
| Filter | `/` or `Ctrl+F` |
| Describe topic | `d` or `Enter` |
| Create, edit, delete topic | `n`, `e`, `Ctrl+D` |
| Refresh topics | `Ctrl+R` |
| Copy topic or record JSON | `y` (needs an OSC 52 terminal) |
| Export record JSON | `Ctrl+E` (consumer) |
| Consume more records | `n` (consumer) |
| Change chunk size | `#` |

`Ctrl+C` always quits, even with text selected. Copy selected screen text with
`Cmd+C` on macOS or `Ctrl+Shift+C` on Linux.

## Settings

Personal preferences live in `settings.yaml`, loaded automatically from
`$KASKADE_SETTINGS`, else `$XDG_CONFIG_HOME/kaskade/settings.yaml`, else
`~/.config/kaskade/settings.yaml`. Themes, custom themes, keymaps, and the
admin refresh interval are in [references/settings.md](references/settings.md).

## Troubleshooting

- **Logs:** `~/.local/state/kaskade/kaskade.log` (or under `$XDG_STATE_HOME`).
- **Slow or distant cluster:** raise `--timeout consumer.request=20` or
  `--timeout admin.read=20`.
- **Some consumer groups missing in admin:** the principal lacks `Describe` on
  those groups; Kaskade hides them on purpose.
- **A record shows `⚠`:** the key, value, or a header failed to decode. It is
  shown as bytes with the error; consumption continues. Check the
  deserializer and framing.
- **`y` copies nothing:** the terminal does not support OSC 52 (Apple
  Terminal.app and VTE-based terminals such as GNOME Terminal do not).
- **Restricted to one consumer group:** set `--kafka group.id=NAME`.
  Otherwise Kaskade uses an ephemeral `kaskade-<uuid>` group.

Full documentation: [USAGE.md](https://github.com/sauljabin/kaskade/blob/main/USAGE.md).

## Credits

Based on the [Kaskade](https://github.com/sauljabin/kaskade) documentation by
Saúl Piña.
