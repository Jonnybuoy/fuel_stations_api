from django.core.management.base import BaseCommand

from fuel_routes_api.tasks import load_fuel_data


class Command(BaseCommand):
    """Helper management command to load the csv file data to db."""

    help = "Management command to load the csv file data and \
        persist to database"
    
    def add_arguments(self, parser):
        """Add arguments to the management command."""
        parser.add_argument("-f", "--file",
                            help="A csv file with the customer data.")
    
    def handle(self, *args, **kwargs):
        """Entry point for the management command"""
        csv_file = kwargs.get("file")

        if csv_file:
            load_fuel_data(csv_file)
            self.stdout.write(
                self.style.SUCCESS(
                    "Fuel price data successfully stored to database."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING("The file is required for processing")
            )
