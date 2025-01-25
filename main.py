import subprocess
import time

# USIエンジンのパス
engine_path = "C:\\Users\\hikar\\yaneuraou\\YaneuraOu_NNUE-tournament-clang++-avx2.exe"

try:
    engine = subprocess.Popen(engine_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    print("✅ 将棋エンジンを起動しました")
except FileNotFoundError:
    print("❌ エンジンのパスが正しくありません！")
    exit()
except Exception as e:
    print(f"❌ エンジン起動エラー: {e}")
    exit()

def send_command(cmd):
    """エンジンにコマンドを送る"""
    print(f"📝 コマンド送信: {cmd}")
    engine.stdin.write(cmd + "\n")
    engine.stdin.flush()

def read_output(timeout=10):
    """エンジンの出力を一定時間内で取得"""
    start_time = time.time()
    while True:
        if time.time() - start_time > timeout:
            print("⚠️ 応答がありません")
            return None
        line = engine.stdout.readline().strip()
        if line:
            print(f"🔹 {line}")  # 出力を表示
        if "usiok" in line or "readyok" in line or "bestmove" in line:
            return line

# ① USIエンジンの起動確認
send_command("usi")
response = read_output()

if response is None:
    print("❌ エンジンが応答しませんでした")
    engine.terminate()
    exit()

# ② USIオプションを設定
send_command("setoption name EvalDir value C:\\Users\\hikar\\yaneuraou\\eval")
send_command("setoption name USI_OwnBook value false")  # 定跡機能を無効化
send_command("setoption name MultiPV value 1")  # MultiPV を1に設定
send_command("setoption name USI_Hash value 256")  # メモリ使用量を削減

# ③ エンジンの準備確認
send_command("isready")
response = read_output()
if response is None:
    print("❌ エンジンが準備できません")
    engine.terminate()
    exit()

print("✅ エンジンの起動確認OK！")

# ④ 初期局面をセット
send_command("position startpos")

# ⑤ 10手先まで読む → 無制限に探索して数秒後に停止
send_command("go infinite")
time.sleep(3)  # 3秒間計算を続ける
send_command("stop")  # 探索を強制停止

# ⑥ 指し手を取得
best_move = read_output(timeout=10)
if best_move is not None:
    print("✅ エンジンの指し手:", best_move)

# ⑦ エンジンを終了
send_command("quit")
engine.terminate()
print("✅ エンジンを終了しました")
