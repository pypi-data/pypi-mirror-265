# ----------------------------------------------------------------------
# |
# |  Api.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-02 12:16:00
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the Api object"""


# ----------------------------------------------------------------------
class Api:
    def Transform(self, value):
        return f"Hello, {value.lower()}, from the Api!"
