from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

ITEM_LINK = "https://www.amazon.ca/dp/B0CXSS2D29/ref=sspa_dk_detail_1?content-id=amzn1.sym.d8c43617-c625-45bd-a63f-ad8715c2c055&pd_rd_i=B0CXSS2D29&pd_rd_r=4e9ba8b3-de18-40f1-9832-5cf069632a0b&pd_rd_w=5RZ4b&pd_rd_wg=wAOuT&pf_rd_p=d8c43617-c625-45bd-a63f-ad8715c2c055&pf_rd_r=1ZH5P62HWHG2TF28EMPV&psc=1&s=hi&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWw"
PRICE_IN_MIND = 100

HEADERS = eval(os.getenv("HEADERS"))

item_page = requests.get(url=ITEM_LINK, headers=HEADERS).text
soup = BeautifulSoup(item_page, "html.parser")
print(soup.prettify())
item_name = " ".join(soup.select_one("#productTitle").getText().split())
price_whole = soup.select_one("#corePriceDisplay_desktop_feature_div .a-price-whole").getText()
price_fraction = soup.select_one("#corePriceDisplay_desktop_feature_div .a-price-fraction").getText()
item_price = float(price_whole + price_fraction)

if item_price <= PRICE_IN_MIND:
    my_email = os.getenv("MY_EMAIL")
    with smtplib.SMTP(host=os.getenv("SMTP_ADDRESS"), port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=os.getenv("PASSWORD"))
        connection.sendmail(
            from_addr=my_email,
            to_addrs=os.getenv("RECIPIENT_EMAIL"),
            msg=f"Subject: Amazon Price Alert!\n\n"
                f"{item_name} is now {item_price}\n{ITEM_LINK}".encode("UTF-8"),
        )
        # UTF-8 enables unicode, good for letters with accent