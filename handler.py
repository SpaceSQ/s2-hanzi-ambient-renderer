#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2 Hanzi Ambient Renderer - Native Code Plugin Handler
Core Logic: Dialectical Physics Engine & Hanzi Morphological Mapping
Author: Space2.world
"""

import os
import sys
import json
import urllib.request
import logging

# 配置极客风日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s [S2-RENDERER] %(message)s')

class DialecticalPhysicsEngine:
    """
    S2 核心算法：东方辩证物理引擎
    将环境六要素与人类情绪，映射为汉字的“形、音、义、态”。
    """
    
    def __init__(self):
        # 从环境变量读取安装时用户配置的参数 (由 openclaw.plugin.json 的 config_schema 注入)
        self.panel_ip = os.environ.get("DISPLAY_PANEL_IP", "")
        self.theme = os.environ.get("RENDER_THEME", "ink_wash")
        self.privacy_consent = os.environ.get("S2_PRIVACY_CONSENT", "0")

    def calculate_thermal_quadrant(self, temp: float, humidity: float) -> dict:
        """
        核心算法 1：四象限温湿舒适区计算 (冰火六态演化)
        返回冰火图腾的形态参数 (权重 0.0 ~ 1.0)
        """
        # 极简版 THI (温湿指数) 逻辑，用于推演物理象限
        # 实际开发中可替换为你专利中的精准算法
        fire_weight = 0.0
        ice_weight = 0.0
        
        if temp > 26.0:
            fire_weight = min(1.0, (temp - 26.0) * 0.15 + (humidity * 0.005))
            ice_weight = 0.0
        elif temp < 20.0:
            ice_weight = min(1.0, (20.0 - temp) * 0.15 + ((100-humidity) * 0.005))
            fire_weight = 0.0
        else:
            # 舒适区 (Equilibrium)：冰与火处于太极平衡态
            fire_weight = 0.2
            ice_weight = 0.2

        return {
            "primary_totem": "火" if fire_weight > ice_weight else "冰" if ice_weight > fire_weight else "和",
            "fire_intensity": round(fire_weight, 2),
            "ice_crystallization": round(ice_weight, 2)
        }

    def map_emotion_to_fluidity(self, emotion: str) -> dict:
        """
        核心算法 2：情绪共鸣场映射
        将人类情绪转化为汉字笔画的流转度 (Fluidity) 和呼吸频率 (Breathing Hz)
        """
        if self.privacy_consent != "1":
            return {"fluidity": 0.5, "breathing_hz": 0.2} # 默认无情感平稳态

        emotion = emotion.lower()
        if emotion in ["tense", "anxious", "angry", "fatigued"]:
            # 治愈模式：水墨流转度极高，呼吸频率极慢 (如 0.1Hz，10秒一次深呼吸)
            return {"fluidity": 0.9, "breathing_hz": 0.1}
        elif emotion in ["joyful", "excited", "active"]:
            # 跃动模式：笔画边缘清晰，呼吸频率加快 (如 0.3Hz)
            return {"fluidity": 0.2, "breathing_hz": 0.3}
        else:
            # 平静模式
            return {"fluidity": 0.5, "breathing_hz": 0.15}

    def push_to_display_panel(self, payload: dict):
        """
        局域网渲染推送：向别墅大屏或全息终端下发 JSON 渲染指令
        """
        if not self.panel_ip:
            logging.error("DISPLAY_PANEL_IP is not configured. Aborting render push.")
            return json.dumps({"status": "error", "message": "Missing Panel IP"})

        url = f"http://{self.panel_ip}:8080/api/v1/render/hanzi"
        logging.info(f"Pushing morphological payload to {url}...")
        
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), 
                                         headers={'Content-Type': 'application/json'}, method='POST')
            with urllib.request.urlopen(req, timeout=3) as response:
                res_data = response.read()
                logging.info(f"Panel Response: {res_data.decode('utf-8')}")
                return json.dumps({"status": "success", "message": "Ambient shift applied."})
        except Exception as e:
            logging.error(f"Network push failed: {str(e)}")
            return json.dumps({"status": "error", "message": f"Push failed: {str(e)}"})

    def handle_tool_call(self, args: dict):
        """
        OpenClaw 3.22 工具调用入口
        """
        temp = float(args.get("temperature", 24.0))
        humidity = float(args.get("humidity", 50.0))
        emotion = args.get("emotion", "neutral")
        
        logging.info(f"Initiating Dialectical Engine -> Temp: {temp}C, RH: {humidity}%, Emotion: {emotion}")

        # 1. 计算物理象限 (冰火之争)
        thermal_state = self.calculate_thermal_quadrant(temp, humidity)
        
        # 2. 计算情绪共鸣 (笔画与呼吸)
        emotion_state = self.map_emotion_to_fluidity(emotion)
        
        # 3. 合成最终的渲染参数 (Payload)
        render_payload = {
            "protocol": "S2-Hanzi-Ambient",
            "theme": self.theme,
            "totem": thermal_state["primary_totem"],
            "morph_parameters": {
                "fire_weight": thermal_state["fire_intensity"],
                "ice_weight": thermal_state["ice_crystallization"],
                "stroke_fluidity": emotion_state["fluidity"],
                "breathing_frequency": emotion_state["breathing_hz"]
            }
        }
        
        logging.info(f"Morphological Payload Generated: {json.dumps(render_payload, ensure_ascii=False)}")

        # 4. 推送至物理终端
        return self.push_to_display_panel(render_payload)

# ==========================================
# OpenClaw 3.22 标准进程入口
# ==========================================
if __name__ == "__main__":
    # OpenClaw 插件通常通过 stdin/stdout 或命令行参数与主进程通信
    # 这里我们模拟一个标准的 JSON-RPC 工具调用读取
    engine = DialecticalPhysicsEngine()
    
    try:
        # 读取 OpenClaw 传来的 JSON 字符串 (假设从命令行参数传入，或 stdin)
        # 例如: python3 handler.py '{"temperature": 28, "humidity": 70, "emotion": "tense"}'
        if len(sys.argv) > 1:
            input_args = json.loads(sys.argv[1])
            result = engine.handle_tool_call(input_args)
            print(result)
        else:
            logging.warning("No dialectical parameters provided. Awaiting instructions.")
    except Exception as e:
        logging.error(f"Fatal execution error: {str(e)}")
        print(json.dumps({"status": "fatal", "error": str(e)}))