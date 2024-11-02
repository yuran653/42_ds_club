import json
import country_converter as coco # https://github.com/IndEcol/country_converter/
from tqdm import tqdm

class CountryCodeAlpha3:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.data = None

    def load_data(self):
        with open(self.input_file, 'r', encoding='utf-8') as file:
            self.data = json.load(file)
        print(f"CountryCodeAlpha3 -> Data is loaded from '{self.input_file}'")

    def process_country_codes(self):
        if self.data is None:
            print('CountryCodeAlpha3 -> Data was not loaded')
            return

        for user in tqdm(self.data['users'], desc="Processing and verifying contries"):
            # Converts country name to ISO Alpha-3 using country_converter
            iso_alpha3_code = coco.convert(names=user['location_country'], to='ISO2')
            
            if iso_alpha3_code and len(iso_alpha3_code) == 2 and iso_alpha3_code.isupper():
                user['location_country'] = iso_alpha3_code
            else:
                print(f"Conversion failed: {user['firstname']} {user['lastname']} -> {user['location_country']}")

    def save_data(self):
        if self.data is None:
            print('CountryCodeAlpha3 -> No data to save')
            return

        with open(self.output_file, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
        print(f"CountryCodeAlpha3 -> Data processing complete. Updated data saved to '{self.output_file}'")

    def run(self):
        self.load_data()
        self.process_country_codes()
        self.save_data()

# Usage example
input_file = 'batch15users.json'
output_file = 'country_batch15users.json'
CountryCodeAlpha3(input_file, output_file).run()
