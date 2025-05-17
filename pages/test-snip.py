import csv
def read_write_csv(input_file, output_file):
    try:
        with open(input_file, 'r', newline='') as infile:
            reader = csv.DictReader(infile)
            data = [row for row in reader]
            with open(output_file, 'w', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
                return True
    except Exception as e:
        print(f'Error: {e}')
        return False