import csv

# Dimmer models, their links, series, and dimming protocols
dimmers = [
    ("DVCL-253P", "https://www.lutron.com/en-US/products/pages/dimmers/dvcl-253p", "DVCL Series", "Triac"),
    ("DVCL-153P", "https://www.lutron.com/en-US/products/pages/dimmers/dvcl-153p", "DVCL Series", "Triac"),
    ("CTCL-153P", "https://www.lutron.com/en-US/products/pages/dimmers/ctcl-153p", "CTCL Series", "ELV"),
    ("SCL-153P", "https://www.lutron.com/en-US/products/pages/dimmers/scl-153p", "SCL Series", "ELV"),
    ("AYCL-153P", "https://www.lutron.com/en-US/products/pages/dimmers/aycl-153p", "AYCL Series", "Triac"),
    ("AYCL-253P", "https://www.lutron.com/en-US/products/pages/dimmers/aycl-253p", "AYCL Series", "Triac"),
    ("NTCL-250", "https://www.lutron.com/en-US/products/pages/dimmers/ntcl-250", "NTCL Series", "0-10V"),
    ("RCL-153PNL", "https://www.lutron.com/en-US/products/pages/dimmers/rcl-153pnl", "RCL Series", "0-10V"),
    ("PD-6WCL", "https://www.lutron.com/en-US/products/pages/dimmers/pd-6wcl", "PD Series", "0-10V"),
    ("PD-10NXD", "https://www.lutron.com/en-US/products/pages/dimmers/pd-10nxd", "PD Series", "0-10V"),
    ("MACL-153M", "https://www.lutron.com/en-US/products/pages/dimmers/macl-153m", "MACL Series", "ELV"),
    ("MACL-LFQ", "https://www.lutron.com/en-US/products/pages/dimmers/macl-lfq", "MACL Series", "ELV"),
    ("MSCL-OP153M", "https://www.lutron.com/en-US/products/pages/dimmers/mscl-op153m", "MSCL Series", "Triac"),
    ("STCL-153PR", "https://www.lutron.com/en-US/products/pages/dimmers/stcl-153pr", "STCL Series", "Triac")
]

# Writing data to CSV
with open("dimmer_models_with_series_and_protocol.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["Dimmer Model", "Manufacturer Link", "Series", "Dimming Protocol"])

    # Write each dimmer model, link, series, and dimming protocol
    for dimmer in dimmers:
        writer.writerow(dimmer)

print("Dimmer models with series and dimming protocol saved to dimmer_models_with_series_and_protocol.csv")
