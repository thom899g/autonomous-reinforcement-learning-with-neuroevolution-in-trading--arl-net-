"""
ARL-Net Configuration Module
Centralized configuration management with validation
"""
import os
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from enum import Enum
import yaml
from dotenv import load_dotenv

load_dotenv()

class TradingMode(Enum):
    BACKTEST = "backtest"
    PAPER = "paper"
    LIVE = "live"

class EvolutionStrategy(Enum):
    NEAT = "neat"
    HYPERNEAT = "hyperneat"
    ES = "evolutionary_strategy"

@dataclass
class FirebaseConfig:
    """Firebase configuration with validation"""
    project_id: str = field(default_factory=lambda: os.getenv("FIREBASE_PROJECT_ID", "arl-net-default"))
    credential_path: str = field(default_factory=lambda: os.getenv("FIREBASE_CREDENTIAL_PATH", "./config/firebase_credentials.json"))
    database_url: str = field(default_factory=lambda: os.getenv("FIREBASE_DATABASE_URL", ""))
    collection_prefix: str = "arl_net_"
    
    def validate(self) -> None:
        """Validate Firebase configuration"""
        if not self.project_id:
            raise ValueError("Firebase project_id must be configured")
        if not os.path.exists(self.credential_path):
            raise FileNotFoundError(f"Firebase credentials not found at: {self.credential_path}")

@dataclass
class TradingConfig:
    """Trading-specific configuration"""
    initial_balance: float = 10000.0
    max_position_size: float = 0.1  # 10% of portfolio
    transaction_cost: float = 0.001  # 0.1% per trade
    risk_free_rate: float = 0.02  # 2% annual
    
    # Risk management
    max_drawdown: float = 0.20  # 20% max drawdown
    stop_loss_pct: float = 0.05  # 5% stop loss
    take_profit_pct: float = 0.10  # 10% take profit
    
    def validate(self) -> None:
        """Validate trading configuration"""
        if self.initial_balance <= 0:
            raise ValueError("Initial balance must be positive")
        if not 0 <= self.max_position_size <= 1:
            raise ValueError("Max position size must be between 0 and 1")
        if self.transaction_cost < 0:
            raise ValueError("Transaction cost cannot be negative")

@dataclass
class RLConfig:
    """Reinforcement Learning configuration"""
    gamma: float = 0.99  # Discount factor
    learning_rate: float = 0.001
    buffer_size: int = 10000
    batch_size: int = 64
    tau: float = 0.005  # Target network update rate
    
    # PPO specific
    ppo_epochs: int = 10
    clip_epsilon: float = 0.2
    entropy_coef: float = 0.01
    
    def validate(self) -> None:
        """Validate RL configuration"""
        if not 0 <= self.gamma <= 1:
            raise ValueError("Gamma must be between 0 and 1")
        if self.learning_rate <= 0:
            raise ValueError("Learning rate must be positive")
        if self.buffer_size <= 0:
            raise ValueError("Buffer size must be positive")

@dataclass
class NeuroevolutionConfig:
    """Neuroevolution configuration"""
    population_size: int = 50
    mutation_rate: float = 0.1
    crossover_rate: float = 0.7
    elitism_count: int = 2
    
    # Architecture mutation
    add_node_rate: float = 0.03
    add_connection_rate: float = 0.05
    remove_node_rate: float = 0.01
    
    # Complexity constraints
    max_hidden_layers: int = 5
    max_nodes_per_layer: int = 128
    min_nodes_per_layer: int = 4
    
    def validate(self) -> None:
        """Validate neuroevolution configuration"""
        if self.population_size <= 0:
            raise ValueError("Population size must be positive")
        if not 0 <= self.mutation