# Agent Skills

A collection of [Agent Skills](https://agentskills.io/) for AI coding agents
such as Claude Code, Codex, Cursor, GitHub Copilot, and others. Each skill is a
folder with a `SKILL.md` file that follows the
[Agent Skills specification](https://agentskills.io/specification), and the
whole collection installs with the [skills](https://www.skills.sh/) CLI.

## Skills

| Skill | What it does |
| --- | --- |
| [conventional-commits](skills/conventional-commits/SKILL.md) | Writes commit messages in the Conventional Commits style: eleven standard types, a scope chosen from what the diff changes, lowercase imperative subjects, `!` for breaking changes, and an `Assisted-by` trailer as the only AI attribution. |
| [kantrip](skills/kantrip/SKILL.md) | Uses [Kantrip](https://github.com/sauljabin/kantrip) to store Kafka connection profiles and run kcat, the Kafka and Confluent CLIs, Kaskade, kaf, and kcl against a named cluster, keeping secrets in an OS vault. Knows the commands, exit codes, client limits, and when to hand a prompt to the user. |
| [kaskade](skills/kaskade/SKILL.md) | Uses [Kaskade](https://github.com/sauljabin/kaskade), the Kafka terminal UI, to browse topics and consumer groups and to consume and decode records (JSON, Avro, Protobuf, Confluent or Apicurio Registry). Builds the command line, `client.ini`, and `settings.yaml` for TLS, SASL, Confluent Cloud, and MSK IAM. |
| [explain-simply](skills/explain-simply/SKILL.md) | Explains code, errors, and concepts, and writes documentation such as `README.md` and `USAGE.md`, in short plain sentences without losing information: one concrete example with real values, each fact said once with one home, links instead of repeated text, and plain wording instead of filler. |

## Install the skills CLI

The `skills` CLI installs and updates skills for every supported agent.

### Homebrew (recommended)

```bash
brew install skills
```

### Without Homebrew

Install it globally with npm (requires Node.js):

```bash
npm install -g skills
```

Or run it without installing, by putting `npx` in front of any command in this
guide:

```bash
npx skills add sauljabin/agentskills
```

Check the installation:

```bash
skills --version
```

## Usage

### Add this repository

Install the skills from this repository. The CLI asks which skills and which
agents to install to:

```bash
skills add sauljabin/agentskills
```

See which skills the repository has without installing anything:

```bash
skills add sauljabin/agentskills --list
```

### Install only one skill

Pass `--skill` (or `-s`) with the skill name:

```bash
skills add sauljabin/agentskills --skill conventional-commits
```

Several at once:

```bash
skills add sauljabin/agentskills --skill kantrip kaskade
```

### Choose the scope and agent

Skills install into the current project by default. Use `-g` to install them
for your user instead, and `-a` to pick agents:

```bash
skills add sauljabin/agentskills --skill explain-simply -g
```

```bash
skills add sauljabin/agentskills --skill kantrip -a claude-code cursor
```

Install every skill to every agent without prompts:

```bash
skills add sauljabin/agentskills --all
```

### Manage installed skills

```bash
skills list
```

```bash
skills update
```

```bash
skills remove conventional-commits
```

Add `-g` to any of them to work on user-level skills.

## Repository layout

```text
skills/
  <skill-name>/
    SKILL.md          # Required: frontmatter (name, description) + instructions
    references/       # Optional: detail loaded only when needed
```

Each `name` in the frontmatter matches its folder name, as the specification
requires. Long reference material lives in `references/` so agents load it only
when a task needs it.

## License

This work is licensed under the
[Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/)
(CC BY 4.0). See [LICENSE](LICENSE).

## Links

- [skills.sh](https://www.skills.sh/): the open agent skills directory and CLI
- [agentskills.io](https://agentskills.io/): the Agent Skills specification
- [mcpservers.org agent skills](https://mcpservers.org/es/agent-skills): a catalog of agent skills
