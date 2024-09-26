# MaskIt

## Overview

**MaskIt** is a Python tool designed to help you redact sensitive information from text files. It automatically identifies and replaces sensitive data like IP addresses, file paths, URLs, email addresses, and more with descriptive placeholders, ensuring privacy and security.

### Features

- **Easy File Selection via GUI**: MaskIt provides a user-friendly interface for browsing and selecting files to be processed.
- **Automated Redaction**: Replaces sensitive information with placeholders (e.g., `[REDACTED-EMAIL]`, `[REDACTED-PHONE]`).
- **Multiple Data Formats Supported**: Handles various data types, including IP addresses, file paths, emails, and more.

### Redactions

MaskIt replaces the following data points:

| Data Point               | Replacement               |
|--------------------------|---------------------------|
| IP Address               | `x.x.x.x`                 |
| Windows File Path        | `drive:\\path\\to\\file.extension` |
| Unix File Path           | `/path/to/file.extension`  |
| URL                      | `protocol://subdomain.domain.tld:port/directory` |
| Email Address            | `[REDACTED-EMAIL]`        |
| Telephone Number         | `[REDACTED-PHONE]`        |
| Username                 | `[REDACTED-USERNAME]`     |
| Password                 | `[REDACTED-PASSWORD]`     |
| Social Security Number   | `[REDACTED-SSN]`          |
| Credit Card Number       | `[REDACTED-CREDIT-CARD]`  |

## Installation

### Requirements

- Python 3.x
- Tkinter (Python's built-in GUI library)

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/maskit.git
    cd maskit
    ```

2. Install any dependencies (if required):

    ```bash
    pip install -r requirements.txt
    ```

> **Note**: MaskIt uses Python's standard libraries, so no additional dependencies may be needed.

## Usage

1. Run the `maskit.py` script:

    ```bash
    python maskit.py
    ```

2. A GUI will appear, allowing you to browse and select the file to process.

3. MaskIt will scan the selected file for sensitive data and redact it automatically.

4. You will be prompted to choose a location to save the redacted file.

### Example

For the input file:

```
username: johndoe, password: MySecurePassword123
Email: johndoe@example.com
Phone: (123) 456-7890
Social Security Number: 123-45-6789
```

The redacted output will look like this:

```
username: [REDACTED-USERNAME], password: [REDACTED-PASSWORD]
Email: [REDACTED-EMAIL]
Phone: [REDACTED-PHONE]
Social Security Number: [REDACTED-SSN]
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contribution

Contributions are welcome! Feel free to open issues or pull requests on GitHub.

