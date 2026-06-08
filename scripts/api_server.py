#!/usr/bin/env python3
"""MadStory REST API + WebSocket 服务 v3 — 电影级分镜设计引擎（Harness Engineering 驱动）
支持多平台适配（Seedance / Runway / Kling / Sora），集成 PPAF 循环
安全加固: Session TTL 30min + 请求限流 (60 req/min) + 输入过滤
"""

import json
import os
import sys
import time
import asyncio
from datetime import datetime
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mad_story_engine import (
    MadStoryEngine, AdMode, QualityGate,
)

try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
    from fastapi.responses import HTMLResponse
    from pydantic import BaseModel, Field
    import uvicorn
except ImportError:
    print("需要安装依赖: pip install fastapi uvicorn pydantic")
    sys.exit(1)

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
REFS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references")

app = FastAPI(
    title="MadStory API",
    description="电影级影视分镜引擎 REST API — Harness Engineering 驱动，支持多平台适配",
    version="3.0.0",
)

engine = MadStoryEngine(ASSETS, REFS)
active_sessions = {}
active_ws = set()

# === 安全加固: Session TTL + 请求限流 ===
SESSION_TTL = 1800  # 30 分钟
RATE_LIMIT = 60     # 每分钟请求数
_request_log: list[tuple[float]] = []  # (timestamp,) 用于滑动窗口限流


def _cleanup_expired_sessions():
    """清理过期 Session（Design for Failure: 防止内存泄漏）"""
    now = time.time()
    expired = [sid for sid, data in active_sessions.items()
               if now - data.get("created_at", 0) > SESSION_TTL]
    for sid in expired:
        del active_sessions[sid]


def _check_rate_limit():
    """滑动窗口请求限流（R.E.S.T Security）"""
    now = time.time()
    window_start = now - 60
    global _request_log
    _request_log = [t for t in _request_log if t > window_start]
    if len(_request_log) >= RATE_LIMIT:
        raise HTTPException(429, "请求过于频繁，请稍后重试")
    _request_log.append(now)


class GenerateRequest(BaseModel):
    mode: str = Field(..., description="创作模式", examples=["cinematic"])
    concept: str = Field(..., description="核心创意描述")
    timeline: str = Field(default="0-15s", description="时间轴")
    composition: str = Field(default="center frame", description="构图方式")
    camera: str = Field(default="static", description="镜头运动")
    lighting: str = Field(default="default", description="光影描述")
    sound: str = Field(default="ambient", description="声音设计")
    duration: int = Field(default=15, ge=1, le=300, description="时长(秒)")
    script: Optional[str] = Field(default=None, description="短剧剧本(仅short_drama模式)")


class ValidateRequest(BaseModel):
    output: dict = Field(..., description="待校验的分镜输出 JSON")


class SessionCreateRequest(BaseModel):
    mode: str = Field(..., description="创作模式")


class SessionStepRequest(BaseModel):
    session_id: str = Field(..., description="会话 ID")
    input: str = Field(..., description="当前阶段输入")


async def broadcast(msg):
    for ws in list(active_ws):
        try:
            await ws.send_json(msg)
        except Exception:
            active_ws.discard(ws)


@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.get("/modes")
async def list_modes():
    return [
        {"key": k, "label": v, "seedance_mode": AdMode.DEFAULT_SEEDANCE_MODE.get(k)}
        for k, v in AdMode.LABELS.items()
    ]


@app.post("/generate")
async def generate(req: GenerateRequest):
    _check_rate_limit()  # 请求限流
    if req.mode not in AdMode.LABELS:
        raise HTTPException(400, f"无效模式。可选: {list(AdMode.LABELS.keys())}")
    eng = MadStoryEngine(ASSETS, REFS)
    eng.current_state["mode"] = req.mode
    eng.current_state["duration"] = req.duration

    if req.mode == AdMode.SHORT_DRAMA and req.script:
        eng.drama_engine.parse_script(req.script)
    if req.mode == AdMode.ONE_SHOT:
        from mad_story_engine import OneShotEngine
        eng.one_shot_engine.add_image("start frame", 1)
        eng.one_shot_engine.add_image("end frame", 2)
    if req.mode == AdMode.VIRAL_REPLICATE:
        eng.viral_engine.set_reference(req.concept, "creative_shoot")

    eng.current_state["concept"] = req.concept
    eng.current_state["timeline"] = req.timeline
    eng.current_state["composition"] = req.composition
    eng.current_state["camera"] = req.camera
    eng.current_state["lighting"] = req.lighting
    eng.current_state["sound"] = req.sound
    eng.current_state["phase"] = 5

    result = eng.generate_final_output()
    result["checklist"] = eng.run_checklist(result)

    await broadcast({
        "event": "generation_complete",
        "mode": req.mode,
        "timestamp": datetime.now().isoformat(),
    })
    return result


