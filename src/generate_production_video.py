#!/usr/bin/env python3
"""
Production Video Generator for Autonomous Primavera P6 AI
Generates 1080p video with neural voiceover, large kinetic CC subtitles, and multi-scene visual montage.
"""

import os
import sys
import subprocess
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = "/home/ubuntu/projects/p6-ai-orchestrator/output"
ASSETS_DIR = "/home/ubuntu/projects/p6-ai-orchestrator/output/video_assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

FONT_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REG_FONT_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

def get_font(size, bold=True):
    path = FONT_PATH if bold else REG_FONT_PATH
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def draw_header(draw, title_text, category="AUTONOMOUS PROJECT CONTROLS AI"):
    # Header ribbon
    draw.rectangle([(0, 0), (1920, 110)], fill=(15, 23, 42))
    draw.line([(0, 110), (1920, 110)], fill=(2, 132, 199), width=4)
    
    font_cat = get_font(22, bold=True)
    font_brand = get_font(20, bold=False)
    draw.text((60, 22), category, font=font_cat, fill=(56, 189, 248))
    draw.text((1420, 22), "ANTIGRAVITY x GEMINI 3.8", font=font_brand, fill=(148, 163, 184))
    
    font_title = get_font(34, bold=True)
    draw.text((60, 56), title_text, font=font_title, fill=(255, 255, 255))

def draw_footer(draw, cta="LINK IN FIRST COMMENT 👇"):
    # Footer ribbon
    draw.rectangle([(0, 970), (1920, 1080)], fill=(15, 23, 42))
    draw.line([(0, 970), (1920, 970)], fill=(30, 58, 138), width=3)
    
    font_cta = get_font(26, bold=True)
    font_info = get_font(20, bold=False)
    draw.text((60, 1010), "ORACLE PRIMAVERA P6 + MCP MESH", font=font_info, fill=(148, 163, 184))
    draw.text((1450, 1010), cta, font=font_cta, fill=(255, 230, 0))

def create_scene_1():
    # Hook / Title Slide
    img = Image.new("RGB", (1920, 1080), color=(10, 15, 30))
    draw = ImageDraw.Draw(img)
    
    # Background subtle grid / glow
    for y in range(0, 1080, 60):
        draw.line([(0, y), (1920, y)], fill=(20, 30, 55), width=1)
    for x in range(0, 1920, 60):
        draw.line([(x, 0), (x, 1080)], fill=(20, 30, 55), width=1)
        
    draw_header(draw, "THE FUTURE OF MEGAPROJECT PLANNING")
    draw_footer(draw, "POWERED BY ANTIGRAVITY & GEMINI")
    
    # Main Hero Box
    draw.rounded_rectangle([(140, 200), (1780, 880)], radius=20, fill=(15, 23, 42, 230), outline=(2, 132, 199), width=3)
    
    font_hero_pre = get_font(32, bold=True)
    font_hero = get_font(74, bold=True)
    font_hero_sub = get_font(36, bold=False)
    
    draw.text((220, 270), "TIRED OF SPENDING 7 DAYS DRAFTING A P6 BASELINE?", font=font_hero_pre, fill=(255, 230, 0))
    draw.text((220, 340), "BUILD FULL P6 BASELINES IN 10 MINS", font=font_hero, fill=(255, 255, 255))
    draw.text((220, 440), "Zero Excel Imports • Direct MCP Database Injection • 100% DCMA Compliance", font=font_hero_sub, fill=(56, 189, 248))
    
    # 4 Metric Cards inside Hero
    metrics = [
        ("98.2%", "SPEEDUP", (2, 132, 199)),
        ("14/14", "DCMA AUDIT", (34, 197, 94)),
        ("SAR 2.0M", "BUDGET BALANCED", (245, 158, 11)),
        ("3 MINS", "NARRATIVE REPORT", (168, 85, 247))
    ]
    card_w = 340
    card_gap = 40
    start_x = 220
    card_y = 540
    for i, (val, lbl, col) in enumerate(metrics):
        cx = start_x + i * (card_w + card_gap)
        draw.rounded_rectangle([(cx, card_y), (cx + card_w, card_y + 240)], radius=14, fill=(30, 41, 59), outline=col, width=2)
        draw.text((cx + 30, card_y + 40), val, font=get_font(48, bold=True), fill=col)
        draw.text((cx + 30, card_y + 130), lbl, font=get_font(22, bold=True), fill=(255, 255, 255))
        draw.text((cx + 30, card_y + 175), "Class-A Automated", font=get_font(18, bold=False), fill=(148, 163, 184))
        
    img.save(f"{ASSETS_DIR}/scene_01.jpg", quality=95)
    print("Created Scene 1")

