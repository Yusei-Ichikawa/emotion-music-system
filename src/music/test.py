import time
import heapq
import threading
import random
import fluidsynth
import sys
import cv2

import music.config as state_file
from music.config import *


# ========= FluidSynth 初期化 =========
fs = fluidsynth.Synth()
fs.start(driver="coreaudio")  # Windows: "dsound", Linux: "alsa"
sfid = fs.sfload(SOUNDFONT_PATH)

# --- 音色 ---
fs.program_select(CH_MELODY, sfid, 0,   0)   # Acoustic Grand
fs.program_select(CH_CHORD,  sfid, 0,   0)   # Acoustic Grand
fs.program_select(CH_GUIT,   sfid, 0,  27)   # Clean Guitar
fs.program_select(CH_BASS,   sfid, 0,  33)   # Finger Bass
fs.program_select(CH_DRUM,   sfid, 128, 0)   # Standard Drum Kit
fs.program_select(CH_STRINGS, sfid, 0, 48)  # Strings Ensemble
fs.program_select(CH_BRASS, sfid, 0, 61) # Trumpet

# --- ミキサー（CC） ---
def set_channel_volumes(mel=130, chord=80, guit=80, bass=110, strings=100, brass=100):
    fs.cc(CH_MELODY, 7, mel)
    fs.cc(CH_CHORD,  7, chord)
    fs.cc(CH_GUIT,   7, guit)
    fs.cc(CH_BASS,   7, bass)
    fs.cc(CH_STRINGS, 7, strings)
    fs.cc(CH_BRASS,  7, brass)
    for ch in [CH_MELODY, CH_CHORD, CH_GUIT, CH_BASS, CH_STRINGS, CH_BRASS]:
        fs.cc(ch, 10, 64)   # Pan
        fs.cc(ch, 91, 35)   # Reverb send
        fs.cc(ch, 93, 15)   # Chorus send

fs.setting("synth.gain", MASTER_GAIN)
set_channel_volumes()

# ========= 共有パラメータ（ロック保護） =========
state_lock = threading.RLock()
state = state_file.make_initial_state()

def _send_cc7(part: str, value: int):
    """パート名→チャンネルにマップしてCC7送信"""
    value = max(0, min(127, int(value)))
    if part == "melody":
        fs.cc(CH_MELODY, 7, value)
    elif part == "chord":
        fs.cc(CH_CHORD, 7, value)
    elif part == "guitar":
        fs.cc(CH_GUIT, 7, value)
    elif part == "bass":
        fs.cc(CH_BASS, 7, value)
    elif part == "strings" and 'CH_STRINGS' in globals():
        fs.cc(CH_STRINGS, 7, value)
    elif part == "brass" and 'CH_BRASS' in globals():
        fs.cc(CH_BRASS, 7, value)

def get_spb_active():
    return 60.0 / state["active_bpm"]

def get_bar_sec_active():
    return get_spb_active() * BAR_BEATS

def get_spb():
    with state_lock:
        return 60.0 / state["bpm"]

def get_bar_sec():
    return get_spb() * BAR_BEATS

# ========= ユーティリティ =========
def humanize_time():
    return random.randint(-HUMAN_T_MS, HUMAN_T_MS) / 1000.0

def humanize_vel(v):
    return max(1, min(127, v + random.randint(-HUMAN_VEL, HUMAN_VEL)))

def swing_offset(start_beats):
    with state_lock:
        SWING = state["swing"]
    frac = start_beats - int(start_beats)
    if abs(frac - 0.5) < 1e-7:       # 8分裏
        return get_spb() * SWING
    return 0.0

# ========= スケジューラ（カウンタ付きヒープ） =========
_event_q = []  # (abs_time, counter, fn, args)
_event_cv = threading.Condition()
_event_counter = 0
_running = True

