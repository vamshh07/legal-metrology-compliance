from datetime import datetime


def generate_report(details, results, score, final_status):

    # Current date and time
    scan_time = datetime.now().strftime(
        "%d-%m-%Y %I:%M %p"
    )

    # Start HTML report
    report = f"""
    <!DOCTYPE html>
    <html>
    <head>

        <title>Compliance Report</title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f5f7fa;
            }}

            .container {{
                background: white;
                padding: 30px;
                border-radius: 10px;
            }}

            h1 {{
                text-align: center;
            }}

            h2 {{
                margin-top: 30px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }}

            th, td {{
                border: 1px solid #cccccc;
                padding: 12px;
                text-align: left;
            }}

            th {{
                background-color: #eeeeee;
            }}

            .compliant {{
                color: green;
                font-weight: bold;
            }}

            .missing {{
                color: red;
                font-weight: bold;
            }}

            .info {{
                color: #666666;
            }}

        </style>

    </head>

    <body>

    <div class="container">

        <h1>Packaged Commodity Compliance Report</h1>

        <p>
            <strong>Scan Date:</strong>
            {scan_time}
        </p>

        <hr>

        <h2>Compliance Summary</h2>

        <p>
            <strong>Compliance Score:</strong>
            {score:.0f}%
        </p>

        <p>
            <strong>Final Status:</strong>
            {final_status}
        </p>


        <h2>Extracted Product Information</h2>

        <table>

            <tr>
                <th>Declaration</th>
                <th>Detected Value</th>
            </tr>
    """

    # Add extracted details
    for key, value in details.items():

        if value:
            display_value = value
        else:
            display_value = "Not Detected"

        report += f"""
            <tr>
                <td>{key}</td>
                <td>{display_value}</td>
            </tr>
        """

    # Compliance results section
    report += """

        </table>

        <h2>Compliance Requirement Check</h2>

        <table>

            <tr>
                <th>Requirement</th>
                <th>Status</th>
                <th>Details</th>
            </tr>
    """

    # Add compliance results
    for field, result in results.items():

        status = result["status"]
        message = result["message"]

        # Select CSS class
        if status == "COMPLIANT":
            status_class = "compliant"

        elif status == "MISSING":
            status_class = "missing"

        else:
            status_class = "info"

        report += f"""
            <tr>
                <td>{field}</td>
                <td class="{status_class}">
                    {status}
                </td>
                <td>{message}</td>
            </tr>
        """

    # End report
    report += f"""

        </table>

        <br>

        <hr>

        <p class="info">
            This report is an automated preliminary assessment
            based on OCR and rule-based analysis. Final legal
            compliance verification should be performed by an
            authorized authority.
        </p>

    </div>

    </body>
    </html>
    """

    return report