import json
import os

class MadStoryEngine:
    def __init__(self, assets_path, references_path):
        self.assets_path = assets_path
        self.references_path = references_path
        self.current_state = {
            "phase": 1,
            "concept": "",
            "composition": "",
            "camera": "",
            "lighting": "",
            "sound": "",
            "params": {}
        }
        self.load_resources()

    def load_resources(self):
        with open(os.path.join(self.assets_path, 'cheat_sheet.json'), 'r', encoding='utf-8') as f:
            self.cheat_sheet = json.load(f)

    def next_phase(self, user_input):
        if self.current_state["phase"] == 1:
            self.current_state["concept"] = user_input
            self.current_state["phase"] = 2
            return "很好，核心创意已锁定。现在，让我们聊聊**视觉构图**：你希望画面比例是多少？角色在画面中处于什么位置？（例如：三分法、中心构图、或上传一张参考图）"
        
        elif self.current_state["phase"] == 2:
            self.current_state["composition"] = user_input
            self.current_state["phase"] = 3
            return "构图方案已记录。接下来是**动态运镜**：你希望镜头如何运动？（推、拉、摇、移、跟，或者描述一段参考视频的动作节奏）"

        elif self.current_state["phase"] == 3:
            self.current_state["camera"] = user_input
            self.current_state["phase"] = 4
            return "镜头语言已确定。现在是**光影氛围**：想要什么样的色调和光影？（比如：黄金时刻、赛博朋克、黑白电影质感）"

        elif self.current_state["phase"] == 4:
            self.current_state["lighting"] = user_input
            self.current_state["phase"] = 5
            return "氛围感拉满了。最后，**声音设计**：需要什么样的背景音乐或音效来增强沉浸感？"

        elif self.current_state["phase"] == 5:
            self.current_state["sound"] = user_input
            self.current_state["phase"] = 6
            return self.generate_final_output()

    def generate_final_output(self):
        # 简单模拟提示词生成逻辑
        prompt = f"Cinematic shot: {self.current_state['concept']}. Composition: {self.current_state['composition']}. " \
                 f"Camera movement: {self.current_state['camera']}. Lighting: {self.current_state['lighting']}. " \
                 f"Vibe: high quality, 4k, seedance 2.0 style."
        
        output = {
            "STANDARD_PROMPT": prompt,
            "CAMERA_MOVEMENT": self.current_state['camera'],
            "MOTION_STRENGTH": 5,
            "IMAGE_REF_ADVICE": "建议上传一张具有相似色调和构图的高质量图像作为参考",
            "VIBE_ADVICE": self.current_state['lighting'],
            "SOUND_DESIGN": self.current_state['sound']
        }
        
        return output

    def render_to_html(self, output):
        with open(os.path.join(self.assets_path, 'storyboard_template.html'), 'r', encoding='utf-8') as f:
            template = f.read()
        
        for key, value in output.items():
            template = template.replace(f"{{{{{key}}}}}", str(value))
            
        return template

if __name__ == "__main__":
    # 示例运行
    assets = "/Users/jonki/.trae/skills/mad-story/assets"
    refs = "/Users/jonki/.trae/skills/mad-story/references"
    engine = MadStoryEngine(assets, refs)
    
    print("Welcome to MadStory!")
    # 这里只是为了演示逻辑
    # print(engine.next_phase("一个赛博朋克风格的街头武士，正在雨中行走"))
