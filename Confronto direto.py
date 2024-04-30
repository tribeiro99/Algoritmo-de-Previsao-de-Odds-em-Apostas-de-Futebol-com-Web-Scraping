import requests
from bs4 import BeautifulSoup

def calculate_odds(probability, adjustment_percentage=60):
    if probability is not None and probability != 0:
        odds = 1 / probability
        adjusted_odds = odds * (1 + (adjustment_percentage / 100))
        return adjusted_odds
    else:
        print("Invalid probability value:", probability)
        return None

def calculate_head_to_head_probability(matches, team_name):
    total_matches = 0
    wins = 0
    draws = 0

    for match in matches:
        home_team, result, away_team = match[2], match[3], match[4]

        if home_team == team_name or away_team == team_name:
            total_matches += 1

            if 'ET' in result:
                result = result.split(' ')[0]

            goals_home, goals_away = map(int, result.split('-'))

            if home_team == team_name and goals_home > goals_away:
                wins += 1
            elif away_team == team_name and goals_away > goals_home:
                wins += 1
            elif goals_home == goals_away:
                draws += 1

    if total_matches > 0:
        probability = (wins + draws) / total_matches
        return probability
    else:
        return None

def process_data(url):
    global result, home_team, away_team
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', class_='stat-cd3')

        if table:
            matches = []
            home_team = None
            away_team = None
            for row in table.find_all('tr')[1:]:
                columns = row.find_all('td')
                if len(columns) >= 5:
                    date = columns[0].text.strip()
                    competition = columns[1].text.strip()
                    home_team = columns[2].text.strip()
                    result = columns[3].text.strip()
                    away_team = columns[4].text.strip()

                    matches.append((date, competition, home_team, result, away_team))

                    print(f"{date}, {competition}, {home_team}, {result}, {away_team}")

            if matches:
                team_name_1 = home_team
                team_name_2 = away_team

                probability_team_1 = calculate_head_to_head_probability(matches, team_name_1)
                if probability_team_1 is not None and probability_team_1 != 0:
                    odd_team_1 = calculate_odds(probability_team_1)
                    print(f"Odd for {team_name_1} winning: {odd_team_1:.4f}")
                else:
                    print(f"\nNo head-to-head matches found for {team_name_1}")

                probability_team_2 = calculate_head_to_head_probability(matches, team_name_2)
                if probability_team_2 is not None and probability_team_2 != 0:
                    odd_team_2 = calculate_odds(probability_team_2)
                    print(f"Odd for {team_name_2} winning: {odd_team_2:.4f}")

                    # Adjust the odds for odd_team_2 with the same adjustment percentage as odd_team_1
                    adjusted_odd_team_2 = calculate_odds(probability_team_2)
                    print(f"Adjusted Odd for {team_name_2} winning: {adjusted_odd_team_2:.4f}")
                else:
                    print(f"\nNo head-to-head matches found for {team_name_2}")

                if probability_team_1 is not None and probability_team_1 != 0:
                    odd_team_1 = calculate_odds(probability_team_1)
                    odd_team_1_final = odd_team_1 * 0.6
                    return odd_team_1_final
                else:
                    print(f"\nNo head-to-head matches found for {team_name_1}")
                    return None

                if probability_team_2 is not None and probability_team_2 != 0:
                    odd_team_2 = calculate_odds(probability_team_2)
                    odd_team_2_final = odd_team_2 * 0.6
                    print(f"Odd for {team_name_2} winning: {odd_team_2_final:.4f}")
                else:
                    print(f"\nNo head-to-head matches found for {team_name_2}")

                    return odd_team_2_final

            else:
                print("No matches found in the table.")
        else:
            print('\nTable not found on the page.')
    else:
        print(f'\nFailed to retrieve the page. Status code: {response.status_code}')

if __name__ == "__main__":
    url = input("Please enter the URL of the match data: ")
    process_data(url)
