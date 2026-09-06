from PIL import Image
from ocr_engine import extract_text
from extractor import extract_product_details
from compliance_engine import check_compliance


# Open product image
image = Image.open("product.jpg")


# Extract text using OCR
text = extract_text(image)

print("\nExtracted Text:")
print(text)


# Extract important product details
details = extract_product_details(text)

print("\nProduct Details:")

for key, value in details.items():
    print(key, ":", value)


# Check compliance
results, score, final_status = check_compliance(details)


print("\nCompliance Results:")

for field, result in results.items():

    print(
        field,
        ":",
        result["status"]
    )


print("\nCompliance Score:", score, "%")

print("Final Status:", final_status)