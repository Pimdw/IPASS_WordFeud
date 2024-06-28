import csv

def analyze_game_results(filename):
    total_scores_player1 = 0
    total_scores_player2 = 0
    total_games = 0
    wins_count = {'Player1': 0, 'Player2': 0, 'Draw': 0}

    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            total_games += 1
            total_scores_player1 += int(row['Player 1 Total Score'])
            total_scores_player2 += int(row['Player 2 Total Score'])
            winner = row['Winner']
            if winner in wins_count:
                wins_count[winner] += 1

    average_score_player1 = total_scores_player1 / total_games
    average_score_player2 = total_scores_player2 / total_games

    most_wins = max(wins_count, key=wins_count.get)
    most_wins_count = wins_count[most_wins]

    stats_dict = {
        'Average Score Player 1': average_score_player1,
        'Average Score Player 2': average_score_player2,
        'Most Wins': most_wins,
        'Number of Wins': most_wins_count
    }

    return stats_dict
    
print(analyze_game_results('greedy_vs_random.csv'))

# greedy_vs_greedy {'Average Score Player 1': 289.489, 'Average Score Player 2': 306.549, 'Most Wins': 'Player2', 'Number of Wins': 634}
# random_vs_random {'Average Score Player 1': 185.895, 'Average Score Player 2': 183.78, 'Most Wins': 'Player1', 'Number of Wins': 501}
# greedy_vs_random {'Average Score Player 1': 330.205, 'Average Score Player 2': 163.792, 'Most Wins': 'Player1', 'Number of Wins': 988}