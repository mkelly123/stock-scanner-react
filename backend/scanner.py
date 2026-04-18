from fastapi import APIRouter
from scanner_pkg.scan_universe import scan_universe

print("Importing scanner.py...")

router = APIRouter()

# ---------------------------------------------------------
# REST API endpoint
# ---------------------------------------------------------
@router.get("/scan/{filter_type}")
async def scan_api(filter_type: str, strategy: str = "swing"):
    """
    Wrapper around scan_universe that safely forwards strategy
    only if scan_universe supports it.
    """

    try:
        # Try calling scan_universe WITH strategy
        try:
            results = scan_universe(
                universe=["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"],
                filter_type=filter_type,
                strategy=strategy
            )
        except TypeError:
            # Fallback: scan_universe does NOT accept strategy
            print(">>> scan_universe() does not accept 'strategy' — calling without it")
            results = scan_universe(
                universe=["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"],
                filter_type=filter_type
            )

        return results

    except Exception as e:
        print("[ERROR] Scanner crashed:", e)
        return []
