"""update database

Revision ID: 65704c3dedca
Revises: fc6ed569a35f
Create Date: 2022-10-21 11:33:15.384309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65704c3dedca'
down_revision = 'fc6ed569a35f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_pic', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'user_pic')
    # ### end Alembic commands ###