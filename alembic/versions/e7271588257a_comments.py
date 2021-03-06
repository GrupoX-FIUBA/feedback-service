"""Comments

Revision ID: e7271588257a
Revises: 927c1856c72f
Create Date: 2022-05-19 23:15:34.528274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7271588257a'
down_revision = '927c1856c72f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('album_id', sa.Integer(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'album_id')
    )
    op.create_index(op.f('ix_comment_id'), 'comment', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comment_id'), table_name='comment')
    op.drop_table('comment')
    # ### end Alembic commands ###
