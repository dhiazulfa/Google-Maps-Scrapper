from playwright.sync_api import sync_playwright
import pandas as pd
import argparse
import json

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://www.google.com/maps/search/" + search_for, timeout=60000)
        page.wait_for_timeout(3000)

        listings = []
        previously_counted = 0

        while True:
            page.mouse.wheel(0, 10000)
            page.wait_for_timeout(3000)

            current_count = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count()

            if current_count >= total:
                listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()[:total]
                print(f"Total data: {len(listings)}")
                break
            elif current_count == previously_counted:
                listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()
                print(f"Kurir sedang menuju lokesiong\nTotal Data yang diambil: {len(listings)}")
                break
            else:
                previously_counted = current_count
                print(f"Currently Found: {current_count}")

        names_list = []
        address_list = []
        website_list = []
        phones_list = []
        reviews_c_list = []
        reviews_a_list = []
        store_s_list = []
        in_store_list = []
        store_del_list = []
        place_t_list = []
        open_list = []
        intro_list = []

        for listing in listings:
            listing.click(timeout=60000)
            page.wait_for_timeout(5000)

            name_xpath = '//div[@class="TIHn2 "]//h1[@class="DUwDvf lfPIob"]'
            address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
            website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
            phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
            reviews_count_xpath = '//div[@class="TIHn2 "]//div[@class="fontBodyMedium dmRWX"]//div//span//span//span[@aria-label]'
            reviews_average_xpath = '//div[@class="TIHn2 "]//div[@class="fontBodyMedium dmRWX"]//div//span[@aria-hidden]'
            info1 = '//div[@class="LTs0Rc"][1]'  # store
            info2 = '//div[@class="LTs0Rc"][2]'  # pickup
            info3 = '//div[@class="LTs0Rc"][3]'  # delivery
            opens_at_xpath = '//button[contains(@data-item-id, "oh")]//div[contains(@class, "fontBodyMedium")]'  # time
            opens_at_xpath2 = '//div[@class="MkV9"]//span[@class="ZDu9vd"]//span[2]'
            place_type_xpath = '//div[@class="LBgpqf"]//button[@class="DkEaL "]'  # type of place
            intro_xpath = '//div[@class="WeS02d fontBodyMedium"]//div[@class="PYvSYb "]'

            name = page.locator(name_xpath).inner_text() if page.locator(name_xpath).count() > 0 else ""
            address = page.locator(address_xpath).inner_text() if page.locator(address_xpath).count() > 0 else ""
            website = page.locator(website_xpath).inner_text() if page.locator(website_xpath).count() > 0 else ""
            phone_number = page.locator(phone_number_xpath).inner_text() if page.locator(phone_number_xpath).count() > 0 else ""
            reviews_count = int(page.locator(reviews_count_xpath).inner_text().replace('(', '').replace(')', '').replace(',', '')) if page.locator(reviews_count_xpath).count() > 0 else ""
            reviews_average = float(page.locator(reviews_average_xpath).inner_text().replace(' ', '').replace(',', '.')) if page.locator(reviews_average_xpath).count() > 0 else ""
            store_shopping = page.locator(info1).inner_text().split('·')[1].replace("\n", "") if page.locator(info1).count() > 0 and 'shop' in page.locator(info1).inner_text() else ""
            in_store_pickup = page.locator(info2).inner_text().split('·')[1].replace("\n", "") if page.locator(info2).count() > 0 and 'pickup' in page.locator(info2).inner_text() else ""
            store_delivery = page.locator(info3).inner_text().split('·')[1].replace("\n", "") if page.locator(info3).count() > 0 and 'delivery' in page.locator(info3).inner_text() else ""
            place_type = page.locator(place_type_xpath).inner_text() if page.locator(place_type_xpath).count() > 0 else ""
            opens_at = page.locator(opens_at_xpath).inner_text().split('⋅')[1].replace("\u202f", "") if page.locator(opens_at_xpath).count() > 0 else ""
            introduction = page.locator(intro_xpath).inner_text() if page.locator(intro_xpath).count() > 0 else ""

            names_list.append(name)
            address_list.append(address)
            website_list.append(website)
            phones_list.append(phone_number)
            reviews_c_list.append(reviews_count)
            reviews_a_list.append(reviews_average)
            store_s_list.append(store_shopping)
            in_store_list.append(in_store_pickup)
            store_del_list.append(store_delivery)
            place_t_list.append(place_type)
            open_list.append(opens_at)
            intro_list.append(introduction)

        # Membuat DataFrame
        data = {
            "Name": names_list,
            "Address": address_list,
            "Website": website_list,
            "Phone Number": phones_list,
            "Review Count": reviews_c_list,
            "Average Review Count": reviews_a_list,
            "Store Shopping": store_s_list,
            "In Store Pickup": in_store_list,
            "Store Delivery": store_del_list,
            "Place Type": place_t_list,
            "Opens At": open_list,
            "Introduction": intro_list
        }

        df = pd.DataFrame(data)

        # Hapus data yang tidak memiliki nomor telepon
        df_filtered = df[df['Phone Number'] != ""]

        # Konversi DataFrame ke JSON
        json_data = df_filtered.to_dict(orient='records')

        # Simpan hasil ke file JSON
        with open("scraped_data.json", "w") as json_file:
            json.dump(json_data, json_file, indent=4)
        print("Data saved to scraped_data.json")

        browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--total', type=int, required=True, help='Total number of results to scrape')
    parser.add_argument('--search_for', type=str, required=True, help='Search query for Google Maps')
    args = parser.parse_args()
    total = args.total
    search_for = args.search_for
    main()
