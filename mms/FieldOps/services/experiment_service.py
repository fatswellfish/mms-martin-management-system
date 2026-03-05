from sqlalchemy.orm import Session
from typing import List, Optional
from . import models

# --- Service Functions ---

def get_active_experiments(db: Session) -> List[models.Experiment]:
    """Return all active experiments (status = 'active') with their scenarios."""
    return db.query(models.Experiment).filter(
        models.Experiment.status == "active"
    ).all()

def get_scenario_by_id(db: Session, scenario_id: str) -> Optional[models.Scenario]:
    """Get a specific scenario by ID."""
    return db.query(models.Scenario).filter(
        models.Scenario.scenario_id == scenario_id
    ).first()

def run_experiment(db: Session, experiment_id: str, batch_ids: List[str]) -> dict:
    """Run an experiment on given batches and return recommendation.

    Args:
        db: SQLAlchemy session
        experiment_id: UUID of the experiment
        batch_ids: List of batch IDs to evaluate

    Returns:
        Dict with recommendation result including best scenario, confidence, success rate, cost savings.
    """
    # Find experiment
    experiment = db.query(models.Experiment).filter(
        models.Experiment.experiment_id == experiment_id
    ).first()
    
    if not experiment:
        raise ValueError(f"Experiment {experiment_id} not found")
    
    # Get all scenarios for this experiment
    scenarios = db.query(models.Scenario).filter(
        models.Scenario.experiment_id == experiment_id
    ).order_by(models.Scenario.priority.desc()).all()
    
    # Simulate evaluation logic (in real app, this would use ML or rules)
    results = []
    for scenario in scenarios:
        # Simple scoring based on priority + parameters
        # In real system: use historical data, disease model, cost analysis
        score = scenario.priority
        
        # Add bonus for dose > 2.5 (higher protection)
        if scenario.parameters.get("dose", 0) > 2.5:
            score += 1
        
        # Add bonus for multi-phase schedules
        if len(scenario.parameters.get("schedule", [])) > 2:
            score += 1
        
        # Estimate success rate (simplified)
        estimated_success_rate = min(0.95, 0.7 + (score * 0.05))
        
        # Cost savings (simplified)
        cost_savings = max(0, 10 + (scenario.priority - 5) * 3)
        
        results.append({
            "scenario_id": str(scenario.scenario_id),
            "name": scenario.name,
            "score": score,
            "estimated_success_rate": estimated_success_rate,
            "cost_savings": cost_savings
        })
    
    # Sort by score (descending)
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Select best
    best = results[0]
    
    return {
        "success": True,
        "recommendation": {
            "best_scenario": best["name"],
            "confidence": 0.92,
            "estimated_success_rate": best["estimated_success_rate"],
            "cost_savings": best["cost_savings"]
        },
        "details": results
    }