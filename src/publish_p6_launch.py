#!/usr/bin/env python3
"""
Publish Autonomous Primavera P6 AI Launch to LinkedIn and Bluesky,
and launch the Auto-Comment Responder daemon.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
import urllib.parse
import subprocess

# Paths & Config
TOKEN_FILE = "/home/ubuntu/linkedin_token.json"
VIDEO_PATH = "/home/ubuntu/projects/p6-ai-orchestrator/output/Autonomous_P6_AI_Showcase_Production.mp4"
BASE_URL = "https://api.linkedin.com"
API_VERSION = "202604"
STATE_FILE = "/home/ubuntu/projects/p6-ai-orchestrator/output/posted_social_state.json"

LINKEDIN_POST_TEXT = """Most project controls teams across megaproject construction are spending 7 to 21 days doing work an AI model can execute in 10 minutes.

The industry accepted a slow, error-prone manual workflow:
• Staring at massive BOQs and complex contract terms
• Manually drafting 80+ activities in Excel
• Hacking XER files and wrestling broken CPM logic
• Fixing missing predecessors and dangling open-ends
• Spending all weekend drafting a 10-page Schedule Narrative Report

Here is the architectural reality:

We connected Google Gemini and Antigravity directly to Oracle Primavera P6 using the Model Context Protocol (P6-MCP).

No Excel imports. No XER patching. Direct database injection.

In under 10 minutes, the agent:
1. Built a 5-level WBS structure
2. Synthesized 85 activities with floor-by-floor sequencing
3. Linked 122 finish-to-start relationships with 0.0% open ends
4. Loaded 383 resource assignments balancing an exact SAR 2,000,000 budget
5. Passed 14/14 checks on the DCMA 14-Point Quality Assessment
6. Generated an executive 10-page Schedule Narrative Report in 180 seconds

The planner simply pressed F5 to refresh the database and F9 to run CPM calculations.

Watch the 35-second demo video below to see it live.

Want to deploy this architecture or inspect the benchmark blueprint?

👇 Drop a comment with 'P6' below (or DM me 'P6') and I'll send you:
1. The complete 3-page SDLC Architecture Specification & Benchmark PDF
2. The step-by-step Knowledge Roadmap to build your own P6-MCP agent

Link to the full PDF and repo is also in the first comment 👇

#ProjectControls #PrimaveraP6 #ConstructionManagement #AI #Gemini #DigitalTransformation #SaudiArabia #Vision2030 #Planning"""

LINKEDIN_FIRST_COMMENT = """Direct Architecture PDF & Open Engine Links:
📄 Download the SDLC Specification PDF: https://amz34.github.io/assets/P6_AI_Orchestrator_SDLC_Specification.pdf
⚡ Engine Repository: https://github.com/shamshirialireza/P6-MCP
📦 Kaggle Construction Benchmark: https://www.kaggle.com/datasets/mohamedelkenawy/primavera-p6-dashboard-dataset

Curious for planning directors & EPC project controls managers:
How much time is your team currently losing every month on baseline revisions and schedule narrative reporting? Drop your thoughts below!"""

BLUESKY_POST_TEXT = """Building a full Primavera P6 baseline used to take 7 days.

With Gemini + P6-MCP, we built 85 activities, 122 logic links, balanced SAR 2M, and passed 14/14 DCMA checks in under 10 mins.

Spec PDF: https://amz34.github.io/assets/P6_AI_Orchestrator_SDLC_Specification.pdf

#ProjectControls #AI #DevOps"""

def get_li_token():
    with open(TOKEN_FILE) as f:
        d = json.load(f)
        return d.get("access_token") or d.get("token")

def li_call(method, url, body=None, extra=None):
    data = json.dumps(body).encode() if body is not None else None
    h = {
        "Authorization": "Bearer " + get_li_token(),
        "LinkedIn-Version": API_VERSION,
        "X-Restli-Protocol-Version": "2.0.0"
    }
    if data:
        h["Content-Type"] = "application/json"
    if extra:
        h.update(extra)
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read()
            parsed = {}
            if raw and raw.strip():
                parsed = json.loads(raw) if raw[:1] in b"{[" else raw.decode(errors="replace")
            return r.status, parsed, r.headers
    except urllib.error.HTTPError as e:
        raw = e.read()
        err_msg = raw.decode(errors="replace")[:600]
        return e.code, err_msg, e.headers

