# Helpdesk Ticket Merger Module for Odoo

This Odoo module allows support agents to merge multiple helpdesk tickets into a single, surviving ticket while preserving all relevant information from the original tickets. The oldest ticket among the selected tickets will be used as the final surviving merged ticket, and the newer ones will be archived. The surviving ticket will include links to the archived tickets that were merged into it.

## Features

- Merge multiple helpdesk tickets into one ticket
- The oldest ticket becomes the surviving ticket
- Newer tickets are archived with a link provided in the surviving ticket
- Merges titles, descriptions, timesheets, and time estimations

## Installation

1. Place the `helpdesk_ticket_merger` folder inside your Odoo `addons` directory.
2. Update the addons list in your Odoo instance.
3. Install the "Helpdesk Ticket Merger" module from the Apps menu.

## Usage

This basic implementation assumes you will create a button or action in the user interface to call the `action_merge_tickets` function in the `helpdesk_ticket.py` file. Please refer to the Odoo documentation on how to create buttons or actions for a specific model.

## Contributing

Please feel free to submit pull requests or report issues to improve the module. Your contributions are greatly appreciated.

## License

This module is released under the [LGPLv3 License](https://www.gnu.org/licenses/lgpl-3.0.en.html).
