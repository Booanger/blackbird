"""
Platform URL Manager for Blackbird OSINT tool.

This module provides a class for managing platform URLs and generating
profile links for various social media and online platforms.
"""

import os
import json
from typing import Dict, Optional, List
import logging
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
)

import config


class PlatformURLManager:
    """
    Manages platform URLs and provides methods for generating profile links.

    This class loads platform URL templates from a configuration file and
    provides methods to generate profile links for various platforms.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the PlatformURLManager.

        Args:
            config_path: Path to the platform URLs configuration file.
                         If None, uses the default path.
        """
        self.platforms = {}
        self.categories = {}

        # Default config path is in the data directory
        if config_path is None:
            config_path = config.PLATFORM_URLS_PATH

        self.load_platforms(config_path)

    def load_platforms(self, config_path: str) -> None:
        """
        Load platform URLs from a configuration file.

        Args:
            config_path: Path to the configuration file.
        """
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.platforms = data.get('platforms', {})
                    self.categories = data.get('categories', {})
            else:
                # If the file doesn't exist, use the default hardcoded map
                self._load_default_platforms()
                # Save the default map to the config file for future use
                self.save_platforms(config_path)
        except Exception as e:
            logging.error(f"Error loading platform URLs: {str(e)}")
            self._load_default_platforms()

    def _load_default_platforms(self) -> None:
        """Load the default hardcoded platform URLs."""
        self.platforms = {
            "Bandcamp": "https://bandcamp.com/{}",
            "Chess.com": "https://www.chess.com/member/{}",
            "Codeforces": "https://codeforces.com/profile/{}",
            "DeviantArt": "https://www.deviantart.com/{}",
            "Disqus": "https://disqus.com/by/{}/",
            "DockerHub": "https://hub.docker.com/u/{}",
            "Eyeem": "https://www.eyeem.com/u/{}",
            "GitLab": "https://gitlab.com/{}",
            "Hacker News": "https://news.ycombinator.com/user?id={}",
            "Hackerearth": "https://www.hackerearth.com/@{}",
            "Imgur": "https://imgur.com/user/{}",
            "Instructables": "https://www.instructables.com/member/{}",
            "Keybase": "https://keybase.io/{}",
            "Livejournal": "https://{}.livejournal.com",
            "Patreon": "https://www.patreon.com/{}",
            "Reddit": "https://www.reddit.com/user/{}",
            "SoundCloud": "https://soundcloud.com/{}",
            "Spotify": "https://open.spotify.com/user/{}",
            "Steam": "https://steamcommunity.com/user/{}",
            "Telegram": "https://t.me/{}",
            "TikTok": "https://www.tiktok.com/@{}",
            "Tumblr": "https://{}.tumblr.com",
            "Trello": "https://trello.com/u/{}",
            "Twitch": "https://www.twitch.tv/{}",
            "Twitter": "https://twitter.com/{}",
            "Vimeo": "https://vimeo.com/{}",
            "YouTube": "https://www.youtube.com/{}",
            "About.me": "https://about.me/{}",
            "Academia.edu": "https://independent.academia.edu/{}",
            "AngelList": "https://angel.co/{}",
            "Behance": "https://www.behance.net/{}",
            "Bitbucket": "https://bitbucket.org/{}",
            "Blogger": "https://{}.blogspot.com",
            "Codepen": "https://codepen.io/{}",
            "Dribbble": "https://dribbble.com/{}",
            "Etsy": "https://www.etsy.com/shop/{}",
            "Facebook": "https://www.facebook.com/{}",
            "Flickr": "https://www.flickr.com/people/{}",
            "Freelancer": "https://www.freelancer.com/u/{}",
            "Goodreads": "https://www.goodreads.com/user/show/{}",
            "Instagram": "https://www.instagram.com/{}",
            "Last.fm": "https://www.last.fm/user/{}",
            "LinkedIn": "https://www.linkedin.com/in/{}",
            "Medium": "https://medium.com/@{}",
            "Pinterest": "https://www.pinterest.com/{}",
            "Product Hunt": "https://www.producthunt.com/@{}",
            "Quora": "https://www.quora.com/profile/{}",
            "ResearchGate": "https://www.researchgate.net/profile/{}",
            "Snapchat": "https://www.snapchat.com/add/{}",
            "TripAdvisor": "https://www.tripadvisor.com/members/{}",
            "VK": "https://vk.com/{}",
            "Wikipedia": "https://en.wikipedia.org/wiki/User:{}",
            "Duolingo": "https://www.duolingo.com/profile/{}",
            "smule": "https://www.smule.com/{}",
            "TryHackMe": "https://tryhackme.com/p/{}",
            "Hackerrank": "https://www.hackerrank.com/{}",
            "lichess.org": "https://lichess.org/@/{}",
        }

        # Default categories
        self.categories = {
            "social": [
                "Facebook", "Twitter", "Instagram", "LinkedIn", "Pinterest",
                "Snapchat", "TikTok", "Reddit", "Tumblr", "VK"
            ],
            "professional": [
                "LinkedIn", "GitHub", "GitLab", "Bitbucket", "DockerHub",
                "Behance", "Dribbble", "Freelancer", "AngelList", "Product Hunt"
            ],
            "creative": [
                "DeviantArt", "Behance", "Dribbble", "SoundCloud", "Bandcamp",
                "YouTube", "Vimeo", "Flickr", "Etsy", "Medium"
            ],
            "gaming": [
                "Steam", "Twitch", "Chess.com", "lichess.org", "TryHackMe"
            ],
            "tech": [
                "GitHub", "GitLab", "Bitbucket", "DockerHub", "Codeforces",
                "Hackerrank", "Hackerearth", "Hacker News", "Codepen"
            ],
            "education": [
                "Academia.edu", "ResearchGate", "Duolingo", "Quora"
            ]
        }

    def save_platforms(self, config_path: str) -> bool:
        """
        Save platform URLs to a configuration file.

        Args:
            config_path: Path to save the configuration file.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(config_path), exist_ok=True)

            data = {
                'platforms': self.platforms,
                'categories': self.categories
            }

            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            logging.error(f"Error saving platform URLs: {str(e)}")
            return False

    def get_profile_url(self, platform_name: str, username: str, fallback_url: Optional[str] = None) -> str:
        """
        Generate a profile URL for the given platform and username.

        Args:
            platform_name: Name of the platform.
            username: Username to insert into the URL.
            fallback_url: URL to use if the platform is not found in the map.

        Returns:
            str: The generated profile URL.
        """
        url_template = self.platforms.get(platform_name)

        if url_template:
            return url_template.format(username)
        elif fallback_url:
            return fallback_url
        else:
            return f"Unknown platform: {platform_name}"

    def add_platform(self, platform_name: str, url_template: str, categories: Optional[List[str]] = None) -> None:
        """
        Add a new platform to the manager.

        Args:
            platform_name: Name of the platform.
            url_template: URL template with {} placeholder for username.
            categories: List of categories to add this platform to.
        """
        self.platforms[platform_name] = url_template

        if categories:
            for category in categories:
                if category in self.categories:
                    if platform_name not in self.categories[category]:
                        self.categories[category].append(platform_name)
                else:
                    self.categories[category] = [platform_name]

    def remove_platform(self, platform_name: str) -> bool:
        """
        Remove a platform from the manager.

        Args:
            platform_name: Name of the platform to remove.

        Returns:
            bool: True if the platform was removed, False if it wasn't found.
        """
        if platform_name in self.platforms:
            del self.platforms[platform_name]

            # Also remove from categories
            for category in self.categories:
                if platform_name in self.categories[category]:
                    self.categories[category].remove(platform_name)

            return True
        return False

    def get_platforms_by_category(self, category: str) -> List[str]:
        """
        Get a list of platforms in a specific category.

        Args:
            category: Category name.

        Returns:
            List[str]: List of platform names in the category.
        """
        return self.categories.get(category, [])

    def get_all_platforms(self) -> Dict[str, str]:
        """
        Get all platforms and their URL templates.

        Returns:
            Dict[str, str]: Dictionary of platform names and URL templates.
        """
        return self.platforms

    def get_all_categories(self) -> Dict[str, List[str]]:
        """
        Get all categories and their platforms.

        Returns:
            Dict[str, List[str]]: Dictionary of category names and platform lists.
        """
        return self.categories
