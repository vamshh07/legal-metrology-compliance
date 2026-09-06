import re


def extract_product_details(text):

    details = {
        "Product Name": None,
        "MRP": None,
        "Net Quantity": None,
        "Packed Date": None,
        "Use By / Best Before": None,
        "Manufacturer": None,
        "Consumer Care": None,
        "Unit Sale Price": None,
        "Country of Origin": None
    }

    # Convert multiple spaces/newlines into single space
    clean_text = re.sub(r"\s+", " ", text)


    # -----------------------------------------
    # PRODUCT NAME
    # -----------------------------------------

    product_keywords = [
        "chips",
        "biscuits",
        "shampoo",
        "soap",
        "namkeen",
        "snacks",
        "chocolate",
        "juice",
        "noodles",
        "rice",
        "oil"
    ]

    for keyword in product_keywords:
        if keyword.lower() in clean_text.lower():
            details["Product Name"] = keyword.title()
            break


    # -----------------------------------------
    # MRP
    # -----------------------------------------

    mrp_pattern = r"MRP.*?([0-9]+(?:\.[0-9]+)?)"

    mrp_match = re.search(
        mrp_pattern,
        clean_text,
        re.IGNORECASE
    )

    if mrp_match:
        details["MRP"] = "₹ " + mrp_match.group(1)


    # -----------------------------------------
    # NET QUANTITY
    # -----------------------------------------

    quantity_pattern = (
        r"(?:NET\s+WEIGHT|NET\s+WT|NET\s+QUANTITY)"
        r"\s*:?\s*"
        r"([0-9]+(?:\.[0-9]+)?)"
        r"\s*"
        r"(kg|g|ml|l|9)"
    )

    quantity_match = re.search(
        quantity_pattern,
        clean_text,
        re.IGNORECASE
    )

    if quantity_match:

        number = quantity_match.group(1)
        unit = quantity_match.group(2)

        # OCR may read 'g' as '9'
        if unit == "9":
            unit = "g"

        details["Net Quantity"] = number + " " + unit


    # -----------------------------------------
    # PACKED / MANUFACTURE DATE
    # -----------------------------------------

    date_pattern = (
        r"(?:PACKED\s*ON|PACKED|PKD|MFD|MANUFACTURED)"
        r".*?"
        r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"
    )

    date_match = re.search(
        date_pattern,
        clean_text,
        re.IGNORECASE
    )

    if date_match:
        details["Packed Date"] = date_match.group(1)


    # -----------------------------------------
    # USE BY / BEST BEFORE
    # -----------------------------------------

    expiry_pattern = (
        r"(?:USE\s*BY|BEST\s*BEFORE|EXPIRY|EXP)"
        r".*?"
        r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"
    )

    expiry_match = re.search(
        expiry_pattern,
        clean_text,
        re.IGNORECASE
    )

    if expiry_match:
        details["Use By / Best Before"] = expiry_match.group(1)


    # -----------------------------------------
    # MANUFACTURER
    # -----------------------------------------

    manufacturer_keywords = [
        "manufactured by",
        "manufacturer",
        "packed by",
        "marketed by"
    ]

    for keyword in manufacturer_keywords:
        if keyword in clean_text.lower():
            details["Manufacturer"] = "Found"
            break


    # -----------------------------------------
    # CONSUMER CARE
    # -----------------------------------------

    consumer_keywords = [
        "consumer care",
        "customer care",
        "consumer complaint",
        "complaints",
        "feedback",
        "helpline",
        "contact",
        "care"
    ]

    for keyword in consumer_keywords:
        if keyword in clean_text.lower():
            details["Consumer Care"] = "Found"
            break


    # -----------------------------------------
    # UNIT SALE PRICE
    # -----------------------------------------

    unit_price_pattern = (
        r"(?:UNIT\s+SALE\s+PRICE)"
        r".*?"
        r"([0-9]+(?:\.[0-9]+)?)"
        r"\s*(?:per|/)"
    )

    unit_price_match = re.search(
        unit_price_pattern,
        clean_text,
        re.IGNORECASE
    )

    if unit_price_match:
        details["Unit Sale Price"] = (
            "₹ " + unit_price_match.group(1)
        )


    # -----------------------------------------
    # COUNTRY OF ORIGIN
    # -----------------------------------------

    country_pattern = (
        r"(?:COUNTRY\s+OF\s+ORIGIN|MADE\s+IN)"
        r"\s*:?\s*"
        r"([A-Za-z ]+)"
    )

    country_match = re.search(
        country_pattern,
        clean_text,
        re.IGNORECASE
    )

    if country_match:
        details["Country of Origin"] = (
            country_match.group(1).strip()
        )


    return details