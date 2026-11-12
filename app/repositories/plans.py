from typing import List, Optional
from uuid import UUID

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.plans import Plan


async def check_plan_name_exists(
    db: AsyncSession, name: str, exclude_plan_id: Optional[UUID] = None
) -> bool:

    query = select(exists().where(Plan.name == name))

    if exclude_plan_id:
        query = select(
            exists().where((Plan.name == name) & (Plan.id != exclude_plan_id))
        )

    return await db.scalar(query)


async def create_plan(db: AsyncSession, plan: Plan) -> Plan:
    db.add(plan)
    await db.commit()
    await db.refresh(plan)
    return plan


async def get_plan(db: AsyncSession, plan_id: UUID) -> Optional[Plan]:
    return await db.get(Plan, plan_id)


async def list_plans(
    db: AsyncSession,
    offset: int,
    limit: int,
    search: Optional[str] = None,
) -> List[Plan]:
    query = select(Plan).where(Plan.is_active)

    if search:
        search_filter = f'%{search}%'
        query = query.where(Plan.name.ilike(search_filter))

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    return list(result.scalars().all())


async def updated_plan(
    db: AsyncSession,
    plan: Plan,
) -> Plan:
    db.add(plan)
    await db.commit()
    await db.refresh(plan)
    return plan


async def delete_plan(
    db: AsyncSession,
    plan: Plan,
) -> None:
    db.add(plan)
    await db.commit()
