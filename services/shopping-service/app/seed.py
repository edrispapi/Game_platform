"""Seed helper for shopping service data."""
from __future__ import annotations

import argparse
import random
import uuid
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from .database import SessionLocal, init_db
from . import models


def seed_shopping(target: int = 100) -> int:
    init_db()
    session: Session = SessionLocal()
    try:
        existing = session.query(models.ShoppingCart).count()
        missing = max(0, target - existing)
        if missing == 0:
            return 0

        for offset in range(missing):
            idx = existing + offset + 1
            cart = models.ShoppingCart(
                uuid=str(uuid.uuid4()),
                user_id=str((idx % 100) + 1),
                status="active" if random.random() > 0.2 else "saved",
                currency="USD",
                subtotal=round(random.uniform(5, 120), 2),
                discount_amount=round(random.uniform(0, 20), 2),
                tax_amount=round(random.uniform(0.5, 10), 2),
                total_amount=round(random.uniform(10, 150), 2),
                expires_at=datetime.utcnow() + timedelta(days=random.randint(3, 30)),
                extra_metadata={"channel": random.choice(["web", "mobile"])},
            )

            for item_offset in range(random.randint(1, 3)):
                cart.items.append(
                    models.CartItem(
                        game_id=str(random.randint(1, 200)),
                        game_name=f"Sample Game {random.randint(1, 200)}",
                        quantity=random.randint(1, 3),
                        unit_price=round(random.uniform(4.99, 59.99), 2),
                        discount_amount=round(random.uniform(0, 10), 2),
                        total_price=round(random.uniform(4.99, 59.99), 2),
                    )
                )

            session.add(cart)
            if (offset + 1) % 20 == 0:
                session.flush()

        session.commit()
        return missing
    finally:
        session.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Seed the shopping service database with carts/items."
    )
    parser.add_argument("--count", type=int, default=100)
    args = parser.parse_args()
    created = seed_shopping(args.count)
    print(f"Shopping service seed complete (inserted {created} carts).")


if __name__ == "__main__":
    main()

