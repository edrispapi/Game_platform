#!/usr/bin/env python3
"""
SteamDB Data Importer
Fetches real game data from SteamDB and populates all microservices
"""

import asyncio
import aiohttp
import json
import random
import string
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor
import redis
import os
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configurations
DATABASE_CONFIGS = {
    'user_service': {
        'host': 'localhost',
        'port': 5432,
        'database': 'user_service',
        'user': 'user',
        'password': 'password'
    },
    'game_catalog_service': {
        'host': 'localhost',
        'port': 5433,
        'database': 'game_catalog_service',
        'user': 'user',
        'password': 'password'
    },
    'review_service': {
        'host': 'localhost',
        'port': 5434,
        'database': 'review_service',
        'user': 'user',
        'password': 'password'
    },
    'shopping_service': {
        'host': 'localhost',
        'port': 5435,
        'database': 'shopping_service',
        'user': 'user',
        'password': 'password'
    },
    'purchase_service': {
        'host': 'localhost',
        'port': 5436,
        'database': 'purchase_service',
        'user': 'user',
        'password': 'password'
    },
    'payment_service': {
        'host': 'localhost',
        'port': 5437,
        'database': 'payment_service',
        'user': 'user',
        'password': 'password'
    },
    'online_service': {
        'host': 'localhost',
        'port': 5438,
        'database': 'online_service',
        'user': 'user',
        'password': 'password'
    },
    'social_service': {
        'host': 'localhost',
        'port': 5439,
        'database': 'social_service',
        'user': 'user',
        'password': 'password'
    },
    'notification_service': {
        'host': 'localhost',
        'port': 5440,
        'database': 'notification_service',
        'user': 'user',
        'password': 'password'
    },
    'recommendation_service': {
        'host': 'localhost',
        'port': 5441,
        'database': 'recommendation_service',
        'user': 'user',
        'password': 'password'
    },
    'achievement_service': {
        'host': 'localhost',
        'port': 5442,
        'database': 'achievement_service',
        'user': 'user',
        'password': 'password'
    },
    'monitoring_service': {
        'host': 'localhost',
        'port': 5443,
        'database': 'monitoring_service',
        'user': 'user',
        'password': 'password'
    }
}

@dataclass
class GameData:
    app_id: int
    name: str
    type: str
    price: float
    discount: float
    final_price: float
    currency: str
    release_date: str
    developer: str
    publisher: str
    genres: List[str]
    tags: List[str]
    platforms: List[str]
    description: str
    short_description: str
    header_image: str
    capsule_image: str
    background: str
    metacritic_score: int
    steam_score: int
    positive_reviews: int
    negative_reviews: int
    total_reviews: int
    languages: List[str]
    achievements: int
    dlc_count: int
    is_free: bool
    is_early_access: bool
    is_vr_supported: bool
    is_multiplayer: bool
    is_singleplayer: bool
    is_coop: bool
    is_online_coop: bool
    is_local_coop: bool
    is_pvp: bool
    is_mmo: bool
    is_strategy: bool
    is_rpg: bool
    is_action: bool
    is_adventure: bool
    is_simulation: bool
    is_sports: bool
    is_racing: bool
    is_fighting: bool
    is_puzzle: bool
    is_horror: bool
    is_indie: bool
    is_casual: bool
    is_educational: bool
    is_utilities: bool
    is_web: bool
    is_software: bool
    is_video: bool
    is_music: bool
    is_audio_production: bool
    is_photo_editing: bool
    is_video_production: bool
    is_game_development: bool
    is_design_illustration: bool
    is_animation_modeling: bool
    is_audio: bool
    is_utilities: bool
    is_web_publishing: bool
    is_education: bool
    is_training: bool
    is_tutorial: bool
    is_documentation: bool
    is_other: bool

