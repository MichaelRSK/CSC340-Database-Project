"""Minimal entrypoint for DB/auth smoke checks."""

from store_app.auth import seed_manager_account


def main() -> None:
    created = seed_manager_account()
    if created:
        print("Manager seed account created.")
    else:
        print("Manager seed account already exists.")


if __name__ == "__main__":
    main()
