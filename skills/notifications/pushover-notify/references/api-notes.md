# Pushover API Notes

## Limits enforced by the helper

- `message`: 1024 characters
- `title`: 250 characters
- `url`: 512 characters
- `url_title`: 100 characters

The helper counts Python Unicode characters for these limits before sending the request.

## Formatting supported by the helper

- `--html` sets `html=1`
- `--monospace` sets `monospace=1`
- These modes are mutually exclusive
- Common HTML tags documented by Pushover include `<b>`, `<i>`, `<u>`, and `<font color="#rrggbb">`
- Pushover strips HTML and monospace formatting from the immediate mobile notification and renders the formatting after the device client opens and syncs the message

## Friendly API behavior encoded in the helper

- The helper does not auto-retry requests
- `4xx` responses are treated as non-retryable until the payload, quota, or credentials change
- `5xx` responses and transport failures are treated as temporary; wait at least 5 seconds before retrying
- The helper is a single-request CLI, so it naturally stays far below Pushover's guidance to avoid more than 2 concurrent requests

## Useful options

- `--priority`: pass one of `-2`, `-1`, `0`, `1`, `2`
- `--sound`: override the default sound, defaulting here to `pushover`
- `--url` and `--url-title`: add a supplementary link beneath the message
- `--ttl`: set message time-to-live in seconds
- `--timestamp`: override the displayed message time
- `--device`: target a specific device name

## Suggested usage patterns

- Use arguments for short one-line notifications
- Pipe stdin for multiline reports or command output
- Use `--dry-run` during development to confirm the payload shape and lengths without sending a notification
