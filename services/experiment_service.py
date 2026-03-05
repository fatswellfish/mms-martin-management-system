"""
Experiment Service Layer

This module implements the business logic for experiment management in FieldOps.
"""

from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from .models import Experiment, Scenario
from .database import get_db_session


class ExperimentService:
    """Service class for managing experiments and scenarios"""
    
    def __init__(self, db_session: Session = None):
        self.db_session = db_session or get_db_session()

    def get_active_experiments(self) -> List[Dict]:
        """Get all active experiments with their scenarios"""
        try:
            # Query all experiments with status 'active'
            experiments = self.db_session.query(Experiment).filter(
                Experiment.status == "active"
            ).all()
            
            # Convert to list of dictionaries with scenarios
            result = []
            for exp in experiments:
                exp_dict = exp.to_dict()
                # Add scenarios sorted by priority (descending)
                scenarios = sorted(
                    [s.to_dict() for s in exp.scenarios],
                    key=lambda x: x["priority"], reverse=True
                )
                exp_dict["scenarios"] = scenarios
                result.append(exp_dict)
            
            return result
        
        except Exception as e:
            print(f"Error retrieving active experiments: {e}")
            raise

    def get_scenario_by_id(self, scenario_id: str) -> Optional[Dict]:
        """Get a specific scenario by ID"""
        try:
            # Query for the scenario
            scenario = self.db_session.query(Scenario).filter(
                Scenario.scenario_id == scenario_id
            ).first()
            
            if scenario:
                return scenario.to_dict()
            else:
                return None
        
        except Exception as e:
            print(f"Error retrieving scenario {scenario_id}: {e}")
            raise

    def run_experiment(self, experiment_id: str, batch_ids: List[str]) -> Dict:
        """Run an experiment on a list of batches and return recommendation results"""
        try:
            # Validate experiment exists and is active
            experiment = self.db_session.query(Experiment).filter(
                Experiment.experiment_id == experiment_id,
                Experiment.status == "active"
            ).first()
            
            if not experiment:
                raise ValueError(f"Experiment {experiment_id} not found or not active")
            
            # Get all scenarios for this experiment
            scenarios = self.db_session.query(Scenario).filter(
                Scenario.experiment_id == experiment_id
            ).order_by(Scenario.priority.desc()).all()
            
            # Simulate experiment results - in real implementation, this would call
            # actual evaluation logic based on the parameters in each scenario
            results = []
            for scenario in scenarios:
                # Simple simulation based on priority and some random factors
                # In real implementation, this would be complex calculations
                success_rate = 0.7 + (scenario.priority / 10) * 0.2 + (0.1 * (1 - scenario.priority / 10))
                cost_estimate = 100 - (scenario.priority * 5) + (5 * (10 - scenario.priority))
                confidence = 0.8 + (scenario.priority / 10) * 0.1
                
                # Apply some randomness
                success_rate += (0.05 * (2 * (hash(scenario.name) % 100) / 100 - 1))
                cost_estimate += (10 * (2 * (hash(scenario.name) % 100) / 100 - 1))
                
                # Ensure bounds
                success_rate = max(0.5, min(1.0, success_rate))
                cost_estimate = max(50, min(150, cost_estimate))
                
                results.append({
                    "scenario_id": scenario.scenario_id,
                    "name": scenario.name,
                    "success_rate": round(success_rate, 2),
                    "cost_estimate": round(cost_estimate, 2),
                    "confidence": round(confidence, 2)
                })
            
            # Find best scenario (highest success rate, then highest confidence)
            best_scenario = max(results, key=lambda x: (x["success_rate"], x["confidence"]))
            
            # Calculate cost savings based on best scenario vs average
            avg_cost = sum(r["cost_estimate"] for r in results) / len(results)
            cost_savings = round(avg_cost - best_scenario["cost_estimate"], 2)
            
            # Return recommendation
            recommendation = {
                "best_scenario": best_scenario["name"],
                "confidence": best_scenario["confidence"],
                "estimated_success_rate": best_scenario["success_rate"],
                "cost_savings": cost_savings
            }
            
            return {
                "success": True,
                "recommendation": recommendation,
                "results": results
            }
            
        except Exception as e:
            print(f"Error running experiment {experiment_id}: {e}")
            raise

# Global service instance
service = ExperimentService()