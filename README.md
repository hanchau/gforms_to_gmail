### gforms_to_gmail
#### A tool to watch the google sheet and trigger an email on insert to the sheet.

1. Watcher - watches the given sheet-worksheet.
    1. Authenticates with service account.
    2. Loads the given sheet-worksheet.
    3. Downloads the sheet data.
    4. Compare the number of records with the cached records.
    5. Triggers a mail if the new records have been added.
    
2. Emailer - Send a custome email to the given mail_id.
    1. Creates the message as per the logic.
    2. Sends the custom message to the given mail id.