def scheduler_worker():
    """# 予約イベントを時刻どおりに実行"""
    while _running:
        with _event_cv:
            while _running and (not _event_q or _event_q[0][0] > time.perf_counter()):
                timeout = None
                if _event_q:
                    timeout = max(0.0, _event_q[0][0] - time.perf_counter())
                _event_cv.wait(timeout=timeout)
            if not _running:
                break
            t, _, fn, args = heapq.heappop(_event_q)
        now = time.perf_counter()
        if t > now:
            time.sleep(t - now)
        try:
            fn(*args)
        except Exception:
            pass

def schedule_at(abs_time, fn, *args):
    """# 指定“絶対時刻(秒)”に関数を実行するよう登録"""
    global _event_counter
    with _event_cv:
        _event_counter += 1
        heapq.heappush(_event_q, (abs_time, _event_counter, fn, args))
        _event_cv.notify()

_sched_th = threading.Thread(target=scheduler_worker, daemon=True)
_sched_th.start()

# ========= ノート制御 =========
def _note_on(ch, note, vel): fs.noteon(ch, note, vel)
def _note_off(ch, note):     fs.noteoff(ch, note)

def schedule_note(ch, note, vel, start_beats, length_beats, bar_start_abs, swing=True):
    """
    # ノートを“絶対時刻”で予約（感情ノブ：vel倍率/メロディOct反映）
    """
    with state_lock:
        ks = state["key_shift"]
        spb = 60.0 / state["active_bpm"]
        mel_oct = state["melody_oct"]
        scales = state["vel_scale"]

    start = bar_start_abs + start_beats * spb + (swing_offset(start_beats) if swing else 0.0) + humanize_time()
    end   = start + (length_beats * spb)

    # ベロシティ倍率（感情）
    scale = 1.0
    if ch == CH_MELODY: scale = scales["melody"]
    elif ch == CH_CHORD: scale = scales["chord"]
    elif ch == CH_GUIT:  scale = scales["guitar"]
    elif ch == CH_BASS:  scale = scales["bass"]
    elif ch == CH_STRINGS: scale = scales.get("strings", 1.0)
    v2 = max(1, min(127, int(humanize_vel(vel) * scale)))

    # メロディだけオクターブ移動
    n2 = note + ks + (mel_oct if ch == CH_MELODY else 0)

    schedule_at(start, _note_on, ch, n2, v2)
    schedule_at(end,   _note_off, ch, n2)

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

# ========= 感情を導入 =========
def apply_emotion_group(gname: str):
    """# 感情グループのプリセットを状態に反映（次小節から有効・音色/音量は即時）"""
    if gname not in EMOTION_PRESETS:
        print(f"[emotion] unknown group: {gname}  (use: group1..group5)")
        return
    p = EMOTION_PRESETS[gname]
    if "progression" in p:
        state["pending_prog"] = p["progression"]
    with state_lock:
        # 次小節から反映する系
        state["pending_bpm"] = max(40, min(220, p["bpm"]))
        state["swing"] = max(0.0, min(0.5, p["swing"]))
        state["pending_key"] = max(-24, min(24, p["key_shift"]))
        state["emotion_group"] = gname
        state["drum_energy"] = p["drum_energy"]
        state["drum_hat_div"] = p["drum_hat_div"]
        state["drum_fill_rate"] = p["drum_fill_rate"]
        state["bass_style"] = p["bass_style"]
        state["melody_oct"] = int(p["melody_oct"])
        state["vel_scale"] = p["vel_scale"].copy()

        # 音量は即時反映
        v = p["vol"]
        state["mel_vol"], state["chd_vol"] = v["melody"], v["chord"]
        state["gtr_vol"], state["bass_vol"] = v["guitar"], v["bass"]
        state["strings_vol"], state["brass_vol"] = v["strings"], v["brass"]
        # 目標ボリュームをセット（未使用パートは無視）
        state["target_vol"] = {
            "melody": state["mel_vol"],
            "chord":  state["chd_vol"],
            "guitar": state["gtr_vol"],
            "bass":   state["bass_vol"],
            "strings": state["strings_vol"],
            "brass": state["brass_vol"],
        }
        # fs.cc(CH_MELODY, 7, state["mel_vol"])
        # fs.cc(CH_CHORD,  7, state["chd_vol"])
        # fs.cc(CH_GUIT,   7, state["gtr_vol"])
        # fs.cc(CH_BASS,   7, state["bass_vol"])
        # fs.cc(CH_STRINGS, 7, state["strings_vol"])
        # fs.cc(CH_BRASS,  7, state["brass_vol"])

        # ギターパッチ変更（即時）
        name, prog = p["guitar_patch"]
        fs.program_select(CH_GUIT, sfid, 0, prog)

        # cur_bpm = state.get("active_bpm", state["bpm"])
        # print(f"[emotion] -> {gname}  (BPM now={cur_bpm:.1f}, next={state['pending_bpm']}, "
        #     f"swing={state['swing']}, key next={state['pending_key']}, guitar={name}, prog={state["pending_prog"]})",)

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

