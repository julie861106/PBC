rank_value_dict = {
    'A': 1,
    'J': 11,
    'Q': 12,
    'K': 13,
}
for value in range(2, 11):
    rank_value_dict[str(value)] = value

# 建構名為 Card 的物件
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self.get_value()

    # 轉為數值
    def get_value(self):
        return rank_value_dict[self.rank]

    # 是否相鄰
    def is_adjacent(self, another_card):
        # 相差一就是相鄰
        if (abs(self.value - another_card.value) == 1):
            return True
        # K 和 A 也相鄰
        elif ((self.value + another_card.value) == 14):
            return True
        else:
            return False
    
    # 是否同一花色
    def has_same_suit(self, another_card):
        if self.suit == another_card.suit:
            return True
        else:
            return False

    # 是否同一點數
    def has_same_rank(self, another_card):
        if self.rank == another_card.rank:
            return True
        else:
            return False

    def is_larger_by_one(self, another_card):
        if self.suit == another_card.suit:
            if (self.value == (another_card.value + 1)):
                return True
            elif (((self.value + another_card.value) == 14) and 
                (self.rank == 'A')):  # K A
                return True
            else:
                return False
        else:
            return False


# 將少於 5 張牌的規則做成 function
def get_score_by_rule_ab(same_rank_record, a_count):
    score = 0  # 累計
    for same_rank_count in same_rank_record:

        # same_rank_count 等於三但不是葫蘆
        if same_rank_count == 3:
            # 如果是 A 就可以計 3 分
            if a_count == 3:
                score += 3
            # 否則只能算一對的分數
            else:
                score += 2

        # same_rank_count 等於二，不論用兩張 A 或一對都是 2 分
        else:
            score += 2
    
    # 在點數相同累計分數的時候已經算過出現 2 和 3 張 A 的分數
    # 只剩一張 A 還沒算
    if a_count == 1:
        score += 1

    return score       

class Deck:
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        # 確保新增加的卡片沒有違反新規定
        # 只有當前排數少於 5 才會考慮新增卡
        if len(self.cards) < 5:
            is_valid = True
            for existed_card in self.cards:
                if card.is_larger_by_one(existed_card):    
                    self.cards.remove(existed_card)
                    is_valid = False
                    break
            if is_valid:
                self.cards.append(card)

    # 回傳牌組總分
    def get_score(self):
        sorted_cards = sorted(self.cards, key=lambda card: card.value)
        # 先檢查分數多的規則
        # 檢查幾個屬性：同花（5 張）、是否為順子（5 張）、
            # 同樣點數的有幾張（4 張、3 張、2 張有幾次）、幾張 A
        adjacent_pair_count = 0
        flush = True
        cache_rank = 0
        same_rank_record = []
        a_count = 0
        same_rank_count = 0
        card_loop_index = []
        card_count = len(sorted_cards)
        for index in range(card_count):
            card_loop_index.append(index)
        card_loop_index.append(0)
        for loop_index in range(card_count):
            previous_card = sorted_cards[card_loop_index[loop_index]]
            next_card = sorted_cards[card_loop_index[loop_index + 1]]

            # 檢查相鄰
            if previous_card.is_adjacent(next_card):
                adjacent_pair_count += 1
            
            # 檢查同花
            if not previous_card.has_same_suit(next_card):
                flush = False
            
            # 檢查一樣的點數
            # 最後一張跟第一張是否一樣不可以再重複算
            if loop_index == card_count - 1:  
                if same_rank_count != 0:
                    same_rank_record.append(same_rank_count)
            else:
                if previous_card.has_same_rank(next_card): 
                    
                    if cache_rank == 0:  # 第一對一樣點數的牌
                        cache_rank = previous_card.rank
                        same_rank_count = 2

                    elif next_card.rank == cache_rank:  # 同一對一樣點數的牌再一張
                        same_rank_count += 1
                    
                    else:  # 第二對一樣點數的牌
                        same_rank_count = 2
                        cache_rank = previous_card.rank
                else:
                    if same_rank_count != 0:
                        same_rank_record.append(same_rank_count)
                    same_rank_count = 0

            # 紀錄 A 的次數
            if next_card.rank == 'A':
                a_count += 1

        # 是否有順子
        if adjacent_pair_count == 4:
            straight = True
        else:
            straight = False

        # 是否符合同花
        real_flush = False
        if flush and card_count == 5:
            real_flush = True


        # 將一樣點數的數量排序、由大到小
        same_rank_record.sort(reverse=True)


        # 從最高分： 同花順（100、5 張）
        if straight and real_flush:  
            score = 100

        # 四條（20、4 張 + 1 張）
        elif len(same_rank_record) == 1:
            if same_rank_record[0] == 4:
                score = 20
                # 檢查剩餘的那一張是不是 A
                if a_count == 1:
                    score += 1
            # 只有一個一對或一個三張一樣點數的牌、不是四條
            # 也不會是同花順、順子、葫蘆，有可能是同花
            # 有可能沒有五張牌
            else:
                if real_flush:
                    score = 3
                # 也不是同花，以規則 a 和 b 計分
                else:
                    score = get_score_by_rule_ab(same_rank_record, a_count)


        # 葫蘆（10、5 張）
        elif len(same_rank_record) == 2:
            if ((same_rank_record[0] == 3) and (same_rank_record[1] == 2)):
                score = 10
            # 有兩個一對、不是葫蘆（也不會是同花順、順子、四條，同花比兩個一對分數低）
            else:
                score = get_score_by_rule_ab(same_rank_record, a_count)

        # 順子（5、5 張）
        elif straight:    
            score = 5

        # 同花（3、5 張）
        elif real_flush:
            score = 3

        # 五張才可以出的高分牌已經出完了
        # 剩下的情境是不需要五張牌的規則，彼此不是獨立的情境：一對、A
        # 可能會少於五張牌
        else:
            score = get_score_by_rule_ab(same_rank_record, a_count)

        return score

deck_count = int(input())
answers = []
for each in range(deck_count):
    line = input().split(',')
    deck = Deck()
    for element in line:
        card = Card(element[0], element[1:])
        deck.add_card(card)

    score = deck.get_score()
    answers.append(score)

print(','.join('%d' % answer for answer in  answers))
            