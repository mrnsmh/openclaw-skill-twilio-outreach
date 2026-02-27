#!/usr/bin/env python3
"""
twilio_send.py - Twilio SMS/WhatsApp outreach CLI
Usage:
  python3 twilio_send.py sms <phone> "<message>"
  python3 twilio_send.py whatsapp <phone> "<message>"
  python3 twilio_send.py bulk <contacts.csv>
  python3 twilio_send.py inbox [--limit 20]
  python3 twilio_send.py status <MESSAGE_SID>
"""

import os
import sys
import csv
import argparse
from twilio.rest import Client

ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.environ.get("TWILIO_FROM", "+19302075190")

if not ACCOUNT_SID or not AUTH_TOKEN:
    print("[ERROR] Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables.", file=sys.stderr)
    sys.exit(1)

client = Client(ACCOUNT_SID, AUTH_TOKEN)


def send_sms(to: str, body: str):
    msg = client.messages.create(body=body, from_=FROM_NUMBER, to=to)
    print(f"[SMS] SID={msg.sid}  status={msg.status}  to={to}")
    return msg.sid


def send_whatsapp(to: str, body: str):
    wa_from = f"whatsapp:{FROM_NUMBER}"
    wa_to   = f"whatsapp:{to}"
    msg = client.messages.create(body=body, from_=wa_from, to=wa_to)
    print(f"[WhatsApp] SID={msg.sid}  status={msg.status}  to={to}")
    return msg.sid


def send_bulk(csv_path: str):
    if not os.path.exists(csv_path):
        print(f"[ERROR] File not found: {csv_path}", file=sys.stderr)
        sys.exit(1)
    results = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            phone   = row.get("phone", "").strip()
            message = row.get("message", "").strip()
            channel = row.get("channel", "sms").strip().lower()
            if not phone or not message:
                print(f"[SKIP] Empty phone or message: {row}")
                continue
            try:
                if channel == "whatsapp":
                    sid = send_whatsapp(phone, message)
                else:
                    sid = send_sms(phone, message)
                results.append({"phone": phone, "sid": sid, "status": "sent"})
            except Exception as e:
                print(f"[ERROR] {phone}: {e}")
                results.append({"phone": phone, "sid": None, "status": "failed"})
    print(f"\n[Bulk] Done: {len(results)} processed")


def list_inbox(limit: int = 20):
    messages = client.messages.list(limit=limit)
    if not messages:
        print("No messages found.")
        return
    print(f"{'SID':<35} {'From':<20} {'To':<20} {'Status':<12} {'Date'}")
    print("-" * 110)
    for m in messages:
        print(f"{m.sid:<35} {m.from_:<20} {m.to:<20} {m.status:<12} {m.date_sent}")


def check_status(sid: str):
    try:
        msg = client.messages(sid).fetch()
        print(f"SID     : {msg.sid}")
        print(f"Status  : {msg.status}")
        print(f"From    : {msg.from_}")
        print(f"To      : {msg.to}")
        print(f"Body    : {msg.body}")
        print(f"Sent    : {msg.date_sent}")
        print(f"Updated : {msg.date_updated}")
        if msg.error_code:
            print(f"Error   : [{msg.error_code}] {msg.error_message}")
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Twilio SMS/WhatsApp outreach CLI")
    sub = parser.add_subparsers(dest="command")

    # sms
    p_sms = sub.add_parser("sms", help="Send SMS")
    p_sms.add_argument("phone", help="Destination phone (+E.164)")
    p_sms.add_argument("message", help="Message text")

    # whatsapp
    p_wa = sub.add_parser("whatsapp", help="Send WhatsApp message")
    p_wa.add_argument("phone", help="Destination phone (+E.164)")
    p_wa.add_argument("message", help="Message text")

    # bulk
    p_bulk = sub.add_parser("bulk", help="Send from CSV (columns: phone, message[, channel])")
    p_bulk.add_argument("csv", help="Path to CSV file")

    # inbox
    p_inbox = sub.add_parser("inbox", help="List recent messages")
    p_inbox.add_argument("--limit", type=int, default=20)

    # status
    p_status = sub.add_parser("status", help="Check message status")
    p_status.add_argument("sid", help="Message SID")

    args = parser.parse_args()

    if args.command == "sms":
        send_sms(args.phone, args.message)
    elif args.command == "whatsapp":
        send_whatsapp(args.phone, args.message)
    elif args.command == "bulk":
        send_bulk(args.csv)
    elif args.command == "inbox":
        list_inbox(args.limit)
    elif args.command == "status":
        check_status(args.sid)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
