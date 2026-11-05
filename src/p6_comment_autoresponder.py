#!/usr/bin/env python3
"""
Autonomous LinkedIn Comment Responder & Lead Watchdog for P6 AI Orchestrator
Monitors inbound comments on the P6 launch post, replies directly on the commenter's thread,
and delivers the direct SDLC PDF roadmap link while notifying Aamir via @AzGem_Bot.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime

STATE_DIR = "/home/ubuntu/projects/p6-ai-orchestrator/state"
POST_STATE_FILE = "/home/ubuntu/projects/p6-ai-orchestrator/output/posted_social_state.json"
REPLIED_FILE = os.path.join(STATE_DIR, "p6_replied_comments.json")
LOG_FILE = os.path.join(STATE_DIR, "p6_autoresponder.log")
TOKEN_FILE = "/home/ubuntu/linkedin_token.json"
TG_CHAT_ID = "8843884232" # @AzGem_Bot
PDF_LINK = "https://amz34.github.io/assets/P6_AI_Orchestrator_SDLC_Specification.pdf"

os.makedirs(STATE_DIR, exist_ok=True)

sys.path.insert(0, "/home/ubuntu/clients/invertio/multi-agent/tg-jobs")
try:
    from jobs_manager import read_bot_token, tg_call
except Exception:
    def read_bot_token(): return ""
    def tg_call(token, method, payload): return {}

def log_msg(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

def send_telegram_alert(commenter_name, comment_text, reply_text, post_url):
    token = read_bot_token()
    if not token:
        return False
    msg = (
        f"🎯 [LinkedIn Inbound P6 Lead Alert]\n\n"
        f"👤 Lead: {commenter_name}\n"
        f"💬 Comment: \"{comment_text}\"\n"
        f"⚡ Direct Thread Reply: \"{reply_text[:120]}...\"\n"
        f"📄 Delivered: {PDF_LINK}\n\n"
        f"🔗 Post: {post_url}"
    )
    try:
        res = tg_call(token, "sendMessage", {"chat_id": TG_CHAT_ID, "text": msg})
        return res.get("ok", False)
    except Exception as e:
        log_msg(f"Telegram alert error: {e}")
        return False

def get_li_token():
    with open(TOKEN_FILE) as f:
        return json.load(f).get("access_token")

def load_replied():
    if os.path.exists(REPLIED_FILE):
        try:
            with open(REPLIED_FILE, "r") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_replied(replied_set):
    with open(REPLIED_FILE, "w") as f:
        json.dump(list(replied_set), f, indent=2)

def generate_reply(commenter_name, comment_text):
    first_name = commenter_name.split()[0] if commenter_name else "there"
    text = comment_text.lower()
    
    if "p6" in text or "roadmap" in text or "pdf" in text or "send" in text or "blueprint" in text:
        return (
            f"Here is your direct access, {first_name}! 🚀\n\n"
            f"📄 SDLC Architecture & Knowledge Roadmap PDF: {PDF_LINK}\n\n"
            f"This covers the exact 5-level WBS synthesis, 100% DCMA 14-point audit rules, "
            f"and budget balancing engine. Check it out and let me know how it fits your current planning workflow!"
        )
    elif any(k in text for k in ["cost", "budget", "price", "license"]):
        return (
            f"Appreciate the question, {first_name}! For budget allocation, the agent balanced an exact "
            f"SAR 2,000,000 cost envelope with zero variance. You can inspect the entire financial framework "
            f"and monetization breakdown in Section 4 of the roadmap PDF: {PDF_LINK}"
        )
    elif any(k in text for k in ["cpm", "logic", "float", "dcma", "audit"]):
        return (
            f"Great technical inquiry, {first_name}. The logic graph enforces zero open ends (0.00% missing logic) "
            f"and propagates critical path float with 100% compliance on all 14 DCMA checks. "
            f"Full verification matrix is detailed in the PDF: {PDF_LINK}"
        )
    else:
        return (
            f"Thanks for joining the conversation, {first_name}! "
            f"If you'd like to inspect the complete 3-page SDLC Architecture Specification & Knowledge Roadmap, "
            f"here is the direct link: {PDF_LINK} — curious to hear your take on autonomous scheduling!"
        )

def reply_to_comment_api(post_urn, comment_urn, reply_text, author_urn):
    """Replies directly to the specific comment thread."""
    tok = get_li_token()
    encoded_post = urllib.parse.quote(post_urn, safe="")
    url = f"https://api.linkedin.com/v2/socialActions/{encoded_post}/comments"
    payload = {
        "actor": author_urn,
        "message": {"text": reply_text},
        "parentComment": comment_urn
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json", "X-Restli-Protocol-Version": "2.0.0"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as r:
            res = json.loads(r.read())
            return True, res.get("id")
    except Exception as e:
        return False, str(e)

def check_and_respond_once():
    if not os.path.exists(POST_STATE_FILE):
        log_msg("Post state file not found yet.")
        return 0
        
    with open(POST_STATE_FILE) as f:
        pstate = json.load(f)
        
    post_urn = pstate.get("linkedin", {}).get("post_urn")
    post_url = pstate.get("linkedin", {}).get("url")
    if not post_urn:
        log_msg("No LinkedIn post URN recorded.")
        return 0
        
    tok = get_li_token()
    encoded_post = urllib.parse.quote(post_urn, safe="")
    url = f"https://api.linkedin.com/v2/socialActions/{encoded_post}/comments"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {tok}", "X-Restli-Protocol-Version": "2.0.0"}
    )
    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
    except Exception as e:
        log_msg(f"Could not fetch comments via API: {e}")
        return 0
        
    replied = load_replied()
    elements = data.get("elements", [])
    author_urn = "urn:li:person:ZXkhXV9MAp"
    responded_count = 0
    
    for c in elements:
        c_id = c.get("$URN") or c.get("id")
        actor = c.get("actor")
        # Ignore our own comments
        if actor == author_urn or c_id in replied:
            continue
            
        comment_text = c.get("message", {}).get("text", "")
        commenter_name = "Planning Colleague"
        
        reply_body = generate_reply(commenter_name, comment_text)
        log_msg(f"Responding to comment {c_id}: \"{comment_text[:60]}...\"")
        
        ok, res = reply_to_comment_api(post_urn, c_id, reply_body, author_urn)
        if ok:
            log_msg(f"Successfully posted threaded reply: {res}")
            replied.add(c_id)
            save_replied(replied)
            send_telegram_alert(commenter_name, comment_text, reply_body, post_url)
            responded_count += 1
        else:
            log_msg(f"Failed to post threaded reply: {res}")
            
    return responded_count

if __name__ == "__main__":
    log_msg("P6 Comment Autoresponder initialized.")
    if "--once" in sys.argv:
        cnt = check_and_respond_once()
        log_msg(f"Single pass completed: {cnt} responses sent.")
    else:
        log_msg("Entering polling daemon loop (60s interval)...")
        while True:
            try:
                check_and_respond_once()
            except Exception as e:
                log_msg(f"Loop error: {e}")
            time.sleep(60)
