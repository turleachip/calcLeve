import math

class LeveCalculator:
    def __init__(self, debug=False):
        # レベルごとの必要経験値テーブル
        self.level_exp_requirements = {
            # レベル: 次のレベルまでに必要な経験値
            80: 5992000,
            81: 6171000,
            82: 6942000,
            83: 7205000,
            84: 7948000,
            85: 8287000,
            86: 9231000,
            87: 9529000,
            88: 10459000,
            89: 10838000,
            90: 13278000,
            91: 13659000,
            92: 15348000,
            93: 15912000,
            94: 17534000,
            95: 18263000,
            96: 20322000,
            97: 20957000,
            98: 22979000,
            99: 23789000
        }
        
        # リーヴクエストの基本経験値テーブル（職業ごと）
        self.leve_rewards = {
            'CRP': {  # 木工
                80: 935000,
                82: 846040,
                84: 1255600,
                86: 2028020,
                88: 2297800,
                90: 2695430,  # より高い経験値のものを選択
                92: 3115640,
                94: 2454760,
                96: 4125360,
                98: 4664730
            },
            'BSM': {  # 鍛冶
                80: 1355750,
                82: 1582910,
                84: 1746150,
                86: 1443780,
                88: 2297800,
                90: 2695430,
                92: 3115640,
                94: 3559400,
                96: 4125360,
                98: 4664730
            },
            'ARM': {  # 甲冑
                80: 935000,
                82: 1582910,
                84: 1255600,
                86: 1503270,
                88: 2257300,
                90: 1440660,
                92: 2148720,
                94: 2454760,
                96: 4554260,
                98: 3459540
            },
            'GSM': {  # 彫金
                80: 514250,
                82: 1525130,
                84: 1067020,
                86: 2028020,
                88: 2297800,
                90: 2695430,
                92: 3115640,
                94: 2454760,
                96: 3059520,
                98: 4183380
            },
            'LTW': {  # 革細工
                80: 935000,
                82: 1582910,
                84: 1725980,
                86: 1503270,
                88: 1703250,
                90: 1440660,
                92: 2148720,
                94: 2454760,
                96: 4125360,
                98: 5149700
            },
            'WVR': {  # 裁縫
                80: 935000,
                82: 1582910,
                84: 1255600,
                86: 1922600,
                88: 2257300,
                90: 2695430,
                92: 3115640,
                94: 3929450,
                96: 4125360,
                98: 5149700
            }
        }
        
        # 納品物データ
        self.leve_items = {
            'CRP': {  # 木工
                80: "ホースチェスナット・グラインディングホイール",
                82: "パーム・レンジャーブレスレット",
                84: "レッドパイン・フィッシングロッド",
                86: "アイアンウッドスピア",
                88: "インテグラル・マジテックロッド",
                90: "ウコギ・イヤリング",
                92: "セイバ・ウィング",
                94: "ダークマホガニー・フィッシングロッド",
                96: "アカシア・ロングボウ",
                98: "クラロウォルナット・スピア"
            },
            'BSM': {  # 鍛冶
                80: "ハイダリウムタスラム",
                82: "ハイダリウムナイフ",
                84: "ビスマスウォーサイズ",
                86: "マンガン・ガーデンサイズ",
                88: "コンドライト・マジテックアクス",
                90: "オルコクロマイト・ツインファング",
                92: "ルテニウム・ウォーアクス",
                94: "コバルトタングステン・ククリ",
                96: "ゴールドチタン・グレートソード",
                98: "カザナル・ツインファング"
            },
            'ARM': {  # 甲冑
                80: "ハイダリウム・スレイヤーアームガード",
                82: "ハイダリウム・ディフェンダーアーマー",
                84: "ビスマス・アレピック",
                86: "マンガン・ディセンドドラゴンヘルム",
                88: "コンドライト・スレイヤートップス",
                90: "オルコクロマイト・タワーシールド",
                92: "ルテニウム・スレイヤーヴァンブレイス",
                94: "コバルトタングステン・アレンビック",
                96: "ゴールドチタン・ディフェンダースパイクアーマー",
                98: "カザナル・スレイヤーグリーヴ"
            },
            'GSM': {  # 彫金
                80: "アメトリン・ディフェンダーリング",
                82: "ピューターペンデュラム",
                84: "フリギアン・ヒーラーイヤーカフ",
                86: "マンガンレイピア",
                88: "コンドライト・マジテックプラニスフィア",
                90: "ラァー・ペンデュラム",
                92: "ルテニウム・フォールディングファン",
                94: "コバルトタングステン・ニードル",
                96: "ホワイトゴールド・スレイヤーハーフマスク",
                98: "カザナル・ロッド"
            },
            'LTW': {  # 革細工
                80: "象皮足袋",
                82: "マウンテンチキン・スカウトジャケット",
                84: "サイガ・ディフェンダーコート",
                86: "クンビーラ・ブラックグリフィングローブ",
                88: "オピオタウロス・ヒーラーブーツ",
                90: "シルバリオ・ディフェンダーアミュレット",
                92: "ハンマーヘッドダイル・スカウトレギンス",
                94: "ブラーシャ・クラフターハーフグローブ",
                96: "ゴンフォテリウム・ギャザラーダブレット",
                98: "ガルガンチュア・ストライカートラウザー"
            },
            'WVR': {  # 裁縫
                80: "ダークヘンプ・ヒーラーフィンガレスグローブ",
                82: "アルマスティ・ヒーラーコート",
                84: "スノーリネン・クラフターターバン",
                86: "スカーレットモコ・ライズドラゴンガスキン",
                88: "カエアンビロード・スカウトボトム",
                90: "スノーコットン・ジャケット",
                92: "マウンテンリネン・キャスタークローク",
                94: "サーセネット・レンジャースロップ×3",
                96: "ロネークサージ・ギャザラートラウザー",
                98: "サンダーヤードシルク・キャスターコート"
            }
        }
        
        self.debug = debug
        
    def debug_print(self, message):
        if self.debug:
            print(f"[DEBUG] {message}")
            
    def validate_exp_gain(self, current_exp, gained_exp, level):
        """経験値の増加が正しいかを検証"""
        if self.debug:
            next_level_exp = self.level_exp_requirements.get(level, float('inf'))
            self.debug_print(f"現在の経験値: {current_exp:,}")
            self.debug_print(f"獲得経験値: {gained_exp:,}")
            self.debug_print(f"Lv{level}→{level+1}に必要な経験値: {next_level_exp:,}")
            
    def calculate_exp_needed(self, current_level, target_level, current_exp=0):
        """現在のレベルと経験値から目標レベルまでに必要な経験値を計算"""
        if current_level >= target_level:
            return 0
            
        total_exp = 0
        # 現在のレベルの残り経験値を計算
        if current_level in self.level_exp_requirements:
            remaining_exp = self.level_exp_requirements[current_level] - current_exp
            total_exp += remaining_exp
            
            if self.debug:
                self.debug_print(f"Lv{current_level}の残り必要経験値: {remaining_exp:,}")
        
        # 次のレベルから目標レベルまでの経験値を計算
        for level in range(current_level + 1, target_level):
            if level in self.level_exp_requirements:
                level_exp = self.level_exp_requirements[level]
                total_exp += level_exp
                
                if self.debug:
                    self.debug_print(f"Lv{level}の必要経験値: {level_exp:,}")
        
        return total_exp
    
    def calculate_leves_needed(self, current_level, target_level, job, is_hq=False, current_exp=0):
        """
        必要なリーヴ回数を計算して最適な組み合わせを返す
        job: 'CRP', 'BSM', 'ARM', 'GSM', 'LTW', 'WVR'のいずれか
        is_hq: HQ納品の場合はTrue（経験値2倍）
        current_exp: 現在の経験値
        """
        total_exp_needed = self.calculate_exp_needed(current_level, target_level, current_exp)
        multiplier = 2 if is_hq else 1
        
        if self.debug:
            self.debug_print(f"現在の経験値: {current_exp:,}")
            self.debug_print(f"必要総経験値: {total_exp_needed:,}")
            self.debug_print(f"HQ倍率: {multiplier}")
        
        best_combination = {
            'total_leves': 0,
            'details': []
        }
        
        remaining_exp = total_exp_needed
        current_working_level = current_level
        current_working_exp = current_exp
        
        while remaining_exp > 0:
            if self.debug:
                self.debug_print(f"\n現在のレベル: {current_working_level}")
                self.debug_print(f"現在の経験値: {current_working_exp:,}")
                self.debug_print(f"残り必要経験値: {remaining_exp:,}")
            
            # 現在のレベルで利用可能な全てのリーヴを取得
            available_leves = {
                level: exp for level, exp in self.leve_rewards[job].items()
                if level <= current_working_level
            }
            
            if not available_leves:
                if self.debug:
                    self.debug_print("利用可能なリーヴがありません")
                break
            
            # 最も効率の良いリーヴを選択
            best_level = max(available_leves.items(), key=lambda x: x[1])[0]
            exp_per_leve = self.leve_rewards[job][best_level] * multiplier
            
            if self.debug:
                self.debug_print(f"選択されたリーヴ: Lv{best_level}")
                self.debug_print(f"1回あたりの経験値: {exp_per_leve:,}")
            
            # 次のレベルまでに必要な経験値を計算
            exp_needed_for_next_level = self.level_exp_requirements.get(current_working_level, float('inf')) - current_working_exp
            
            # 必要なリーヴ回数を計算
            exp_for_calculation = min(remaining_exp, exp_needed_for_next_level)
            leves_needed = math.ceil(exp_for_calculation / exp_per_leve)
            exp_gained = exp_per_leve * leves_needed
            
            best_combination['details'].append({
                'level': best_level,
                'count': leves_needed,
                'exp_per_leve': exp_per_leve,
                'total_exp': exp_gained
            })
            
            # 経験値の更新
            current_working_exp += exp_gained
            remaining_exp -= exp_gained
            
            # レベルアップの処理
            while current_working_level < target_level:
                level_cap = self.level_exp_requirements.get(current_working_level, float('inf'))
                if current_working_exp >= level_cap:
                    if self.debug:
                        self.debug_print(f"レベルアップ: {current_working_level} → {current_working_level + 1}")
                    current_working_exp -= level_cap
                    current_working_level += 1
                else:
                    break
        
        best_combination['total_leves'] = sum(detail['count'] for detail in best_combination['details'])
        return best_combination
