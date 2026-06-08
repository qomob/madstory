#!/usr/bin/env python3
"""MadStory Batch Runner — 目录级批量生产流水线"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mad_story_engine import (
    MadStoryEngine, AdMode,
)

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
REFS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references")


class BatchRunner:
    def __init__(self, input_dir, output_dir, mode=None, workers=4, dry_run=False):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.mode = mode
        self.workers = workers
        self.dry_run = dry_run
        self.results = []
        self.errors = []
        self.start_time = None

    def scan_inputs(self):
        files = []
        if not os.path.isdir(self.input_dir):
            return files

        for f in sorted(os.listdir(self.input_dir)):
            path = os.path.join(self.input_dir, f)
            if f.endswith(".json") and not f.startswith("_"):
                files.append(("json", path))
            elif f.endswith(".txt") and not f.startswith("_"):
                files.append(("script", path))

        return files

    def _process_json(self, path):
        with open(path, "r", encoding="utf-8") as f:
            spec = json.load(f)

        eng = MadStoryEngine(ASSETS, REFS)
        mode = spec.get("mode", self.mode or "cinematic")
        if mode not in AdMode.LABELS:
            return {"error": f"无效模式: {mode}", "file": path}

        eng.current_state["mode"] = mode
        eng.current_state["duration"] = spec.get("duration", 15)
        eng.current_state["concept"] = spec.get("concept", "")
        eng.current_state["timeline"] = spec.get("timeline", "0-15s")
        eng.current_state["composition"] = spec.get("composition", "center frame")
        eng.current_state["camera"] = spec.get("camera", "static")
        eng.current_state["lighting"] = spec.get("lighting", "default")
        eng.current_state["sound"] = spec.get("sound", "ambient")
        eng.current_state["phase"] = 5

        if mode == AdMode.ONE_SHOT:
            for i, img_desc in enumerate(spec.get("image_sequence", ["start", "end"])):
                eng.one_shot_engine.add_image(img_desc, i + 1)
        if mode == AdMode.VIRAL_REPLICATE:
            eng.viral_engine.set_reference(
                spec.get("reference_video", "@video"),
                spec.get("strategy", "creative_shoot"),
            )
            if spec.get("replacement_subject"):
                eng.viral_engine.set_replacement(spec["replacement_subject"])
        if mode == AdMode.SHORT_DRAMA:
            eng.drama_engine.parse_script(spec.get("concept", ""))

        result = eng.generate_final_output()
        result["checklist"] = eng.run_checklist(result)
        result["_source"] = os.path.basename(path)
        return result

    def _process_script(self, path):
        with open(path, "r", encoding="utf-8") as f:
            script_text = f.read()

        eng = MadStoryEngine(ASSETS, REFS)
        eng.current_state["mode"] = AdMode.SHORT_DRAMA
        eng.current_state["concept"] = script_text
        eng.drama_engine.parse_script(script_text)

        result = eng.generate_final_output()
        result["checklist"] = eng.run_checklist(result)
        result["_source"] = os.path.basename(path)
        return result

    def run(self):
        self.start_time = time.time()
        os.makedirs(self.output_dir, exist_ok=True)

        files = self.scan_inputs()
        if not files:
            print(f"输入目录无有效文件: {self.input_dir}")
            return self

        print(f"扫描到 {len(files)} 个文件")
        if self.dry_run:
            for ftype, fpath in files:
                print(f"  [{ftype}] {fpath}")
            return self

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = {}
            for ftype, fpath in files:
                if ftype == "json":
                    fut = executor.submit(self._process_json, fpath)
                else:
                    fut = executor.submit(self._process_script, fpath)
                futures[fut] = fpath

            for fut in as_completed(futures):
                fpath = futures[fut]
                try:
                    result = fut.result()
                    if "error" in result:
                        self.errors.append(result)
                        print(f"  [ERROR] {os.path.basename(fpath)}: {result['error']}")
                    else:
                        self.results.append(result)
                        self._save_output(result, fpath)
                        print(f"  [OK] {os.path.basename(fpath)} → {result.get('MODE', '?')}")
                except Exception as e:
                    self.errors.append({"file": fpath, "error": str(e)})
                    print(f"  [CRASH] {os.path.basename(fpath)}: {e}")

        self._save_summary()
        return self

    def _save_output(self, result, source_path):
        base_name = os.path.splitext(os.path.basename(source_path))[0]
        out_json = os.path.join(self.output_dir, f"{base_name}.output.json")
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        eng = MadStoryEngine(ASSETS, REFS)
        html = eng.render_to_html(result)
        out_html = os.path.join(self.output_dir, f"{base_name}.preview.html")
        with open(out_html, "w", encoding="utf-8") as f:
            f.write(html)

    def _save_summary(self):
        elapsed = time.time() - self.start_time
        summary = {
            "timestamp": datetime.now().isoformat(),
            "input_dir": self.input_dir,
            "output_dir": self.output_dir,
            "elapsed_seconds": round(elapsed, 1),
            "total": len(self.results) + len(self.errors),
            "success": len(self.results),
            "errors": len(self.errors),
            "results": [
                {
                    "source": r["_source"],
                    "mode": r.get("MODE", "?"),
                    "checklist_pass": r.get("checklist", {}).get("all_passed", False),
                    "issues": len(r.get("QUALITY_WARNINGS", [])),
                }
                for r in self.results
            ],
            "error_details": self.errors,
        }
        path = os.path.join(self.output_dir, "_batch_summary.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"\n总结: {summary['success']}/{summary['total']} 成功, {summary['errors']} 失败")
        print(f"耗时: {elapsed:.1f}s, 输出目录: {self.output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MadStory Batch Runner — 批量生产流水线")
    parser.add_argument("input_dir", help="输入目录 (JSON规格文件 或 剧本 .txt)")
    parser.add_argument("output_dir", help="输出目录")
    parser.add_argument("--mode", "-m", choices=list(AdMode.LABELS.keys()),
                        help="统一创作模式 (JSON文件可逐个覆盖)")
    parser.add_argument("--workers", "-w", type=int, default=4, help="并行线程数")
    parser.add_argument("--dry-run", action="store_true", help="仅扫描，不执行")
    args = parser.parse_args()

    runner = BatchRunner(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        mode=args.mode,
        workers=args.workers,
        dry_run=args.dry_run,
    )
    runner.run()
