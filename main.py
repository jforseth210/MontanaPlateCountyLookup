import argparse

parser = argparse.ArgumentParser()
# Use argparse to take plates as command line arguments
parser.add_argument('plates', metavar='License Plates', type=str, nargs='*',
                    help='A license plate or list of plates to look up the states for')

# Also optionally prompt for plates interactively
parser.add_argument('--interactive',
                    action="store_true", help="Prompt for plates interactively")


def load_counties():
    """
    Read the counties from the csv file
    """
    with open('MontanaCounties.csv', "r") as file:
        # Read out the lines, ignore the header
        lines = file.readlines()[1:]

        counties = []
        for line in lines:
            # Remove the newline, and split into columns
            columns = line.strip().split(",")

            # Create a county dictionary with readable names
            county = {
                "county": columns[0],
                "seat": columns[1],
                "prefix": columns[2]
            }

            # Add county dictionary to list of counties
            counties.append(county)
    return counties


def lookup(counties, plate):
    """
    Find a county in a given list of counties
    for the given license plate
    """
    # Get the county number
    plate_prefix = plate.split("-")[0]

    # Look for the county with that number
    for county in counties:
        if county["prefix"] == plate_prefix:
            return county
    return None


def main():
    """
    Find counties based on license plates
    """
    counties = load_counties()

    args = parser.parse_args()

    # Start with plates given on the command line
    plates = args.plates

    # If no plates are provided on the command line
    # and we want to prompt for them, do so.
    if not plates and args.interactive:
        # Add the inputted plates to the list
        plates = input(
            "Enter license plates separated by spaces (leave blank to quit): ").split(" ")

    # Look up plates until we aren't given any more
    while plates:
        # Lookup this batch of plates
        for plate in args.plates:
            # Lookup the county
            county = lookup(counties, plate)

            if county:
                # Print the county if we find one
                print("Plate: ", plate)
                print("County: ", county["county"])
                print("County Seat: ", county["seat"])
                print()
            else:
                # Print an error if we don't find one
                print(f"Didn't find a county for plate: {plate}")

        # Get rid of the plates we've looked up
        plates.clear()

        # Optionally prompt for more plates
        if args.interactive:
            plates = input(
                "Enter license plates separated by spaces (leave blank to quit): ").split(" ")


if __name__ == "__main__":
    main()
