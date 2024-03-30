### Pixlr API Usage Guide

This Python module provides a simple interface for automating actions on the Pixlr platform, including registration, email verification, generating images, and deleting accounts. Below is a guide on how to use this module effectively:

#### Prerequisites:

- Python 3.x installed on your system.
- Necessary Python libraries installed, including `requests`.

#### Usage Steps:

1. **Import the Module:**

   ```python
   from pixlr_private_api.main import PixlrApi
   ```

2. **Initialize PixlrApi Object:**

   ```python
   pixlr = PixlrApi()
   ```

3. **Registration:**

   ```python
   registered = pixlr.register()
   if registered:
       print("Successfully registered!")
   ```

4. **Email Verification:**

   ```python
   verified = pixlr.verify_email()
   if verified:
       print("Email verified successfully!")
   ```

5. **Generate Image:**

   ```python
   # Provide width, height, amount, and prompt for image generation
   images = pixlr.generate_image(width, height, amount, prompt)
   # 'images' will contain paths to the generated images
   ```

6. **Delete Account (Optional):**
   ```python
   deleted = pixlr.delete_account()
   if deleted:
       print("Account deleted successfully!")
   ```

#### Additional Notes:

- Ensure to handle errors and exceptions appropriately for robust usage.
- This module interacts with Pixlr through web requests, so network connectivity is required.
- API requests may be rate-limited or subject to changes by Pixlr, so handle responses accordingly.

This guide provides a basic overview of how to use the Pixlr API module. For detailed information on method parameters and return values, refer to the module's source code or documentation.
