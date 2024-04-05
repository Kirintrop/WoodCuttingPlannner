import time
import os
import tkinter as tk
from tkinter import filedialog



class Board:
    def __init__(self, width, height, board_id, x=0, y=0):
        self.width = width
        self.height = height
        self.board_id = board_id
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Board(w={self.width}, h={self.height}, id={self.board_id}, x={self.x}, y={self.y})"

def select_file():
    # Tkインスタンスを作成し、直後にウィンドウを隠す
    root = tk.Tk()
    root.withdraw()

    # ファイル選択ダイアログを表示
    file_path = filedialog.askopenfilename(
        title="ファイルを選択してください",
        filetypes=(("テキストファイル", "*.txt"), ("すべてのファイル", "*.*"))
    )
    return file_path


# 初期設定


# ファイル選択関数を呼び出し
cutlist_file_path = select_file()

# ファイル名（拡張子を除く）と拡張子を取得
base_name, _ = os.path.splitext(cutlist_file_path)

# 実行時間の計測開始
start_time = time.time()

# 出力ファイル名を生成
output_file_name = f"{base_name}.dxf"

cut_list = []  # カットリストを格納するための空のリストを初期化




def load_cutlist_from_file(file_path):
    """
    テキストファイルからカットリストを読み込み、リストとして返す。

    Args:
        file_path (str): カットリストが保存されているテキストファイルのパス。

    Returns:
        list of tuple: 読み込んだカットリスト。各要素は(width, height, quantity)の形式のタプル。
    """
    cutlist = []  # カットリストを格納するための空のリストを初期化
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 3:  # 幅、高さ、数量の3つのデータがあることを確認
                try:
                    width, height, quantity = map(int, parts)
                    cutlist.append((width, height, quantity))
                except ValueError:
                    print(f"データの形式が正しくありません: {line}")
    return cutlist


cut_list = load_cutlist_from_file(cutlist_file_path)


raw_board_size = (1820, 910)
# 原板ごとに1500mm下に移動
board_offset_y = -1500
# グレーに相当するACI値 (グレーは8)
gray_aci = 8

# 原板IDの表示高さ

ID_text_height =100
ID_text_align =250
Dim_text_height=25
Dim_text_align_origin=-100
Dim_text_align_product=-50




boards = []  # 残り板リスト
products = []  # 製品リスト
raw_board_id = 0

# カットリストから残りのカットリストを生成
remaining_cuts = []
for width, height, quantity in cut_list:
    for _ in range(quantity):
        remaining_cuts.append((width, height))
remaining_cuts.sort(key=lambda x: x[0] * x[1], reverse=True)

def add_new_raw_board():
    global raw_board_id
    boards.append(Board(raw_board_size[0], raw_board_size[1], raw_board_id))
    raw_board_id += 1

def cut_board():
    global boards, products
    if not remaining_cuts:
        return False  # カットするものがなければ終了
    for cut in list(remaining_cuts):
        for board in list(boards):
            if cut[0] <= board.width and cut[1] <= board.height:
                new_product = Board(cut[0], cut[1], board.board_id, board.x, board.y)
                products.append(new_product)
                remaining_cuts.remove(cut)
                # 残り板の更新
                boards.remove(board)
                if board.width > cut[0]:
                    # 縦に残った部分を追加
                    boards.append(Board(board.width - cut[0], board.height, board.board_id, board.x + cut[0], board.y))
                if board.height > cut[1]:
                    # 横に残った部分を追加
                    boards.append(Board(cut[0], board.height - cut[1], board.board_id, board.x, board.y + cut[1]))
                return True
    return False

def summarize_boards(boards):
    summary = {}
    for board in boards:
        key = (board.width, board.height)
        if key in summary:
            summary[key] += 1
        else:
            summary[key] = 1
    return summary

# 初期原板の追加
add_new_raw_board()

# カット処理
while remaining_cuts:
    if not cut_board():
        add_new_raw_board()

# 結果の出力
print(f"原板の数: {raw_board_id}")
print("製品リスト:")
for product in products:
    print(product)
print("残板リスト:")
for board in boards:
    print(board)

# 出力ファイル名を生成
output_file_name_txt = f"{base_name}_result.txt"

# 出力ファイルを開き、結果を書き込む
# 出力ファイルを開き、結果を書き込む
with open(output_file_name_txt, 'w') as file:
    file.write(f"原板の数: {raw_board_id}\n")
    file.write("製品リスト:\n")
    products_summary = summarize_boards(products)
    for (width, height), count in products_summary.items():
        file.write(f"サイズ: 幅 {width} x 高さ {height}, 枚数: {count}\n")
    file.write("残り板リスト:\n")
    boards_summary = summarize_boards(boards)
    for (width, height), count in boards_summary.items():
        file.write(f"サイズ: 幅 {width} x 高さ {height}, 枚数: {count}\n")

