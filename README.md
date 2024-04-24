# Humane Changelog Monitor

Humane Changelog Monitor is a Python script that monitors Humane's changelog for updates and posts them to a Discord webhook. It allows you to stay up-to-date with the latest changes and improvements in Humane's software.

## Features

- Retrieves the latest updates from the Humane's changelog URL
- Parses the update content and extracts relevant information
- Posts the updates to a specified Discord webhook
- Keeps track of previously posted updates to avoid duplicates
- Continuously checks for new updates at a configurable interval

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/theandersmadsen/humane-changelog-monitor.git
   ```

2. Navigate to the project directory:
   ```
   cd humane-changelog-monitor
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project directory and add the following variables:
   ```
   DISCORD_WEBHOOK_URL=your-discord-webhook-url
   ```
   Replace `your-discord-webhook-url` with the actual URL of your Discord webhook.

## Usage

To start monitoring Humane's changelog page, run the following command:
```
python humane_changelog_monitor.py
```

The script will continuously check for updates at the specified interval (default is 600 seconds) and post any new updates to the configured Discord webhook.

## Configuration

You can customize the behavior of the Humane Changelog Monitor by modifying the following variables in the `.env` file:

- `DISCORD_WEBHOOK_URL`: The URL of the Discord webhook where the updates will be posted.
- `HUMANE_CHANGELOG_URL`: The URL of the Humane AI changelog JSON file.

Additionally, you can adjust the `check_interval` parameter in the `main` function to change the frequency of update checks (in seconds).

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## Acknowledgements

- [Humane](https://humane.com/) for providing the changelog data.
- [Python](https://www.python.org/) for the programming language.
- [Requests](https://docs.python-requests.org/) for making HTTP requests.
- [python-dotenv](https://github.com/theskumar/python-dotenv) for loading environment variables from a `.env` file.

## Contact

If you have any questions or feedback, please feel free to reach out:

- Email: anders@andersmadsen.dk
- Twitter: [@AndersMadsenYT](https://twitter.com/AndersMadsenYT)
- GitHub: [theandersmadsen](https://github.com/theandersmadsen)

Happy monitoring!