# ========= 各パート 1小節 ========
# --- ドラム：8ビート＋軽い16分＆4小節フィル ---
def schedule_drum_bar(bar_idx, bar_start_abs):
    """# ドラム：energy / hat_div / fill_rate に応じて過激に変化"""
    with state_lock:
        energy = state["drum_energy"]   # 0..3
        hat_div = state["drum_hat_div"] # 8/16/32
        fill_rate = state["drum_fill_rate"]  # 0..2

    # ハイハット
    steps = 8 if hat_div == 8 else 16 if hat_div == 16 else 32
    unit = 4.0 / steps  # 1小節=4拍を steps 分割
    for i in range(steps):
        t = i * unit
        strong = (i % (steps//4) in [0, (steps//8)])  # 表を強め
        vel = 68 + (6 if strong else 0) + (4 if energy >= 2 else 0)
        schedule_note(CH_DRUM, HH_C, vel, t, min(0.10, unit*0.8), bar_start_abs, swing=False)

    # キック（energyで増量）
    kicks = [0.0, 2.0]
    if energy >= 1: kicks += [0.75, 2.75]
    if energy >= 2: kicks += [1.5, 3.5]
    if energy >= 3: kicks += [0.25, 1.0, 2.25, 3.0]
    for t in sorted(set(kicks)):
        schedule_note(CH_DRUM, KICK, 110 if t in [0.0,2.0] else 100, t, 0.05, bar_start_abs, swing=False)

    # スネア
    sn = 98 if energy <= 1 else 104
    for t in [1.0, 3.0]:
        schedule_note(CH_DRUM, SNARE, sn, t, 0.05, bar_start_abs, swing=False)
    if energy >= 1:
        for t in [0.75, 2.75]:
            schedule_note(CH_DRUM, SNARE, 44 if energy == 1 else 50, t, 0.03, bar_start_abs, swing=False)

    # フィル
    if fill_rate >= 1 and (bar_idx + 1) % 4 == 0:
        # tom 3連 + openHH
        for t, note, v in [(3.25, 45, 92), (3.5, 47, 96), (3.75, 50, 102)]:
            schedule_note(CH_DRUM, note, v, t, 0.08, bar_start_abs, swing=False)
        if fill_rate == 2:
            schedule_note(CH_DRUM, HH_O, 96, 3.75, 0.25, bar_start_abs, swing=False)

# --- ベース：8分ドライブ（ルート/5度/オクターブ） ---
def schedule_bass_bar(chord_name, bar_start_abs):
    """# ベース：drive/pump/walk を感情で切替"""
    roots = {
        "C": NOTE["C"]-12, "G7": NOTE["G"]-12, "F": NOTE["F"]-12,
        "Am": NOTE["A"]-12, "E7": NOTE["E"]-12, "Gm7": NOTE["G"]-12, "C7": NOTE["C"]-12,
    }
    r = roots.get(chord_name, NOTE["C"]-12)
    fifth, octv = r+7, r+12
    with state_lock:
        style = state["bass_style"]

    if style == "pump":  # 4分でどっしり
        for t, n, v in [(0.0,r,110),(1.0,r,104),(2.0,r,106),(3.0,fifth,102)]:
            schedule_note(CH_BASS, n, v, t, 0.95, bar_start_abs)
    elif style == "walk":  # 簡易ウォーク
        seq = [r, r+2, fifth, r+9]  # ルート→2度→5度→6(経過)
        for i, n in enumerate(seq):
            schedule_note(CH_BASS, n, 98+(i%2)*6, i*1.0, 0.95, bar_start_abs)
    else:  # "drive" 8分推進
        pats = [(0.0,r,108),(0.5,fifth,96),(1.0,r,102),(1.5,octv,98),
                (2.0,r,106),(2.5,fifth,96),(3.0,r,100),(3.5,r+(11 if random.random()<0.5 else -1),94)]
        for t, n, v in pats:
            schedule_note(CH_BASS, n, v, t, 0.48, bar_start_abs)

# --- ギター：16分カッティング＋2/4拍ストラム ---
def schedule_guitar_bar(chord_name, bar_start_abs):
    """# ギター：16分カッティング＋薄いストローク"""
    vo = VOICINGS.get(chord_name, VOICINGS["C"])
    arp = sorted([n for n in vo if 52 <= n <= 72]) or vo[:3]
    for i in range(16):
        t = i * 0.25
        n = arp[i % len(arp)]
        v = 82 if (i % 4 in [1,3]) else 86
        schedule_note(CH_GUIT, n, v, t, 0.10, bar_start_abs)
    micro = 0.012 / get_spb()
    for t in [1.0, 3.0]:
        triad = arp[:3]
        for j, n in enumerate(triad):
            schedule_note(CH_GUIT, n, 90 + j*3, t + j*micro, 0.20, bar_start_abs)

# --- ピアノ：主旋律（きらきら星） ---
def schedule_melody_bar(bar_idx, bar_start_abs):
    """# ピアノ：きらきら星の主旋律（C=60基準, A A B A）"""
    C = NOTE["C"]; D = NOTE["D"]; E = NOTE["E"]; F = NOTE["F"]; G = NOTE["G"]; A = NOTE["A"]
    bars = {
        0:  [(0.0,C,1,106),(1.0,C,1,106),(2.0,G,1,104),(3.0,G,1,104)],
        1:  [(0.0,A,1,106),(1.0,A,1,106),(2.0,G,2,110)],
        2:  [(0.0,F,1,102),(1.0,F,1,102),(2.0,E,1,102),(3.0,E,1,102)],
        3:  [(0.0,D,1,100),(1.0,D,1,100),(2.0,C,2,112)],
        4:  [(0.0,G,1,106),(1.0,G,1,106),(2.0,F,1,102),(3.0,F,1,102)],
        5:  [(0.0,E,1,102),(1.0,E,1,102),(2.0,D,2,106)],
        6:  [(0.0,G,1,106),(1.0,G,1,106),(2.0,F,1,102),(3.0,F,1,102)],
        7:  [(0.0,E,1,102),(1.0,E,1,102),(2.0,D,2,106)],
        8:  [(0.0,C,1,108),(1.0,C,1,108),(2.0,G,1,104),(3.0,G,1,104)],
        9:  [(0.0,A,1,108),(1.0,A,1,108),(2.0,G,2,112)],
        10: [(0.0,F,1,104),(1.0,F,1,104),(2.0,E,1,104),(3.0,E,1,104)],
        11: [(0.0,D,1,102),(1.0,D,1,102),(2.0,C,2,114)],
        12: [(0.0,C,1,110),(1.0,C,1,110),(2.0,G,1,106),(3.0,G,1,106)],
        13: [(0.0,A,1,110),(1.0,A,1,110),(2.0,G,2,114)],
        14: [(0.0,F,1,106),(1.0,F,1,106),(2.0,E,1,106),(3.0,E,1,106)],
        15: [(0.0,D,1,106),(1.0,D,1,106),(2.0,C,2,118)],
    }
    for (t, n, l, v) in bars[bar_idx % 16]:
        schedule_note(CH_MELODY, n, v, t, l, bar_start_abs, swing=False)

# --- ピアノ：コード伴奏（薄め） ---
def schedule_chord_bar(chord_name, bar_start_abs):
    """# ピアノ：ブロークン気味の薄い伴奏"""
    voice = VOICINGS.get(chord_name, VOICINGS["C"])
    voice = sorted([n for n in voice if 52 <= n <= 72])[:4] or voice
    def chord(start, length, vel, notes):
        for n in notes:
            schedule_note(CH_CHORD, n, vel, start, length, bar_start_abs)
    chord(0.0, 0.22, 78, [min(voice)])
    chord(0.25,0.18, 76, [sorted(voice)[1]])
    chord(0.5, 0.26, 82, voice)
    chord(2.0, 0.36, 84, voice[:3])
    chord(3.5, 0.22, 80, [max(voice)])

# --- ストリングス：パッド的に和音を1小節伸ばす（低〜中域中心） ---
def schedule_strings_bar(chord_name, bar_start_abs):
    """# ストリングス：パッド的に和音を1小節伸ばす（低〜中域中心）"""
    # 既存の VOICINGS から取得（なければ C をfallback）
    vo = VOICINGS.get(chord_name, VOICINGS.get("C", [52,55,60,64]))
    # 低〜中域の3音程度に間引き
    pad = sorted([n for n in vo if 55 <= n <= 76])[:3] or vo[:3]
    # 少しアタックをずらして重ね感を出す
    for j, n in enumerate(pad):
        start = 0.0 + j * (0.015 / (60.0 / state.get("active_bpm", state["bpm"])))  # 約15msずつ
        schedule_note(CH_STRINGS, n, 90, start, 4.0, bar_start_abs, swing=False)

# --- ブラス：エネルギー低→サスティンPad、高→スタブ（アクセント） ---
def schedule_brass_bar(chord_name, bar_start_abs):
    """# ブラス：エネルギー低→サスティンPad、高→スタブ（アクセント）"""
    # コードの中域3音を抽出
    vo = VOICINGS.get(chord_name, VOICINGS.get("C", [52, 55, 60, 64]))
    mids = sorted([n for n in vo if 55 <= n <= 79])[:3] or vo[:3]

    with state_lock:
        energy = state.get("drum_energy", 1)   # 0..3
        spb = 60.0 / state.get("active_bpm", state.get("bpm", 100))

    if energy <= 1:
        # ---- サスティンPad：1小節伸ばし（軽いアタックずらし）----
        micro = 0.015 / spb   # 約15ms を拍に換算
        for j, n in enumerate(mids):
            schedule_note(CH_BRASS, n, 88 + j*2, 0.0 + j*micro, 4.0, bar_start_abs, swing=False)
    else:
        # ---- スタブ：拍頭で短く強く（1拍＆3拍は強め）----
        hits = [0.0, 1.0, 2.0, 3.0]
        for t in hits:
            base_vel = 102 if t in (1.0, 3.0) else 96
            # 3和音を数msのスプレッドで重ねる
            micro = 0.010 / spb
            for j, n in enumerate(mids):
                schedule_note(CH_BRASS, n, base_vel + j*2, t + j*micro, 0.28, bar_start_abs, swing=False)
            # サビっぽくしたい時のオクターブ補強（軽め）
            if t in (1.0, 3.0):
                top = max(mids) + 12
                schedule_note(CH_BRASS, top, base_vel-6, t + len(mids)*micro, 0.22, bar_start_abs, swing=False)

_PLAYER_THREAD = None
_STARTED = False

def _player_loop():
    # ========= 再生ループ =========
    base_time = time.perf_counter() + LEAD_SEC
    next_bar_start_abs = base_time
    bar_index = 0
    while _running:
        # ---- 小節頭：保留パラメータを“ここでだけ”実効値に反映 ----
        with state_lock:
            if state["pending_bpm"] is None:
                alpha = state["vol_glide_alpha"]
                act = state["active_vol"]
                tgt = state.get("target_vol", {}) or {}
                # 対象パートを走査
                for part, cur in list(act.items()):
                    if cur is None:  # 未使用パート
                        continue
                    if part not in tgt:
                        # 目標が未設定なら今の値を目標とみなす
                        tgt_val = cur
                    else:
                        tgt_val = tgt[part]
                    new_val = int(round(cur + (tgt_val - cur) * alpha))
                    # クリップ & 保存
                    new_val = max(0, min(127, new_val))
                    act[part] = new_val
                    # CC7 送信（実効値を毎小節アップデート）
                    _send_cc7(part, new_val)
            # BPM（グライド版）
            if state["pending_bpm"] is not None:
                target = state["pending_bpm"]
                cur = state["active_bpm"]

                # 1小節で target に近づけるなら steps=1、数小節かけたいなら steps>1
                steps = 4   # 例：4拍かけて移行
                diff = (target - cur) / steps
                # 今回の小節ぶんだけ近づける
                new_bpm = cur + diff

                # alpha = 0.7  # 0.5〜0.9 推奨。大きいほど“速く”寄る
                # new_bpm = cur + (target - cur) * alpha

                # ほぼ到達したら確定
                if abs(target - new_bpm) < 0.5:
                    new_bpm = target
                    state["pending_bpm"] = None

                state["active_bpm"] = new_bpm
                state["bpm"] = int(new_bpm)  # 表示用
            # progression
            if state["pending_prog"] is not None:
                state["progression_name"] = state["pending_prog"]
                state["pending_prog"] = None
            # key
            if state["pending_key"] is not None:
                state["key_shift"] = state["pending_key"]
                state["pending_key"] = None

            prog_name = state["progression_name"]
            progression = PROGRESSIONS[prog_name]

        i = bar_index % len(progression)
        chord_name = progression[i]
        bar_start_abs = next_bar_start_abs

        # --- 全パートをこの小節にスケジュール ---
        schedule_drum_bar(bar_index, bar_start_abs)
        schedule_bass_bar(chord_name, bar_start_abs)
        schedule_guitar_bar(chord_name, bar_start_abs)
        schedule_melody_bar(i % 16, bar_start_abs)
        schedule_chord_bar(chord_name, bar_start_abs)
        schedule_strings_bar(chord_name, bar_start_abs)
        schedule_bass_bar(chord_name, bar_start_abs)

        # セクション頭でクラッシュ
        if i % 4 == 0:
            schedule_note(CH_DRUM, CRASH, 112, 0.0, 0.35, bar_start_abs)

        # ---- 次小節の開始時刻＝“今小節の開始”＋“今小節の長さ（実効BPM基準）” ----
        bar_sec = get_bar_sec_active()
        next_bar_start_abs = bar_start_abs + bar_sec

        # 小節終わりまで待機
        now = time.perf_counter()
        sleep_for = (bar_start_abs + bar_sec) - now
        if sleep_for > 0:
            time.sleep(sleep_for)

        bar_index += 1

def start_music():
    global _PLAYER_THREAD, _STARTED

    # 1) スケジューラ起動（1回だけでOK）
    _sched_th = threading.Thread(target=scheduler_worker, daemon=True)
    _sched_th.start()

    # 2) 実行フラグON
    with state_lock:
        state["running"] = True

    # 3) プレイヤースレッド開始（main.pyをブロックしない）
    _PLAYER_THREAD = threading.Thread(target=_player_loop, daemon=True)
    _PLAYER_THREAD.start()

def stop_music():
    state["running"] = False

def set_expression(most_common_expression, frame):
    if isinstance(most_common_expression, (list, tuple)):
        key = tuple(s.lower() if isinstance(s, str) else None for s in most_common_expression)
    else:
        key = (most_common_expression.lower(), None) if isinstance(most_common_expression, str) else (None, None)

    mapping = {
        ("happy", None):    "group1",
        ("anger", None):    "group2",
        ("fear", None):     "group2",
        ("sad", None):      "group3",
        ("disgust", None):  "group3",
        ("contempt", None): "group3",
        ("surprise", None): "group4",
        ("neutral", None):  "group5",
        (None, None):       "group5",
    }

    g = mapping.get(key)
    cv2.putText(frame, g, (600, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
    if g:
        apply_emotion_group(g)
    else:
        pass

if __name__ == "__main__":
    start_music()