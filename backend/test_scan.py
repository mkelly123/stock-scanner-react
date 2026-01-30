from backend.scanner_pkg.scan_universe import scan_universe


symbols = ["AAPL", "MSFT", "TSLA"]
results = scan_universe(symbols, "momentum")

print(results)