def create_scene_2():
    # Direct P6 Injection Slide
    img = Image.new("RGB", (1920, 1080), color=(10, 15, 30))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "DIRECT ORACLE PRIMAVERA P6 DATABASE INJECTION")
    draw_footer(draw, "NO EXCEL • NO XER EXPORT HACKS")
    
    # Left Box: Code & MCP terminal
    draw.rounded_rectangle([(80, 160), (840, 920)], radius=14, fill=(15, 23, 42), outline=(56, 189, 248), width=2)
    draw.text((120, 200), "AGENTIC ORCHESTRATION PIPELINE", font=get_font(26, bold=True), fill=(255, 230, 0))
    
    terminal_logs = [
        "[INFO] Gemini 3.8: Ingesting BOQ & Sequencing Logic...",
        "[INFO] Connecting to P6 via Model Context Protocol (MCP)",
        "[EXEC] P6-MCP: Creating WBS Nodes (5 Levels)",
        "[EXEC] P6-MCP: Injecting 85 Construction Activities",
        "[EXEC] P6-MCP: Connecting 122 Logic Relationships (FS/SS)",
        "[EXEC] P6-MCP: Assigning 383 Resources & Balancing Budget",
        "[SUCCESS] Total Target Cost: SAR 2,000,000.00 (EXACT)",
        "--------------------------------------------------",
        ">> Planner Action: Press [F5] to Refresh Database",
        ">> Planner Action: Press [F9] to Run CPM Schedule Calc",
        ">> CPM Schedule Completed in 0.84 seconds!"
    ]
    font_mono = get_font(19, bold=False)
    for i, line in enumerate(terminal_logs):
        col = (34, 197, 94) if "SUCCESS" in line or "Completed" in line else (255, 255, 255)
        if "Action:" in line:
            col = (255, 230, 0)
        draw.text((120, 280 + i * 50), line, font=font_mono, fill=col)
        
    # Right Box: Real Primavera P6 Screenshot frame
    frame_path = "/tmp/p6_frames/frame_005.jpg"
    if os.path.exists(frame_path):
        p6_img = Image.open(frame_path)
        p6_img = p6_img.resize((960, 760))
        img.paste(p6_img, (880, 160))
        # Draw frame border
        draw.rounded_rectangle([(880, 160), (1840, 920)], radius=4, outline=(2, 132, 199), width=3)
    
    img.save(f"{ASSETS_DIR}/scene_02.jpg", quality=95)
    print("Created Scene 2")

