#!/usr/bin/env python3
"""
Simple menu interface for the Video Game Database
"""

from pathlib import Path

from osvg.db_class import DB


class GameInterface:
    def __init__(self):
        self.db = DB(Path("videogame_db.sqlite"))

    def show_menu(self):
        print("\n" + "=" * 50)
        print("🎮 VIDEO GAME DATABASE SYSTEM")
        print("=" * 50)
        print("1. 👀 View all games")
        print("2. 👨‍💻 View all developers")
        print("3. 🔍 Search games")
        print("4. ➕ Add new game")
        print("5. ➕ Add new developer")
        print("6. 🗑️ Delete game")
        print("7. 🗑️ Delete developer")
        print("8. 📊 Show statistics")
        print("9. 🧪 Run quick test")
        print("0. 🚪 Exit")
        print("-" * 50)

    def view_all_games(self):
        print("\n🎮 ALL GAMES:")
        print("-" * 40)
        games = self.db.get_all_games()
        if not games:
            print("   No games found. Add some games first!")
            return

        for i, game in enumerate(games, 1):
            status = "✅ Published" if game.is_published else "⏳ Draft"
            price = game.price or "Free"
            print(f"{i:2d}. {game.title}")
            print(f"    Developer: {game.author_name}")
            print(f"    Genre: {game.genre or 'Not specified'}")
            print(f"    Price: {price} | {status}")
            if game.description:
                print(f"    Description: {game.description}")
            print()

    def view_all_developers(self):
        print("\n👨‍💻 ALL DEVELOPERS:")
        print("-" * 40)
        authors = self.db.get_all_authors()
        if not authors:
            print("   No developers found. Add some developers first!")
            return

        for i, author in enumerate(authors, 1):
            status = "✅ Active" if author.is_active else "❌ Inactive"
            print(f"{i:2d}. {author.name} ({author.email}) - {status}")

    def search_games(self):
        print("\n🔍 SEARCH GAMES:")
        search_term = input("Enter game title to search: ").strip()
        if not search_term:
            return

        from sqlalchemy import text

        sql = text("SELECT * FROM video_games WHERE title LIKE :search")

        with self.db.engine.connect() as conn:
            results = conn.execute(sql, {"search": f"%{search_term}%"}).fetchall()

        if not results:
            print(f"   No games found matching '{search_term}'")
            return

        print(f"\n📋 GAMES MATCHING '{search_term}':")
        print("-" * 40)
        for game in results:
            print(f"• {game.title} (ID: {game._id})")

    def add_new_game(self):
        print("\n➕ ADD NEW GAME:")
        print("-" * 30)

        # Get authors first
        authors = self.db.get_all_authors()
        if not authors:
            print("❌ No developers found! Add a developer first.")
            return

        # Show available developers
        print("Available developers:")
        for i, author in enumerate(authors, 1):
            print(f"  {i}. {author.name}")

        try:
            choice = int(input(f"Choose developer (1-{len(authors)}): "))
            if choice < 1 or choice > len(authors):
                print("❌ Invalid choice!")
                return
            author_id = authors[choice - 1]._id
        except ValueError:
            print("❌ Invalid input!")
            return

        title = input("Game title: ").strip()
        if not title:
            print("❌ Title cannot be empty!")
            return

        genre = input("Genre (optional): ").strip() or None
        price = input("Price (optional): ").strip() or None
        description = input("Description (optional): ").strip() or None

        published = input("Published? (y/n): ").strip().lower() == "y"

        game_id = self.db.insert_video_game(
            title=title,
            author_id=author_id,
            genre=genre,
            price=price,
            description=description,
            is_published=published,
        )

        print(f"✅ Added game '{title}' with ID: {game_id}")

    def add_new_developer(self):
        print("\n➕ ADD NEW DEVELOPER:")
        print("-" * 35)

        name = input("Developer name: ").strip()
        if not name:
            print("❌ Name cannot be empty!")
            return

        email = input("Email: ").strip()
        if not email:
            print("❌ Email cannot be empty!")
            return

        author_id = self.db.insert_author(name, email)
        print(f"✅ Added developer '{name}' with ID: {author_id}")

    def show_statistics(self):
        print("\n📊 DATABASE STATISTICS:")
        print("-" * 40)

        total_games = self.db.get_last_row_id("video_games")
        total_authors = self.db.get_last_row_id("authors")

        # Count published games
        from sqlalchemy import text

        sql = text("SELECT COUNT(*) FROM video_games WHERE is_published = 1")
        with self.db.engine.connect() as conn:
            published_count = conn.execute(sql).scalar()

        print(f"📈 Total Games: {total_games}")
        print(f"👨‍💻 Total Developers: {total_authors}")
        print(f"✅ Published Games: {published_count}")
        print(f"⏳ Draft Games: {total_games - published_count}")

    def run_quick_test(self):
        print("\n🧪 RUNNING QUICK TEST:")
        print("-" * 35)

        # Add test data
        test_author_id = self.db.insert_author("Test Developer", "test@example.com")
        test_game_id = self.db.insert_video_game(
            "Test Game", test_author_id, genre="Test", price="Free", is_published=True
        )

        print(f"✅ Created test developer (ID: {test_author_id})")
        print(f"✅ Created test game (ID: {test_game_id})")
        print("✅ Database is working correctly!")

        # Clean up test data
        from sqlalchemy import text

        with self.db.engine.connect() as conn:
            # Delete test game first (due to foreign key)
            conn.execute(
                text("DELETE FROM video_games WHERE _id = :id"), {"id": test_game_id}
            )
            # Delete test author
            conn.execute(
                text("DELETE FROM authors WHERE _id = :id"), {"id": test_author_id}
            )
            conn.commit()

        print("🧹 Cleaned up test data")

    def delete_game(self):
        print("\n🗑️ DELETE GAME:")
        print("-" * 25)

        # Show available games
        games = self.db.get_all_games()
        if not games:
            print("❌ No games found!")
            return

        print("Available games:")
        for i, game in enumerate(games, 1):
            print(f"  {i}. {game.title} (ID: {game._id})")

        try:
            choice = int(input(f"Choose game to delete (1-{len(games)}): "))
            if choice < 1 or choice > len(games):
                print("❌ Invalid choice!")
                return

            game_to_delete = games[choice - 1]

            # Confirm deletion
            confirm = (
                input(
                    f"⚠️ Delete '{game_to_delete.title}'? This cannot be undone! (y/n): "
                )
                .strip()
                .lower()
            )
            if confirm != "y":
                print("❌ Deletion cancelled")
                return

            # Delete the game
            if self.db.delete_game(game_to_delete._id):
                print(f"✅ Deleted game '{game_to_delete.title}'")
            else:
                print("❌ Failed to delete game")

        except ValueError:
            print("❌ Invalid input!")

    def delete_developer(self):
        print("\n🗑️ DELETE DEVELOPER:")
        print("-" * 30)

        # Show available developers
        authors = self.db.get_all_authors()
        if not authors:
            print("❌ No developers found!")
            return

        print("Available developers:")
        for i, author in enumerate(authors, 1):
            print(f"  {i}. {author.name} (ID: {author._id})")

        try:
            choice = int(input(f"Choose developer to delete (1-{len(authors)}): "))
            if choice < 1 or choice > len(authors):
                print("❌ Invalid choice!")
                return

            author_to_delete = authors[choice - 1]

            # Ask about games
            print(f"\n⚠️ Delete '{author_to_delete.name}'?")
            print("1. Delete developer only (will fail if they have games)")
            print("2. Delete developer AND all their games")
            print("3. Cancel")

            delete_choice = input("Choose option (1-3): ").strip()

            if delete_choice == "1":
                # Delete author only
                if self.db.delete_author(author_to_delete._id):
                    print(f"✅ Deleted developer '{author_to_delete.name}'")
                else:
                    print("❌ Failed to delete developer (they may have games)")

            elif delete_choice == "2":
                # Confirm deletion of everything
                confirm = (
                    input(
                        "⚠️ This will delete ALL games by this developer! Continue? (y/n): "
                    )
                    .strip()
                    .lower()
                )
                if confirm == "y":
                    if self.db.delete_author_and_games(author_to_delete._id):
                        print(
                            f"✅ Deleted developer '{author_to_delete.name}' and all their games"
                        )
                    else:
                        print("❌ Failed to delete developer")
                else:
                    print("❌ Deletion cancelled")

            else:
                print("❌ Deletion cancelled")

        except ValueError:
            print("❌ Invalid input!")

    def run(self):
        print("🎉 Welcome to your Video Game Database!")

        while True:
            self.show_menu()

            try:
                choice = input("Choose an option (0-9): ").strip()

                if choice == "0":
                    print("\n👋 Goodbye!")
                    break
                elif choice == "1":
                    self.view_all_games()
                elif choice == "2":
                    self.view_all_developers()
                elif choice == "3":
                    self.search_games()
                elif choice == "4":
                    self.add_new_game()
                elif choice == "5":
                    self.add_new_developer()
                elif choice == "6":
                    self.delete_game()
                elif choice == "7":
                    self.delete_developer()
                elif choice == "8":
                    self.show_statistics()
                elif choice == "9":
                    self.run_quick_test()
                else:
                    print("❌ Invalid option! Please choose 0-9.")

                input("\nPress Enter to continue...")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    """Entry point for the video game database interface."""
    interface = GameInterface()
    interface.run()


if __name__ == "__main__":
    main()
