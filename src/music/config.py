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

# ========= 音名 / ボイシング =========
NOTE = dict(C=60, D=62, E=64, F=65, G=67, A=69, B=71)

VOICINGS = {
    "C":  [52, 55, 60, 64],
    "G7": [50, 55, 59, 62],
    "F":  [53, 57, 60, 65],
    "Am": [57, 60, 64, 69],
    "E7": [52, 56, 59, 64],
    "Gm7":[50, 53, 58, 62],
    "C7": [48, 52, 55, 58],
}

# ========= 進行プリセット =========
PROGRESSIONS = {
    # きらきら星向け（素直）
    "twinkle": ["C","G7","C","G7", "F","C","G7","C", "G7","F","C","G7", "C","G7","C","C"],
    # 丸サ進行（IVMaj7→III7→VIm7→Vm7→I7）をポップ寄りに：Fmaj7 E7 Am7 Gm7 C7
    "marusa":  ["F","E7","Am","Gm7","C7","F","E7","Am","Gm7","C7","F","E7","Am","Gm7","C7","F"],
    # J-POPで多い 1-5-6-4
    "pop1541": ["C","G7","Am","F"]*4,
    # 6-4-1-5（J-POPのしっとり系で定番）
    "sad6415": ["Am","F","C","G"] * 4,
}