def create_scene_3():
    # Real Kaggle Dataset & Cost Envelope
    img = Image.new("RGB", (1920, 1080), color=(10, 15, 30))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "REAL MEGAPROJECT DATASET (KAGGLE & LIVE EPC BENCHMARKS)")
    draw_footer(draw, "GROUNDED ON REAL COMMERCIAL CONTRACTS")
    
    # Left: Kaggle Dataset breakdown
    draw.rounded_rectangle([(80, 160), (920, 920)], radius=14, fill=(15, 23, 42), outline=(245, 158, 11), width=2)
    draw.text((120, 200), "KAGGLE BENCHMARK: PCS_PJ01 (CASA TOWER)", font=get_font(26, bold=True), fill=(255, 230, 0))
    
    kaggle_details = [
        ("WBS Hierarchy:", "5 Main Levels (Civil, MEP, Finishes, Handover)"),
        ("Trade Scope [Civil]:", "Foundations, Retaining Walls, Suspended Slabs"),
        ("Trade Scope [MEP]:", "Drainage, Firefighting, HVAC, Cable Trays"),
        ("Trade Scope [Finishes]:", "Masonry, Cladding, Glazing, Ceilings"),
        ("Total Schedule Scope:", "119 Live Project Activities (August Update)"),
        ("Budget Envelope:", "SAR 2,000,000 Total Baseline Allocation"),
        ("Currency & Calendar:", "SAR (Saudi Riyal) • Standard 6-Day Workweek")
    ]
    for i, (k, v) in enumerate(kaggle_details):
        draw.text((120, 280 + i * 80), k, font=get_font(22, bold=True), fill=(56, 189, 248))
        draw.text((120, 315 + i * 80), v, font=get_font(20, bold=False), fill=(255, 255, 255))
        
    # Right: Real P6 Activity table frame
    frame_path = "/tmp/p6_frames/frame_006.jpg"
    if os.path.exists(frame_path):
        p6_img = Image.open(frame_path).resize((880, 760))
        img.paste(p6_img, (960, 160))
        draw.rounded_rectangle([(960, 160), (1840, 920)], radius=4, outline=(245, 158, 11), width=3)
        
    img.save(f"{ASSETS_DIR}/scene_03.jpg", quality=95)
    print("Created Scene 3")

def create_scene_4():
    # DCMA 14-Point Quality Gate & S-Curve Slide
    img = Image.new("RGB", (1920, 1080), color=(10, 15, 30))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "AUTOMATED DCMA 14-POINT QUALITY GATE & S-CURVE")
    draw_footer(draw, "100% COMPLIANT • READY FOR CLIENT SUBMISSION")
    
    # Left: DCMA Audit Table
    draw.rounded_rectangle([(80, 160), (960, 920)], radius=14, fill=(15, 23, 42), outline=(34, 197, 94), width=2)
    draw.text((120, 200), "DCMA 14-POINT COMPLIANCE AUDIT", font=get_font(26, bold=True), fill=(34, 197, 94))
    
    dcma_checks = [
        ("1. Logic Integrity", "0.00% Missing (0 Tasks)", "PASS"),
        ("2. Leads Check", "0 Leads Detected", "PASS"),
        ("3. Lags Check", "0.00% Controlled Lags", "PASS"),
        ("4. Relationship Types", "93.48% Finish-to-Start", "PASS"),
        ("5. Hard Constraints", "0.00% Zero Hard Locks", "PASS"),
        ("6. High Float", "0.00% High Float", "PASS"),
        ("7. Negative Float", "0 Negative Float", "PASS"),
        ("8. High Duration", "0.00% Duration Outliers", "PASS"),
        ("10. Resources Loaded", "100% All Tasks Resourced", "PASS"),
        ("12. Critical Path Test", "Delay Propagated (120h)", "PASS")
    ]
    for i, (metric, val, res) in enumerate(dcma_checks):
        draw.text((120, 270 + i * 55), metric, font=get_font(20, bold=True), fill=(255, 255, 255))
        draw.text((540, 270 + i * 55), val, font=get_font(18, bold=False), fill=(148, 163, 184))
        draw.text((860, 270 + i * 55), res, font=get_font(20, bold=True), fill=(34, 197, 94))
        
    # Right: Real P6 S-Curve & Cumulative cost histogram frame
    frame_path = "/tmp/p6_frames/frame_007.jpg"
    if os.path.exists(frame_path):
        p6_img = Image.open(frame_path).resize((840, 760))
        img.paste(p6_img, (1000, 160))
        draw.rounded_rectangle([(1000, 160), (1840, 920)], radius=4, outline=(34, 197, 94), width=3)
        
    img.save(f"{ASSETS_DIR}/scene_04.jpg", quality=95)
    print("Created Scene 4")

