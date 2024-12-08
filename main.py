from calcLeve import LeveCalculator
import math

def get_valid_input(prompt, valid_values=None, is_number=False, min_val=None, max_val=None):
    while True:
        value = input(prompt)
        if is_number:
            try:
                value = int(value)
                if min_val is not None and value < min_val:
                    print(f"{min_val}以上の値を入力してください。")
                    continue
                if max_val is not None and value > max_val:
                    print(f"{max_val}以下の値を入力してください。")
                    continue
                return value
            except ValueError:
                print("数値を入力してください。")
        elif valid_values and value not in valid_values:
            print(f"以下の値のいずれかを入力してください: {', '.join(valid_values)}")
        else:
            return value

def main():
    # デバッグモードの選択を追加
    debug_input = get_valid_input("デバッグモードを有効にしますか？ (y/n): ", valid_values=['y', 'n', 'Y', 'N'])
    is_debug = debug_input.lower() == 'y'
    
    calc = LeveCalculator(debug=is_debug)
    
    print("FF14 クラフターリーヴ計算機")
    print("-" * 40)
    
    # 職業の選択
    jobs = {
        "1": ("CRP", "木工師"),
        "2": ("BSM", "鍛冶師"),
        "3": ("ARM", "甲冑師"),
        "4": ("GSM", "彫金師"),
        "5": ("LTW", "革細工師"),
        "6": ("WVR", "裁縫師")
    }
    
    print("\n職業を選択してください：")
    for num, (_, name) in jobs.items():
        print(f"{num}: {name}")
    
    job_num = get_valid_input("番号を入力: ", valid_values=[str(i) for i in range(1, 7)])
    job = jobs[job_num][0]
    
    # レベル入力
    current_level = get_valid_input(
        "現在のレベルを入力してください (80-99): ",
        is_number=True,
        min_val=80,
        max_val=99
    )
    
    #現在の経験値入力
    current_exp = get_valid_input(
        f"現在の経験値を入力してください (0-{calc.level_exp_requirements[current_level]:,}): ",
        is_number=True,
        min_val=0,
        max_val=calc.level_exp_requirements[current_level]
    )
    
    target_level = get_valid_input(
        f"目標レベルを入力してください ({current_level+1}-99): ",
        is_number=True,
        min_val=current_level+1,
        max_val=100
    )
    
    # HQ/NQの選択
    hq_input = get_valid_input("HQで納品しますか？ (y/n): ", valid_values=['y', 'n', 'Y', 'N'])
    is_hq = hq_input.lower() == 'y'
    
    # 計算実行
    result = calc.calculate_leves_needed(current_level, target_level, job, is_hq,current_exp)
    
    print("\n" + "=" * 60)
    print(f"必要な総リーヴ回数: {result['total_leves']}回")
    print(f"消費リーヴ券: {result['total_leves']}枚")
    print("\n最適なリーヴの組み合わせ:")
    
    # 同じレベルのリーヴをまとめる
    combined_details = {}
    for detail in result['details']:
        leve_level = detail['level']
        if leve_level not in combined_details:
            combined_details[leve_level] = {
                'count': 0,
                'exp_per_leve': detail['exp_per_leve'],
                'total_exp': 0
            }
        combined_details[leve_level]['count'] += detail['count']
        combined_details[leve_level]['total_exp'] += detail['total_exp']
    
    # まとめた結果を表示
    for level, detail in sorted(combined_details.items()):
        item_name = calc.leve_items[job][level]
        print(f"\nLv{level}のリーヴ: {detail['count']}回")
        print(f"  納品物: {item_name}")
        print(f"  必要個数: {detail['count']}個" + (" (HQ)" if is_hq else ""))
        print(f"  1回あたりの経験値: {detail['exp_per_leve']:,}")
        print(f"  獲得総経験値: {detail['total_exp']:,}")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nプログラムを終了します。")
    except Exception as e:
        print(f"エラーが発生しました: {e}") 

