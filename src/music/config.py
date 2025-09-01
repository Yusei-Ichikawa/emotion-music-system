# ========= 基本設定（初期値） =========
SOUNDFONT_PATH = "../../FluidR3_GM/FluidR3_GM.sf2"
INITIAL_BPM   = 100
INITIAL_SWING = 0.00
MASTER_GAIN   = 0.85
HUMAN_T_MS    = 4
HUMAN_VEL     = 4
LEAD_SEC      = 0.15           # 未来に予約（同時性向上）
BAR_BEATS     = 4.0
GLIDE_ALPHA = 0.6            # ボリューム・グライドの速さ（0.0〜1.0）

# --- チャンネル割り当て ---
CH_MELODY = 0   # ピアノ（メロディ専用）
CH_CHORD  = 3   # ピアノ（コード伴奏）
CH_GUIT   = 1   # ギター
CH_BASS   = 2   # ベース
CH_DRUM   = 9   # ドラム（GM：Ch.10, Bank128）
CH_STRINGS = 4  # ストリングス
CH_BRASS  = 5  # ブラス

# 感情グループ → パラメータプリセット
EMOTION_PRESETS = {
    # group1: happy（明るく速く・上へ持ち上げ・派手）
    "group1": {
        "bpm": 130,
        "swing": 0.04,
        "key_shift": +2,
        # "key_shift": 0,          # キーはそのまま
        "vol": {"melody": 130, "chord": 100, "guitar": 70, "bass": 70, "strings": 90, "brass": 160},
        "drum_energy": 3,          # ← 最大
        "drum_hat_div": 16,        # 32分ハイハットでキラキラ
        "drum_fill_rate": 2,       # フィル多め
        "bass_style": "drive",     # 8分で推進
        "melody_oct": +12,         # メロディ1オクターブ↑
        "melody_oct": 0,          # メロディはオクターブそのまま
        "vel_scale": {"melody":1.15,"chord":0.85,"guitar":1.05,"bass":1.10},
        "guitar_patch": ("clean", 27),
        "progression": "pop1541",  # 明るい進行に変更
    },
    # group2: anger, fear（攻撃的・速く・低め・歪み）
    "group2": {
        "bpm": 110,
        "swing": 0.00,
        "key_shift": -5,
        "key_shift": 0,          # キーはそのまま
        "vol": {"melody": 90, "chord": 70, "guitar": 100, "bass": 120, "strings": 70, "brass": 70},
        "drum_energy": 3,
        "drum_hat_div": 8,
        "drum_fill_rate": 2,
        "bass_style": "drive",
        "melody_oct": -12,
        "vel_scale": {"melody":1.05,"chord":0.80,"guitar":1.20,"bass":1.20},
        "guitar_patch": ("clean", 27),   # ← ディストーション
        "progression": "marusa",  # 暗めの進行に変更
    },
    # group3: sad, disgust, contempt（遅く・しっとり・下げる・極薄ドラム）
    "group3": {
        "bpm": 80,
        "swing": 0.10,
        "key_shift": -7,
        # "key_shift": 0,          # キーはそのまま
        "vol": {"melody": 112, "chord": 64, "guitar": 78, "bass": 96, "strings": 120, "brass": 90},
        "drum_energy": 0,
        "drum_hat_div": 8,
        "drum_fill_rate": 0,
        "bass_style": "pump",      # 4分主体で重く
        "melody_oct": -12,         # メロディ1オクターブ↓
        "melody_oct": 0,          # メロディはオクターブそのまま
        "vel_scale": {"melody":0.95,"chord":0.75,"guitar":0.80,"bass":0.90},
        "guitar_patch": ("clean", 27),
        "progression": "sad6415"
    },
    # group4: surprise（急に持ち上げる・明るくスピードアップ）
    "group4": {
        "bpm": 140,
        "swing": 0.12,
        "key_shift": +5,
        # "key_shift": 0,          # キーはそのまま
        "vol": {"melody": 126, "chord": 74, "guitar": 98, "bass": 140, "strings": 80, "brass": 120},
        "drum_energy": 2,
        "drum_hat_div": 16,
        "drum_fill_rate": 2,
        "bass_style": "drive",
        "melody_oct": +12,
        "melody_oct": 0,          # メロディはオクターブそのまま
        "vel_scale": {"melody":1.20,"chord":0.80,"guitar":1.05,"bass":1.05},
        "guitar_patch": ("clean", 27),
        "progression": "pop1541",
    },
    # group5: neutral（基準を少しだけ整えたノーマル）
    "group5": {
        "bpm": INITIAL_BPM,
        "swing": 0.00,
        "key_shift": 0,
        "vol": {"melody": 120, "chord": 80, "guitar": 90, "bass": 110, "strings": 100, "brass": 100},
        "drum_energy": 1,
        "drum_hat_div": 8,
        "drum_fill_rate": 1,
        "bass_style": "drive",
        "melody_oct": 0,
        "vel_scale": {"melody":1.00,"chord":1.00,"guitar":1.00,"bass":1.00},
        "guitar_patch": ("clean", 27),
        "progression": "twinkle",
    },
}

def make_initial_state():
    s = {
        "bpm": INITIAL_BPM,
        "swing": INITIAL_SWING,
        "key_shift": 0,                   # 半音移調（0=そのまま）
        "progression_name": "twinkle",    # デフォルト進行

        # 各パート音量
        "mel_vol": 120,
        "chd_vol": 80,
        "gtr_vol": 90,
        "bass_vol": 150,
        "strings_vol": 80,  # ストリングス
        "brass_vol": 80,    # ブラス

        # 感情系
        "emotion_group": "neutral",  # 現在の感情
        "drum_energy": 1,            # 0=静か, 1=普通, 2=元気

        # 実効テンポと次小節反映用
        "active_bpm": INITIAL_BPM,   # 実効テンポ
        "pending_bpm": None,         # 次小節で適用するBPM（絶対値）
        "pending_prog": None,        # 次小節で適用する進行名
        "pending_key": None,         # 次小節で適用する移調

        # 極端プリセット用ノブ
        "melody_oct": 0,             # メロディのオクターブ移動（±12など）
        "vel_scale": {               # 各パートのベロシティ倍率
            "melody": 1.0, "chord": 1.0, "guitar": 1.0, "bass": 1.0
        },
        "drum_hat_div": 16,          # ハイハット分解能 8 / 16 / 32
        "drum_fill_rate": 1,         # 0=無し, 1=普通, 2=多め
        "bass_style": "drive",       # "drive"(8分), "pump"(4分重), "walk"(ｳｫｰｸ)
        "guitar_patch": ("clean", 27),  # ("clean",27) or ("dist",30 など)

        # ボリューム・グライド
        "target_vol": {},            # 目標値（感情切替や vol コマンドで更新）
        "vol_glide_alpha": GLIDE_ALPHA,      # 1小節ごとにどれだけ近づくか（0.0〜1.0）
    }
    # 他キーに依存する派生値を最後にまとめて定義
    s["active_vol"] = {
        "melody": s["mel_vol"],
        "chord":  s["chd_vol"],
        "guitar": s["gtr_vol"],
        "bass":   s.get("bass_vol", 110),
        # 使っている方だけあればOK（両方あっても可）
        "strings": s.get("strings_vol", 95) if 'CH_STRINGS' in globals() else None,
        "brass":   s.get("brass_vol",   95) if 'CH_BRASS'   in globals() else None,
    }
    return s