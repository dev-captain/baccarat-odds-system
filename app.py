from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

def calculate_baccarat_odds(removed_card):
    deck = 8
    decks = [
        16 * deck,
        4 * deck,
        4 * deck,
        4 * deck,
        4 * deck,
        4 * deck,
        4 * deck,
        4 * deck,
        4 * deck,
        4 * deck
    ]

    for x in removed_card:
        decks[x] -= 1
    shoe = sum(decks)
    
    playerWin = 0
    bankerWin = 0
    tieWin = 0

    cards4 = 0
    cards5b = 0
    cards5p = 0
    cards6 = 0

    player2 = 0
    player3 = 0
    banker2 = 0
    banker3 = 0
    
    outcome = [[0] * 10 for _ in range(10)]
    natural = [[0] * 10 for _ in range(10)]
    
    for p1 in range(10):
        wp1 = decks[p1]
        decks[p1] -= 1
        shoe -= 1
        for b1 in range(10):
            wb1 = wp1 * decks[b1]
            decks[b1] -= 1
            shoe -= 1

            for p2 in range(10):
                wp2 = wb1 * decks[p2]
                decks[p2] -= 1
                shoe -= 1

                for b2 in range(10):
                    wb2 = wp2 * decks[b2]
                    decks[b2] -= 1
                    shoe -= 1
                    pt1 = (p1 + p2) % 10
                    bt1 = (b1 + b2) % 10

                    if pt1 > 7 or bt1 > 7 or (pt1 > 5 and bt1 > 5):
                        if bt1 > pt1:
                            bankerWin += wb2 * shoe * (shoe - 1)
                        elif pt1 > bt1:
                            playerWin += wb2 * shoe * (shoe - 1)
                        else:
                            tieWin += wb2 * shoe * (shoe - 1)

                        if bt1 > 7 or pt1 > 7:
                            natural[bt1][pt1] += wb2 * shoe * (shoe - 1)
                        else:
                            outcome[bt1][pt1] += wb2 * shoe * (shoe - 1)

                        player2 += wb2 * shoe * (shoe - 1)
                        banker2 += wb2 * shoe * (shoe - 1)
                        cards4 += wb2 * shoe * (shoe - 1)
                    elif pt1 < 6:
                        for p3 in range(10):
                            wp3 = wb2 * decks[p3]
                            decks[p3] -= 1
                            shoe -= 1
                            pt3 = (p1 + p2 + p3) % 10
                            hit = True

                            if bt1 == 7:
                                hit = False
                            elif bt1 == 6 and (p3 < 6 or p3 > 7):
                                hit = False
                            elif bt1 == 5 and (p3 < 4 or p3 > 7):
                                hit = False
                            elif bt1 == 4 and (p3 < 2 or p3 > 7):
                                hit = False
                            elif bt1 == 3 and p3 == 8:
                                hit = False

                            if hit:
                                for b3 in range(10):
                                    wb3 = wp3 * decks[b3]
                                    decks[b3] -= 1
                                    bt3 = (b1 + b2 + b3) % 10

                                    if bt3 > pt3:
                                        bankerWin += wb3
                                    elif pt3 > bt3:
                                        playerWin += wb3
                                    else:
                                        tieWin += wb3

                                    decks[b3] += 1

                                    outcome[bt3][pt3] += wb3
                                    cards6 += wb3

                                    player3 += wb3
                                    banker3 += wb3
                            else:
                                if bt1 > pt3:
                                    bankerWin += wp3 * shoe
                                elif pt3 > bt1:
                                    playerWin += wp3 * shoe
                                else:
                                    tieWin += wp3 * shoe

                                outcome[bt1][pt3] += wp3 * shoe
                                cards5p += wp3 * shoe

                                player3 += wp3 * shoe
                                banker2 += wp3 * shoe

                            decks[p3] += 1
                            shoe += 1
                    elif bt1 < 6:
                        for b3 in range(10):
                            wb3 = wb2 * decks[b3]
                            decks[b3] -= 1
                            shoe -= 1
                            bt3 = (b1 + b2 + b3) % 10

                            if bt3 > pt1:
                                bankerWin += wb3 * shoe
                            elif pt1 > bt3:
                                playerWin += wb3 * shoe
                            else:
                                tieWin += wb3 * shoe

                            outcome[bt3][pt1] += wb3 * shoe
                            cards5b += wb3 * shoe

                            player2 += wb3 * shoe
                            banker3 += wb3 * shoe

                            decks[b3] += 1
                            shoe += 1

                    decks[b2] += 1
                    shoe += 1

                decks[p2] += 1
                shoe += 1

            decks[b1] += 1
            shoe += 1

        decks[p1] += 1
        shoe += 1


    
    total = bankerWin + playerWin + tieWin

    bankerProb = bankerWin / total
    playerProb = playerWin / total
    tieProb = tieWin / total

    odd = {
        'banker':f"{bankerProb:,.6f}",
        'player':f"{playerProb:,.6f}",
        'tie':f"{tieProb:,.6f}",
        
    }
    return odd

@app.route('/calculate_odds', methods=['POST'])
def calculate_odds():
    data = request.json
    card = data['cardList']
    odds = calculate_baccarat_odds(card)
    return jsonify(odds)


if __name__ == '__main__':
    app.run(debug=True, port=3000)
