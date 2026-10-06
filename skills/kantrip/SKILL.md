---
name: kantrip
description: >-
  Uses Kantrip, a CLI that stores Kafka connection profiles (brokers, TLS,
  SASL/SCRAM, mTLS, OAuth, and a Confluent or Apicurio Schema Registry) and
  runs Kafka clients such as kcat, kafka-topics, the Confluent consoles,
  Kaskade, kaf, and kcl against a chosen profile, with secrets kept in a
  dedicated OS vault. Use when the user wants to add, edit, import, list,
  describe, or remove a Kafka profile, switch between Kafka clusters, run a
  Kafka command against a named cluster, check connectivity with ping, run
  doctor, read KANTRIP_* or KAFKA_*_CONFIG_FILE variables in an app, or fix a
  Kantrip error or exit code. Also use when the user mentions `kantrip`,
  `kan`, or `kantrip exec`.
license: CC-BY-4.0
compatibility: Requires kantrip on Linux or macOS (pipx install kantrip). Commands that store or read secrets need an interactive terminal.
metadata:
  author: sauljabin
  version: "1.0"
---

# Kantrip

Kantrip saves Kafka connection profiles and hands the right one to the client
you are about to run. For each run it writes the client's own config format to
a private temporary directory, starts the client, and deletes the files when
the client exits. Secrets live in a dedicated vault in the OS credential store,
never in the profile or on the command line.

There is no global "current profile". Every command names its profile, or runs
inside a subshell opened for it.

Project: https://github.com/sauljabin/kantrip

## Install and check

```bash
pipx install kantrip
kantrip --version
kantrip doctor
```

`doctor` is read-only and never contacts Kafka. It checks the profile database,
the vault, stored credentials, certificate expiry, sessions, and installed
clients. `kantrip doctor --repair` is the only maintenance command: it
migrates, cleans pending credential entries, and removes stale sessions.

## Core commands

```bash
kantrip add local                                # plaintext, localhost:9092
kantrip list                                     # all profiles
kantrip list -l environment=dev -o json          # filter by label, JSON output
kantrip describe local                           # public fields, never secrets
kantrip ping local                               # connect and authenticate
kantrip exec local -- kcat -L                    # run one client with the profile
kantrip exec local                               # open a subshell for the profile
kantrip current                                  # active profile in a subshell
kantrip edit local --description 'Local broker'  # change only the given fields
kantrip remove local                             # asks for confirmation
```

- `exec PROFILE -- COMMAND ...` passes everything after the command through
  unchanged. Kantrip's own options, such as `--no-color`, go before `PROFILE`.
- Without a command, `exec` opens Bash, Zsh, or Fish (from `SHELL`). Every
  supported client works there without `kantrip exec`. Sessions cannot be
  nested; `exit` first.
- `list`, `describe`, and `ping` accept `-o json` or `-o yaml`. Prefer them when
  parsing output.
- `describe` output is for reading. It is not an export that `add` can import.

## Adding profiles

`add` selects TLS automatically when `--ca-file`, `--auth`, or a client
certificate is given. Credentials never travel over plaintext.

```bash
# TLS with a public CA
kantrip add prod --bootstrap-server kafka.example.com:9093 --transport tls

# Private CA
kantrip add prod --bootstrap-server kafka.internal:9093 --ca-file ./ca.pem

# SCRAM or PLAIN (prompts for the password)
kantrip add prod --bootstrap-server kafka.example.com:9093 \
  --auth scram-sha-512 --username app

# mTLS (prompts only if the key is encrypted)
kantrip add prod --bootstrap-server kafka.example.com:9093 --auth mtls \
  --client-certificate-file ./client.crt --client-key-file ./client.key

# Several brokers, labels, and a Confluent-compatible Registry
kantrip add dev -b kafka-1:9092 -b kafka-2:9092 \
  -l environment=dev -l owner=platform \
  --registry-url http://registry:8081

# Import from an existing Java or librdkafka properties file (no prompts)
kantrip add prod --from-properties ./client.properties

# Import a Strimzi KafkaUser Secret without writing it to disk
kubectl get secret app -n kafka -o yaml |
  kantrip add prod --from-strimzi - \
    --bootstrap-server kafka.example.com:9093 --ca-file ./cluster-ca.pem
```

OAuth, Registry authentication, Apicurio, `edit --unset`, and the import rules
are in [references/profiles.md](references/profiles.md).

## Rules for agents

1. **Never put a secret in an argument, environment variable, file, or
   message.** Kantrip has no option that takes a password, token, or client
   secret on the command line, by design. It reads them from a no-echo prompt.
