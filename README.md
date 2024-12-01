# PYC3



## Arhitecture.

This application serves as a backend capable of processing and reading data from Excel files. To utilize this backend and connect it to a frontend, a user account is required. The account is essential as it provides a unique API key for authentication and authorization.

Excel files are read using Pandas, which converts the file content into a DataFrame. Once transformed into a DataFrame, the data is further converted into JSON format based on the specific functions or filters requested. This enables dynamic and customizable data extraction from the Excel file.

The Excel file itself is stored in the database as a binary large object (BLOB), ensuring secure and efficient storage


## Get and store the excel file

The Excel file is uploaded via the /excel endpoint of the API. At this endpoint, the file undergoes validation to ensure it is an Excel file, even if the frontend does not perform this check. Once validated, the file is renamed for consistency and security.

The renaming process involves appending a unique ID, derived from the user’s API key, to the file name. The resulting format is {ID}.xlsx. The renamed file is then securely stored in the database as a BLOB with its new identifier, ensuring traceability and efficient management.



## How the backend know what data to give you

The below API endpoint, accessible via /<string:para>/<string:ident> with a GET request, dynamically processes Excel files stored in a database. It retrieves the file based on an id query parameter, reads it into a Pandas DataFrame, and executes specific functions depending on the para value (e.g., counting null values, extracting data, summarizing content, filling missing values, or generating charts). The user's existence and identification (ident) are validated against the database, and if necessary, new identification records are created. By utilizing specialized classes (RespondGet and ResponseFill), the endpoint ensures modular and efficient data manipulation while maintaining robust error handling and database consistency.