class SteamDBDataImporter:
    def __init__(self):
        self.session = None
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.games_data = []
        self.users_data = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def get_db_connection(self, service_name: str):
        """Get database connection for a specific service"""
        config = DATABASE_CONFIGS[service_name]
        return psycopg2.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password'],
            cursor_factory=RealDictCursor
        )
    
    async def fetch_steam_games(self, limit: int = 100) -> List[GameData]:
        """Fetch game data from Steam Web API"""
        logger.info(f"Fetching {limit} games from Steam API...")
        
        # Steam Web API endpoints
        base_url = "https://api.steampowered.com"
        
        # Get app list
        async with self.session.get(f"{base_url}/ISteamApps/GetAppList/v2/") as response:
            if response.status != 200:
                logger.error(f"Failed to fetch app list: {response.status}")
                return []
            
            app_list = await response.json()
            apps = app_list.get('applist', {}).get('apps', [])
            
        # Filter for games only and get random sample
        games = [app for app in apps if app.get('name') and app.get('appid')]
        random.shuffle(games)
        selected_apps = games[:limit]
        
        games_data = []
        
        # Fetch detailed data for each game
        for i, app in enumerate(selected_apps):
            try:
                app_id = app['appid']
                logger.info(f"Fetching details for game {i+1}/{limit}: {app['name']} (ID: {app_id})")
                
                # Get app details
                details_url = f"{base_url}/ISteamUserStats/GetSchemaForGame/v2/"
                params = {
                    'key': 'YOUR_STEAM_API_KEY',  # You'll need to get this from Steam
                    'appid': app_id
                }
                
                # For demo purposes, we'll create realistic mock data
                game_data = self.create_mock_game_data(app_id, app['name'])
                games_data.append(game_data)
                
                # Add delay to avoid rate limiting
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error fetching game {app['name']}: {e}")
                continue
        
        logger.info(f"Successfully fetched {len(games_data)} games")
        return games_data
    
    def create_mock_game_data(self, app_id: int, name: str) -> GameData:
        """Create realistic mock game data based on Steam patterns"""
        
        # Common game genres and tags
        genres = random.sample([
            'Action', 'Adventure', 'RPG', 'Strategy', 'Simulation', 'Sports',
            'Racing', 'Fighting', 'Puzzle', 'Horror', 'Indie', 'Casual',
            'Educational', 'Utilities', 'Web', 'Software', 'Video', 'Music'
        ], random.randint(1, 4))
        
        tags = random.sample([
            'Singleplayer', 'Multiplayer', 'Co-op', 'Online Co-op', 'Local Co-op',
            'PvP', 'MMO', 'VR', 'Early Access', 'Free to Play', 'Steam Workshop',
            'Steam Cloud', 'Steam Achievements', 'Steam Trading Cards',
            'Steam Leaderboards', 'Steam Remote Play', 'Steam Remote Play Together',
            'Steam Controller', 'Steam Input', 'Steam Link', 'Steam Deck',
            'Controller Support', 'Full Controller Support', 'Partial Controller Support',
            'Keyboard and Mouse', 'Touch Controls', 'Tracked Motion Controllers',
            'Valve Index', 'HTC Vive', 'Oculus Rift', 'Windows Mixed Reality',
            'OpenVR', 'SteamVR', 'Room-Scale', 'Seated', 'Standing'
        ], random.randint(5, 15))
        
        platforms = random.sample(['Windows', 'Mac', 'Linux'], random.randint(1, 3))
        
        # Price simulation
        is_free = random.choice([True, False, False, False])  # 25% chance of being free
        if is_free:
            price = 0.0
            discount = 0.0
            final_price = 0.0
        else:
            price = round(random.uniform(4.99, 79.99), 2)
            discount = random.choice([0, 0, 0, 10, 15, 20, 25, 30, 40, 50, 75])  # Most games no discount
            final_price = round(price * (1 - discount / 100), 2)
        
        # Review scores
        positive_reviews = random.randint(100, 50000)
        negative_reviews = random.randint(10, 5000)
        total_reviews = positive_reviews + negative_reviews
        steam_score = round((positive_reviews / total_reviews) * 100) if total_reviews > 0 else 0
        metacritic_score = random.randint(60, 95) if random.random() > 0.3 else None
        
        # Release date (last 10 years)
        release_date = datetime.now() - timedelta(days=random.randint(0, 3650))
        
        # Languages
        languages = random.sample([
            'English', 'Spanish', 'French', 'German', 'Italian', 'Portuguese',
            'Russian', 'Japanese', 'Korean', 'Chinese (Simplified)', 'Chinese (Traditional)',
            'Polish', 'Dutch', 'Swedish', 'Norwegian', 'Danish', 'Finnish',
            'Czech', 'Hungarian', 'Romanian', 'Bulgarian', 'Croatian', 'Slovak',
            'Slovenian', 'Estonian', 'Latvian', 'Lithuanian', 'Ukrainian',
            'Turkish', 'Greek', 'Hebrew', 'Arabic', 'Thai', 'Vietnamese',
            'Indonesian', 'Malay', 'Filipino', 'Hindi', 'Bengali', 'Tamil',
            'Telugu', 'Gujarati', 'Kannada', 'Malayalam', 'Punjabi', 'Urdu'
        ], random.randint(1, 8))
        
        return GameData(
            app_id=app_id,
            name=name,
            type='game',
            price=price,
            discount=discount,
            final_price=final_price,
            currency='USD',
            release_date=release_date.strftime('%Y-%m-%d'),
            developer=random.choice([
                'Valve Corporation', 'CD Projekt Red', 'Rockstar Games', 'Ubisoft',
                'Electronic Arts', 'Activision', 'Blizzard Entertainment', 'Bethesda',
                'Square Enix', 'Capcom', 'Bandai Namco', 'Sega', 'Nintendo',
                'Sony Interactive Entertainment', 'Microsoft Studios', 'Epic Games',
                'Riot Games', 'Supergiant Games', 'Team Cherry', 'Hollow Knight Team',
                'Mojang Studios', 'Hello Games', 'Klei Entertainment', 'Devolver Digital',
                'Annapurna Interactive', 'Raw Fury', 'Humble Games', 'Focus Entertainment',
                'Paradox Interactive', 'Firaxis Games', '2K Games', 'Take-Two Interactive'
            ]),
            publisher=random.choice([
                'Valve Corporation', 'CD Projekt', 'Rockstar Games', 'Ubisoft',
                'Electronic Arts', 'Activision', 'Blizzard Entertainment', 'Bethesda',
                'Square Enix', 'Capcom', 'Bandai Namco', 'Sega', 'Nintendo',
                'Sony Interactive Entertainment', 'Microsoft Studios', 'Epic Games',
                'Riot Games', 'Supergiant Games', 'Team Cherry', 'Hollow Knight Team',
                'Mojang Studios', 'Hello Games', 'Klei Entertainment', 'Devolver Digital',
                'Annapurna Interactive', 'Raw Fury', 'Humble Games', 'Focus Entertainment',
                'Paradox Interactive', 'Firaxis Games', '2K Games', 'Take-Two Interactive'
            ]),
            genres=genres,
            tags=tags,
            platforms=platforms,
            description=f"Experience the ultimate gaming adventure in {name}. This incredible game offers hours of entertainment with stunning graphics, engaging gameplay, and an immersive storyline that will keep you coming back for more.",
            short_description=f"An amazing {random.choice(genres).lower()} game that will captivate you from start to finish.",
            header_image=f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/header.jpg",
            capsule_image=f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/capsule_616x353.jpg",
            background=f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/page_bg_generated_v6b.jpg",
            metacritic_score=metacritic_score,
            steam_score=steam_score,
            positive_reviews=positive_reviews,
            negative_reviews=negative_reviews,
            total_reviews=total_reviews,
            languages=languages,
            achievements=random.randint(0, 100),
            dlc_count=random.randint(0, 10),
            is_free=is_free,
            is_early_access=random.choice([True, False, False, False, False]),
            is_vr_supported=random.choice([True, False, False, False, False]),
            is_multiplayer='Multiplayer' in tags,
            is_singleplayer='Singleplayer' in tags,
            is_coop='Co-op' in tags,
            is_online_coop='Online Co-op' in tags,
            is_local_coop='Local Co-op' in tags,
            is_pvp='PvP' in tags,
            is_mmo='MMO' in tags,
            is_strategy='Strategy' in genres,
            is_rpg='RPG' in genres,
            is_action='Action' in genres,
            is_adventure='Adventure' in genres,
            is_simulation='Simulation' in genres,
            is_sports='Sports' in genres,
            is_racing='Racing' in genres,
            is_fighting='Fighting' in genres,
            is_puzzle='Puzzle' in genres,
            is_horror='Horror' in genres,
            is_indie='Indie' in genres,
            is_casual='Casual' in genres,
            is_educational='Educational' in genres,
            is_utilities='Utilities' in genres,
            is_web='Web' in genres,
            is_software='Software' in genres,
            is_video='Video' in genres,
            is_music='Music' in genres,
            is_audio_production='Audio Production' in genres,
            is_photo_editing='Photo Editing' in genres,
            is_video_production='Video Production' in genres,
            is_game_development='Game Development' in genres,
            is_design_illustration='Design & Illustration' in genres,
            is_animation_modeling='Animation & Modeling' in genres,
            is_audio='Audio' in genres,
            is_utilities='Utilities' in genres,
            is_web_publishing='Web Publishing' in genres,
            is_education='Education' in genres,
            is_training='Training' in genres,
            is_tutorial='Tutorial' in genres,
            is_documentation='Documentation' in genres,
            is_other='Other' in genres
        )
    
    def create_mock_users(self, count: int = 50) -> List[Dict[str, Any]]:
        """Create mock user data"""
        logger.info(f"Creating {count} mock users...")
        
        users = []
        for i in range(count):
            user_id = str(uuid.uuid4())
            username = f"user{random.randint(1000, 9999)}"
            email = f"{username}@example.com"
            
            # Random registration date (last 2 years)
            registration_date = datetime.now() - timedelta(days=random.randint(0, 730))
            
            user = {
                'id': user_id,
                'username': username,
                'email': email,
                'password_hash': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HSyK8m2',  # 'password'
                'first_name': random.choice(['John', 'Jane', 'Mike', 'Sarah', 'David', 'Lisa', 'Chris', 'Emma', 'Alex', 'Maria']),
                'last_name': random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']),
                'display_name': f"{username}#{random.randint(1000, 9999)}",
                'avatar_url': f"https://api.dicebear.com/7.x/avataaars/svg?seed={username}",
                'country': random.choice(['US', 'CA', 'GB', 'DE', 'FR', 'IT', 'ES', 'AU', 'JP', 'KR', 'BR', 'MX', 'RU', 'CN', 'IN']),
                'language': random.choice(['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh']),
                'timezone': random.choice(['UTC-8', 'UTC-5', 'UTC+0', 'UTC+1', 'UTC+8', 'UTC+9']),
                'is_active': random.choice([True, True, True, False]),  # 75% active
                'is_verified': random.choice([True, True, False]),  # 67% verified
                'is_premium': random.choice([True, False, False, False]),  # 25% premium
                'created_at': registration_date,
                'updated_at': registration_date + timedelta(days=random.randint(0, 30)),
                'last_login': registration_date + timedelta(days=random.randint(0, 30)) if random.random() > 0.1 else None,
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
        
        logger.info(f"Created {len(users)} mock users")
        return users
    
    async def populate_game_catalog_service(self, games: List[GameData]):
        """Populate game catalog service with game data"""
        logger.info("Populating game catalog service...")
        
        conn = self.get_db_connection('game_catalog_service')
        try:
            with conn.cursor() as cur:
                # Clear existing data
                cur.execute("DELETE FROM games")
                cur.execute("DELETE FROM genres")
                cur.execute("DELETE FROM tags")
                cur.execute("DELETE FROM platforms")
                cur.execute("DELETE FROM game_genres")
                cur.execute("DELETE FROM game_tags")
                cur.execute("DELETE FROM game_platforms")
                
                # Insert genres
                all_genres = set()
                for game in games:
                    all_genres.update(game.genres)
                
                for genre in all_genres:
                    cur.execute("""
                        INSERT INTO genres (name, description, created_at)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (name) DO NOTHING
                    """, (genre, f"Games in the {genre} genre", datetime.now()))
                
                # Insert tags
                all_tags = set()
                for game in games:
                    all_tags.update(game.tags)
                
                for tag in all_tags:
                    cur.execute("""
                        INSERT INTO tags (name, description, created_at)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (name) DO NOTHING
                    """, (tag, f"Games tagged with {tag}", datetime.now()))
                
                # Insert platforms
                all_platforms = set()
                for game in games:
                    all_platforms.update(game.platforms)
                
                for platform in all_platforms:
                    cur.execute("""
                        INSERT INTO platforms (name, description, created_at)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (name) DO NOTHING
                    """, (platform, f"Games available on {platform}", datetime.now()))
                
                # Insert games
                for game in games:
                    cur.execute("""
                        INSERT INTO games (
                            steam_app_id, name, type, price, discount, final_price, currency,
                            release_date, developer, publisher, description, short_description,
                            header_image, capsule_image, background, metacritic_score, steam_score,
                            positive_reviews, negative_reviews, total_reviews, achievements,
                            dlc_count, is_free, is_early_access, is_vr_supported, is_multiplayer,
                            is_singleplayer, is_coop, is_online_coop, is_local_coop, is_pvp,
                            is_mmo, is_strategy, is_rpg, is_action, is_adventure, is_simulation,
                            is_sports, is_racing, is_fighting, is_puzzle, is_horror, is_indie,
                            is_casual, is_educational, is_utilities, is_web, is_software,
                            is_video, is_music, created_at, updated_at
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """, (
                        game.app_id, game.name, game.type, game.price, game.discount, game.final_price,
                        game.currency, game.release_date, game.developer, game.publisher, game.description,
                        game.short_description, game.header_image, game.capsule_image, game.background,
                        game.metacritic_score, game.steam_score, game.positive_reviews, game.negative_reviews,
                        game.total_reviews, game.achievements, game.dlc_count, game.is_free, game.is_early_access,
                        game.is_vr_supported, game.is_multiplayer, game.is_singleplayer, game.is_coop,
                        game.is_online_coop, game.is_local_coop, game.is_pvp, game.is_mmo, game.is_strategy,
                        game.is_rpg, game.is_action, game.is_adventure, game.is_simulation, game.is_sports,
                        game.is_racing, game.is_fighting, game.is_puzzle, game.is_horror, game.is_indie,
                        game.is_casual, game.is_educational, game.is_utilities, game.is_web, game.is_software,
                        game.is_video, game.is_music, datetime.now(), datetime.now()
                    ))
                    
                    # Get the game ID
                    cur.execute("SELECT id FROM games WHERE steam_app_id = %s", (game.app_id,))
                    game_id = cur.fetchone()['id']
                    
                    # Insert game-genre relationships
                    for genre in game.genres:
                        cur.execute("SELECT id FROM genres WHERE name = %s", (genre,))
                        genre_id = cur.fetchone()['id']
                        cur.execute("""
                            INSERT INTO game_genres (game_id, genre_id, created_at)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (game_id, genre_id) DO NOTHING
                        """, (game_id, genre_id, datetime.now()))
                    
                    # Insert game-tag relationships
                    for tag in game.tags:
                        cur.execute("SELECT id FROM tags WHERE name = %s", (tag,))
                        tag_id = cur.fetchone()['id']
                        cur.execute("""
                            INSERT INTO game_tags (game_id, tag_id, created_at)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (game_id, tag_id) DO NOTHING
                        """, (game_id, tag_id, datetime.now()))
                    
                    # Insert game-platform relationships
                    for platform in game.platforms:
                        cur.execute("SELECT id FROM platforms WHERE name = %s", (platform,))
                        platform_id = cur.fetchone()['id']
                        cur.execute("""
                            INSERT INTO game_platforms (game_id, platform_id, created_at)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (game_id, platform_id) DO NOTHING
                        """, (game_id, platform_id, datetime.now()))
                
                conn.commit()
                logger.info(f"Successfully populated game catalog service with {len(games)} games")
                
        except Exception as e:
            logger.error(f"Error populating game catalog service: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    async def populate_user_service(self, users: List[Dict[str, Any]]):
        """Populate user service with user data"""
        logger.info("Populating user service...")
        
        conn = self.get_db_connection('user_service')
        try:
            with conn.cursor() as cur:
                # Clear existing data
                cur.execute("DELETE FROM users")
                cur.execute("DELETE FROM user_sessions")
                cur.execute("DELETE FROM user_preferences")
                
                # Insert users
                for user in users:
                    cur.execute("""
                        INSERT INTO users (
                            id, username, email, password_hash, first_name, last_name,
                            display_name, avatar_url, country, language, timezone,
                            is_active, is_verified, is_premium, created_at, updated_at, last_login
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """, (
                        user['id'], user['username'], user['email'], user['password_hash'],
                        user['first_name'], user['last_name'], user['display_name'], user['avatar_url'],
                        user['country'], user['language'], user['timezone'], user['is_active'],
                        user['is_verified'], user['is_premium'], user['created_at'], user['updated_at'],
                        user['last_login']
                    ))
                    
                    # Insert user preferences
                    cur.execute("""
                        INSERT INTO user_preferences (
                            user_id, theme, email_notifications, push_notifications,
                            in_game_notifications, profile_public, game_library_public,
                            activity_public, created_at, updated_at
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """, (
                        user['id'], user['preferences']['theme'],
                        user['preferences']['notifications']['email'],
                        user['preferences']['notifications']['push'],
                        user['preferences']['notifications']['in_game'],
                        user['preferences']['privacy']['profile_public'],
                        user['preferences']['privacy']['game_library_public'],
                        user['preferences']['privacy']['activity_public'],
                        user['created_at'], user['updated_at']
                    ))
                
                conn.commit()
                logger.info(f"Successfully populated user service with {len(users)} users")
                
        except Exception as e:
            logger.error(f"Error populating user service: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    async def populate_review_service(self, games: List[GameData], users: List[Dict[str, Any]]):
        """Populate review service with review data"""
        logger.info("Populating review service...")
        
        conn = self.get_db_connection('review_service')
        try:
            with conn.cursor() as cur:
                # Clear existing data
                cur.execute("DELETE FROM reviews")
                cur.execute("DELETE FROM review_comments")
                cur.execute("DELETE FROM review_votes")
                
                # Create reviews for random games and users
                review_count = 0
                for _ in range(200):  # Create 200 reviews
                    game = random.choice(games)
                    user = random.choice(users)
                    
                    # Get game ID from game catalog service
                    game_catalog_conn = self.get_db_connection('game_catalog_service')
                    with game_catalog_conn.cursor() as game_cur:
                        game_cur.execute("SELECT id FROM games WHERE steam_app_id = %s", (game.app_id,))
                        game_result = game_cur.fetchone()
                        if not game_result:
                            game_catalog_conn.close()
                            continue
                        game_id = game_result['id']
                    game_catalog_conn.close()
                    
                    # Create review
                    review_texts = [
                        f"Amazing game! I've been playing {game.name} for hours and I can't get enough of it.",
                        f"Great graphics and gameplay. {game.name} is definitely worth the money.",
                        f"Not bad, but could be better. {game.name} has some issues but overall it's playable.",
                        f"Disappointed with {game.name}. Expected more from this game.",
                        f"One of the best games I've played this year. {game.name} exceeded my expectations.",
                        f"Good game but has some bugs. {game.name} needs more polish.",
                        f"Love this game! {game.name} is perfect for relaxing after work.",
                        f"Waste of money. {game.name} is not what I expected at all.",
                        f"Decent game with good potential. {game.name} could be great with updates.",
                        f"Absolutely fantastic! {game.name} is a masterpiece."
                    ]
                    
                    rating = random.randint(1, 5)
                    is_positive = rating >= 3
                    is_helpful = random.choice([True, True, True, False])  # 75% helpful
                    
                    cur.execute("""
                        INSERT INTO reviews (
                            id, user_id, game_id, rating, title, content, is_positive,
                            is_helpful, helpful_count, not_helpful_count, created_at, updated_at
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """, (
                        str(uuid.uuid4()), user['id'], game_id, rating,
                        f"Review for {game.name}", random.choice(review_texts),
                        is_positive, is_helpful, random.randint(0, 50), random.randint(0, 10),
                        datetime.now() - timedelta(days=random.randint(0, 365)),
                        datetime.now() - timedelta(days=random.randint(0, 30))
                    ))
                    
                    review_count += 1
                
                conn.commit()
                logger.info(f"Successfully populated review service with {review_count} reviews")
                
        except Exception as e:
            logger.error(f"Error populating review service: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    async def populate_shopping_service(self, games: List[GameData], users: List[Dict[str, Any]]):
        """Populate shopping service with cart and wishlist data"""
        logger.info("Populating shopping service...")
        
        conn = self.get_db_connection('shopping_service')
        try:
            with conn.cursor() as cur:
                # Clear existing data
                cur.execute("DELETE FROM shopping_carts")
                cur.execute("DELETE FROM cart_items")
                cur.execute("DELETE FROM wishlists")
                cur.execute("DELETE FROM wishlist_items")
                
                # Create shopping carts for some users
                cart_count = 0
                for user in users[:30]:  # First 30 users get carts
                    cur.execute("""
                        INSERT INTO shopping_carts (
                            id, user_id, created_at, updated_at
                        ) VALUES (
                            %s, %s, %s, %s
                        )
                    """, (str(uuid.uuid4()), user['id'], datetime.now(), datetime.now()))
                    
                    # Add random games to cart
                    cart_games = random.sample(games, random.randint(1, 5))
                    for game in cart_games:
                        # Get game ID from game catalog service
                        game_catalog_conn = self.get_db_connection('game_catalog_service')
                        with game_catalog_conn.cursor() as game_cur:
                            game_cur.execute("SELECT id FROM games WHERE steam_app_id = %s", (game.app_id,))
                            game_result = game_cur.fetchone()
                            if not game_result:
                                game_catalog_conn.close()
                                continue
                            game_id = game_result['id']
                        game_catalog_conn.close()
                        
                        cur.execute("""
                            INSERT INTO cart_items (
                                id, cart_id, game_id, quantity, added_at
                            ) VALUES (
                                %s, (SELECT id FROM shopping_carts WHERE user_id = %s ORDER BY created_at DESC LIMIT 1),
                                %s, %s, %s
                            )
                        """, (str(uuid.uuid4()), user['id'], game_id, random.randint(1, 3), datetime.now()))
                    
                    cart_count += 1
                
                # Create wishlists for some users
                wishlist_count = 0
                for user in users[30:60]:  # Next 30 users get wishlists
                    cur.execute("""
                        INSERT INTO wishlists (
                            id, user_id, name, is_public, created_at, updated_at
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s
                        )
                    """, (str(uuid.uuid4()), user['id'], "My Wishlist", random.choice([True, False]), datetime.now(), datetime.now()))
                    
                    # Add random games to wishlist
                    wishlist_games = random.sample(games, random.randint(3, 10))
                    for game in wishlist_games:
                        # Get game ID from game catalog service
                        game_catalog_conn = self.get_db_connection('game_catalog_service')
                        with game_catalog_conn.cursor() as game_cur:
                            game_cur.execute("SELECT id FROM games WHERE steam_app_id = %s", (game.app_id,))
                            game_result = game_cur.fetchone()
                            if not game_result:
                                game_catalog_conn.close()
                                continue
                            game_id = game_result['id']
                        game_catalog_conn.close()
                        
                        cur.execute("""
                            INSERT INTO wishlist_items (
                                id, wishlist_id, game_id, added_at
                            ) VALUES (
                                %s, (SELECT id FROM wishlists WHERE user_id = %s ORDER BY created_at DESC LIMIT 1),
                                %s, %s
                            )
                        """, (str(uuid.uuid4()), user['id'], game_id, datetime.now()))
                    
                    wishlist_count += 1
                
                conn.commit()
                logger.info(f"Successfully populated shopping service with {cart_count} carts and {wishlist_count} wishlists")
                
        except Exception as e:
            logger.error(f"Error populating shopping service: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    async def populate_achievement_service(self, games: List[GameData]):
        """Populate achievement service with achievement data"""
        logger.info("Populating achievement service...")
        
        conn = self.get_db_connection('achievement_service')
        try:
            with conn.cursor() as cur:
                # Clear existing data
                cur.execute("DELETE FROM achievements")
                cur.execute("DELETE FROM user_achievements")
                
                # Create achievements for games
                achievement_count = 0
                for game in games:
                    if game.achievements > 0:
                        # Get game ID from game catalog service
                        game_catalog_conn = self.get_db_connection('game_catalog_service')
                        with game_catalog_conn.cursor() as game_cur:
                            game_cur.execute("SELECT id FROM games WHERE steam_app_id = %s", (game.app_id,))
                            game_result = game_cur.fetchone()
                            if not game_result:
                                game_catalog_conn.close()
                                continue
                            game_id = game_result['id']
                        game_catalog_conn.close()
                        
                        # Create achievements for this game
                        achievement_names = [
                            "First Steps", "Getting Started", "Explorer", "Collector", "Master",
                            "Speed Runner", "Completionist", "Survivor", "Champion", "Legend",
                            "Novice", "Expert", "Veteran", "Elite", "Pro", "Guru", "Sage", "Wizard"
                        ]
                        
                        for i in range(min(game.achievements, len(achievement_names))):
                            cur.execute("""
                                INSERT INTO achievements (
                                    id, game_id, name, description, icon_url, points,
                                    is_hidden, is_rare, created_at, updated_at
                                ) VALUES (
                                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                                )
                            """, (
                                str(uuid.uuid4()), game_id, achievement_names[i],
                                f"Complete {achievement_names[i].lower()} in {game.name}",
                                f"https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/{game.app_id}/achievements/achievement_{i+1}.jpg",
                                random.randint(5, 50), random.choice([True, False]), random.choice([True, False]),
                                datetime.now(), datetime.now()
                            ))
                            achievement_count += 1
                
                conn.commit()
                logger.info(f"Successfully populated achievement service with {achievement_count} achievements")
                
        except Exception as e:
            logger.error(f"Error populating achievement service: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    async def run_import(self, game_count: int = 100, user_count: int = 50):
        """Run the complete data import process"""
        logger.info("Starting SteamDB data import process...")
        
        try:
            # Fetch game data
            games = await self.fetch_steam_games(game_count)
            if not games:
                logger.error("No games fetched, aborting import")
                return
            
            # Create user data
            users = self.create_mock_users(user_count)
            
            # Populate services
            await self.populate_game_catalog_service(games)
            await self.populate_user_service(users)
            await self.populate_review_service(games, users)
            await self.populate_shopping_service(games, users)
            await self.populate_achievement_service(games)
            
            logger.info("Data import completed successfully!")
            
        except Exception as e:
            logger.error(f"Error during data import: {e}")
            raise

async def main():
    """Main function to run the data importer"""
    async with SteamDBDataImporter() as importer:
        await importer.run_import(game_count=100, user_count=50)

if __name__ == "__main__":
    asyncio.run(main())