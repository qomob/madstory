#!/usr/bin/env python3
"""
Platform Adapter — 多视频生成平台适配层 (Harness Engineering: REPL Container)
将平台特定参数从核心引擎中解耦，支持 Seedance / Runway / Kling / Sora 等多平台

设计原则:
- 状态分离: 适配器是无状态纯函数，不持有引擎状态
- 可扩展: 新增平台只需添加 PlatformConfig，无需修改引擎代码
- Design for Failure: 每个适配器都有 fallback 参数
"""

from dataclasses import dataclass, field
from typing import Optional
from ad_mode import AdMode


@dataclass
class PlatformConfig:
    """单个平台的参数配置（REPL 容器抽象）"""
    name: str                           # 平台标识名
    display_name: str                   # 显示名称
    max_duration: int                   # 最大时长(秒)
    max_motion_strength: int            # 最大运动强度
    default_mode: str                   # 默认生成模式
    supported_modes: list[str]          # 支持的生成模式列表
    # 参数映射: 引擎内部参数 → 平台 API 参数
    param_map: dict = field(default_factory=dict)
    # 负面约束模板
    negative_template: str = ""
    # 特殊限制
    constraints: dict = field(default_factory=dict)


# === 内置平台配置 ===

PLATFORMS: dict[str, PlatformConfig] = {
    "seedance_2.0": PlatformConfig(
        name="seedance_2.0",
        display_name="Seedance 2.0 (即梦)",
        max_duration=15,
        max_motion_strength=10,
        default_mode="text-to-video",
        supported_modes=["text-to-video", "image-to-video", "reference-to-video"],
        param_map={
            "motion_strength": "motion_strength",
            "duration": "duration",
            "aspect_ratio": "aspect_ratio",
        },
        negative_template="{base_negative}, no object melting, no random text, no muddy lighting",
        constraints={
            "max_resolution": "1080p",
            "fps_range": (24, 30),
        },
    ),
    "seedance_3.0": PlatformConfig(
        name="seedance_3.0",
        display_name="Seedance 3.0 (即梦 Pro)",
        max_duration=30,
        max_motion_strength=10,
        default_mode="text-to-video",
        supported_modes=["text-to-video", "image-to-video", "reference-to-video"],
        param_map={
            "motion_strength": "motion_strength",
            "duration": "duration",
            "aspect_ratio": "aspect_ratio",
        },
        negative_template="{base_negative}, no object melting, no temporal inconsistency",
        constraints={
            "max_resolution": "4K",
            "fps_range": (24, 60),
        },
    ),
    "runway_gen3": PlatformConfig(
        name="runway_gen3",
        display_name="Runway Gen-3 Alpha",
        max_duration=10,
        max_motion_strength=8,
        default_mode="text-to-video",
        supported_modes=["text-to-video", "image-to-video"],
        param_map={
            "motion_strength": "motion_bucket_id",
            "duration": "duration",
        },
        negative_template="{base_negative}, no blurry faces, no morphing artifacts",
        constraints={
            "max_resolution": "1080p",
            "fps": 24,
        },
    ),
    "kling_v1.5": PlatformConfig(
        name="kling_v1.5",
        display_name="Kling 1.5 (快手)",
        max_duration=10,
        max_motion_strength=10,
        default_mode="text-to-video",
        supported_modes=["text-to-video", "image-to-video"],
        param_map={
            "motion_strength": "cfg_scale",
            "duration": "duration",
        },
        negative_template="{base_negative}, no watermark, no logo, no text overlay",
        constraints={
            "max_resolution": "1080p",
            "fps_range": (24, 30),
        },
    ),
    "sora": PlatformConfig(
        name="sora",
        display_name="Sora (OpenAI)",
        max_duration=60,
        max_motion_strength=10,
        default_mode="text-to-video",
        supported_modes=["text-to-video", "image-to-video"],
        param_map={
            "motion_strength": "motion_level",
            "duration": "duration",
        },
        negative_template="{base_negative}, no distortion, no artifacts",
        constraints={
            "max_resolution": "4K",
            "fps_range": (24, 60),
        },
    ),
}


