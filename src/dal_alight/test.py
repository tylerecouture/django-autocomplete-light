"""Helpers for DAL user story based tests."""

import time


class AlightStory:
    """Define Select2 CSS selectors."""

    clear_selector = '.select2-selection__clear'
    container_selector = '.select2-container'
    dropdown_selector = '.autocomplete-light-box'
    input_selector = 'autocomplete-select input'
    label_selector = '.select2-selection__rendered'
    labels_selector = \
        '.select2-selection__rendered .select2-selection__choice'
    option_selector = '.autocomplete-light-box [data-value]'
    widget_selector = 'autocomplete-select input'

    wait_source = ' '.join((
        'document.querySelectorAll("autocomplete-light[data-bound=\'true\'], autocomplete-select[data-bound=\'true\']").length',
        '==',
        'document.querySelectorAll("autocomplete-select, autocomplete-light").length',
    ))

    def wait_script(self):
        """Wait for scripts to be loaded and ready to work."""
        tries = 100
        while tries:
            try:
                return self.browser.evaluate_script(self.wait_source)
            except:
                time.sleep(.15)
            tries -= 1
        raise Exception('All autocompletes were not bound after 15 seconds.')

    def clean_label(self, label):
        """Remove the "remove" character used in select2."""
        return label.replace('\xd7', '')
