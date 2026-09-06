def check_compliance(details):

    results = {}

    # List of mandatory fields
    mandatory_fields = [
        "MRP",
        "Net Quantity",
        "Packed Date",
        "Manufacturer",
        "Consumer Care"
    ]

    compliant_count = 0

    # Check every mandatory field
    for field in mandatory_fields:

        if details.get(field):

            results[field] = {
                "status": "COMPLIANT",
                "message": field + " is present"
            }

            compliant_count += 1

        else:

            results[field] = {
                "status": "MISSING",
                "message": field + " is missing"
            }


    # Calculate compliance score
    total_fields = len(mandatory_fields)

    score = (compliant_count / total_fields) * 100


    # Final decision
    if score == 100:
        final_status = "COMPLIANT"
    else:
        final_status = "NON-COMPLIANT"


    return results, score, final_status