# ========= ドラムノート（GM） =========
KICK = 36; SNARE = 38; HH_C = 42; HH_O = 46; CRASH = 49

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

    # group6 = happy + (anger, fear): 激情
    # 高揚 + 攻撃性。速め＆前のめり、歪みギター＋推進ベース、ドラム密度高。
    "group6": {
        "bpm": 140, "swing": 0.02, "key_shift": +1, "progression": "pop1541",
        "vol": {"melody":124, "chord":72, "guitar":110, "bass":116, "strings":90, "brass":96},
        "drum_energy": 3, "drum_hat_div": 16, "drum_fill_rate": 2,
        "bass_style": "drive", "melody_oct": +12,
        "vel_scale": {"melody":1.12, "chord":0.82, "guitar":1.18, "bass":1.15, "brass":1.05},
        "guitar_patch": ("dist", 30),
    },

    # group7 = happy + (sad, disgust, contempt): 複雑な心境
    # 明暗が同居。中速、スイング少し、和声は切なめ 6-4-1-5。
    "group7": {
        "bpm": 96, "swing": 0.10, "key_shift": -1, "progression": "sad6415",
        "vol": {"melody":120, "chord":78, "guitar":88, "bass":106, "strings":90, "brass":88},
        "drum_energy": 1, "drum_hat_div": 16, "drum_fill_rate": 1,
        "bass_style": "pump", "melody_oct": 0,
        "vel_scale": {"melody":1.05, "chord":0.92, "guitar":0.95, "bass":1.00, "brass":0.90},
        "guitar_patch": ("clean", 27),
    },

    # group8 = happy + surprise: サプライズ成功
    # 明るく弾む。速め、32分ハットでキラキラ、フィル多め、上方転調寄り。
    "group8": {
        "bpm": 128, "swing": 0.12, "key_shift": +3, "progression": "pop1541",
        "vol": {"melody":126, "chord":72, "guitar":96, "bass":110, "strings":90, "brass":98},
        "drum_energy": 2, "drum_hat_div": 32, "drum_fill_rate": 2,
        "bass_style": "drive", "melody_oct": +12,
        "vel_scale": {"melody":1.20, "chord":0.82, "guitar":1.02, "bass":1.06, "brass":1.06},
        "guitar_patch": ("clean", 27),
    },

    # group9 = (anger, fear) + (sad, disgust, contempt): 叱責
    # 厳しさと重さ。遅め〜中速、低め転調、スネア強め・フィル控えめ、どっしり。
    "group9": {
        "bpm": 84, "swing": 0.02, "key_shift": -4, "progression": "marusa",
        "vol": {"melody":112, "chord":68, "guitar":86, "bass":118, "strings":90, "brass":92},
        "drum_energy": 2, "drum_hat_div": 16, "drum_fill_rate": 0,
        "bass_style": "pump", "melody_oct": -12,
        "vel_scale": {"melody":0.98, "chord":0.80, "guitar":0.95, "bass":1.18, "brass":1.00},
        "guitar_patch": ("dist", 30),
    },

    # group10 = (anger, fear) + surprise: 突然の雷
    # 瞬間的な強打。速い・直進、スイング無し、ハット細かくフィル多め、ブラス強調。
    "group10": {
        "bpm": 136, "swing": 0.00, "key_shift": +2, "progression": "pop1541",
        "vol": {"melody":120, "chord":68, "guitar":112, "bass":116, "strings":90, "brass":104},
        "drum_energy": 3, "drum_hat_div": 32, "drum_fill_rate": 2,
        "bass_style": "drive", "melody_oct": 0,
        "vel_scale": {"melody":1.02, "chord":0.80, "guitar":1.22, "bass":1.15, "brass":1.18},
        "guitar_patch": ("dist", 30),
    },

    # group11 = (sad, disgust, contempt) + surprise: 悪い知らせ
    # 静かな落差。遅め、スイング少し、フィル無し、低め転調、メロ下オクターブ。
    "group11": {
        "bpm": 72, "swing": 0.08, "key_shift": -5, "progression": "sad6415",
        "vol": {"melody":110, "chord":64, "guitar":78, "bass":100, "strings":90, "brass":84},
        "drum_energy": 0, "drum_hat_div": 8, "drum_fill_rate": 0,
        "bass_style": "pump", "melody_oct": -12,
        "vel_scale": {"melody":0.95, "chord":0.75, "guitar":0.85, "bass":0.96, "brass":0.85},
        "guitar_patch": ("clean", 27),
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


mapping = {
    ("happy", None):    "group1",
    ("happy", "happy"):    "group1",
    ("happy", "neutral"):    "group1",

    ("anger", None):    "group2",
    ("fear", None):     "group2",
    ("anger", "anger"):    "group2",
    ("fear", "fear"):     "group2",
    ("anger", "neutral"):    "group2",
    ("fear", "neutral"):     "group2",

    ("sad", None):      "group3",
    ("disgust", None):  "group3",
    ("contempt", None): "group3",
    ("sad", "sad"):      "group3",
    ("disgust", "disgust"):  "group3",
    ("contempt", "contempt"): "group3",
    ("sad", "neutral"):      "group3",
    ("disgust", "neutral"):  "group3",
    ("contempt", "neutral"): "group3",

    ("surprise", None): "group4",
    ("surprise", "surprise"): "group4",
    ("surprise", "neutral"): "group4",

    ("neutral", None):  "group5",
    ("neutral", "neutral"):  "group5",
    (None, None):       "group5",

    # 1+2, 激情
    ("happy", "anger"): "group6",
    ("happy", "fear"):  "group6",

    # 1+3, 複雑な心境
    ("happy", "sad"):      "group7",
    ("happy", "disgust"):  "group7",
    ("happy", "contempt"): "group7",

    # 1+4, サプライズ成功
    ("happy", "surprise"): "group8",

    # 2+3, 叱責
    ("anger", "sad"):      "group9",
    ("anger", "disgust"):  "group9",
    ("anger", "contempt"): "group9",
    ("fear", "sad"):      "group9",
    ("fear", "disgust"):  "group9",
    ("fear", "contempt"): "group9",

    # 2+4, 突然の雷
    ("anger", "surprise"): "group10",
    ("fear", "surprise"):  "group10",

    # 3+4, 悪い知らせ
    ("sad", "surprise"):      "group11",
    ("disgust", "surprise"):  "group11",
    ("contempt", "surprise"): "group11",

# group1: happy
# group2: anger, fear
# group3: sad, disgust, contempt
# group4: surprise
# group5: neutral
}