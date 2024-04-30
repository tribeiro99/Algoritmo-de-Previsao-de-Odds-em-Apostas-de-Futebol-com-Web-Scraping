import requests
from bs4 import BeautifulSoup


def calculate_odds(points, adjustment_percentage=20):
    if points is not None and points != 0:
        odds = 1 / (points / 30)
        adjusted_odds = odds + (odds * (adjustment_percentage / 100))
        return adjusted_odds
    else:
        print("Invalid points value:", points)
        return None


def calculate_points(target_team, home_team, away_team, result):
    if target_team in [home_team, away_team] and '-' in result:
        goal_parts = result.split('-')

        if len(goal_parts) == 2 and goal_parts[0].isdigit() and goal_parts[1].isdigit():
            home_goals, away_goals = map(int, goal_parts)

            if home_team == target_team:
                if home_goals > away_goals:
                    return 3
                elif home_goals == away_goals:
                    return 1
                else:
                    return 0
            elif away_team == target_team:
                if away_goals > home_goals:
                    return 3
                elif away_goals == home_goals:
                    return 1
                else:
                    return 0
    else:
        return None


def calculate_odds_with_adjustment(probability, adjustment_percentage=20):
    if probability is not None and probability != 0:
        odds = 1 / probability
        adjusted_odds = odds * (1 + (adjustment_percentage / 100))
        return adjusted_odds
    else:
        print("Invalid probability value:", probability)
        return None


def get_first_team(url):
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    last_10_table = soup.find_all('table', class_='stat-last10')[1]

    if last_10_table:
        rows = last_10_table.tbody.find_all('tr')

        if rows:
            first_row = rows[0]
            columns = first_row.find_all('td')
            if len(columns) >= 5:
                return columns[2].a.get_text(strip=True)
    return None


def process_data(url):
    target_team = get_first_team(url)

    if target_team:
        response = requests.get(url)
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        last_10_table = soup.find_all('table', class_='stat-last10')[1]

        if last_10_table:
            rows = last_10_table.tbody.find_all('tr')

            points_accumulated = 0

            for row in rows:
                columns = row.find_all('td')
                if len(columns) >= 5:
                    date = columns[0].get_text(strip=True)
                    competition = columns[1].a.get_text(strip=True)
                    home_team = columns[2].a.get_text(strip=True)
                    result = columns[3].a.get_text(strip=True)
                    away_team = columns[4].a.get_text(strip=True)

                    match_points = calculate_points(target_team, home_team, away_team, result)
                    if match_points is not None:
                        points_accumulated += match_points
                        print(f"{date}, {competition}, {home_team}, {result}, {away_team}, Points: {match_points}")
                    else:
                        print(
                            f"{date}, {competition}, {home_team}, {result}, {away_team}, Points: Skipped (Not involving {target_team})")

            if points_accumulated > 0:
                probability_team_last_10_matches = points_accumulated / 30
                odd_team_last_10_matches = calculate_odds_with_adjustment(probability_team_last_10_matches)

                if odd_team_last_10_matches is not None:
                    print(f"\nPoints accumulated in the last 10 matches: {points_accumulated}")
                    print(
                        f"Odd for {target_team} to win the next match based on the last 10 matches (with 20% adjustment): {odd_team_last_10_matches:.4f}")
                else:
                    print("No valid odds found for the last 10 matches.")
            else:
                print("No valid points accumulated in the last 10 matches.")
        else:
            print("Table not found. Check if the HTML structure has changed or the URL is correct.")
    else:
        print("Target team not found. Check if the HTML structure has changed or the URL is correct.")


if __name__ == "__main__":
    url = input("Please enter the URL of the webpage: ")
    process_data(url)
