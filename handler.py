#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2 Hanzi Ambient Renderer & Spatial Palette (V3.0 Local Matrix Edition)
Core Logic: 200-Hanzi Local DB + 7-Color Spectrum + Antonym Physics + Empathic Resonance
Author: Space2.world (Miles Xiang)
"""

import os
import sys
import json
import urllib.request
import logging
import random

# 配置极客风日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s [S2-PALETTE-ENGINE] %(message)s')

class S2LocalHanziDictionary:
    """
    S2 官方内置：本地汉字与诗词映射矩阵 (V3.0 完全体)
    包含 200 个精选意境汉字与 20 首空间诗词。纯本地离线运行。
    """
    def __init__(self):
        self.hanzi_db = {
            "calm_healing": {
                "chars": ["谧", "宁", "静", "憩", "幽", "舒", "安", "闲", "恬", "柔", 
                          "缓", "息", "虚", "旷", "淡", "泊", "寂", "寥", "澈", "穆", 
                          "婉", "眠", "稳", "禅", "隐", "悠", "渊", "沉", "潜", "敛", 
                          "和", "融", "顺", "适", "妥", "泰", "畅", "释", "宽", "慰"],
                "poems": ["夜阑人静，万物归于安宁。", "明月松间照，清泉石上流。", "水流心不竞，云在意俱迟。", "心远地自偏，结庐在人境。"]
            },
            "warm_joyful": {
                "chars": ["煦", "暖", "融", "怡", "欢", "跃", "畅", "悦", "欣", "喜", 
                          "乐", "愉", "酣", "熙", "阳", "晴", "灿", "烂", "晖", "耀", 
                          "朗", "润", "泽", "辉", "煌", "焕", "勃", "昂", "扬", "奋", 
                          "荣", "茂", "俏", "嫣", "妍", "曜", "熠", "烨", "馨", "睦"],
                "poems": ["暖光如豆，室有春风生。", "迟日江山丽，春风花草香。", "白日放歌须纵酒，青春作伴好还乡。", "春风得意马蹄疾，一日看尽长安花。"]
            },
            "cold_focused": {
                "chars": ["澄", "冽", "清", "明", "澈", "净", "醒", "锐", "锋", "肃", 
                          "凛", "寒", "凉", "霜", "雪", "冰", "凝", "聚", "敛", "束", 
                          "严", "峭", "拔", "洁", "粹", "纯", "真", "晶", "莹", "剔", 
                          "透", "爽", "旷", "达", "镜", "泓", "鉴", "泠", "肃", "穆"],
                "poems": ["心如明镜，神似秋水澄。", "清风徐来，水波不兴。", "独坐幽篁里，弹琴复长啸。", "不要人夸好颜色，只留清气满乾坤。"]
            },
            "tense_grounding": {
                "chars": ["定", "稳", "磐", "镇", "守", "寂", "沉", "降", "坠", "伏", 
                          "藏", "蓄", "厚", "重", "实", "坚", "固", "牢", "韧", "强", 
                          "刚", "毅", "泰", "岳", "渊", "渟", "峙", "涵", "容", "忍", 
                          "默", "笃", "钧", "铸", "奠", "夯", "砥", "砺", "堪", "朴"],
                "poems": ["心若冰清，天塌不惊。", "千磨万击还坚劲，任尔东西南北风。", "咬定青山不放松，立根原在破岩中。", "大雪压青松，青松挺且直。"]
            },
            "noisy_agitated": {
                "chars": ["燥", "喧", "烦", "烈", "炙", "沸", "腾", "滚", "烫", "炎", 
                          "炽", "焚", "燃", "烧", "爆", "裂", "轰", "鸣", "噪", "杂", 
                          "乱", "纷", "扰", "攘", "激", "荡", "震", "撼", "狂", "暴", 
                          "猛", "悍", "突", "冲", "撞", "驰", "骤", "奔", "啸", "涌"],
                "poems": ["尘世喧嚣，气结于室，宜静心以对。", "蝉噪林逾静，鸟鸣山更幽。", "结庐在人境，而无车马喧。", "问君何能尔？心远地自偏。"]
            }
        }

    def query(self, category: str) -> dict:
        subset = self.hanzi_db.get(category, self.hanzi_db["calm_healing"])
        return {"hanzi": random.choice(subset["chars"]), "poetry": random.choice(subset["poems"])}

class S2SpatialRenderEngine:
    def __init__(self):
        self.local_db = S2LocalHanziDictionary()
        self.panel_ip = os.environ.get("DISPLAY_PANEL_IP", "")
        self.theme = os.environ.get("RENDER_THEME", "ink_wash")
        self.use_llm_hook = os.environ.get("ENABLE_EXTERNAL_LLM", "0")

    def _evaluate_antonym_logic(self, temp: float, db_level: float) -> dict:
        fire_weight = max(0.0, min(1.0, (temp - 24.0) * 0.1)) if temp > 24 else 0.0
        ice_weight = max(0.0, min(1.0, (24.0 - temp) * 0.1)) if temp < 24 else 0.0
        noise_weight = max(0.0, min(1.0, (db_level - 40.0) * 0.02)) if db_level > 40 else 0.0
        quiet_weight = max(0.0, min(1.0, (40.0 - db_level) * 0.05)) if db_level < 40 else 0.0

        return {
            "thermal_conflict": {"dominant": "火" if fire_weight > ice_weight else "冰", "fire_mask": round(fire_weight,2), "ice_mask": round(ice_weight,2)},
            "acoustic_conflict": {"dominant": "喧" if noise_weight > quiet_weight else "静", "noise_mask": round(noise_weight,2), "quiet_mask": round(quiet_weight,2)}
        }

    def _evaluate_empathic_resonance(self, emotion: str) -> dict:
        emotion = emotion.lower()
        if emotion in ["tense", "anxious", "fatigued", "exhausted"]:
            return {"category": "tense_grounding", "fluidity": 0.9, "breathing_hz": 0.1, "style": "ink_wash"}
        elif emotion in ["joyful", "excited", "happy"]:
            return {"category": "warm_joyful", "fluidity": 0.2, "breathing_hz": 0.3, "style": "particle_flow"}
        else:
            return {"category": "calm_healing", "fluidity": 0.5, "breathing_hz": 0.15, "style": "solid_breathe"}

    def _determine_spatial_color(self, aqi: float, kelvin: float, db_level: float) -> list:
        colors = []
        if db_level < 35: colors.append("blue")
        elif db_level > 65: colors.append("red")
        
        if aqi < 50: colors.append("green")
        else: colors.append("purple")
        
        if kelvin > 5000: colors.append("cyan")
        else: colors.append("orange")
        
        return colors if colors else ["blue", "green"]

    def push_to_display_panel(self, payload: dict):
        if not self.panel_ip:
            logging.warning("DISPLAY_PANEL_IP 未配置。仅在终端输出渲染蓝图。")
            return json.dumps({"status": "simulated", "render_blueprint": payload}, ensure_ascii=False)
        url = f"http://{self.panel_ip}:8080/api/v1/render/hanzi_palette"
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='POST')
            with urllib.request.urlopen(req, timeout=3) as response:
                return json.dumps({"status": "success", "message": "Ambient shift applied."})
        except Exception as e:
            return json.dumps({"status": "error", "message": f"Push failed: {str(e)}"})

    def process_spatial_telemetry(self, args: dict):
        temp = float(args.get("temperature", 24.0))
        db_level = float(args.get("acoustic_db", 35.0))
        kelvin = float(args.get("light_kelvin", 4000.0))
        aqi = float(args.get("air_aqi", 20.0))
        emotion = args.get("emotion", "calm")
        
        logging.info(f"📥 提取空间数据 -> Temp:{temp}C, DB:{db_level}, Kelvin:{kelvin}, AQI:{aqi}, Emotion:{emotion}")

        antonym_state = self._evaluate_antonym_logic(temp, db_level)
        empathic_state = self._evaluate_empathic_resonance(emotion)
        mood_content = self.local_db.query(empathic_state["category"])
        spectrum = self._determine_spatial_color(aqi, kelvin, db_level)

        payload = {
            "protocol": "S2-Spatial-Palette-V3",
            "theme": self.theme,
            "ambient_content": {
                "primary_hanzi": mood_content["hanzi"],
                "poetic_caption": mood_content["poetry"],
                "color_spectrum": spectrum
            },
            "dialectical_physics": antonym_state,
            "morphological_resonance": {
                "render_style": empathic_state["style"],
                "stroke_fluidity": empathic_state["fluidity"],
                "breathing_frequency": empathic_state["breathing_hz"]
            }
        }

        logging.info(f"🎨 空间调色盘矩阵生成完毕:\n{json.dumps(payload, ensure_ascii=False, indent=2)}")
        return self.push_to_display_panel(payload)

if __name__ == "__main__":
    engine = S2SpatialRenderEngine()
    try:
        if len(sys.argv) > 1:
            input_args = json.loads(sys.argv[1])
            result = engine.process_spatial_telemetry(input_args)
            print(result)
        else:
            mock_telemetry = {"temperature": 28.0, "acoustic_db": 45.0, "light_kelvin": 3000.0, "air_aqi": 15.0, "emotion": "fatigued"}
            result = engine.process_spatial_telemetry(mock_telemetry)
            print(result)
    except Exception as e:
        logging.error(f"Fatal execution error: {str(e)}")
        print(json.dumps({"status": "fatal", "error": str(e)}))