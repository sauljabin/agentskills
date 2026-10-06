# Kaskade settings reference

`settings.yaml` holds personal TUI preferences. It is separate from
`client.ini`, which holds connections.

Location, first match wins:

1. `$KASKADE_SETTINGS`
2. `$XDG_CONFIG_HOME/kaskade/settings.yaml`
3. `~/.config/kaskade/settings.yaml`

Invalid values produce an in-app warning; valid values still apply.

## Themes

Default is `eva01-berserk`. The original `eva01` and every Textual built-in
theme (for example `dracula`, `nord`, `gruvbox`) are available.

```yaml
theme: dracula
```

Precedence: `--theme NAME` on the command line, then `theme` in settings,
then `eva01-berserk`. Changing the theme from the command palette (`:`) lasts
only for the session.

## Custom themes

```yaml
theme: solarized-kaskade

themes:
  solarized-kaskade:
    primary: "#268BD2"
    secondary: "#2AA198"
    warning: "#B58900"
    error: "#DC322F"
    success: "#859900"
    accent: "#6C71C4"
    foreground: "#839496"
    background: "#002B36"
    surface: "#073642"
    panel: "#002B36"
    boost: "#0A4050"
    dark: true
```

- Only `primary` is required. Missing `secondary`, `warning`, and `accent`
  fall back to `primary`; `error` and `success` fall back to `secondary`.
- Set `dark: false` for a light theme.
- Quote hex colors: YAML treats an unquoted `#` as a comment.
- Colors may also be `rgb()`, `hsl()`, CSS names, or ANSI names such as
  `ansi_blue`.
- Names use lowercase letters, digits, and single hyphens. A custom theme can
  never replace a built-in name.

## Keymap

Values are Textual key names. Separate aliases with commas.

```yaml
keymap:
  app.quit: ctrl+c
  help.toggle: question_mark,f1
  kaskade.navigation.down: down,j
  kaskade.navigation.up: up,k
  kaskade.topics.filter: slash
  kaskade.topics.delete: D
```

Binding IDs:

| Context | IDs |
| --- | --- |
| Application | `app.quit`, `app.command-palette`, `help.toggle`, `kaskade.help.close` |
| Navigation | `kaskade.navigation.up`, `.down`, `.left`, `.right`, `.first`, `.last`, `.page-up`, `.page-down`, `.select` |
| Topics | `kaskade.topics.describe`, `.copy`, `.filter`, `.refresh`, `.create`, `.edit`, `.delete`, `.show-all` |
| Records | `kaskade.records.show`, `.copy`, `.export`, `.consume`, `.filter`, `.chunk-size`, `.show-all` |
| Record Details | `kaskade.record-details.previous`, `.next`, `.close` |
| Dialogs | `kaskade.filter-topics.apply`, `kaskade.delete-topic.confirm`, `kaskade.filter-records.apply`, `kaskade.chunk-size.select` |
| Editors | `kaskade.create-topic.save`, `kaskade.edit-topic.save` |

Keep shortcuts safe for tmux and Zellij. Unknown IDs or keys produce a warning
and the default binding stays.

## Admin auto-refresh

```yaml
admin:
  refresh-interval: 30
```

`0` disables it; other values must be at least 5 seconds. Override per run
with `kaskade admin --refresh-interval 10`. Auto-refresh pauses outside the
topic list. `Ctrl+R` refreshes now.

## Kantrip profile in the header

When `KANTRIP_PROFILE` is set (inside `kantrip exec`), the header shows
`profile · bootstrap-server`. It is display-only.
