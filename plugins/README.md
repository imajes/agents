# Personal tools marketplace

`marketplace.json` is the permanent personal tools catalog for this machine. Its marketplace identity is `imajes`; keep that identity stable so installed plugin IDs remain valid.

Codex resolves this catalog from the marketplace root `/Users/james`. Every local `source.path` starts with `./` and resolves from that home directory, rather than from `.agents/plugins/`. Package sources can remain in their maintained repositories; adding a catalog entry does not require another source copy.

Mail Operations is installed as `mail-operations@imajes`. Its catalog entry points to `./Projects/sys-related/mail-operations/plugins/mail-operations`, the generated package in the maintained private repository. Run package validation in that repository before refreshing an installation. The installed cache is managed by Codex and must not become the authoring source.

Use the supported CLI to inspect or install from this catalog:

```zsh
codex plugin marketplace list --json
codex plugin list --marketplace imajes --available --json
codex plugin add mail-operations@imajes --json
```

The catalog is also explicitly registered with local source `/Users/james`. Other service/vendor marketplaces remain separate. The former standalone `james-mail-operations` registration was retired from this machine; its old plugin identity is disabled and its cache is preserved. The repository-local marketplace remains available for portable repository installation.

Keep existing plugin entries and in-progress source edits intact when maintaining this catalog. Check both the actual source path and the installed cache: an installed plugin can remain usable even when its authoring path has gone stale. Restart the desktop app when needed for it to pick up changed local plugin files or identity.

Format and path rules: [official OpenAI plugin packaging documentation](https://developers.openai.com/plugins/build/plugins#marketplace-metadata).
