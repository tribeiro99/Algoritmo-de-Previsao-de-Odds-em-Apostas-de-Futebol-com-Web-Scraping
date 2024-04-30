import requests
from bs4 import BeautifulSoup


def process_data(url):
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    table = soup.find('table', class_='results competition-rounds competition-half-padding')

    positions = []
    teams = []
    points = []
    matches_played = []
    wins = []
    draws = []
    losses = []
    goals = []

    rows = table.find_all('tr')[1:]

    for row in rows:
        columns = row.find_all('td')
        positions.append(columns[0].get_text(strip=True))
        team = columns[1].find('a')
        teams.append(team.get_text(strip=True))
        points.append(columns[2].get_text(strip=True))
        matches_played.append(columns[3].get_text(strip=True))
        wins.append(columns[4].get_text(strip=True))
        draws.append(columns[5].get_text(strip=True))
        losses.append(columns[6].get_text(strip=True))
        goals.append(columns[7].get_text(strip=True))

    for i in range(len(positions)):
        print(
            f"Position: {positions[i]}, Team: {teams[i]}, Points: {points[i]}, Matches Played: {matches_played[i]}, Wins: {wins[i]}, Draws: {draws[i]}, Losses: {losses[i]}, Goals: {goals[i]}")


if __name__ == "__main__":
    url = input("Please enter the URL of the webpage: ")
    process_data(url)
