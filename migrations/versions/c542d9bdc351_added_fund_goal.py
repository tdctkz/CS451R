"""added fund goal

Revision ID: c542d9bdc351
Revises: bdcaa6ddc0d4
Create Date: 2022-09-29 15:53:34.674315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c542d9bdc351'
down_revision = 'bdcaa6ddc0d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fundraiser', sa.Column('fund_goal', sa.Integer(), nullable=False))
    op.add_column('fundraiser', sa.Column('raised_amount', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('fundraiser', 'raised_amount')
    op.drop_column('fundraiser', 'fund_goal')
    # ### end Alembic commands ###
