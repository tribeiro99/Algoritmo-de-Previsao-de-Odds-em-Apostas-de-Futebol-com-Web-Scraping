from selenium import webdriver
from bs4 import BeautifulSoup
from collections import Counter

def get_page_content(url):
    driver = webdriver.Chrome()
    driver.get(url)

    driver.implicitly_wait(10)

    page_content = driver.page_source
    driver.quit()

    return page_content

def calculate_odds(wins, matches_played):
    try:
        if wins.isdigit():
            wins_value = int(wins)
        elif wins.upper() == 'V':
            wins_value = 0
        else:
            raise ValueError("Invalid 'Wins' value")

        matches_played_value = int(matches_played)

        if matches_played_value > 0:
            return 1 / (wins_value / matches_played_value)
        else:
            print("Invalid matches_played value:", matches_played_value)
            return None
    except ValueError:
        print("Error: 'Wins' is not a valid integer.")
        return None

def identify_target_team(matches):
    teams = [match.split(", ")[4] for match in matches]
    team_counter = Counter(teams)
    target_team, _ = team_counter.most_common(1)[0]
    return target_team

def process_data(url):
    html_content = get_page_content(url)

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

        casa_section = soup.find('span', class_='stats-subtitle', string='Casa')

        if casa_section:
            table = casa_section.find_next('table', class_='results')

            if table:
                rows = table.find_all('tr')

                headers = [header.get_text(strip=True) for header in table.select('thead th')]
                print('\t'.join(headers))

                for row in rows:
                    cols = row.find_all('td')
                    if cols:
                        position = cols[0].get_text(strip=True)
                        team = cols[1].get_text(strip=True)
                        points = cols[2].get_text(strip=True)
                        matches_played = cols[3].get_text(strip=True)
                        wins = cols[4].get_text(strip=True)
                        draws = cols[5].get_text(strip=True)
                        losses = cols[6].get_text(strip=True)
                        goals = cols[7].get_text(strip=True)

                        if team.lower() == target_team.lower():
                            print(
                                f"Position: {position}, Team: {team}, Points: {points}, Matches Played: {matches_played}, Wins: {wins}, Draws: {draws}, Losses: {losses}, Goals: {goals}")

                            odds = calculate_odds(wins, matches_played)
                            if odds is not None:
                                print(f"Odds for HOME TEAM to win: {odds:.4f},{team}")

            else:
                print("Sub-table not found in the 'Casa' section")
        else:
            print("Casa section not found")
    else:
        print("Table not found. Check if the HTML structure has changed or the URL is correct.")

if __name__ == "__main__":
    url = input("Please enter the URL of the webpage: ")
    process_data(url)
