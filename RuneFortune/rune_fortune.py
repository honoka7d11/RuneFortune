import sqlite3
import random
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk  #, ImageOps  Pillowライブラリをインポート

# データベース接続
conn = sqlite3.connect("rune_fortune.db")
cursor = conn.cursor()

# テーブル作成
def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS runes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            meaning TEXT NOT NULL,
            reversed_meaning TEXT,
            image_path TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            rune_name TEXT NOT NULL,
            interpretation TEXT NOT NULL
        )
    ''')
    # 初期データを一度だけ挿入する処理
    insert_runes_data()
    conn.commit()

# ルーンデータの挿入
def insert_runes_data():
    # すでにデータが挿入されているか確認
    cursor.execute("SELECT COUNT(*) FROM runes")
    if cursor.fetchone()[0] == 0:
        # データが存在しなければ、初期データを挿入
        runes_data = [
            ("Fehu",
             "富、成功、繁栄を意味します。金銭的な成功や安定が期待できる時期です。新しいスタートに向けて準備が整い、自分の持っている資源をうまく活用することで、さらなる成功をつかむことができるでしょう。", 
             "損失、障害を意味します。この時期は、物質的な面で困難に直面するかもしれませんが、焦らずに計画を見直し、冷静に対応することが重要です。", 
             "fehu.png"),
            ("Uruz", 
             "力、勇気、エネルギーを意味します。勇気と決断力を持って新しい挑戦に向かう時期であり、自分の力を信じて行動することが成功を引き寄せます。", 
             "混乱、弱さを意味します。また、自分を疑うことや無謀な行動への警告も含まれています。この時期は、無理をせず休息を取り、変化に対して柔軟に対応することが大切です。", 
             "uruz.png"),
            ("Thurisaz", 
             "保護、防御、直感を意味します。今は困難を乗り越える力が備わっている時期であり、強い意志とエネルギーを持って行動することで、目標達成や試練の克服が可能です。",
             "過剰反応、攻撃性を意味します。無謀な行動を避け、冷静に状況を見極めることが大切です。内面的な葛藤や不安に直面することがあり、慎重に行動し、準備が整うのを待つことが重要な時期です。", 
             "thurisaz.png"),
            ("Ansuz", 
             "知識、コミュニケーション、創造性を意味します。学びや表現がうまくいき、インスピレーションや洞察を得ることができる時期です。また、精神的な成長や他者への影響力を高めるチャンスがあるでしょう。",
             "誤解、不注意、自己表現の制限を意味します。直感や表現が鈍っている時期であり、冷静に状況を整理し、慎重に判断することが重要です。", 
             "ansuz.pmg"),
            ("Raido", 
             "旅、行動、進歩を意味します。新しい状況やチャンスに向かって順調に進む時期であり、調和を保ちながら、流れに乗って前進することが重要です。",	
             "停滞、行き詰まりを意味します。調和が欠けていることを示唆し、無理に進もうとすることのリスクもあります。焦らず、冷静に状況を見極めることが大切です。", 
             "raido.png"),
            ("Kenaz",
             "創造性、啓示、光を意味します。今はインスピレーションが高まり、物事がはっきり見えて、創造的な活動や自己表現が順調に進む時期です。",	
             "迷い、暗闇、隠された真実を意味します。アイデアや進展が遅れ、自己表現が難しい時期です。また、癒しが遅れ、不安定な状況が続くこともあります。焦らず冷静に進むことが大切です。", 
             "kenaz.png"),
            ("Gebo",
             "贈り物、パートナーシップ、結びつきの意味します。周りの人と互いに支え合い、調和の取れた関係が大切な時期です。また、人間関係やパートナーシップが強化されることを示唆しています。",  
             "不均衡な関係、取引の失敗を意味します。与えることと受け取ることのバランスを見直し、周囲との協力や助け合いを大切にする時期です。調和を取り戻す努力が求められます。",
             "gebo.png"),
            ("Wunjo",
             "喜び、幸福、調和を意味します。今は良いエネルギーに包まれ、ポジティブな変化や成果が期待できる時期です。人間関係も順調で、幸福感が得られる兆しです。", 
             "不安、不安定、失望を意味します。今は人間関係や成果において少しずつ調整が必要な時期です。焦らず、心を落ち着けて問題に向き合い、改善に向けた一歩を踏み出すことが大切です。", 
             "wunjo.png"),
            ("Hagalaz",	
             "破壊、混乱、変革を意味します。浄化や破壊を通じて新しい始まりが待っている一方で、予測不可能な出来事に備える警告の役割も果たします。困難を乗り越える力が試される時期です。",
             "不安定な状況、進展の遅れを意味します。自己破壊的な行動や過去の問題を解決しないことで、さらに困難を招くことになります。現状に固執せず、適切な変化を受け入れることが求められます。",
             "hagalaz.png"),
            ("Nauthiz", 
             "必要、制限、耐久力を意味します。制約や困難がある一方で、それを乗り越えるための強さや成長のチャンスもあります。今は忍耐強く、状況に適応して行動し、自分を磨くことに集中する時期です。",	
             "不満、過度の制約、忍耐力の欠如を意味します。自己制限や必要なことへの気づきが足りない時期です。困難が長引くかもしれませんが焦らず、現状を見直し、適切な行動を取ることが大切です。",
             "nauthiz.png"),
            ("Isa",
             "冷静、停滞、内省を意味します。今は状況が動かないことを受け入れ、冷静に判断し、忍耐強く次のステップを準備する時期です。急がずに、しっかりと心を落ち着けることが大切です。", 
             "遅延、積極性の欠如を意味します。停滞からの解放や進展の兆しも意味しますが、焦ったり感情を抑えすぎることに注意が必要です。進展が遅れることもあるので、冷静に状況を整理することが大切です。",
             "isa.png"),
            ("Jera",
             "収穫、循環、季節の変化を意味します。努力が実を結び、成果を得る時期です。物事が順調に進み、調和が取れた状態で、次のステップに進む準備が整っています。",
             "失敗、遅れ、成果の欠如を意味します。今は焦らず、計画を見直し、調整する時期です。無理に進めず、状況が安定するまで待つことが重要です。", 
             "jera.png"),
            ("Eihwaz",
             "防御、変革、精神的成長を意味します。変化や成長の過程で、耐久力や不屈の精神を持って進むことが求められ、困難な状況でも乗り越える力を得られる時期です。精神的な成長が促される時期でもあります。",
             "自信の欠如、恐れ、不安を意味します。変化が遅れ、精神的に不安定な状況が続くかもしれません。進むべき道が不確実であり、今は焦らず状況を見直すことが求められる時期です。",
             "eihwaz.png"),
            ("Perthro", 
             "神秘、運命、偶然を意味します。自分の可能性を信じ、目の前にある選択やチャンスを大切にすることが重要です。また、隠れた真実を受け入れることで、新しい成長の機会を得られるかもしれません。",
             "運命の歯車が逆に回る、誤った決断を意味します。状況を無理にコントロールせず、冷静かつ柔軟に対応することが大切です。また、自分の可能性を見直すことで好転のきっかけがつかめるでしょう。",	
             "perthro.png"),
            ("Algiz", "保護、守護、警戒を意味します。あなたは守られ、正しい道を進むための強い直感とエネルギーを持っています。警戒心を持ちながら、自信を持って新たな始まりに向かって進んでいくべき時です。", 
             "防御が無効、危険な状況を意味します。今は冷静に周囲を見守り、注意深く行動することが必要です。成長が遅れていると感じた場合は、焦らず、一歩一歩着実に進んでいくことが大切です。",
             "algiz.png"),
            ("Sowilo",
             "太陽、成功、エネルギーを意味します。自信を持って進み、何をすべきかがはっきりしている今、成功をつかむチャンスです。成長や癒しが進み、良い変化が訪れる時期です。",
             "エネルギー不足、迷走を意味します。エネルギーや成長が停滞している状態で、変化が不安定に感じることがあります。今は冷静になって自分の進むべき道を再確認し、方向を見直すことが必要です。", 
             "sowilo.png"),
            ("Tiwaz",
             "勝利、戦士の精神、正義を意味します。公正な行動が報われ、リーダーシップや決断力が求められる時期です。困難を乗り越え、目標達成に向けて積極的に行動することが成功の鍵となります。",
             "不正、敗北、無力感を意味します。自分の行動に疑問を感じたり、リーダーシップを取ることに迷いがあるのではないですか？状況を見直し、戦略を練り直す必要があることを示しています。",	
             "tiwaz.png"),
            ("Berkano",	
             "成長、母性、新しい始まりを意味します。新しいプロジェクトや人間関係がうまく進んでいく時期です。また、家族や愛情面での絆が深まり、心と体が癒されて安定して成長できる良いタイミングです。",
             "停滞、不妊、変化の不足を意味します。癒しや安定が求められる時期であり、過去の傷や関係の見直しが必要です。焦らず、心身を整えながら状況を改善するための努力が重要です。",
             "berkano.png"),
            ("Ehwaz",
             "協力、パートナーシップ、調和を意味します。今が良いタイミングです。信頼と協力を大切にしながら前に進んでください。また、柔軟な姿勢で変化を受け入れることが成功の鍵となります。",
             "関係の不調、変化への抵抗を意味します。焦らず現状を見直し、変化を受け入れる柔軟さを持つことが求められます。また、周囲と信頼関係を結び直し、進むべき道を慎重に考えることが大切です。",	
             "ehwaz.png"),
            ("Mannaz",
             "人間性、自己理解、協力を意味しています。自分自身や他者との関係を見つめ直し、内面的な成長と調和を大切にする時期です。人間関係を振り返り、協力の重要性を再確認する良いタイミングです。",
             "孤立、自己中心的、誤解を意味します。自分自身や他者との関係を振り返り、自分がどう思っているかを再確認することが大切です。また、他の人と協力したり、お互いに理解し合うために努力する時期です。",
             "mannaz.png"),
            ("Laguz", 
             "感情、直感、流れを意味します。人生の流れを柔軟に受け入れることや、自分の感情と直感を信じて行動することが大切です。また、心の癒しや内面の成長、新しいことへの挑戦を促しています。",
             "感情の混乱、誤った直感を意味します。自然の流れを受け入れることを意識し、感情や直感にしっかり向き合ってください。また、エネルギーを取り戻すために休息や自己ケアを大切にすると良いでしょう。",
             "laguz.png"),
            ("Inguz",
             "新たな始まり、家族、繁栄を意味します。物事が良い方向に進み始めていて、成功のきざしが見えてきています。新しいことを始める準備が整い、心の安定や家族との関係もうまくいくタイミングです。", 
             "停滞、変化の不安、家族問題を意味します。どの方向に進むべきかをよく考え、自分の心や今の状況を整えることが大切です。焦らずにしっかりと準備を進めて、確かな土台を作りましょう。",	
             "inguz.png"),
            ("Dagaz",
             "明晰さ、変革、目覚めを意味します。これまでの努力が報われ、新しい希望や機会が訪れます。転換点を迎えた今、自分の進むべき道に自信を持ち、次のステップに進む準備が整っているようです。",
             "盲目的な行動、変化への抵抗を意味します。自己認識が不足して不安定な状態にあり、過去に囚われてチャンスを逃す可能性があります。冷静に状況を見直すことが大切です。",	
             "dagaz.png"),
            ("Othala",
             "遺産、家族、伝統を意味しています。あなたが直面している問題を解決するためには過去の経験や価値観を振り返り、それが現在の自分にどう影響を与えているかを考えることが大切です。",
             "財産の損失、家族や伝統の崩壊を意味しています。自分の立場や方向性を根本から見直すことが重要です。また、過去からの解放や新しい方向性を見つけることが求められる時期かもしれません。",	
             "othala.png"),
        ]
        
        cursor.executemany("INSERT INTO runes (name, meaning, reversed_meaning, image_path) VALUES (?, ?, ?, ?)", runes_data)
        print("初期データが挿入されました。")
    else:
        print("データはすでに存在しています。挿入をスキップします。")

# 画像をリサイズして表示する関数
# 画像を設定する関数の修正
# 画像を表示する関数
def display_rune_image(image_file, size=(200, 200)):  # サイズ指定
    global rune_image  # 画像の参照を保持するグローバル変数
    try:
        # Pillowを使って画像を開く
        image = Image.open(image_file)
        image = image.resize(size, Image.LANCZOS)  # 高品質なリサンプリングを指定
        rune_image = ImageTk.PhotoImage(image)  # 画像オブジェクトを保存

        # ラベルに画像を設定
        rune_image_label.config(image=rune_image)
        rune_image_label.image = rune_image  # 参照を保持
    except Exception as e:
        # エラー時は背景だけを表示
        rune_image_label.config(image="", bg="#5233a6")
        messagebox.showerror("エラー", f"画像の読み込みに失敗しました: {e}")

# カスタムメッセージボックスの関数
def show_custom_messagebox(title, message):
    # Toplevelウィンドウを作成
    custom_box = tk.Toplevel(root)
    custom_box.title(title)
    custom_box.geometry("500x300")
    custom_box.configure(bg="#2c3e50")
    custom_box.resizable(False, False)

    # メッセージを表示するラベル
    label = tk.Label(
        custom_box, 
        text=message, 
        bg="#2c3e50", 
        fg="#ecf0f1", 
        font=("Arial", 14), 
        wraplength=400,
        justify="center"
    )
    label.pack(pady=30)

    # OKボタン
    ok_button = tk.Button(
        custom_box, 
        text="OK", 
        command=custom_box.destroy, 
        font=("Arial", 14), 
        bg="#34495e", 
        fg="white", 
        width=10
    )
    ok_button.pack(pady=10)

    # モーダルにする
    custom_box.transient(root)
    custom_box.grab_set()
    root.wait_window(custom_box)

# カスタムメッセージボックスを使用するよう変更
# ルーンを占う
def draw_rune():
    cursor.execute("SELECT * FROM runes")
    runes = cursor.fetchall()

    selected_rune = random.choice(runes)
    is_reversed = random.choice([True, False])
    interpretation = f"逆位置: {selected_rune[3]}" if is_reversed else f"正位置: {selected_rune[2]}"

    # 結果を履歴に保存
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO history (date, rune_name, interpretation) VALUES (?, ?, ?)",
                   (date, selected_rune[1], interpretation))
    conn.commit()

    # 画像を表示
    display_rune_image(selected_rune[4])

    # カスタムメッセージボックスを表示
    show_custom_messagebox(
        "ルーン占い結果", 
        f"選ばれたルーン: {selected_rune[1]}\n\n意味: {interpretation}"
    )

# 履歴を見る
def show_history():
    cursor.execute("SELECT * FROM history ORDER BY date DESC")
    history = cursor.fetchall()

    history_window = tk.Toplevel(root)
    history_window.title("履歴")
    history_window.geometry("500x400")
    history_window.configure(bg="#1e1e2e")

    if history:
        tree = ttk.Treeview(history_window, columns=("date", "rune_name", "interpretation"), show="headings")
        tree.heading("date", text="日付")
        tree.heading("rune_name", text="ルーン")
        tree.heading("interpretation", text="解釈")
        tree.column("date", width=70)
        tree.column("rune_name", width=70)
        tree.column("interpretation", width=230)
        tree.pack(fill=tk.BOTH, expand=True)

        for record in history:
            tree.insert("", "end", values=(record[1], record[2], record[3]))
    else:
        tk.Label(history_window, text="履歴はまだありません。", fg="white", bg="#1e1e2e", font=("Arial", 14)).pack(pady=20)

def on_exit():
    # 確認ダイアログ
    if messagebox.askokcancel("終了", "本当に終了しますか？"):
        # データベース接続を閉じる
        conn.close()
        # メインウィンドウを破棄してプログラムを終了
        root.destroy()

# メインウィンドウの設定
root = tk.Tk()
root.title("RuneFortune")
root.geometry("600x500")
root.configure(bg="#1e1e2e")

# 背景画像
bg_image = ImageTk.PhotoImage(Image.open("background.png"))
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# メインラベル
label = tk.Label(root, text="RuneFortune", font=("Times New Roman", 24, "bold"), fg="#d4af37", bg="#1e1e2e")
label.pack(pady=20)

# 画像ラベル（初期状態で背景と一致）
rune_image_label = tk.Label(
    root,
    bg="#5233a6",         # 背景色をウィンドウ全体と一致
    borderwidth=0,        # 枠線をなくす
    highlightthickness=0  # ハイライトも削除
)
rune_image_label.pack(pady=(0, 10))  # 適切な余白を設定


# ボタン
draw_button = tk.Button(root, text="ルーンを占う", command=draw_rune, font=("Helvetica", 16), bg="#3e3e4e", fg="white")
draw_button.pack(pady=10)

history_button = tk.Button(root, text="履歴を見る", command=show_history, font=("Helvetica", 16), bg="#3e3e4e", fg="white")
history_button.pack(pady=10)

exit_button = tk.Button(root, text="終了", command=on_exit, font=("Helvetica", 16), bg="#3e3e4e", fg="white")
exit_button.pack(pady=10)

# アプリの初期化
create_table()

# メインループ
root.mainloop()

# データベース接続を閉じる
conn.close()


