from datetime import datetime

from app.extensions import db


class EmployeeSkill(db.Model):
    __tablename__ = "employee_skills"
    __table_args__ = (
        db.UniqueConstraint("employee_id", "skill_id", name="uq_employee_skill"),
    )

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("employees.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    skill_id = db.Column(
        db.Integer,
        db.ForeignKey("skills.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    employee = db.relationship(
        "Employee", back_populates="employee_skills", overlaps="employees,skills"
    )
    skill = db.relationship(
        "Skill", back_populates="employee_skills", overlaps="employees,skills"
    )
