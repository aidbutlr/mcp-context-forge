#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# Author: Pipeline Team
# Description: 🛠️ MCP Gateway CI/CD Smoke Test

Simplified smoke test for CI/CD pipeline validation.
Tests basic functionality of the MCP Gateway after deployment.

Usage:
  python3 .sps/SmokeTest.py
  python3 .sps/SmokeTest.py --url https://gateway.example.com
  python3 .sps/SmokeTest.py --skip-auth
  python3 .sps/SmokeTest.py --clone-repo
"""

# Future
from __future__ import annotations

# Standard
import argparse
import json
import logging
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Dict, Optional
from urllib.parse import urljoin, urlparse

try:
    # Third-Party
    import requests
except ImportError:
    print("❌ requests library not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    # Third-Party
    import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def clone_github_project(
    gh_user: Optional[str] = None,
    gh_token: Optional[str] = None,
    gh_project: Optional[str] = None,
    target_dir: Optional[str] = None
) -> bool:
    """
    Clone a GitHub project using credentials from environment variables.
    
    Args:
        gh_user: GitHub username (defaults to GH_USER env var)
        gh_token: GitHub personal access token (defaults to GH_TOKEN env var)
        gh_project: GitHub project URL (defaults to GH_PROJECT env var)
        target_dir: Target directory for cloning (optional)
    
    Returns:
        bool: True if clone was successful, False otherwise
    
    Environment Variables:
        GH_USER: The GitHub username
        GH_TOKEN: The GitHub personal access token
        GH_PROJECT: The URL of the GitHub project
    
    Example:
        >>> clone_github_project()
        >>> # Or with explicit parameters:
        >>> clone_github_project(
        ...     gh_user="myuser",
        ...     gh_token="ghp_xxxxx",
        ...     gh_project="https://github.com/owner/repo.git"
        ... )
    """
    # Get credentials from parameters or environment variables
    gh_user = gh_user or os.getenv("GH_USER")
    gh_token = gh_token or os.getenv("GH_TOKEN")
    gh_project = gh_project or os.getenv("GH_PROJECT")
    
    # Validate required parameters
    if not gh_user:
        logger.error("❌ GH_USER not provided (set environment variable or pass as parameter)")
        return False
    
    if not gh_token:
        logger.error("❌ GH_TOKEN not provided (set environment variable or pass as parameter)")
        return False
    
    if not gh_project:
        logger.error("❌ GH_PROJECT not provided (set environment variable or pass as parameter)")
        return False
    
    try:
        # Parse the project URL to extract repository information
        parsed_url = urlparse(gh_project)
        
        # Handle different URL formats
        if parsed_url.scheme in ['http', 'https']:
            # Extract path and remove .git suffix if present
            repo_path = parsed_url.path.strip('/').rstrip('.git')
            
            # Construct authenticated clone URL
            clone_url = f"https://{gh_user}:{gh_token}@{parsed_url.netloc}/{repo_path}.git"
            
            # Extract repository name for target directory
            repo_name = repo_path.split('/')[-1]
        else:
            logger.error(f"❌ Invalid GitHub project URL format: {gh_project}")
            return False
        
        # Determine target directory
        if target_dir:
            clone_target = target_dir
        else:
            clone_target = repo_name
        
        logger.info(f"🔄 Cloning GitHub repository: {repo_path}")
        logger.info(f"📁 Target directory: {clone_target}")
        
        # Check if directory already exists
        if os.path.exists(clone_target):
            logger.warning(f"⚠️  Directory {clone_target} already exists")
            response = input(f"Remove existing directory and re-clone? (y/N): ").strip().lower()
            if response == 'y':
                # Standard
                import shutil
                logger.info(f"🗑️  Removing existing directory: {clone_target}")
                shutil.rmtree(clone_target)
            else:
                logger.info("ℹ️  Skipping clone operation")
                return True
        
        # Execute git clone command
        # Note: We use subprocess to avoid exposing the token in logs
        cmd = ["git", "clone", clone_url, clone_target]
        
        # Run git clone with suppressed output to avoid token exposure
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            logger.info(f"✅ Successfully cloned repository to {clone_target}")
            
            # Verify the clone
            if os.path.isdir(os.path.join(clone_target, ".git")):
                logger.info("✅ Repository verification passed")
                return True
            else:
                logger.error("❌ Repository verification failed - .git directory not found")
                return False
        else:
            # Sanitize error message to remove token
            error_msg = result.stderr.replace(gh_token, "***TOKEN***")
            logger.error(f"❌ Git clone failed: {error_msg}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("❌ Git clone operation timed out after 5 minutes")
        return False
    except Exception as e:
        # Sanitize exception message to remove token
        error_msg = str(e).replace(gh_token, "***TOKEN***") if gh_token else str(e)
        logger.error(f"❌ Error cloning repository: {error_msg}")
        return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="MCP Gateway CI/CD Smoke Test"
    )
    parser.add_argument(
        "--url",
        default=os.getenv("GATEWAY_URL", "https://localhost:4444"),
        help="Gateway base URL (default: https://localhost:4444)"
    )
    parser.add_argument(
        "--token",
        default=os.getenv("MCPGATEWAY_BEARER_TOKEN"),
        help="Bearer token for authentication"
    )
    parser.add_argument(
        "--skip-auth",
        action="store_true",
        help="Skip tests that require authentication"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--clone-repo",
        action="store_true",
        help="Clone GitHub repository using GH_USER, GH_TOKEN, and GH_PROJECT env vars"
    )
    parser.add_argument(
        "--gh-user",
        default=os.getenv("GH_USER"),
        help="GitHub username (default: GH_USER env var)"
    )
    parser.add_argument(
        "--gh-token",
        default=os.getenv("GH_TOKEN"),
        help="GitHub token (default: GH_TOKEN env var)"
    )
    parser.add_argument(
        "--gh-project",
        default=os.getenv("GH_PROJECT"),
        help="GitHub project URL (default: GH_PROJECT env var)"
    )
    parser.add_argument(
        "--target-dir",
        help="Target directory for cloning (optional)"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Handle repository cloning if requested
    if args.clone_repo:
        success = clone_github_project(
            gh_user=args.gh_user,
            gh_token=args.gh_token,
            gh_project=args.gh_project,
            target_dir=args.target_dir
        )
        sys.exit(0 if success else 1)

    # Disable SSL warnings for self-signed certificates
    # Third-Party
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

   

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()