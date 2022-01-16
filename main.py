import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://www.hltv.org/stats/players?startDate=all")

links = driver.find_elements(By.CLASS_NAME, "playerCol")

player_links = []
players_scores = []

for link in links[1:]:
    player_links.append(link.find_elements(By.TAG_NAME, "a")[0].get_attribute("href"))

for player in player_links:
    driver.get(player)
    stats = driver.find_elements(By.CLASS_NAME, "stats-row")
    player_stats = [
        driver.find_element(By.CLASS_NAME, "summaryNickname").text,
        driver.find_element(By.CLASS_NAME, "summaryRealname").find_element(By.TAG_NAME, "div").text,
        driver.find_element(By.CLASS_NAME, "summaryRealname").find_element(By.TAG_NAME, "img").get_attribute("alt"),
        driver.find_element(By.CLASS_NAME, "SummaryTeamname").text
    ]
    for stat in stats:
        player_stats.append(float(str(stat.find_elements(By.TAG_NAME, "span")[1].text).replace("%", "")))
    players_scores.append(player_stats)

driver.close()

df = pd.DataFrame(players_scores,
                  columns=['nickname', 'name', 'nationality', 'team', 'total_kills', 'headshot_%', 'total_deaths',
                           'kills/deaths', 'damage/round', 'grenade_dmg/round', 'maps_played', 'rounds_played',
                           'kills/round', 'assists/round', 'deaths/round', 'saved_by_teammate/round',
                           'saved_teammates/round', 'rating'])
df.to_csv("players_score.csv")