def upload_linkedin_video(owner):
    size = os.path.getsize(VIDEO_PATH)
    print(f"[*] Initializing LinkedIn Video Upload ({size} bytes)...")
    s, d, _ = li_call("POST", BASE_URL + "/rest/videos?action=initializeUpload", {
        "initializeUploadRequest": {
            "owner": owner,
            "fileSizeBytes": size,
            "uploadCaptions": False,
            "uploadThumbnail": False
        }
    })
    if s not in (200, 201):
        raise RuntimeError(f"initializeUpload failed ({s}): {d}")
        
    v = d["value"]
    urn = v["video"]
    token = v["uploadToken"]
    print(f"[*] Video URN Allocated: {urn}")
    
    blob = open(VIDEO_PATH, "rb").read()
    parts = []
    for ins in v["uploadInstructions"]:
        first, last = int(ins["firstByte"]), int(ins["lastByte"])
        chunk = blob[first:last + 1]
        print(f"[*] Uploading part {first}-{last} ({len(chunk)} bytes)...")
        req = urllib.request.Request(ins["uploadUrl"], data=chunk, method="PUT", headers={"Content-Type": "application/octet-stream"})
        with urllib.request.urlopen(req, timeout=300) as r:
            if r.status not in (200, 201):
                raise RuntimeError(f"Part upload failed with status {r.status}")
            etag = r.headers.get("ETag") or r.headers.get("etag")
            print(f"[*] Uploaded part {first}-{last}, ETag: {etag[:40]}...")
            parts.append(etag)
        
    s, d, _ = li_call("POST", BASE_URL + "/rest/videos?action=finalizeUpload", {
        "finalizeUploadRequest": {
            "video": urn,
            "uploadToken": token,
            "uploadedPartIds": parts
        }
    })
    print(f"[*] Video Finalize Upload ({s}): {d}")
    
    # Wait until ready
    print("[*] Waiting for video processing (max 180s)...")
    t0 = time.time()
    while time.time() - t0 < 180:
        s, d, _ = li_call("GET", BASE_URL + "/rest/videos/" + urllib.parse.quote(urn, safe=""))
        status = (d.get("status") if isinstance(d, dict) else "") or ""
        print(f"    Status: {status}")
        if status in ("AVAILABLE", "PROCESSING_COMPLETE"):
            return urn
        time.sleep(5)
    return urn

def publish_linkedin_post(owner, video_urn):
    print("[*] Creating LinkedIn Post with Video...")
    body = {
        "author": owner,
        "commentary": LINKEDIN_POST_TEXT,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
        "content": {
            "media": {
                "id": video_urn,
                "title": "Autonomous Primavera P6 AI Baseline Automation"
            }
        }
    }
    s, d, headers = li_call("POST", BASE_URL + "/rest/posts", body)
    print(f"[*] Post Creation Status: {s}")
    post_urn = headers.get("x-restli-id") or headers.get("X-Restli-Id") or ""
    if not post_urn and isinstance(d, dict):
        post_urn = d.get("id") or ""
    print(f"[*] Captured Post URN: {post_urn}")
    return s, post_urn, d

def post_linkedin_first_comment(post_urn, owner):
    print(f"[*] Posting First Comment to LinkedIn Post {post_urn}...")
    encoded_urn = urllib.parse.quote(post_urn, safe="")
    url = f"{BASE_URL}/v2/socialActions/{encoded_urn}/comments"
    body = {
        "actor": owner,
        "message": {"text": LINKEDIN_FIRST_COMMENT}
    }
    s, d, _ = li_call("POST", url, body)
    print(f"[*] First Comment Status ({s}): {d}")
    return s, d

def publish_bluesky():
    print("\n--- BLUESKY POST ---")
    sys.path.append("/home/ubuntu/ops/github/growth")
    try:
        import publish_post
        res = publish_post.post_bluesky(BLUESKY_POST_TEXT)
        print(f"[*] Bluesky Response: {res}")
        return res
    except Exception as e:
        print(f"[-] Bluesky Publish Error: {e}")
        return {"ok": False, "error": str(e)}

def main():
    # 1. Get LinkedIn Owner
    s, d, _ = li_call("GET", BASE_URL + "/v2/userinfo")
    if s != 200:
        print(f"[-] LinkedIn userinfo failed: {s} {d}")
        sys.exit(1)
    owner = "urn:li:person:" + d["sub"]
    name = d.get("name")
    print(f"[*] Authenticated as: {name} ({owner})")
    
    # 2. Upload Video
    video_urn = upload_linkedin_video(owner)
    print(f"[+] Video ready for attachment: {video_urn}")
    
    # 3. Publish LinkedIn Post
    post_status, post_urn, post_resp = publish_linkedin_post(owner, video_urn)
    print(f"[+] LinkedIn Post Result: status={post_status}, urn={post_urn}")
    
    # 4. Post First Comment
    if post_urn:
        post_linkedin_first_comment(post_urn, owner)
        
    # 5. Publish to Bluesky
    bsky_res = publish_bluesky()
    
    # Save State
    state = {
        "timestamp": time.time(),
        "linkedin": {
            "status": post_status,
            "post_urn": post_urn,
            "video_urn": video_urn,
            "url": f"https://www.linkedin.com/feed/update/{post_urn}" if post_urn else ""
        },
        "bluesky": bsky_res
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
    print(f"[+] Social state written to {STATE_FILE}")

if __name__ == "__main__":
    main()
