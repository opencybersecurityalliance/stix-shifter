# Validate STIX bundle

You can easily validate your stix bundle file by following the below steps:

## Prerequisites:

The following needs to be installed on your local machine:

* Python 3
* GIT

If you have not already cloned the [stix-shifter github project](https://github.com/opencybersecurityalliance/stix-shifter): 
```
git clone https://github.com/opencybersecurityalliance/stix-shifter.git
```

## Validator Usage:

1. Open a terminal 
2. cd into /stix-shifter/bundle_validator
3. Copy your STIX 2.0 or 2.1 bundle JSON file into the `bundle_validator` directory
4. Run the validate.sh script. You need to specify the bundle JSON file name and the STIX specification version (2.0 or 2.1)

    `./validate.sh <STIX Bundle JSON FIle> <2.0 or 2.1>`

    Example:
    ```
    ./validate.sh my_stix_2_1_bundle.json 2.1
    ```
5. After successful validation, you should see a message in your terminal: `STIX Bundle validated!!`
6. For unsuccessful validation, you should see two types of errors:
    * If the JSON format in the bundle is invalid: `Malformed JSON in the STIX Bundle: <ERROR details>`
    * If the file contains invalid STIX Objects, you should see errors and/or warnings with the heading `[X] STIX JSON: Invalid`. It is mandatory to fix the errors marked red as `[X]`. Warnings which are marked yellow as `[!]`, can be ignored but are recommended to fix. For example:


        ```
        [X] STIX JSON: Invalid
            [!] Warning: identity--33fa3e56-6511-40de-bc69-c5ffeb3838f9: {213} identity_class contains a value not in the identity-class-ov vocabulary.
            [X] observed-data--ed82dd61-cc41-485b-b608-d278469e6259: 'number_observed' is a required property
        ```
        
        To debug the above error `[X]`, find `observed-data--ed82dd61-cc41-485b-b608-d278469e6259` "id" in the bundle file and you will see the `number_observed` property is missing in the STIX object. 