print(f"txtファイルの生成完了：{output_file_name_txt}")

# DXFファイルの生成については、専門のライブラリ（例：ezdxf）が必要です。

import ezdxf

print("dxfファイルの生成")
# 新しいDXFドキュメントを作成
doc = ezdxf.new('R2010')
msp = doc.modelspace()

# 寸法スタイルを作成し、テキストの高さを設定
dimstyle = 'CustomDimStyle'

doc.dimstyles.new(dimstyle, dxfattribs={'dimtxt': Dim_text_height})  # テキストの高さを50に設定

# このレイヤーが既に存在する場合は、新たに追加しない
if 'Dim' not in doc.layers:
    doc.layers.new('Dim')

# 原板と製品、残り板を描画
for board_id in range(raw_board_id):
    # 原板の描画
    origin_x = 0
    origin_y = board_id * board_offset_y
    msp.add_lwpolyline([
        (origin_x, origin_y),
        (origin_x + raw_board_size[0], origin_y),
        (origin_x + raw_board_size[0], origin_y + raw_board_size[1]),
        (origin_x, origin_y + raw_board_size[1]),
        (origin_x, origin_y)])
    # 原板のIDをテキストで描画
    msp.add_text(
        str(board_id),
        dxfattribs={
            'insert': (origin_x - ID_text_align, origin_y + raw_board_size[1] / 2),
            'height': ID_text_height
        }
    )

    # この原板からの製品を描画
    for product in filter(lambda p: p.board_id == board_id, products):

        # 製品の外枠を描画
        product_points = [
            (product.x + origin_x, product.y + origin_y),
            (product.x + product.width + origin_x, product.y + origin_y),
            (product.x + product.width + origin_x, product.y + product.height + origin_y),
            (product.x + origin_x, product.y + product.height + origin_y),
            (product.x + origin_x, product.y + origin_y)]

        # 先にHATCHオブジェクトで塗りつぶしを追加
        hatch = msp.add_hatch(color=gray_aci)
        hatch.paths.add_polyline_path(product_points, is_closed=True)

        # HATCHオブジェクトの後にポリラインの外枠を描画
        msp.add_lwpolyline(product_points + [product_points[0]], dxfattribs={'color': 0})  # 黒色で外枠を描画

    # この原板からの残り板を描画
    for board in filter(lambda b: b.board_id == board_id, boards):
        board_points = [
            (board.x + origin_x, board.y + origin_y),
            (board.x + board.width + origin_x, board.y + origin_y),
            (board.x + board.width + origin_x, board.y + board.height + origin_y),
            (board.x + origin_x, board.y + board.height + origin_y),
            (board.x + origin_x, board.y + origin_y)]
        msp.add_lwpolyline(board_points)


        # 原板の横の寸法を記述
        msp.add_aligned_dim(p1=(origin_x, origin_y),
                            p2=(origin_x + raw_board_size[0], origin_y),
                            distance=Dim_text_align_origin,  # 寸法線を原板の外側に表示
                            dxfattribs={'dimstyle': dimstyle,'layer': 'Dim'}).render()

        # 原板の縦の寸法を記述
        msp.add_aligned_dim(p1=(origin_x, origin_y),
                            p2=(origin_x, origin_y + raw_board_size[1]),
                            distance=-Dim_text_align_origin,  # 寸法線を原板の外側に表示
                            dxfattribs={'dimstyle': dimstyle,'layer': 'Dim'}).render()

    for product in filter(lambda p: p.board_id == board_id, products):
        # 製品の横の寸法を記述
        msp.add_aligned_dim(p1=(product.x + origin_x, product.y + origin_y),
                            p2=(product.x + product.width + origin_x, product.y + origin_y),
                            distance=Dim_text_align_product,  # 寸法線を製品の外側に表示
                            dxfattribs={'dimstyle': dimstyle,'layer': 'Dim'}).render()

        # 製品の縦の寸法を記述
        msp.add_aligned_dim(p1=(product.x + origin_x, product.y + origin_y),
                            p2=(product.x + origin_x, product.y + product.height + origin_y),
                            distance=-Dim_text_align_product,  # 寸法線を製品の外側に表示
                            dxfattribs={'dimstyle': dimstyle,'layer': 'Dim'}).render()
# DXFファイルを保存
doc.saveas(output_file_name)


print(f"dxfファイルの生成完了: {output_file_name}")
# 実行時間の計測終了
end_time = time.time()
# 実行時間の表示
print(f"実行時間: {end_time - start_time:.2f}秒")

# ユーザーが何かキーを押すのを待つ
input("何かキーを押すと終了します...")