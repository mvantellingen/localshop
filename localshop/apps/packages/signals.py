from django.dispatch import Signal

release_file_notfound = Signal(providing_args=["release_file"])
