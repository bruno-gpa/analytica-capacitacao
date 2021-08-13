# Imports
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
import pandas as pd
import os

def get_charts(chart="regional", country="global", recurrence="daily", date="latest"):
    """
    Returns a DataFrame with requested Spotify charts data.

    Args:
    chart (Chart Type)
    'regional' => Top 200 [default]
    'viral'    => Viral 50

    country (Country):
    'global' => Global chart [default]
    'br'     => Country chart 
        (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements)

    recurrence (Recurrence):
    'daily'  => Daily chart
    'weekly' => Weekly chart

    date (Date):
    'latest'     => Latest chart
    'yyyy-mm-dd' => Specific date, for 'daily' recurrence
    'yyyy-mm-dd--YYYY-MM-DD' => Specific week range (e.g. 2021-07-30--2021-08-06), for 'weekly' recurrence
    """


    # Create headless webdriver
    """
    Download the correct webdriver for your system and place it in this root folder
    geckodriver download (for Firefox): https://github.com/mozilla/geckodriver/releases
    chromedriver download (for Chrome): https://chromedriver.chromium.org/downloads
    """
    browser = "chrome"
    PATH = r"C:\Program Files (x86)\driver\chromedriver.exe"

    if browser == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options, executable_path=PATH)


    ## Gets download page
    param = {}

    """
    Chart Type:
    'regional' => Top 200
    'viral'    => Viral 50
    """
    param["chart"] = chart

    """
    Country:
    'global' => Global chart
    'br'     => Country chart 
        (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements)
    """
    param["country"] = country

    """
    Recurrence:
    'daily'  => Daily chart
    'weekly' => Weekly chart
    """
    param["recurrence"] = recurrence

    """
    Date:
    'latest'     => Latest chart
    'yyyy-mm-dd' => Specific date, for 'daily' recurrence
    'yyyy-mm-dd--YYYY-MM-DD' => Specific week range (e.g. 2021-07-30--2021-08-06), for 'weekly' recurrence
    """
    param["date"] = date

    addr = "https://spotifycharts.com/"
    params = f"{param['chart']}/{param['country']}/{param['recurrence']}/{param['date']}/"
    driver.get(f"{addr}{params}")


    # Scrapes Spotify Charts table data
    df = pd.DataFrame()

    if param["chart"] == "regional":
        table = driver.find_elements_by_xpath("/html/body/div/div/div/div/span/table/tbody/tr")
        for row in table:
            row_data = {}
            row_data["url"] = row.find_element_by_xpath(".//td[1]/a").get_attribute("href")
            row_data["img"] = row.find_element_by_xpath(".//td[1]/a/img").get_attribute("src")
            row_data["position"] = int(row.find_element_by_xpath(".//td[2]").text)
            row_data["track"] = row.find_element_by_xpath(".//td[4]/strong").text
            row_data["artists"] = row.find_element_by_xpath(".//td[4]/span").text[3:].split(", ")
            row_data["streams"] = int(row.find_element_by_xpath(".//td[5]").text.replace(",",""))

            row_df = pd.DataFrame.from_records([row_data])
            df = pd.concat([df, row_df], ignore_index=True)

    else:
        table = driver.find_elements_by_xpath("/html/body/div/div/div/div/span/table/tbody/tr")
        for row in table:
            row_data = {}
            row_data["url"] = row.find_element_by_xpath(".//td[1]/a").get_attribute("href")
            row_data["img"] = row.find_element_by_xpath(".//td[1]/a/img").get_attribute("src")
            row_data["position"] = int(row.find_element_by_xpath(".//td[2]").text)
            row_data["track"] = row.find_element_by_xpath(".//td[4]/strong").text
            row_data["artists"] = row.find_element_by_xpath(".//td[4]/span").text[3:].split(", ")

            row_df = pd.DataFrame.from_records([row_data])
            df = pd.concat([df, row_df], ignore_index=True)


    # Closes webdriver
    driver.close()

    os.makedirs("./data", exist_ok=True)
    df.to_csv(f"./data/{param['chart']}_{param['country']}_{param['recurrence']}_{param['date']}.csv", 
                sep=";", index=False)

    return df

if __name__ == "__main__":
    for country in ["global", "br", "us", "jp", "sa"]:
        get_charts(country=country)
        print(f"Scraped country {country}")