def get_platform(platform_id: str) -> PlatformConfig:
    """获取平台配置，未找到时 fallback 到 seedance_2.0（Design for Failure）"""
    return PLATFORMS.get(platform_id, PLATFORMS["seedance_2.0"])


def adapt_params(engine_output: dict, platform_id: str = "seedance_2.0") -> dict:
    """将引擎输出适配为目标平台 API 参数

    Args:
        engine_output: MadStoryEngine.generate_final_output() 的结果
        platform_id: 目标平台 ID

    Returns:
        适配后的参数字典，可直接用于目标平台 API 调用
    """
    config = get_platform(platform_id)
    base_negative = engine_output.get("NEGATIVE_PROMPT", "")

    # 基础参数适配
    adapted = {
        "platform": platform_id,
        "display_name": config.display_name,
        "prompt": engine_output.get("STANDARD_PROMPT", ""),
        "negative_prompt": config.negative_template.format(base_negative=base_negative),
        "duration": _clamp(engine_output.get("DURATION", 15), 1, config.max_duration),
        "motion_strength": _clamp(engine_output.get("MOTION_STRENGTH", 5), 0, config.max_motion_strength),
        "mode": engine_output.get("MODE_KEY", "cinematic"),
        "camera": engine_output.get("CAMERA", "static"),
        "lighting": engine_output.get("LIGHTING", engine_output.get("lighting", "")),
        "sound_design": engine_output.get("SOUND_DESIGN", ""),
        "timeline": engine_output.get("TIMELINE", ""),
        "shot_list": engine_output.get("SHOT_LIST", []),
    }

    # 平台特有参数映射
    for engine_key, api_key in config.param_map.items():
        if engine_key in engine_output:
            adapted[api_key] = engine_output[engine_key]

    # 应用平台约束
    if "max_resolution" in config.constraints:
        adapted["resolution"] = config.constraints["max_resolution"]

    return adapted


def list_platforms() -> list[dict]:
    """列出所有可用平台及其能力概览"""
    return [
        {
            "id": p.name,
            "name": p.display_name,
            "max_duration": p.max_duration,
            "max_motion": p.max_motion_strength,
            "modes": p.supported_modes,
        }
        for p in PLATFORMS.values()
    ]


def recommend_platform(duration: int, motion: int) -> str:
    """根据时长和运动强度推荐最佳平台"""
    candidates = []
    for pid, cfg in PLATFORMS.items():
        if duration <= cfg.max_duration and motion <= cfg.max_motion_strength:
            candidates.append((pid, cfg.max_duration))
    # 选最长支持的平台作为推荐
    if not candidates:
        return "seedance_2.0"  # fallback
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[0][0]


def validate_for_platform(output: dict, platform_id: str) -> list[str]:
    """校验输出是否符合目标平台约束（R.E.S.T Security）"""
    config = get_platform(platform_id)
    issues = []
    duration = output.get("DURATION", 0)
    motion = output.get("MOTION_STRENGTH", 0)

    if duration > config.max_duration:
        issues.append(f"时长 {duration}s 超过 {config.display_name} 上限 {config.max_duration}s")
    if motion > config.max_motion_strength:
        issues.append(f"运动强度 {motion} 超过 {config.display_name} 上限 {config.max_motion_strength}")

    mode = output.get("MODE_KEY", "")
    mode_map = AdMode.DEFAULT_SEEDANCE_MODE.get(mode, "text-to-video")
    if mode_map not in config.supported_modes:
        issues.append(f"模式 '{mode}' 对应的 '{mode_map}' 不被 {config.display_name} 支持")

    return issues


# === 工具函数 ===

def _clamp(value: int, min_val: int, max_val: int) -> int:
    """值域裁剪（Design for Failure: 防止越界参数）"""
    return max(min_val, min(value, max_val))