def create_scene_5():
    # 10-Page Narrative Report Slide
    img = Image.new("RGB", (1920, 1080), color=(10, 15, 30))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "10-PAGE SCHEDULE NARRATIVE REPORT (PDF)")
    draw_footer(draw, "GENERATED FROM LIVE P6 CPM DATA IN 3 MINUTES")
    
    # Left: Narrative Report Features
    draw.rounded_rectangle([(80, 160), (960, 920)], radius=14, fill=(15, 23, 42), outline=(168, 85, 247), width=2)
    draw.text((120, 200), "EXECUTIVE CONTRACTOR-READY DELIVERABLE", font=get_font(26, bold=True), fill=(255, 230, 0))
    
    features = [
        ("Executive Summary:", "High-level milestones, critical path, budget status"),
        ("EVM Analytics:", "CPI, SPI, EAC, and monthly planned value curve"),
        ("Resource Histograms:", "Manpower, equipment hours, peak staffing dates"),
        ("Critical Path Floats:", "Driving path analysis & near-critical sensitivity"),
        ("Delay Prevention Plan:", "Long-lead procurement risks & mitigation gates"),
        ("Compilation Speed:", "Produced in under 180 seconds direct from P6"),
        ("Branded Format:", "Full corporate styling, signed off and client-ready")
    ]
    for i, (k, v) in enumerate(features):
        draw.text((120, 280 + i * 80), k, font=get_font(22, bold=True), fill=(168, 85, 247))
        draw.text((120, 315 + i * 80), v, font=get_font(20, bold=False), fill=(255, 255, 255))
        
    # Right: Real report preview frame from demo
    frame_path = "/tmp/p6_frames/frame_011.jpg"
    if os.path.exists(frame_path):
        p6_img = Image.open(frame_path).resize((840, 760))
        img.paste(p6_img, (1000, 160))
        draw.rounded_rectangle([(1000, 160), (1840, 920)], radius=4, outline=(168, 85, 247), width=3)
        
    img.save(f"{ASSETS_DIR}/scene_05.jpg", quality=95)
    print("Created Scene 5")

def create_scene_6():
    # Outro & CTA Slide
    img = Image.new("RGB", (1920, 1080), color=(10, 15, 30))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "THE FUTURE OF PROJECT CONTROLS IS AUTONOMOUS")
    draw_footer(draw, "TELEGRAM @AzGem_Bot • AZGEM AI INFRAMESH")
    
    draw.rounded_rectangle([(140, 200), (1780, 880)], radius=20, fill=(15, 23, 42), outline=(2, 132, 199), width=3)
    
    draw.text((220, 280), "ELEVATE YOUR MEGAPROJECT EXECUTION TODAY", font=get_font(30, bold=True), fill=(56, 189, 248))
    draw.text((220, 350), "ANTIGRAVITY x ORACLE PRIMAVERA P6", font=get_font(68, bold=True), fill=(255, 255, 255))
    draw.text((220, 450), "Deploy the P6-MCP Server & AI Agent directly into your Enterprise PMO.", font=get_font(32, bold=False), fill=(148, 163, 184))
    
    # 3 CTA Boxes
    boxes = [
        ("1. TEST THE P6-MCP CLI", "Run 'p6-mcp inspect' & 'p6-mcp dcma' directly on your VM", (2, 132, 199)),
        ("2. DOWNLOAD SDLC PDF", "Read the complete 3-page Architecture Specification", (34, 197, 94)),
        ("3. AUTOMATE YOUR RETROFIT", "Connect via Telegram @AzGem_Bot or Antigravity CLI", (255, 230, 0))
    ]
    for i, (head, desc, col) in enumerate(boxes):
        by = 550 + i * 95
        draw.rounded_rectangle([(220, by), (1700, by + 75)], radius=10, fill=(30, 41, 59), outline=col, width=2)
        draw.text((250, by + 12), head, font=get_font(24, bold=True), fill=col)
        draw.text((250, by + 42), desc, font=get_font(18, bold=False), fill=(255, 255, 255))
        
    img.save(f"{ASSETS_DIR}/scene_06.jpg", quality=95)
    print("Created Scene 6")

