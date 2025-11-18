"""Run the seeders for every service that exposes ``app.seed``."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SERVICE_PATHS = [
    "user-service",
    "game-catalog-service",
    "review-service",
    "shopping-service",
    "purchase-service",
    "payment-service",
    "online-service",
    "social-service",
    "notification-service",
    "recommendation-service",
]


def run_seeder(service_dir: Path, count: int) -> None:
    cmd = [sys.executable, "-m", "app.seed", "--count", str(count)]
    subprocess.run(cmd, cwd=service_dir, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed all service databases.")
    parser.add_argument(
        "--count",
        type=int,
        default=100,
        help="Target record count per service (default: 100)",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    services_root = repo_root / "services"

    for service in SERVICE_PATHS:
        service_path = services_root / service
        if not service_path.exists():
            print(f"Skipping {service} (directory not found)")
            continue
        print(f"Seeding {service}...")
        run_seeder(service_path, args.count)

    print("All seed jobs completed.")


if __name__ == "__main__":
    main()