2. **Prompts need the user's terminal.** These commands may ask for a password
   or open a desktop vault window:
   - `add` or `edit` that stores a secret (`--auth`, `--registry-auth`,
     `--replace-secret`)
   - any command when the vault is locked or does not exist yet (`exec`,
     `ping`, `doctor`, `remove` of a profile with credentials)

   You cannot answer those prompts. Give the user the exact command to run in
   their own terminal, then continue after they confirm. Without a terminal, a
   locked vault fails at once with guidance; it does not hang.
3. **`list`, `describe`, `current`, and `--help` never touch the vault.** Use
   them freely to inspect state.
4. **Ask before destructive commands.** `remove` deletes the profile and its
   credentials. It needs `-y/--yes` without a terminal. Get explicit approval
   before adding `--yes`.
5. **Do not pass connection options to clients.** Kantrip rejects arguments
   that would override the profile, such as `-b`, `--bootstrap-server`,
   `--command-config`, `-F`, or `--config`. Pass only resource and output
   options (topics, groups, offsets, formats).
6. **Do not repeat a command after exit code 3 or 4.** See the table below.
7. **Use symlinks, not aliases,** for short names (`kan`, `kas`). Kantrip
   cannot tell which client an alias or wrapper script runs.

## Exit codes for add, edit, and remove

| Code | Meaning | What to do |
| --- | --- | --- |
| `0` | Change and cleanup finished | Nothing |
| `1` | The change certainly was not committed | Fix the cause and retry |
| `2` | Invalid options or values; nothing changed | Read the message and fix the arguments |
| `3` | Committed, but cleanup or the follow-up check did not finish | Run `kantrip describe` and `kantrip doctor --repair`; do not repeat the command |
| `4` | Unknown whether the change was committed | Stop retries; inspect with `describe` and `doctor` first |

`ping` exits `0` only when every attempted check is ok, and `1` otherwise.
`ping --quiet` prints nothing and only sets the exit status. `exec` exits with
the client's own exit code, or `128 + signal` when a signal killed it.

## Running clients

```bash
kantrip exec prod -- kcat -C -t orders
kantrip exec prod -- kafka-topics --list
kantrip exec prod -- kafka-console-consumer.sh --topic orders --from-beginning
kantrip exec prod -- kafka-avro-console-consumer --topic orders --from-beginning
kantrip exec prod -- kaskade admin
kantrip exec prod -- kaskade consumer --topic orders -v registry
kantrip exec prod -- kaf topics
kantrip exec prod -- kcl topic list
```

Each client has its own limits, mostly around Registry providers and OAuth.
Before suggesting a client for a profile with OAuth, Apicurio, or Registry
authentication, read [references/clients.md](references/clients.md).

## Using a profile from your own program

Programs started with `kantrip exec` (or inside its subshell) get file paths,
never connection values:

| Variable | Contents |
| --- | --- |
| `KAFKA_JAVA_CONFIG_FILE` | Java client properties with the full Kafka connection |
| `KAFKA_LIBRDKAFKA_CONFIG_FILE` | librdkafka properties with the same connection |
| `SCHEMA_REGISTRY_JAVA_CONFIG_FILE` | Java properties: Kafka plus `schema.registry.*` (Confluent provider) |
| `SCHEMA_REGISTRY_LIBRDKAFKA_CONFIG_FILE` | Registry-only properties for librdkafka clients (Confluent provider) |
| `APICURIO_REGISTRY_CONFIG_FILE` | Native Apicurio Registry properties |
| `KANTRIP_PROFILE` | Profile display name |
| `KANTRIP_SESSION_ID`, `KANTRIP_SESSION_DIR` | Session metadata |

Kantrip removes any inherited `KAFKA_*`, `SCHEMA_REGISTRY_*`, `APICURIO_*`, and
JVM option variables first. Read the config file in your app. Never log the
environment or the file contents.

## Troubleshooting

- **Something is wrong but unclear:** `kantrip doctor PROFILE -v`.
- **Connection fails:** `kantrip ping PROFILE`, then `ping -o json` for the
  per-service `error` and `cause`. A passing ping proves the connection and
  authentication, not topic or schema permissions.
- **"database created by a pre-release version":** move the database aside
  (path from `doctor --verbose`) and add the profiles again.
- **Missing credential:** `kantrip edit PROFILE --replace-secret FIELD`. Field
  names come from `kantrip describe PROFILE`, such as `kafka.auth.password`.
- **Client too old:** the error names the minimum release. See
  [references/clients.md](references/clients.md).
- **Prompt integration:** shells can show `$KANTRIP_PROFILE`. It is set only
  inside a `kantrip exec PROFILE` subshell.

Full documentation: [USAGE.md](https://github.com/sauljabin/kantrip/blob/main/USAGE.md)
and [COMPATIBILITY.md](https://github.com/sauljabin/kantrip/blob/main/COMPATIBILITY.md).

## Credits

Based on the [Kantrip](https://github.com/sauljabin/kantrip) documentation by
Saúl Piña.
