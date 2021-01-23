# Github Webhook processor

prerequisites: Flask and dotenv

Accepts `push` webhooks from github, checkes the message integrity, 
and does the action in ./action.py

## Configuration
in `action.py`:

| variable | Type | Purpose |
| ---- | ---- | ----|
| `actions` | an array of functions | An array of actions to be run |
| `secret`  | `string` | the secret configured at github |
| `ref`     | `string` | the ref to only do the action when a specific event happened |
| `event`   | `string` | the event that is supposed to be listened to |

reference:
`https://docs.github.com/en/developers/webhooks-and-events/webhook-events-and-payloads#push`
