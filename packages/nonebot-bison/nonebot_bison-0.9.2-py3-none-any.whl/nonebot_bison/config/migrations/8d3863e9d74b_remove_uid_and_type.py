"""remove uid and type

Revision ID: 8d3863e9d74b
Revises: 67c38b3f39c2
Create Date: 2023-03-20 15:38:20.220599

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8d3863e9d74b"
down_revision = "67c38b3f39c2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("nonebot_bison_user", schema=None) as batch_op:
        batch_op.drop_column("uid")
        batch_op.drop_column("type")

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("nonebot_bison_user", schema=None) as batch_op:
        batch_op.add_column(sa.Column("type", sa.VARCHAR(length=20), nullable=False))
        batch_op.add_column(sa.Column("uid", sa.INTEGER(), nullable=False))

    # ### end Alembic commands ###
