import requests
from bs4 import BeautifulSoup


def calculate_odds(probability):
    return 1 / probability


def process_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        home_goal_data = extract_goal_data(soup, True)
        away_goal_data = extract_goal_data(soup, False)

        print_goal_data(home_goal_data, "Home Team")
        print_goal_data(away_goal_data, "Away Team")

        calculate_and_print_odds(home_goal_data, "Home Team")
        calculate_and_print_odds(away_goal_data, "Away Team")

    else:
        print(f'Failed to retrieve the page. Status code: {response.status_code}')


def extract_goal_data(soup, is_home_team=True):
    goal_data = []
    tables = soup.find_all('table', class_='stat-goals')
    team_index = 0 if is_home_team else 1

    if team_index < len(tables):
        rows = tables[team_index].find('tbody').find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 4:
                minute_range = columns[0].get_text(strip=True)
                goals_text = columns[2].get_text(strip=True)

                goals = int(goals_text) if goals_text.isdigit() else 0

                goal_data.append((minute_range, goals))

    return goal_data


def print_goal_data(goal_data, team_name):
    print(f"\n{team_name} Goal Data:")
    for minute_range, goals in goal_data:
        print(f"Minute Range: {minute_range}\tGoals: {goals}")


def calculate_and_print_odds(goal_data, team_name):
    print(f"\n{team_name} Odds:")

    total_team_goals = sum(goals for _, goals in goal_data)

    for minute_range, goals in goal_data:
        prob_goal = calculate_probability(goals, total_team_goals)
        if prob_goal is not None:
            odd_goal = calculate_odds(prob_goal)
            print(f"Odd for {team_name} to score in minute range {minute_range}: {odd_goal:.4f}")
        else:
            print(f"No goals scored in minute range {minute_range}")



def calculate_probability(goals, total_team_goals):

    if goals > 0 and total_team_goals > 0:
        return 1 / (1 / (goals / total_team_goals))
    else:
        return None




if __name__ == "__main__":
    url = input("Please enter the URL of the game: ")
    process_data(url)
