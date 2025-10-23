#!/usr/bin/env python3
"""
Simple Test Script for Steam Clone Services
Tests the data import and basic functionality without Docker
"""

import asyncio
import aiohttp
import json
import random
import string
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleSteamCloneTester:
    def __init__(self):
        self.games_data = []
        self.users_data = []
        
    def create_sample_games(self, count: int = 20) -> List[Dict[str, Any]]:
        """Create sample game data"""
        logger.info(f"Creating {count} sample games...")
        
        games = []
        for i in range(count):
            game = {
                'app_id': 100000 + i,
                'name': f"Sample Game {i+1}",
                'type': 'game',
                'price': round(random.uniform(4.99, 79.99), 2),
                'discount': random.choice([0, 0, 0, 10, 15, 20, 25, 30]),
                'final_price': 0,  # Will be calculated
                'currency': 'USD',
                'release_date': (datetime.now() - timedelta(days=random.randint(0, 3650))).strftime('%Y-%m-%d'),
                'developer': random.choice([
                    'Valve Corporation', 'CD Projekt Red', 'Rockstar Games', 'Ubisoft',
                    'Electronic Arts', 'Activision', 'Blizzard Entertainment', 'Bethesda',
                    'Square Enix', 'Capcom', 'Bandai Namco', 'Sega', 'Nintendo'
                ]),
                'publisher': random.choice([
                    'Valve Corporation', 'CD Projekt', 'Rockstar Games', 'Ubisoft',
                    'Electronic Arts', 'Activision', 'Blizzard Entertainment', 'Bethesda',
                    'Square Enix', 'Capcom', 'Bandai Namco', 'Sega', 'Nintendo'
                ]),
                'genres': random.sample([
                    'Action', 'Adventure', 'RPG', 'Strategy', 'Simulation', 'Sports',
                    'Racing', 'Fighting', 'Puzzle', 'Horror', 'Indie', 'Casual'
                ], random.randint(1, 4)),
                'tags': random.sample([
                    'Singleplayer', 'Multiplayer', 'Co-op', 'Online Co-op', 'Local Co-op',
                    'PvP', 'MMO', 'VR', 'Early Access', 'Free to Play', 'Steam Workshop',
                    'Controller Support', 'Steam Achievements', 'Steam Trading Cards'
                ], random.randint(5, 10)),
                'platforms': random.sample(['Windows', 'Mac', 'Linux'], random.randint(1, 3)),
                'description': f"Experience the ultimate gaming adventure in Sample Game {i+1}. This incredible game offers hours of entertainment with stunning graphics, engaging gameplay, and an immersive storyline.",
                'short_description': f"An amazing game that will captivate you from start to finish.",
                'header_image': f"https://cdn.akamai.steamstatic.com/steam/apps/{100000 + i}/header.jpg",
                'capsule_image': f"https://cdn.akamai.steamstatic.com/steam/apps/{100000 + i}/capsule_616x353.jpg",
                'background': f"https://cdn.akamai.steamstatic.com/steam/apps/{100000 + i}/page_bg_generated_v6b.jpg",
                'metacritic_score': random.randint(60, 95) if random.random() > 0.3 else None,
                'steam_score': random.randint(70, 95),
                'positive_reviews': random.randint(100, 50000),
                'negative_reviews': random.randint(10, 5000),
                'total_reviews': 0,  # Will be calculated
                'achievements': random.randint(0, 100),
                'dlc_count': random.randint(0, 10),
                'is_free': random.choice([True, False, False, False]),
                'is_early_access': random.choice([True, False, False, False, False]),
                'is_vr_supported': random.choice([True, False, False, False, False]),
                'is_multiplayer': random.choice([True, False]),
                'is_singleplayer': random.choice([True, False]),
                'is_coop': random.choice([True, False]),
                'is_pvp': random.choice([True, False]),
                'is_mmo': random.choice([True, False]),
                'is_strategy': random.choice([True, False]),
                'is_rpg': random.choice([True, False]),
                'is_action': random.choice([True, False]),
                'is_adventure': random.choice([True, False]),
                'is_simulation': random.choice([True, False]),
                'is_sports': random.choice([True, False]),
                'is_racing': random.choice([True, False]),
                'is_fighting': random.choice([True, False]),
                'is_puzzle': random.choice([True, False]),
                'is_horror': random.choice([True, False]),
                'is_indie': random.choice([True, False]),
                'is_casual': random.choice([True, False]),
                'is_educational': random.choice([True, False]),
                'is_utilities': random.choice([True, False]),
                'is_web': random.choice([True, False]),
                'is_software': random.choice([True, False]),
                'is_video': random.choice([True, False]),
                'is_music': random.choice([True, False]),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            # Calculate derived fields
            game['final_price'] = round(game['price'] * (1 - game['discount'] / 100), 2)
            game['total_reviews'] = game['positive_reviews'] + game['negative_reviews']
            
            games.append(game)
        
        logger.info(f"Created {len(games)} sample games")
        return games
    
    def create_sample_users(self, count: int = 10) -> List[Dict[str, Any]]:
        """Create sample user data"""
        logger.info(f"Creating {count} sample users...")
        
        users = []
        for i in range(count):
            user = {
                'id': str(uuid.uuid4()),
                'username': f"user{random.randint(1000, 9999)}",
                'email': f"user{random.randint(1000, 9999)}@example.com",
                'password_hash': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HSyK8m2',  # 'password'
                'first_name': random.choice(['John', 'Jane', 'Mike', 'Sarah', 'David', 'Lisa', 'Chris', 'Emma', 'Alex', 'Maria']),
                'last_name': random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']),
                'display_name': f"user{random.randint(1000, 9999)}#{random.randint(1000, 9999)}",
                'avatar_url': f"https://api.dicebear.com/7.x/avataaars/svg?seed=user{i+1}",
                'country': random.choice(['US', 'CA', 'GB', 'DE', 'FR', 'IT', 'ES', 'AU', 'JP', 'KR']),
                'language': random.choice(['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko']),
                'timezone': random.choice(['UTC-8', 'UTC-5', 'UTC+0', 'UTC+1', 'UTC+8', 'UTC+9']),
                'is_active': True,
                'is_verified': random.choice([True, True, False]),
                'is_premium': random.choice([True, False, False, False]),
                'created_at': (datetime.now() - timedelta(days=random.randint(0, 730))).isoformat(),
                'updated_at': datetime.now().isoformat(),
                'last_login': (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat() if random.random() > 0.1 else None,
                'preferences': {
                    'theme': random.choice(['dark', 'light', 'auto']),
                    'notifications': {
                        'email': random.choice([True, False]),
                        'push': random.choice([True, False]),
                        'in_game': True
                    },
                    'privacy': {
                        'profile_public': random.choice([True, False]),
                        'game_library_public': random.choice([True, False]),
                        'activity_public': random.choice([True, False])
                    }
                }
            }
            users.append(user)
        
        logger.info(f"Created {len(users)} sample users")
        return users
    
    def create_sample_reviews(self, games: List[Dict], users: List[Dict], count: int = 30) -> List[Dict[str, Any]]:
        """Create sample review data"""
        logger.info(f"Creating {count} sample reviews...")
        
        reviews = []
        for i in range(count):
            game = random.choice(games)
            user = random.choice(users)
            
            review_texts = [
                f"Amazing game! I've been playing {game['name']} for hours and I can't get enough of it.",
                f"Great graphics and gameplay. {game['name']} is definitely worth the money.",
                f"Not bad, but could be better. {game['name']} has some issues but overall it's playable.",
                f"Disappointed with {game['name']}. Expected more from this game.",
                f"One of the best games I've played this year. {game['name']} exceeded my expectations.",
                f"Good game but has some bugs. {game['name']} needs more polish.",
                f"Love this game! {game['name']} is perfect for relaxing after work.",
                f"Waste of money. {game['name']} is not what I expected at all.",
                f"Decent game with good potential. {game['name']} could be great with updates.",
                f"Absolutely fantastic! {game['name']} is a masterpiece."
            ]
            
            rating = random.randint(1, 5)
            is_positive = rating >= 3
            
            review = {
                'id': str(uuid.uuid4()),
                'user_id': user['id'],
                'game_id': game['app_id'],
                'rating': rating,
                'title': f"Review for {game['name']}",
                'content': random.choice(review_texts),
                'is_positive': is_positive,
                'is_helpful': random.choice([True, True, True, False]),
                'helpful_count': random.randint(0, 50),
                'not_helpful_count': random.randint(0, 10),
                'created_at': (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat(),
                'updated_at': (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
            }
            reviews.append(review)
        
        logger.info(f"Created {len(reviews)} sample reviews")
        return reviews
    
    def create_sample_achievements(self, games: List[Dict], count: int = 50) -> List[Dict[str, Any]]:
        """Create sample achievement data"""
        logger.info(f"Creating {count} sample achievements...")
        
        achievements = []
        achievement_names = [
            "First Steps", "Getting Started", "Explorer", "Collector", "Master",
            "Speed Runner", "Completionist", "Survivor", "Champion", "Legend",
            "Novice", "Expert", "Veteran", "Elite", "Pro", "Guru", "Sage", "Wizard"
        ]
        
        for i in range(count):
            game = random.choice(games)
            
            achievement = {
                'id': str(uuid.uuid4()),
                'game_id': game['app_id'],
                'name': random.choice(achievement_names),
                'description': f"Complete {random.choice(achievement_names).lower()} in {game['name']}",
                'icon_url': f"https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/{game['app_id']}/achievements/achievement_{i+1}.jpg",
                'points': random.randint(5, 50),
                'is_hidden': random.choice([True, False]),
                'is_rare': random.choice([True, False]),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            achievements.append(achievement)
        
        logger.info(f"Created {len(achievements)} sample achievements")
        return achievements
    
    def generate_data_summary(self, games: List[Dict], users: List[Dict], reviews: List[Dict], achievements: List[Dict]):
        """Generate a summary of the created data"""
        logger.info("\n" + "="*60)
        logger.info("📊 DATA GENERATION SUMMARY")
        logger.info("="*60)
        
        # Games summary
        free_games = sum(1 for game in games if game['is_free'])
        paid_games = len(games) - free_games
        avg_price = sum(game['price'] for game in games if not game['is_free']) / paid_games if paid_games > 0 else 0
        
        logger.info(f"\n🎮 GAMES ({len(games)} total):")
        logger.info(f"  Free games: {free_games}")
        logger.info(f"  Paid games: {paid_games}")
        logger.info(f"  Average price: ${avg_price:.2f}")
        logger.info(f"  Genres: {len(set(genre for game in games for genre in game['genres']))}")
        logger.info(f"  Tags: {len(set(tag for game in games for tag in game['tags']))}")
        logger.info(f"  Platforms: {len(set(platform for game in games for platform in game['platforms']))}")
        
        # Users summary
        verified_users = sum(1 for user in users if user['is_verified'])
        premium_users = sum(1 for user in users if user['is_premium'])
        
        logger.info(f"\n👤 USERS ({len(users)} total):")
        logger.info(f"  Verified: {verified_users}")
        logger.info(f"  Premium: {premium_users}")
        logger.info(f"  Countries: {len(set(user['country'] for user in users))}")
        logger.info(f"  Languages: {len(set(user['language'] for user in users))}")
        
        # Reviews summary
        positive_reviews = sum(1 for review in reviews if review['is_positive'])
        avg_rating = sum(review['rating'] for review in reviews) / len(reviews) if reviews else 0
        
        logger.info(f"\n⭐ REVIEWS ({len(reviews)} total):")
        logger.info(f"  Positive: {positive_reviews}")
        logger.info(f"  Negative: {len(reviews) - positive_reviews}")
        logger.info(f"  Average rating: {avg_rating:.2f}/5")
        
        # Achievements summary
        rare_achievements = sum(1 for achievement in achievements if achievement['is_rare'])
        hidden_achievements = sum(1 for achievement in achievements if achievement['is_hidden'])
        avg_points = sum(achievement['points'] for achievement in achievements) / len(achievements) if achievements else 0
        
        logger.info(f"\n🏆 ACHIEVEMENTS ({len(achievements)} total):")
        logger.info(f"  Rare: {rare_achievements}")
        logger.info(f"  Hidden: {hidden_achievements}")
        logger.info(f"  Average points: {avg_points:.1f}")
        
        logger.info("\n" + "="*60)
        logger.info("✅ DATA GENERATION COMPLETED SUCCESSFULLY!")
        logger.info("="*60)
    
    def save_data_to_files(self, games: List[Dict], users: List[Dict], reviews: List[Dict], achievements: List[Dict]):
        """Save generated data to JSON files"""
        logger.info("💾 Saving data to files...")
        
        # Save games data
        with open('/workspace/steam-clone/sample_data/games.json', 'w') as f:
            json.dump(games, f, indent=2)
        
        # Save users data
        with open('/workspace/steam-clone/sample_data/users.json', 'w') as f:
            json.dump(users, f, indent=2)
        
        # Save reviews data
        with open('/workspace/steam-clone/sample_data/reviews.json', 'w') as f:
            json.dump(reviews, f, indent=2)
        
        # Save achievements data
        with open('/workspace/steam-clone/sample_data/achievements.json', 'w') as f:
            json.dump(achievements, f, indent=2)
        
        logger.info("✅ Data saved to sample_data/ directory")
    
    def run_test(self):
        """Run the complete test"""
        logger.info("🚀 Starting Steam Clone Simple Test...")
        
        # Create sample data
        games = self.create_sample_games(20)
        users = self.create_sample_users(10)
        reviews = self.create_sample_reviews(games, users, 30)
        achievements = self.create_sample_achievements(games, 50)
        
        # Generate summary
        self.generate_data_summary(games, users, reviews, achievements)
        
        # Save data to files
        import os
        os.makedirs('/workspace/steam-clone/sample_data', exist_ok=True)
        self.save_data_to_files(games, users, reviews, achievements)
        
        logger.info("\n🎉 Test completed successfully!")
        logger.info("📁 Sample data saved to sample_data/ directory")
        logger.info("🔗 You can now use this data to test the services")

def main():
    """Main function"""
    tester = SimpleSteamCloneTester()
    tester.run_test()

if __name__ == "__main__":
    main()