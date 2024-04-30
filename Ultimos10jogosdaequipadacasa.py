import requests
from bs4 import BeautifulSoup
from collections import Counter

def calculate_odds(points):
    if points is not None and points != 0:
        return 1 / (points / 30)
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
            else:
                if away_goals > home_goals:
                    return 3
                elif away_goals == home_goals:
                    return 1
                else:
                    return 0
    else:
        return None

def identify_target_team(matches):
    teams = [match.split(", ")[4] for match in matches]
    team_counter = Counter(teams)
    target_team, _ = team_counter.most_common(1)[0]
    return target_team




def process_data(url):
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    last_10_table = soup.find('table', class_='stat-last10')

    if last_10_table:
        matches = []

        for row in last_10_table.tbody.find_all('tr'):
            columns = row.find_all('td')
            if len(columns) >= 5:
                match_info = ", ".join([columns[i].get_text(strip=True) for i in range(5)])
                matches.append(match_info)

        target_team = identify_target_team(matches)
        print(f"Identified target team: {target_team}")



        points_accumulated = 0

        for match in matches:
            match_info = match.split(", ")
            date, competition, home_team, result, away_team = match_info
            match_points = calculate_points(target_team, home_team, away_team, result)

            if match_points is not None:
                points_accumulated += match_points
                print(f"{date}, {competition}, {home_team}, {result}, {away_team}, Points: {match_points}")
            else:
                print(
                    f"{date}, {competition}, {home_team}, {result}, {away_team}, Points: Skipped (Not involving {target_team})")

        probability_team_last_10_matches = points_accumulated / 30
        odd_team_last_10_matches = calculate_odds(points_accumulated)

        print(f"\nPoints accumulated in the last 10 matches: {points_accumulated}")
        print(
            f"Odd for {target_team} to win the next match based on the last 10 matches: {odd_team_last_10_matches:.4f}")

    else:
        print("Table not found. Check if the HTML structure has changed or the URL is correct.")


if __name__ == "__main__":
    url = input("Please enter the URL of the match data: ")
    process_data(url)
