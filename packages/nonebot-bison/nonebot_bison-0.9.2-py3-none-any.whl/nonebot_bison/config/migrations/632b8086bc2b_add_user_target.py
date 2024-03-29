"""add user_target

Revision ID: 632b8086bc2b
Revises: aceef470d69c
Create Date: 2023-03-20 00:39:30.199915

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = "632b8086bc2b"
down_revision = "aceef470d69c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("nonebot_bison_user", schema=None) as batch_op:
        batch_op.drop_constraint("unique-user-constraint", type_="unique")
        batch_op.add_column(
            sa.Column(
                "user_target",
                sa.JSON().with_variant(JSONB, "postgresql"),
                nullable=True,
            )
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("nonebot_bison_user", schema=None) as batch_op:
        batch_op.drop_column("user_target")
        batch_op.create_unique_constraint("unique-user-constraint", ["type", "uid"])

    # ### end Alembic commands ###
