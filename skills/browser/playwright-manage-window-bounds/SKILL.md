---
name: playwright-manage-window-bounds
description: Set and restore real Chrome window bounds in headed Playwright sessions
  via CDP rather than emulated viewport resizing. Use for responsive breakpoint checks,
  reproducing user-resized browser issues, and returning sessions to manually resizable
  windows after scripted tests.
---

# Playwright Window Bounds

## Overview

Use this skill to resize the actual Chrome window through DevTools Protocol (`Browser.setWindowBounds`) while keeping a headed Playwright session.
Prefer this over Playwright viewport emulation when you need behavior that matches manual browser resizing.

## Prerequisites

- Use a named Playwright CLI session.
- Keep the browser headed (`--headed`).
- Use `run-code` with a function expression: `async (page) => { ... }`.

Set once in shell:

```bash
export AGENTS_SKILLS_HOME="${AGENTS_SKILLS_HOME:-$HOME/.agents/skills}"
export PWCLI="$AGENTS_SKILLS_HOME/browser/playwright-automate-browser/scripts/playwright_cli.sh"
export PLAYWRIGHT_CLI_SESSION="smokeclouds-bridge"
```

## Quick Start

1. Capture current browser/window dimensions (baseline).

```bash
"$PWCLI" --session "$PLAYWRIGHT_CLI_SESSION" eval \
"JSON.stringify({innerWidth: window.innerWidth, innerHeight: window.innerHeight, outerWidth: window.outerWidth, outerHeight: window.outerHeight})"
```

2. Resize real Chrome window using CDP.

```bash
"$PWCLI" --session "$PLAYWRIGHT_CLI_SESSION" run-code \
"async (page) => {
  const cdp = await page.context().newCDPSession(page);
  const info = await cdp.send('Browser.getWindowForTarget');
  await cdp.send('Browser.setWindowBounds', {
    windowId: info.windowId,
    bounds: { width: 1420, height: 980 }
  });
  await page.waitForTimeout(150);
  return await page.evaluate(() => ({
    innerWidth: window.innerWidth,
    innerHeight: window.innerHeight,
    outerWidth: window.outerWidth,
    outerHeight: window.outerHeight
  }));
}"
```

3. Reload and validate at that size.

```bash
"$PWCLI" --session "$PLAYWRIGHT_CLI_SESSION" reload
"$PWCLI" --session "$PLAYWRIGHT_CLI_SESSION" screenshot
```

4. Restore baseline size when done.

## Standard Workflow

1. Record baseline `outerWidth/outerHeight` and `innerWidth/innerHeight`.
2. Resize using `Browser.setWindowBounds`.
3. Run checks (reload/screenshot/snapshot).
4. Restore baseline before handing control back.

If a user needs manual resizing, always return to a normal window-driven session state after scripted checks.

## Keep Manual Resizing Available

If viewport emulation was previously forced, reopen with `viewport: null`.

`/tmp/playwright-browser-windowed.json`:

```json
{
  "browser": {
    "launchOptions": {
      "headless": false,
      "channel": "chrome"
    },
    "contextOptions": {
      "viewport": null
    }
  }
}
```

Reopen command:

```bash
"$PWCLI" --session "$PLAYWRIGHT_CLI_SESSION" close
"$PWCLI" --session "$PLAYWRIGHT_CLI_SESSION" open "http://localhost:4321/" --headed --config /tmp/playwright-browser-windowed.json
```

## Troubleshooting

- `run-code` throws syntax errors:
  Use `async (page) => { ... }`, not raw statements.
- Size change seems ignored:
  Confirm a headed Chrome session and use CDP `Browser.setWindowBounds`.
- Window exists but wrong page:
  Navigate explicitly with `open`/`goto`, then `reload`.
- Need proof of applied size:
  Return both `inner*` and `outer*` values via `eval` or `run-code`.
