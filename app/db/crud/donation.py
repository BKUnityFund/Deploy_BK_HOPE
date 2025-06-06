from sqlalchemy.orm import Session
from app.db.models import Donation, Account, Project
from app.db.schemas.request.donation_request import DonationCreate
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from typing import Optional
from datetime import datetime, date

def create_donation(db: Session, donation_data: DonationCreate, id:str) -> Donation:
    new_donation = Donation(
        account_id= id,
        project_id=donation_data.project_id,
        amount=donation_data.amount,
        paytime=donation_data.paytime,
        transaction_id=donation_data.transaction_id
    )
    db.add(new_donation)
    db.commit()
    db.refresh(new_donation)
    return new_donation

def get_donation_by_project_id(db: Session, project_id: str):
    donors = (
        db.query(Donation)
        .filter_by(project_id=project_id)
        .options(
            joinedload(Donation.account),   # load bảng Account
            joinedload(Donation.project)    # load bảng Project
        )
        .all()
    )
    return donors

def get_all_donations(
    db: Session,
    skip: int = 0,
    limit: int = 40,
    account_name: Optional[str] = None,
    project_name: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    query = db.query(Donation).options(
        joinedload(Donation.account),
        joinedload(Donation.project)
    ).join(Donation.account).join(Donation.project)

    if account_name:
        query = query.filter(Account.full_name.ilike(f"%{account_name}%"))
    if project_name:
        query = query.filter(Project.name_project.ilike(f"%{project_name}%"))
    if start_date and end_date:
        query = query.filter(Donation.paytime >= start_date, Donation.paytime <= end_date)
    elif start_date:
        query = query.filter(Donation.paytime >= start_date)
    elif end_date:
        query = query.filter(Donation.paytime <= end_date)
    total = query.count()
    donations = query.offset(skip).limit(limit).all()
    return donations, total
