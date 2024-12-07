
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from treys import Card, Evaluator, Deck

class PokerAssistant:
    def __init__(self):
        self.evaluator = Evaluator()
        self.deck = Deck()

    def analyze_hand(self, hand_input, board_input, players):
        try:
            hand = [Card.new(card.strip()) for card in hand_input.split()]
            board = [Card.new(card.strip()) for card in board_input.split()] if board_input else []
        except Exception:
            return "输入格式错误，请输入正确的手牌和公共牌（例如 Ah Kh 或 Qh Jh Th）。"

        win_rate, tie_rate, lose_rate = self.simulate(hand, board, players)
        advice = self.get_advice(win_rate)

        return (
            f"【分析结果】\n"
            f"胜率：{win_rate:.2f}%\n"
            f"平局率：{tie_rate:.2f}%\n"
            f"败率：{lose_rate:.2f}%\n"
            f"建议：{advice}"
        )

    def simulate(self, hand, board, players):
        total_simulations = 1000
        wins, ties = 0, 0

        for _ in range(total_simulations):
            deck = Deck()
            deck.cards = [card for card in deck.cards if card not in hand + board]
            other_hands = [deck.draw(2) for _ in range(players - 1)]
            remaining_board = deck.draw(5 - len(board))
            full_board = board + remaining_board

            our_score = self.evaluator.evaluate(full_board, hand)
            all_scores = [our_score] + [
                self.evaluator.evaluate(full_board, other_hand) for other_hand in other_hands
            ]

            if our_score == min(all_scores):
                if all_scores.count(our_score) == 1:
                    wins += 1
                else:
                    ties += 1

        win_rate = (wins / total_simulations) * 100
        tie_rate = (ties / total_simulations) * 100
        lose_rate = 100 - win_rate - tie_rate
        return win_rate, tie_rate, lose_rate

    def get_advice(self, win_rate):
        if win_rate > 70:
            return "大幅加注"
        elif win_rate > 50:
            return "跟注或小幅加注"
        elif win_rate > 30:
            return "谨慎跟注"
        else:
            return "弃牌"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("欢迎使用德州扑克算牌助手！请输入手牌、公共牌和玩家人数进行分析。格式如下：\n\n"
                              "/calculate Ah Kh Qh Jh Th 3")

def calculate(update: Update, context: CallbackContext) -> None:
    try:
        args = context.args
        if len(args) < 3:
            update.message.reply_text("输入格式错误，请提供手牌、公共牌和玩家人数，例如：/calculate Ah Kh Qh Jh Th 3")
            return

        hand_input = " ".join(args[:2])  # 手牌
        board_input = " ".join(args[2:-1]) if len(args) > 3 else ""  # 公共牌
        players = int(args[-1])  # 玩家人数

        assistant = PokerAssistant()
        result = assistant.analyze_hand(hand_input, board_input, players)
        update.message.reply_text(result)
    except Exception as e:
        update.message.reply_text(f"发生错误：{e}")

def main():
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("calculate", calculate))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
