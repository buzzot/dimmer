import csv

# Leviton dimmer models, their links, series, and dimming protocols
leviton_dimmers = [
    ("6672", "https://www.leviton.com/en/products/6672", "Rocker Series", "Triac"),
    ("6674", "https://www.leviton.com/en/products/6674", "Rocker Series", "Triac"),
    ("IPL06-10Z", "https://www.leviton.com/en/products/ipl06-10z", "IPL Series", "0-10V"),
    ("DSL06-1LZ", "https://www.leviton.com/en/products/dsl06-1lz", "DSL Series", "0-10V"),
    ("TSL06", "https://www.leviton.com/en/products/tsl06", "TSL Series", "Triac"),
    ("RDL06-10Z", "https://www.leviton.com/en/products/rdl06-10z", "RDL Series", "0-10V"),
    ("RNL06-10Z", "https://www.leviton.com/en/products/rnl06-10z", "RNL Series", "0-10V"),
    ("DH6HD", "https://www.leviton.com/en/products/dh6hd", "DH Series", "ELV"),
    ("DDL06-1LZ", "https://www.leviton.com/en/products/ddl06-1lz", "DDL Series", "0-10V"),
    ("DW1KD-1BZ", "https://www.leviton.com/en/products/dw1kd-1bz", "DW Series", "Triac"),
    ("DDL06-BLZ", "https://www.leviton.com/en/products/ddl06-blz", "DDL Series", "0-10V"),
    ("DDMX1-BLZ", "https://www.leviton.com/en/products/ddmx1-blz", "DDMX Series", "ELV"),
    ("DDE06-BLZ", "https://www.leviton.com/en/products/dde06-blz", "DDE Series", "0-10V"),
    ("DL1KD", "https://www.leviton.com/en/products/dl1kd", "DL Series", "Triac")
]

# Writing data to CSV
with open("leviton_dimmer_models_with_series_and_protocol.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["Dimmer Model", "Manufacturer Link", "Series", "Dimming Protocol"])

    # Write each Leviton dimmer model, link, series, and dimming protocol
    for dimmer in leviton_dimmers:
        writer.writerow(dimmer)

print(
    "Leviton dimmer models with series and dimming protocol saved to leviton_dimmer_models_with_series_and_protocol.csv")
