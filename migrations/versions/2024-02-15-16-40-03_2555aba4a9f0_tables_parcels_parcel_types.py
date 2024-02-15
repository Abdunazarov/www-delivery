"""Tables: parcels & parcel_types

Revision ID: 2555aba4a9f0
Revises:
Create Date: 2024-02-15 16:40:03.578263

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2555aba4a9f0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # parcel_types table
    op.create_table(
        "parcel_types",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("name", sa.String(), nullable=False, unique=True),
    )

    op.execute(
        """
        INSERT INTO parcel_types (name) VALUES
        ('одежда'),
        ('электроника'),
        ('разное')
    """
    )

    # parcels table
    op.create_table(
        "parcels",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True, index=True),
        sa.Column("name", sa.String(), index=True),
        sa.Column("weight", sa.Float()),
        sa.Column("type_id", sa.Integer(), sa.ForeignKey("parcel_types.id"), nullable=False),
        sa.Column("content_value", sa.Float()),
        sa.Column("delivery_cost", sa.Float(), default=0.0),
    )


def downgrade():
    op.drop_table("parcels")
    op.drop_table("parcel_types")
