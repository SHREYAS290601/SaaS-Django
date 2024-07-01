from typing import Any

import helpers
from django.conf import settings
from django.core.management.base import BaseCommand

VENDOR_STORAGE_DIR = getattr(settings, "STATICFILES_VENDOR_DIR")


VENDOR_FILES = {
    "flowbite.min.css": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.css",
    "flowbite.min.js": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js",
}


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        self.stdout.write("Downloading vendor static files...")
        for name, urls in VENDOR_FILES.items():
            downloadable_entity = []
            self.stdout.write(f"\nDownloading {name} from {urls}\n")
            output = helpers.download_to_local(
                url=urls, out_path=VENDOR_STORAGE_DIR / name, parent_mkdir=True
            )
            if output:
                downloadable_entity.append(urls)
                self.stdout.write(f"Downloaded {name} to {output}\n")
            else:
                self.stderr.write(
                    self.style.ERROR(f"\nFailed to download {name} from {urls}\n")
                )

        # second check to see if the correct files are downloaded or not
        if set(downloadable_entity) == set(VENDOR_FILES.values()):
            self.stderr.write(
                self.style.WARNING(
                    f"\nFailed to download required values {downloadable_entity}\n"
                )
            )
        else:
            self.stdout.write(self.style.SUCCESS("\nDownloaded successfully\n"))
