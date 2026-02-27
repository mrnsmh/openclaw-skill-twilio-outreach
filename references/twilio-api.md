# Twilio API Reference

## Authentication
- **Account SID**: from Twilio Console → Dashboard
- **Auth Token**: from Twilio Console → Dashboard
- **Base URL**: `https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/`

## Key Endpoints

### Send Message
`POST /Accounts/{AccountSid}/Messages.json`
```
Body=Hello&From=+1XXX&To=+1YYY
```
Returns: `{ sid, status, from, to, body, date_sent, ... }`

### List Messages
`GET /Accounts/{AccountSid}/Messages.json?PageSize=20`

### Fetch Message
`GET /Accounts/{AccountSid}/Messages/{MessageSid}.json`

## Message Statuses
- `queued` → `sending` → `sent` → `delivered`
- `failed`, `undelivered` (check error_code)

## WhatsApp
- From: `whatsapp:+19302075190`
- To: `whatsapp:+212600000000`
- Sandbox: must opt-in first via WhatsApp join code

## CSV Bulk Format
```csv
phone,message,channel
+212600000001,Hello World,sms
+212600000002,Hi via WA,whatsapp
```

## Error Codes
| Code  | Meaning                     |
|-------|-----------------------------|
| 21211 | Invalid 'To' phone number   |
| 21408 | Permission denied for region|
| 30003 | Unreachable destination     |
| 30005 | Unknown destination handset |

## Docs
- https://www.twilio.com/docs/sms/api
- https://www.twilio.com/docs/whatsapp/api
