from datetime import datetime

from app.extensions import db


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    position_id = db.Column(
        db.Integer,
        db.ForeignKey("positions.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    name = db.Column(db.String(140), nullable=False)
    email = db.Column(db.String(160), nullable=False, unique=True, index=True)
    phone = db.Column(db.String(30), nullable=True)
    document = db.Column(db.String(40), nullable=False, unique=True, index=True)
    birth_date = db.Column(db.Date, nullable=True)
    admission_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="ativo", index=True)
    photo_path = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    position = db.relationship("Position", back_populates="employees")
    employee_skills = db.relationship(
        "EmployeeSkill", back_populates="employee", cascade="all, delete-orphan"
    )
    skills = db.relationship(
        "Skill",
        secondary="employee_skills",
        back_populates="employees",
        overlaps="employee,employee_skills,skill",
    )

    @property
    def department(self):
        return self.position.department if self.position else None

    def to_dict(self):
        return {
            "id": self.id,
            "position_id": self.position_id,
            "position": self.position.name if self.position else None,
            "department_id": self.department.id if self.department else None,
            "department": self.department.name if self.department else None,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "document": self.document,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "admission_date": (
                self.admission_date.isoformat() if self.admission_date else None
            ),
            "status": self.status,
            "photo_path": self.photo_path,
            "skills": [skill.to_dict() for skill in self.skills],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
