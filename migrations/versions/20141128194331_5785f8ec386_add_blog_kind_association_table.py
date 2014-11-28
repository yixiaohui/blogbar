"""add blog kind association_table

Revision ID: 5785f8ec386
Revises: 2b9daee1ee63
Create Date: 2014-11-28 19:43:31.680089

"""

# revision identifiers, used by Alembic.
revision = '5785f8ec386'
down_revision = '2b9daee1ee63'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_kind',
    sa.Column('kind_id', sa.Integer(), nullable=True),
    sa.Column('blog_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['blog_id'], ['blog.id'], ),
    sa.ForeignKeyConstraint(['kind_id'], ['kind.id'], )
    )
    op.drop_column(u'blog', 'kind_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'blog', sa.Column('kind_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_table('blog_kind')
    ### end Alembic commands ###
