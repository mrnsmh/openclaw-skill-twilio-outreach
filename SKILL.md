---
name: twilio-outreach
description: Send SMS and WhatsApp messages (single or bulk) via Twilio, list inbox, and check message status.
license: MIT
metadata:
  version: 1.0.0
  author: Jack2
  tags: twilio, sms, whatsapp, outreach, messaging
---

# twilio-outreach

Send SMS and WhatsApp messages via Twilio — single sends, bulk CSV campaigns, inbox browsing, and delivery status checks.

## Setup

Set environment variables (or rely on hardcoded defaults for Marouane's account):

```bash
export TWILIO_ACCOUNT_SID="your_account_sid"
export TWILIO_AUTH_TOKEN="your_auth_token"
export TWILIO_FROM="+19302075190"  # Your Twilio number
```

Install dependency:
```bash
pip install twilio --break-system-packages
```

## Usage

```bash
# Send SMS
python3 scripts/twilio_send.py sms +212600000000 "Hello from Twilio!"

# Send WhatsApp
python3 scripts/twilio_send.py whatsapp +212600000000 "Hello via WhatsApp!"

# Bulk send from CSV (columns: phone, message, channel[optional])
python3 scripts/twilio_send.py bulk contacts.csv

# List recent inbox (default 20 messages)
python3 scripts/twilio_send.py inbox
python3 scripts/twilio_send.py inbox --limit 50

# Check message delivery status
python3 scripts/twilio_send.py status SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## CSV Format (bulk)

```csv
phone,message,channel
+212600000001,Bonjour depuis Twilio,sms
+212600000002,Salut via WhatsApp,whatsapp
```

If `channel` column is omitted, defaults to `sms`.

## Files

| File | Purpose |
|------|---------|
| `scripts/twilio_send.py` | Main CLI script |
| `references/twilio-api.md` | Twilio API quick reference & error codes |