@app.post("/validate")
async def validate(req: ValidateRequest):
    eng = MadStoryEngine(ASSETS, REFS)
    issues = eng.run_quality_gates(req.output)
    checklist = eng.run_checklist(req.output) if req.output.get("MODE_KEY") else {}
    return {
        "passed": len(issues) == 0,
        "issue_count": len(issues),
        "issues": issues,
        "checklist": checklist,
    }


@app.post("/session/create")
async def session_create(req: SessionCreateRequest):
    _check_rate_limit()
    _cleanup_expired_sessions()  # 清理过期 Session
    if req.mode not in AdMode.LABELS:
        raise HTTPException(400, f"无效模式")
    import uuid
    sid = str(uuid.uuid4())[:8]
    eng = MadStoryEngine(ASSETS, REFS)
    eng.select_mode(req.mode)
    active_sessions[sid] = {"engine": eng, "created_at": time.time(), "mode": req.mode}
    return {"session_id": sid, "mode": req.mode, "phase": 0, "ttl_seconds": SESSION_TTL}


@app.post("/session/step")
async def session_step(req: SessionStepRequest):
    session = active_sessions.get(req.session_id)
    if not session:
        raise HTTPException(404, "会话不存在或已过期")
    eng = session["engine"]
    result = eng.next_phase(req.input)
    if isinstance(result, dict):
        result["checklist"] = eng.run_checklist(result)
        return {"done": True, "output": result, "session_id": req.session_id}
    return {"done": False, "message": result, "phase": eng.current_state["phase"]}


@app.post("/session/save")
async def session_save(session_id: str):
    session = active_sessions.get(session_id)
    if not session:
        raise HTTPException(404, "会话不存在或已过期")
    eng = session["engine"]
    import tempfile
    path = os.path.join(tempfile.gettempdir(), f"madstory_session_{session_id}.json")
    eng.save_session(path)
    return {"session_id": session_id, "path": path}


@app.post("/session/load")
async def session_load(session_id: str):
    session = active_sessions.get(session_id)
    if not session:
        raise HTTPException(404, "会话不存在或已过期")
    eng = session["engine"]
    return {
        "session_id": session_id,
        "mode": eng.current_state["mode"],
        "phase": eng.current_state["phase"],
        "concept": eng.current_state.get("concept", ""),
    }


@app.get("/platforms")
async def list_platforms():
    """列出所有支持的视频生成平台及其参数能力"""
    from platform_adapter import list_platforms as _list
    return {"platforms": _list(), "default": "seedance_2.0"}


@app.post("/adapt")
async def adapt_for_platform(req: GenerateRequest):
    """将分镜输出适配到指定平台参数"""
    from platform_adapter import adapt_params, validate_for_platform
    eng = MadStoryEngine(ASSETS, REFS)
    eng.current_state["mode"] = req.mode
    eng.current_state["duration"] = req.duration
    output = eng.generate_final_output()
    platform_id = getattr(req, 'platform', 'seedance_2.0')
    adapted = adapt_params(output, platform_id)
    issues = validate_for_platform(output, platform_id)
    adapted["validation_issues"] = issues
    return adapted


@app.websocket("/ws/validate")
async def websocket_validate(ws: WebSocket):
    await ws.accept()
    active_ws.add(ws)
    eng = MadStoryEngine(ASSETS, REFS)
    try:
        await ws.send_json({"event": "connected", "message": "MadStory 实时校验就绪"})
        while True:
            data = await ws.receive_json()
            output = data.get("output", data)
            issues = eng.run_quality_gates(output)
            checklist = eng.run_checklist(output) if output.get("MODE_KEY") else {}
            await ws.send_json({
                "event": "validation_result",
                "passed": len(issues) == 0,
                "issues": issues,
                "checklist": checklist,
                "timestamp": time.time(),
            })
    except WebSocketDisconnect:
        pass
    finally:
        active_ws.discard(ws)


@app.get("/", response_class=HTMLResponse)
async def root():
    template_path = os.path.join(ASSETS, "storyboard_template.html")
    if os.path.exists(template_path):
        with open(template_path, "r") as f:
            return f.read()
    return "<h1>MadStory API Server</h1><p>POST /generate | POST /validate | /modes | /health</p>"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="MadStory API Server")
    parser.add_argument("--host", default="0.0.0.0", help="绑定地址")
    parser.add_argument("--port", type=int, default=8787, help="端口")
    parser.add_argument("--reload", action="store_true", help="开发模式热重载")
    args = parser.parse_args()
    print(f"MadStory API Server starting on http://{args.host}:{args.port}")
    print(f"Docs: http://{args.host}:{args.port}/docs")
    uvicorn.run("api_server:app", host=args.host, port=args.port, reload=args.reload)
