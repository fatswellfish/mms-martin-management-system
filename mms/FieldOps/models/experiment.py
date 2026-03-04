from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.orm_engine import Base
from datetime import datetime


class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    experiment_name = Column(String, unique=True, index=True)  # 例如：一免疫苗实验、二免对照组
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    
    # 免疫方案类型（A/B/C）
    vaccine_plan = Column(String, index=True)  # A: 疫苗足够，全量接种；B: 疫苗不足，部分只做1免；C: 疫苗更少，全部只做1免
    total_vaccine_doses = Column(Integer, default=0)  # 实际生产疫苗数量：2900, 3600, 5000 头份
    
    # 实验参数：
    target_population = Column(Integer, default=0)  # 预计留种或育肥的猪数：200~400头
    sample_size_1st = Column(Integer, default=0)  # 1免样本数量（可变）
    sample_size_2nd = Column(Integer, default=0)  # 2免样本数量（可变）
    
    # 实验状态与时间线：
    status = Column(String, default="planning")  # planning, in_progress, completed, cancelled
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    
    # 外键关系：一个实验属于一个批次，一个批次可以有多个实验（如分阶段免疫）
    batch = relationship("Batch", backref="experiments")
    
    def to_dict(self):
        return {
            "id": self.id,
            "experiment_name": self.experiment_name,
            "batch_id": self.batch_id,
            "vaccine_plan": self.vaccine_plan,
            "total_vaccine_doses": self.total_vaccine_doses,
            "target_population": self.target_population,
            "sample_size_1st": self.sample_size_1st,
            "sample_size_2nd": self.sample_size_2nd,
            "status": self.status,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None
        }

    def __repr__(self):
        return f"<Experiment(id={self.id}, name='{self.experiment_name}', plan='{self.vaccine_plan}')>"