def generate_voiceover_and_subtitles():
    script_text = (
        "Imagine building a full Primavera P6 baseline in under ten minutes with zero Excel imports. "
        "Powered by Antigravity and Gemini, the P6-MCP engine injects eighty-five activities, "
        "one hundred and twenty-two logic links, and balances a two million SAR budget directly into Oracle Primavera. "
        "Tested against real Kaggle construction data, it passes all fourteen DCMA quality checks with zero open ends. "
        "Then, it produces a contractor-grade ten-page Schedule Narrative Report in under three minutes. "
        "The future of project controls is autonomous. Check the link in the first comment to get started right now."
    )
    
    mp3_path = f"{OUTPUT_DIR}/voiceover_aura.mp3"
    vtt_path = f"{OUTPUT_DIR}/subtitles.vtt"
    ass_path = f"{OUTPUT_DIR}/subtitles.ass"
    
    edge_tts_bin = "/home/ubuntu/.venvs/tts/bin/edge-tts"
    cmd = [
        edge_tts_bin,
        "--voice", "en-US-ChristopherNeural",
        "--rate", "+18%",
        "--pitch", "+15Hz",
        "--text", script_text,
        "--write-media", mp3_path,
        "--write-subtitles", vtt_path
    ]
    subprocess.run(cmd, check=True)
    print(f"Generated Voiceover: {mp3_path}")
    
    # Convert VTT to ASS format with Large Bold Kinetic Typography
    ass_header = """[Script Info]
Title: P6 AI Video Aura Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Liberation Sans,54,&H0000E6FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,5,3,2,60,60,80,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    # Parse VTT and write ASS events
    with open(vtt_path, "r", encoding="utf-8") as f:
        vtt_lines = f.readlines()
        
    events = []
    i = 0
    while i < len(vtt_lines):
        line = vtt_lines[i].strip()
        if "-->" in line:
            parts = line.split("-->")
            start = parts[0].strip().replace(".", ",")
            end = parts[1].strip().replace(".", ",")
            
            # format timestamps for ASS: H:MM:SS.cc
            def vtt_to_ass_time(t):
                t = t.replace(",", ".")
                chunks = t.split(":")
                if len(chunks) == 3:
                    h, m, s = chunks
                    return f"{int(h)}:{m}:{float(s):05.2f}"
                return t
                
            start_ass = vtt_to_ass_time(start)
            end_ass = vtt_to_ass_time(end)
            
            i += 1
            text_lines = []
            while i < len(vtt_lines) and vtt_lines[i].strip() != "" and not vtt_lines[i].strip().isdigit():
                text_lines.append(vtt_lines[i].strip())
                i += 1
            caption_text = " ".join(text_lines)
            events.append(f"Dialogue: 0,{start_ass},{end_ass},Default,,0,0,0,,{caption_text}")
        else:
            i += 1
            
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(events) + "\n")
    print(f"Generated ASS Subtitles: {ass_path}")
    return mp3_path, ass_path

def compile_final_video():
    create_scene_1()
    create_scene_2()
    create_scene_3()
    create_scene_4()
    create_scene_5()
    create_scene_6()
    
    mp3_path, ass_path = generate_voiceover_and_subtitles()
    
    # Get audio duration
    res = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', mp3_path], capture_output=True, text=True)
    audio_dur = float(res.stdout.strip())
    print(f"Audio Duration: {audio_dur:.2f} seconds")
    
    # 6 scenes distributed over audio_dur
    scene_dur = audio_dur / 6.0
    
    # Create FFmpeg concat list
    concat_txt = f"{ASSETS_DIR}/concat_list.txt"
    with open(concat_txt, "w") as f:
        for i in range(1, 7):
            f.write(f"file '{ASSETS_DIR}/scene_{i:02d}.jpg'\n")
            f.write(f"duration {scene_dur:.3f}\n")
        # repeat last image for safe finish
        f.write(f"file '{ASSETS_DIR}/scene_06.jpg'\n")
        
    final_video = f"{OUTPUT_DIR}/Autonomous_P6_AI_Showcase_Production.mp4"
    
    # Render with FFmpeg, burning in ASS subtitles and adding audio
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-i", mp3_path,
        "-vf", f"ass={ass_path}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        final_video
    ]
    print("Compiling final production video with FFmpeg...")
    subprocess.run(cmd, check=True)
    print(f"SUCCESS: Final Video Generated at {final_video}")
    size = os.path.getsize(final_video)
    print(f"Video File Size: {size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    compile_final_video()
