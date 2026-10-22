# Installation

Employer Brand Auditor is a skills-only Claude Code plugin. It has no servers or scripts, and needs no API keys of its own.

## Prerequisites

- **Claude Code CLI**, installed and logged in. Every command below was tested with Claude Code **2.1.282** on macOS.

There are three ways to install:
- **Option A** installs permanently from GitHub. This is the recommended way.
- **Option B** loads the plugin from a local folder for one session.
- **Option C** installs permanently from a local folder.

## Option A — Install from GitHub (recommended)

Add the repository as a plugin marketplace:

```bash
claude plugin marketplace add denzjama/employer-brand-auditor
```

Install the plugin:

```bash
claude plugin install employer-brand-auditor@employer-brand-auditor
```

The plugin is installed at user scope and enabled in your Claude Code sessions. Start a new session to use it.

## Option B — Load for one session from a local folder

Get the plugin folder, either from a clone of the repository or from an unpacked release download. Then start Claude Code with it:

```bash
claude --plugin-dir /path/to/employer-brand-auditor
```

The folder is the one that contains `.claude-plugin/plugin.json`. `--plugin-dir` also accepts a `.zip` of that folder. The plugin is active only in that session; nothing is installed.

## Option C — Install permanently from a local folder

The plugin folder includes a single-plugin marketplace definition (`.claude-plugin/marketplace.json`). Add the folder as a marketplace, then install:

```bash
claude plugin marketplace add /path/to/employer-brand-auditor
```

```bash
claude plugin install employer-brand-auditor@employer-brand-auditor
```

Keep the folder where it is: the marketplace entry points to that path.

## Verify the installation

For Options A and C, list your installed plugins:

```bash
claude plugin list
```

Expected: `employer-brand-auditor@employer-brand-auditor`, version 0.3.1, status enabled.

Show what the plugin contains:

```bash
claude plugin details employer-brand-auditor@employer-brand-auditor
```

Expected: three skills, `career-content-review`, `employer-brand-audit` and `evp-stress-test`, and no agents, hooks or MCP servers.

For either option, run a first task in Claude Code, for example:

```text
Is this a strong EVP? "Grow with us and make an impact."
```

You should get an EVP verdict (STRONG / PROMISING BUT GENERIC / WEAK / NOT YET AN EVP) with the reasoning behind it. Then follow [`FIRST_RUN.md`](FIRST_RUN.md) for a full audit.

## Update

**Option B:** start Claude Code with `--plugin-dir` pointing to the new version of the folder.

**Options A and C:**
1. Option C only: replace the local folder with the new version, at the same path. For Option A, the marketplace reads the latest version from GitHub.
2. Refresh the marketplace, then update the plugin:

```bash
claude plugin marketplace update employer-brand-auditor
```

```bash
claude plugin update employer-brand-auditor@employer-brand-auditor
```

3. Restart Claude Code to apply the update. If the version has not changed, the update command reports that the plugin is already at the latest version.

## Disable, enable or uninstall (Options A and C)

Turn the plugin off without removing it:

```bash
claude plugin disable employer-brand-auditor@employer-brand-auditor
```

Turn it back on:

```bash
claude plugin enable employer-brand-auditor@employer-brand-auditor
```

Remove it:

```bash
claude plugin uninstall employer-brand-auditor@employer-brand-auditor
```

Optionally, remove the marketplace entry as well:

```bash
claude plugin marketplace remove employer-brand-auditor
```

**Option B** needs no uninstall: start Claude Code without `--plugin-dir`.

## If something goes wrong

See [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md).
